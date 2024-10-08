import os
import asyncio
from configparser import ConfigParser
import streamlit as st
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import logging
from bs4 import BeautifulSoup
from backend.mongo_connect import MongoHandler
from backend.llm import OpenAIChat
import platform
from concurrent.futures import ThreadPoolExecutor
# Check if images folder exists, if not create it
if not os.path.exists('images'):
    os.makedirs('images')
    

class LinkedInOperations:
    def __init__(self, max_concurrent_connections=3):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir = os.path.abspath(os.path.join(self.script_dir, '..'))
        self.config_path = os.path.join(self.parent_dir, 'config.ini')
        self.config = ConfigParser()
        self.llm = OpenAIChat()
        self.profile_extraction_prompt = """Extract the following information from the given text:
1. Name of the person/entity
2. Email address
3. Phone number
4. About the person/entity
5. Work experiences and details or Company details and services
6. Educations
"""
        try:
            self.config.read(self.config_path)
            self.username = self.config['LINKEDIN']['username']
            self.password = self.config['LINKEDIN']['password']
        except KeyError:
            self.username = st.secrets["LINKEDIN"]["username"]
            self.password = st.secrets["LINKEDIN"]["password"]

        self.mongo_handler = MongoHandler()
        self.semaphore = asyncio.Semaphore(max_concurrent_connections)

    async def login_and_get_cookies(self):
        async with async_playwright() as p:
            browser = None
            try:
                browser = await p.chromium.launch(headless=True)  # Set to False for debugging
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                    viewport={"width": 1920, "height": 1080},
                    device_scale_factor=1,
                    is_mobile=False,
                    has_touch=False,
                    locale="en-US",
                    timezone_id="Asia/Singapore",
                    geolocation={"latitude": 1.3521, "longitude": 103.8198},  # Singapore
                    permissions=["geolocation"],
                    color_scheme="light",
                    reduced_motion="no-preference",
                    forced_colors="none",
                    accept_downloads=True,
                    extra_http_headers={
                        "Accept-Language": "en-US,en;q=0.9",
                        "Sec-Ch-Ua-Platform": '"Windows"',
                        "Sec-Ch-Ua": '"Chromium";v="127", "Not=A?Brand";v="24"',
                    }
                )
                
                # Set the device name
                page = await context.new_page()
                await page.goto('https://www.linkedin.com/login', timeout=20000)
                await page.fill('#username', self.username)
                await page.fill('#password', self.password)
                await page.click('button:has-text("Sign in")')
                
                # Add error handling and additional checks
                # Wait for navigation and check for login challenges
                try:
                    await page.wait_for_navigation(timeout=30000)
                except PlaywrightTimeoutError:
                    self.logger.warning("Navigation timeout after login attempt. Checking current page.")
                
                # Check for login challenges or CAPTCHA
                if await self.check_for_login_challenge(page):
                    self.logger.error("Login challenge or CAPTCHA detected. Manual intervention required.")
                    return None
                
                # Check if we're on the feed page
                if 'feed' not in page.url:
                    self.logger.error(f"Login unsuccessful, current page: {page.url}")
                    return None
                
                cookies = await context.cookies()
                li_at = next((cookie for cookie in cookies if cookie['name'] == 'li_at'), None)
                return li_at
            except Exception as e:
                self.logger.error(f'An error occurred during login: {str(e)}')
                return None
            finally:
                if browser:
                    await browser.close()
                    
    async def check_for_login_challenge(self, page):
        challenge_selectors = [
            'input#challenge_response',  # Phone verification
            'div.recaptcha-checkbox-border',  # reCAPTCHA
            'input#captcha-internal',  # Internal CAPTCHA
            'form#two-step-challenge'  # Two-step verification
        ]
        
        for selector in challenge_selectors:
            if await page.query_selector(selector):
                return True
        return False
    
    async def retry_with_exponential_backoff(self, coroutine, max_retries=3, base_delay=5):
        retries = 0
        while retries < max_retries:
            try:
                return await coroutine()
            except Exception as e:
                wait_time = base_delay * (2 ** retries)
                self.logger.warning(f"Attempt {retries + 1} failed: {str(e)}. Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                retries += 1
        
        self.logger.error(f"All {max_retries} attempts failed")
        raise Exception("Max retries exceeded")
                        
    async def check_cookie_validity(self, cookie):
        async with async_playwright() as p:
            browser = None
            try:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                )
                await context.add_cookies([cookie])
                
                page = await context.new_page()
                try:
                    await page.goto('https://www.linkedin.com/feed/', wait_until="networkidle", timeout=60000)
                except PlaywrightTimeoutError:
                    self.logger.warning("Timeout while loading feed page. Checking if we're logged in anyway.")
                
                # Check if we're logged in by looking for specific elements
                try:
                    await page.wait_for_selector('div.feed-identity-module', timeout=10000)
                    self.logger.info("Cookie is valid")
                    return True
                except PlaywrightTimeoutError:
                    self.logger.info("Cookie is invalid or expired")
                    return False
            except Exception as e:
                self.logger.error(f"An error occurred while checking cookie validity: {str(e)}")
                return False
            finally:
                if browser:
                    await browser.close()
                    
    async def scrape_linkedin_profile(self, url, cookies):
        async with async_playwright() as p:
            browser = None
            try:
                browser = await p.chromium.launch(headless=True)  # Set to False for debugging
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                    viewport={"width": 1920, "height": 1080},
                    device_scale_factor=1,
                    is_mobile=False,
                    has_touch=False,
                    locale="en-US",
                    timezone_id="Asia/Singapore",
                    geolocation={"latitude": 1.3521, "longitude": 103.8198},  # Singapore
                    permissions=["geolocation"],
                    color_scheme="light",
                    reduced_motion="no-preference",
                    forced_colors="none",
                    accept_downloads=True,
                    extra_http_headers={
                        "Accept-Language": "en-US,en;q=0.9",
                        "Sec-Ch-Ua-Platform": '"Windows"',
                        "Sec-Ch-Ua": '"Chromium";v="127", "Not=A?Brand";v="24"',
                    }
                )
                await context.add_cookies(cookies)
                
                # Set the device name
                await context.add_init_script("Object.defineProperty(navigator, 'platform', {get: () => 'Windows PC'})")

                page = await context.new_page()
                self.logger.info(f"Navigating to {url}")
                await page.goto(url, wait_until="networkidle", timeout=20000)
                await page.wait_for_selector('section.artdeco-card', timeout=30000)

                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')

                name = soup.select_one('h1')
                name = name.text.strip() if name else "Name not found"
                title = soup.select_one('.text-body-medium')
                title = title.text.strip() if title else "Title not found"

                profile_data = {
                    'name': name,
                    'title': title
                }

                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await page.wait_for_timeout(1000)
                await page.screenshot(path=f'images/linkedin_profile_{name}.png', full_page=True)
                return profile_data, f'images/linkedin_profile_{name}.png'

            except Exception as e:
                self.logger.error(f"An error occurred during scraping: {str(e)}")
                return None, None
            finally:
                if browser:
                    await browser.close()

    async def update_cookies(self):
        new_cookie = await self.login_and_get_cookies()
        if new_cookie:
            self.mongo_handler.store_cred_cookie('linkedin', new_cookie)
            self.logger.info('New cookie stored in MongoDB')
            return new_cookie
        else:
            self.logger.error('Failed to obtain new cookie')
            return None

    async def process_profile(self, profile_url, valid_cookie):
        async with self.semaphore:
            if valid_cookie:
                profile_data, image_path = await self.scrape_linkedin_profile(profile_url, [valid_cookie])
                
                if profile_data:
                    self.logger.info('Successfully scraped profile with existing cookie')
                    final_prompt = f"On profile: {profile_data['name']} - {profile_data['title']}\n\n{self.profile_extraction_prompt}"
                    profile_context = self.llm.chat_image(final_prompt, 
                                        self.llm.encode_image(image_path), 
                                        max_tokens=1000)
                    # Remove the image after processing
                    os.remove(image_path) 
                    
                    return profile_context
                else:
                    self.logger.error('Failed to scrape profile even with valid cookie')
                    return None
            else:
                self.logger.error('No valid cookie available')
                return None

    async def process_profiles_concurrently(self, profile_urls):
        existing_cookie = self.mongo_handler.get_cred_cookie('linkedin')
        
        if existing_cookie:
            self.logger.info('Checking existing cookie validity')
            is_valid = await self.retry_with_exponential_backoff(lambda: self.check_cookie_validity(existing_cookie))
            if not is_valid:
                self.logger.info('Existing cookie is invalid, attempting new login')
                existing_cookie = await self.retry_with_exponential_backoff(self.login_and_get_cookies)
                if not existing_cookie:
                    self.logger.error('Failed to obtain new cookie after multiple attempts')
                    return dict(zip(profile_urls, [None] * len(profile_urls)))
        else:
            self.logger.info('No existing cookie found, attempting new login')
            existing_cookie = await self.retry_with_exponential_backoff(self.login_and_get_cookies)
            if not existing_cookie:
                self.logger.error('Failed to obtain new cookie after multiple attempts')
                return dict(zip(profile_urls, [None] * len(profile_urls)))

        tasks = [self.process_profile(url, existing_cookie) for url in profile_urls]
        results = await asyncio.gather(*tasks)
        return dict(zip(profile_urls, results))
    
async def classify_li_async(profile_urls, max_concurrent_connections=3):
    linkedin_ops = LinkedInOperations(max_concurrent_connections)
    results = await linkedin_ops.process_profiles_concurrently(profile_urls)
    return results

def classify_li(profile_urls, max_concurrent_connections=3):
    def run_in_executor(_profile_urls):
        def run_async():
            if platform.system() == 'Windows':
                loop = asyncio.ProactorEventLoop()
            else:
                loop = asyncio.new_event_loop()
            
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(classify_li_async(_profile_urls, max_concurrent_connections))
            finally:
                loop.close()

        with ThreadPoolExecutor() as executor:
            future = executor.submit(run_async)
            return future.result()

    return run_in_executor(profile_urls)

if __name__ == "__main__":
    profile_urls = ['https://www.linkedin.com/in/arumkang/', 'https://www.linkedin.com/in/jindrichkarasek/']
    results = classify_li(profile_urls)
    import json
    with open('linkedin_results.json', 'w') as f:
        json.dump(results, f, indent=4)
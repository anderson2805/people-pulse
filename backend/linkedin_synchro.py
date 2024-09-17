import os
from configparser import ConfigParser
import streamlit as st
from playwright.sync_api import sync_playwright
import logging
from bs4 import BeautifulSoup
from backend.mongo_connect import MongoHandler
from backend.llm import OpenAIChat
from concurrent.futures import ThreadPoolExecutor, as_completed

class LinkedInOperations:
    def __init__(self):
        # Logging setup
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Configuration setup
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
4. Work experiences and details or Company details and services
5. Educations
"""
        try:
            self.config.read(self.config_path)
            self.username = self.config['LINKEDIN']['username']
            self.password = self.config['LINKEDIN']['password']
        except KeyError:
            self.username = st.secrets["LINKEDIN"]["username"]
            self.password = st.secrets["LINKEDIN"]["password"]

        self.mongo_handler = MongoHandler()

    def login_and_get_cookies(self):
        with sync_playwright() as p:
            browser = None
            try:
                browser = p.chromium.launch()
                page = browser.new_page()

                page.goto('https://www.linkedin.com/login')
                page.fill('#username', self.username)
                page.fill('#password', self.password)
                page.click('button:has-text("Sign in")')
                page.wait_for_load_state('networkidle')
                
                cookies = page.context.cookies()
                li_at = next((cookie for cookie in cookies if cookie['name'] == 'li_at'), None)
                return li_at
            except Exception as e:
                self.logger.error(f'An error occurred during login: {str(e)}')
                return None
            finally:
                if browser:
                    browser.close()

    def scrape_linkedin_profile(self, url, cookies):
        with sync_playwright() as p:
            browser = None
            try:
                browser = p.chromium.launch()
                context = browser.new_context()
                context.add_cookies(cookies)
                context.set_extra_http_headers({'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"})
                
                page = context.new_page()
                self.logger.info(f"Navigating to {url}")
                page.goto(url, wait_until="networkidle", timeout=20000)
                page.wait_for_selector('section.artdeco-card', timeout=30000)

                content = page.content()
                soup = BeautifulSoup(content, 'html.parser')

                name = soup.select_one('h1')
                name = name.text.strip() if name else "Name not found"
                title = soup.select_one('.text-body-medium')
                title = title.text.strip() if title else "Title not found"

                profile_data = {
                    'name': name,
                    'title': title
                }

                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                page.wait_for_timeout(1000)
                page.screenshot(path=f'images/linkedin_profile_{name}.png', full_page=True)
                return profile_data, f'images/linkedin_profile_{name}.png'

            except Exception as e:
                self.logger.error(f"An error occurred during scraping: {str(e)}")
                return None, None
            finally:
                if browser:
                    browser.close()

    def update_cookies(self):
        new_cookie = self.login_and_get_cookies()
        if new_cookie:
            self.mongo_handler.store_cred_cookie('linkedin', new_cookie)
            self.logger.info('New cookie stored in MongoDB')
            return new_cookie
        else:
            self.logger.error('Failed to obtain new cookie')
            return None

    def process_profile(self, profile_url):
        # Try to get existing cookie from MongoDB
        existing_cookie = self.mongo_handler.get_cred_cookie('linkedin')
        
        if existing_cookie:
            self.logger.info('Using existing cookie from MongoDB')
            profile_data, image_path = self.scrape_linkedin_profile(profile_url, [existing_cookie])
            
            if profile_data:
                self.logger.info('Successfully scraped profile with existing cookie')
                final_prompt = f"On profile: {profile_data['name']} - {profile_data['title']}\n\n{self.profile_extraction_prompt}"
                profile_context = self.llm.chat_image(final_prompt, 
                                    self.llm.encode_image(image_path), 
                                    max_tokens=1000)
                return profile_context
            else:
                self.logger.info('Failed to scrape with existing cookie, attempting new login')
        else:
            self.logger.info('No existing cookie found, attempting new login')
        
        # If we reach here, either there was no existing cookie or it failed to scrape
        # Attempt new login and get new cookie
        new_cookie = self.login_and_get_cookies()
        
        if new_cookie:
            self.mongo_handler.store_cred_cookie('linkedin', new_cookie)
            self.logger.info('New cookie stored in MongoDB')
            
            # Attempt to scrape with new cookie
            profile_data, image_path = self.scrape_linkedin_profile(profile_url, [new_cookie])
            
            if profile_data:
                self.logger.info('Successfully scraped profile with new cookie')
                final_prompt = f"On profile: {profile_data['name']} - {profile_data['title']}\n\n{self.profile_extraction_prompt}"
                profile_context = self.llm.chat_image(final_prompt, 
                                    self.llm.encode_image(image_path), 
                                    max_tokens=1000)
                return profile_context
            else:
                self.logger.error('Failed to scrape profile even with new cookie')
                return None
        else:
            self.logger.error('Failed to obtain new cookie')
            return None

    def process_profiles_concurrently(self, profile_urls, max_workers=3):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(self.process_profile, url): url for url in profile_urls}
            results = {}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    results[url] = data
                except Exception as exc:
                    print(f'{url} generated an exception: {exc}')
                    results[url] = None
        return results

def classify_li(profile_urls):
    linkedin_ops = LinkedInOperations()
    results = linkedin_ops.process_profiles_concurrently(profile_urls)
    return results

if __name__ == "__main__":
    linkedin_ops = LinkedInOperations()
    profile_urls = ['https://www.linkedin.com/in/arumkang/', 'https://www.linkedin.com/in/jindrichkarasek/']
    results = linkedin_ops.process_profiles_concurrently(profile_urls)
    # Store results in json
    import json
    with open('linkedin_results.json', 'w') as f:
        json.dump(results, f, indent=4)
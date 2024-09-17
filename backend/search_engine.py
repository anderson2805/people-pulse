import requests
from typing import Literal
from urllib.parse import quote
from configparser import ConfigParser
from linkedin import LinkedInOperations
from backend.mongo_connect import MongoHandler
import time
from datetime import datetime, timezone
import asyncio
import aiohttp
import json

config = ConfigParser()
config.read('config.ini')
jina_api_key = config['JINA']['api_key']
cse_api_key = config['GOOGLE']['api_key']
cx = config['GOOGLE']['cx']

def google_search(query: str) -> list[dict]:
    """Google search on technology sources that return latest news in the last 24 hours. The results are sorted by relevance and not by date."""
    url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={cse_api_key}&cx={cx}'
    response = requests.get(url)
    results = response.json()
    search_results = [{'title': result['title'], 'link': result['link'], 'snippet': result['snippet']} for result in results['items']]
    return search_results

async def jina_ai_request(input_text: str, request_type: Literal['search', 'reader'], api_key=jina_api_key) -> list[dict]:
    """Send an asynchronous request to Jina AI services."""
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    if request_type == 'search':
        encoded_query = quote(input_text)
        url = f'https://s.jina.ai/{encoded_query}'
    elif request_type == 'reader':
        if not input_text.startswith('http'):
            raise ValueError("For reader service, the input should be a valid URL starting with 'http' or 'https'")
        url = f'https://r.jina.ai/{input_text}'
    else:
        raise ValueError("Invalid request_type. Use 'search' for summarization or 'reader' for reranking.")

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise Exception(f"Request failed with status code {response.status}: {await response.text()}")
            return await response.json()

async def process_searches(google_result, li_process = bool):
    """
    Process the search results from Google and Jina AI services concurrently.
    
    :param google_result: The search results from Google
    :return: A list containing the processed search results
    """
    li_handler = LinkedInOperations()

    async def get_context(search_result):
        print("Processing:", search_result['link'])
        url = search_result['link']
        context = None

        if 'linkedin.com' in url:
            if li_process:
                await asyncio.sleep(2)
                context = await li_handler.process_profile(url)
        else:
            context = await jina_ai_request(url, 'reader')
            
        return {**search_result, 'context': context}

    # Use asyncio.gather to process all searches concurrently
    processed_searches = await asyncio.gather(*[get_context(result) for result in google_result])
    return processed_searches

async def main():
    query = "Scott Hale United Kingdom"
    li_handler = LinkedInOperations()
    await li_handler.update_cookies()
    google_results = google_search(query)
    print(google_results)
    # processed_searches = await process_searches(google_results)
    # print(processed_searches)

if __name__ == "__main__":
    asyncio.run(main())
from pymongo import MongoClient, ASCENDING, ReadPreference,WriteConcern, UpdateOne
from pymongo.errors import OperationFailure
from pymongo.read_concern import ReadConcern
from pydantic import BaseModel, Field
from configparser import ConfigParser
from typing import Literal, TypedDict
from datetime import datetime as dt
import logging
from urllib.parse import quote_plus
import asyncio
import streamlit as st
import os


# If it's not an absolute path, make it relative to the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
config_path = os.path.join(parent_dir, 'config.ini')
config = ConfigParser()
try:
    config.read(config_path)
    username = config['MONGODB']['username']
    password = config['MONGODB']['password']
except KeyError: # If the key is not found in the config file
    username = st.secrets["MONGODB"]["username"]
    password = st.secrets["MONGODB"]["password"]


class MongoHandler:
    def __init__(self, username=username, password=password):
        # MongoDB connection setup
        username = quote_plus(username)
        password = quote_plus(password)
        uri = f"mongodb+srv://{username}:{password}@people-pulse.exlqa.mongodb.net/?retryWrites=true&w=majority&appName=people-pulse"
        self.client = MongoClient(uri)
        self.db = self.client.get_database('people_pulse')
        
        # Set up basic logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
    def store_cred_cookie(self, platform: str, cred_cookie: dict):
        filter_query = {platform: {"$exists": True}}
        update_query = {"$set": {platform: cred_cookie}}
        
        result = self.db.cred_cookies.update_one(
            filter_query,
            update_query,
            upsert=True
        )
        
        if result.matched_count > 0:
            logging.info(f'Credential cookie for {platform} updated in MongoDB')
        else:
            logging.info(f'New credential cookie for {platform} inserted in MongoDB')
        
    def get_cred_cookie(self, platform: str):
        query = {platform: {"$exists": True}}
        cred_cookie = self.db.cred_cookies.find_one(query)
        if cred_cookie:
            return cred_cookie[platform]
        return None
        
    
if __name__ == '__main__':
    handler = MongoHandler()

    cookie_in_db = handler.get_cred_cookie('linkedin')
    print('Cookie retrieved from MongoDB:', cookie_in_db)
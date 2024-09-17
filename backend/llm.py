import os
import openai
from typing import List, Optional
import base64
import json
from configparser import ConfigParser
import backoff
from openai import OpenAI
import streamlit as st
from pydantic import BaseModel

class ChatFunctionCall(BaseModel):
    name: str
    arguments: str

class ChatResponse(BaseModel):
    content: Optional[str] = None
    function_call: Optional[ChatFunctionCall] = None

class OpenAIChat:
    DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant in reading website."

    def __init__(self):
        self.api_key = self._load_config()
        self.client = OpenAI(api_key=self.api_key, max_retries=5)

    def _load_config(self) -> str:
        config = ConfigParser()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
        config_path = os.path.join(parent_dir, 'config.ini')
        
        try:
            config.read(config_path)
            return config['OPENAI']['api_key']
        except:
            return st.secrets['OPENAI']['api_key']

    @staticmethod
    def encode_image(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    @backoff.on_exception(backoff.expo, (openai.APIConnectionError, openai.RateLimitError), max_time=6000)
    def chat_func(
        self,
        prompt: str,
        functions: List[dict],
        system_message: str = DEFAULT_SYSTEM_MESSAGE,
        model: str = "gpt-4o",
        temperature: float = 0,
        max_tokens: int = 500,
        function_call: Optional[str] = None
    ) -> ChatResponse:
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=functions,
            tool_choice={"type": "function", "function": {"name": function_call}} if function_call else "auto"
        )
        
        response_data = json.loads(response.model_dump_json())
        message = response_data["choices"][0]['message']
        
        if 'tool_calls' in message and message['tool_calls']:
            function_call_data = message['tool_calls'][0]['function']
            return ChatResponse(function_call=ChatFunctionCall(**function_call_data))
        else:
            return ChatResponse(content=message.get('content'))

    @backoff.on_exception(backoff.expo, (openai.APIConnectionError, openai.RateLimitError), max_time=6000)
    def chat_image(
        self,
        prompt: str,
        base64_image: str,
        model: str = "gpt-4o-2024-08-06",
        temperature: float = 0,
        max_tokens: int = 500
    ) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}",
                            "detail": "high"
                        },
                    },
                ],
            }],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        response_data = json.loads(response.model_dump_json())
        return response_data['choices'][0]['message']['content']
    
if __name__ == '__main__':
    chat = OpenAIChat()
    li_extraction_prompt = """Extract the following information from the given text:
1. Name of the person
2. Email address
3. Phone number
4. About the person
4. Work experiences and details
5. Educations
"""
    print(chat.chat_image(li_extraction_prompt, chat.encode_image('profile_arumkang.png'), max_tokens=1000))
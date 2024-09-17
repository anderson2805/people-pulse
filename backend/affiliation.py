import concurrent.futures
import json
from typing import List, Dict, Literal
import numpy as np
import pandas as pd
from backend.llm import OpenAIChat
from pydantic import BaseModel, Field


class Affiliation(BaseModel):
    status: Literal["Current", "Past"] = Field(..., description="The status of the affiliation with the organization.")
    organization: str = Field(..., description="The name of the organization.")
    
class AffiliationExtraction(BaseModel):
    """Affiliation Extraction"""
    name: str = Field(..., description="The name of the individual.")
    affiliations: None | List[Affiliation] = Field(..., description="The affiliations of the individual. None, if there are no affiliations.")
    
extract_affiliation = {
    "type": "function",
    "function": {
        "name": "extract_affiliation",
        "description": "Extract the affiliations of an individual. The affiliations include the name of the organization and the status of the affiliation (current or past).",
        "parameters": AffiliationExtraction.model_json_schema()
    }
}

    
openai_chat = OpenAIChat()
def extract_affiliate_func(prompt: str, model: str) -> Dict:
    # This function should make the API call to OpenAI
    # For this example, I'll use a placeholder
    response = openai_chat.chat_func(prompt, [extract_affiliation], model=model, function_call="extract_affiliation", max_tokens=1028)
    return json.loads(response.function_call.arguments)


def process_record(row: pd.Series, model: str) -> Dict:

    final_prompt = f"Extract the affiliations (company or school) of {row['Name']}\n\nInformation about the individual:\n{row['Perplexity Context']}"
    if row['LinkedIn Context']:
        final_prompt += f"\n\nAdditional LinkedIn context:\n{row['LinkedIn Context']}"
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(extract_affiliate_func, final_prompt, model)}
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
            except Exception as exc:
                print(f'Generated an exception: {exc}')
    
    return result

def extract_affiliate_llm(input_df: pd.DataFrame, model: str  = "gpt-4o-2024-08-06"):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _, row in input_df[['Name', 'Perplexity Context', 'LinkedIn Context']].iterrows():
            if row['Name'] is not np.nan:
                print(f"Processing record for {row['Name']}")
                future = executor.submit(process_record, row, model)
                futures.append(future)
            else:
                print("Name is not available for the record")
            
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result['affiliations']:  # Only add results with non-empty ssoc_codes
                    results.append(result)
            except Exception as exc:
                print(f'Generated an exception: {exc}')

    # Combine results into a single dictionary
    combined_results = {result['name']: result['affiliations'] for result in results}
    return combined_results
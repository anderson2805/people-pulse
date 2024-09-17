import concurrent.futures
import json
from typing import List, Dict
import numpy as np
import pandas as pd
from backend.llm import OpenAIChat
from pydantic import BaseModel, Field
from itertools import chain

df = pd.read_excel("about/ssoc2024-detailed-definitions.xlsx")

def group_and_chunk(records, chunk_size=150):
    groups = {}
    for record in records:
        key = str(record['ssoc_code'])[0]
        groups.setdefault('X' if key.isalpha() else int(key), []).append(record)
    
    return list(chain.from_iterable(
        [group[i:i+chunk_size] for i in range(0, len(group), chunk_size)]
        for group in groups.values()
    ))

ssoc_detail_chunks = group_and_chunk(df.to_dict('records'))

class SSOCDetail(BaseModel):
    """Singapore Standard Occupational Classification, SSOC 2024. The Singapore Standard Occupational Classification (SSOC) is the national standard for classifying occupations and is used for censuses of population, household surveys and administrative databases. 
    """
    task: str = Field(..., description="A sentence describing how the SSOC specfic task matches the individual information. Keep it within 50 words.")
    code: int = Field(..., description="SSOC code for the occupation")
    title: str = Field(..., description="SSOC title of the occupation")
    
    
class SSOCClassifier(BaseModel):
    """Singapore Standard Occupational Classification SSOC 2024"""
    name: str = Field(..., description="The name of the individual the SSOC is classified to.") 
    ssoc_codes: None | List[SSOCDetail] = Field(..., description="Singapore Standard Occupational Classification details of the individual. None, if it is not classified to any of the portion of SSOC code.")
    
classify_ssoc = {
    "type": "function",
    "function": {
        "name": "classify_ssoc",
        "description": "Classify a individual to Singapore Standard Occupational Classification SSOC 2024. The specific range to check for is in the prompt.",
        "parameters": SSOCClassifier.model_json_schema()
    }
}

openai_chat = OpenAIChat()
def classify_ssoc_func(prompt: str, model: str) -> Dict:
    # This function should make the API call to OpenAI
    # For this example, I'll use a placeholder
    system_message = "You are a expert in Singapore Standard Occupational Classification SSOC 2024, please classify the individual to the SSOC code. You are straight forward with the task description."
    response = openai_chat.chat_func(prompt, [classify_ssoc], system_message, model=model, function_call="classify_ssoc", max_tokens=4000)
    return json.loads(response.function_call.arguments)

def process_chunk(row: pd.Series, ssoc_chunk: str, model: str) -> Dict:
    final_prompt = f"Specific segments of SSOC:\n\n{str(ssoc_chunk)}\n\nClassify *{row['Name']}* skill(s) on technology.\n\nInformation about the individual:\n{row['Perplexity Context']}"
    if row['LinkedIn Context']:
        final_prompt += f"\n\nAdditional LinkedIn context:\n{row['LinkedIn Context']}"
    return classify_ssoc_func(final_prompt, model)

def process_record(row: pd.Series, ssoc_chunks: List[str], model: str) -> Dict:
    records_ssoc_classified = {'name': row['Name'], 'ssoc_codes': []}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_chunk = {executor.submit(process_chunk, row, chunk, model): chunk for chunk in ssoc_chunks}
        for future in concurrent.futures.as_completed(future_to_chunk):
            try:
                result = future.result()
                if result.get("ssoc_codes") is not None:
                    records_ssoc_classified['ssoc_codes'].extend(result['ssoc_codes'])
            except Exception as exc:
                print(f'Generated an exception: {exc}')
    
    return records_ssoc_classified

def classify_ssoc_llm(input_df: pd.DataFrame, ssoc_detail_chunks: List[str] = ssoc_detail_chunks , model: str  = "gpt-4o-2024-08-06"):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _, row in input_df[['Name', 'Perplexity Context', 'LinkedIn Context']].iterrows():
            if row['Name'] is not np.nan:
                print(f"Processing record for {row['Name']}")
                future = executor.submit(process_record, row, ssoc_detail_chunks, model)
                futures.append(future)
            else:
                print("Name is not available for the record")
            
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result['ssoc_codes']:  # Only add results with non-empty ssoc_codes
                    results.append(result)
            except Exception as exc:
                print(f'Generated an exception: {exc}')

    # Combine results into a single dictionary
    combined_results = {result['name']: result['ssoc_codes'] for result in results}
    return combined_results
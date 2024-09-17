import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple, Optional
import pandas as pd
from backend.tech_class import classify_technologies
from backend.llm import OpenAIChat

openai_chat = OpenAIChat()
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

topic_mapper: Dict[str, str] = {
    "adv_computing_ai": "Advanced Computing, AI, and Information Technologies",
    "adv_materials_manufacture": "Advanced Materials and Manufacturing",
    "energy_sys_propulsion": "Energy Systems and Propulsion",
    "sensors_electronics_comm": "Sensors, Electronics, and Communication",
    "auto_systems_robotics": "Autonomous Systems and Robotics",
    "space_aerospace_tech": "Space and Aerospace Technologies",
    "biotech_med_human_perf": "Biotechnology, Medical, and Human Performance",
    "def_sec_societal_tech": "Defense, Security, and Societal Technologies",
    "env_sustain_tech": "Environmental and Sustainability Technologies"
}

def process_row(name: str, perplexity_context: str, linkedIn_context: str) -> Optional[Tuple[Dict, List[Dict[str, str]]]]:
    try:
        final_prompt = f"Based on the technologies and topics mentioned in the text, classify *{name}* skill(s) on technology.\n\nInformation about the individual:\n{perplexity_context}"
        if linkedIn_context:
            final_prompt += f"\n\nAdditional LinkedIn context:\n{linkedIn_context}"
        response = openai_chat.chat_func(final_prompt, [classify_technologies], model="gpt-4o-2024-08-06", function_call="classify_technologies")
        
        try:
            result = json.loads(response.function_call.arguments)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON for {name}. Response: {response.function_call.arguments}")
            return None
        
        if 'technologies_applicable' not in result:
            logger.warning(f"No 'technologies_applicable' found for {name}")
            return result, []
        
        row_tech_skills: List[Dict[str, str]] = []
        for topic in result['technologies_applicable']:
            if not topic:
                logger.warning(f"Empty topic found for {name}")
                continue
            
            try:
                main_topic_key = next(iter(topic.keys()))
            except StopIteration:
                logger.warning(f"No keys found in topic for {name}")
                continue
            
            if main_topic_key not in topic_mapper:
                logger.warning(f"Unknown main topic '{main_topic_key}' for {name}")
                continue
            
            main_topic = topic_mapper[main_topic_key]
            
            for subtopic in topic[main_topic_key]:
                tech_dict = {
                    'name': name,
                    'main_topic': main_topic,
                    'sub_topic': subtopic.get('subtopic', ''),
                    'focus_area': ''
                }
                
                for focus_area in subtopic.get('specifics', []):
                    tech_dict['focus_area'] = focus_area
                    row_tech_skills.append(tech_dict.copy())
        
        return result, row_tech_skills
    
    except Exception as e:
        logger.error(f"Error processing {name}: {str(e)}")
        return None

def classify_tech_llm(df: pd.DataFrame) -> List[Dict[str, str]]:
    results: List[Dict] = []
    tech_skill_compile: List[Dict[str, str]] = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_row = {executor.submit(process_row, row['Name'], row['Perplexity Context'], row['LinkedIn Context']): (index, row) for index, row in df[['Name', 'Perplexity Context', 'LinkedIn Context']].iterrows()}
        
        for future in as_completed(future_to_row):
            index, row = future_to_row[future]
            try:
                result = future.result()
                if result:
                    if isinstance(result, tuple):
                        results.append(result[0])
                        tech_skill_compile.extend(result[1])
                    else:
                        results.append(result)
            except Exception as exc:
                logger.error(f'{row["Name"]} generated an exception: {exc}')

    logger.info(f"Processed {len(results)} entries, compiled {len(tech_skill_compile)} tech skills.")
    return tech_skill_compile

import openai
from langchain.llms.base import LLM
from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage, AnyMessage

import openai
import json
import os
import re
import pandas as pd
from langchain.schema.messages import HumanMessage
from typing import List, Optional

api_key = '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'
results_file = '../output_metric/Quantity_metrics.csv'

class OpenLLMAPI(LLM):
    model: str  # Define the model name to use for completion

    @property
    def _llm_type(self) -> str:
        return "OpenLLMAPI"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs
    ) -> str:
        if 'max_tokens' not in kwargs:
            kwargs['max_tokens'] = 512
        if 'n' in kwargs and kwargs['n'] != 1:
            kwargs['n'] = 1
            print('Warning: resetting n=1')
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stop=stop,
            temperature=0,
            **kwargs,
        )
        result = response.choices[0].message["content"].strip()
        return result

    def chat(
        self,
        messages: List[AnyMessage],
        stop: Optional[List[str]] = None,
        **kwargs
    ) -> str:
        
        if 'max_tokens' not in kwargs:
            kwargs['max_tokens'] = 512
        if 'n' in kwargs and kwargs['n'] != 1:
            kwargs['n'] = 1
            print('Warning: resetting n=1')
        
        conversation = []
        for msg in messages:
            if msg.type == 'human':
                conversation.append({
                    'role': 'user',
                    'content': msg.content,
                })
            elif msg.type == 'ai':
                conversation.append({
                    'role': 'assistant',
                    'content': msg.content,
                })
            else:
                raise ValueError(f'Unsupported role: {msg.type}')
        assert messages[-1].type == 'human', 'Last message should be from human.'

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=conversation,
            stop=stop,
            **kwargs,
        )
        result = response.choices[0].message["content"].strip()
        return result

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model": self.model}


# Define the function for creating OpenLLMAPI
def create_open_llm(model):
    openai.api_key = api_key
    print("OpenAI API key set successfully.")
    return OpenLLMAPI(model=model)


# Function to extract JSON objects from the model's response
def extract_json(input_str: str) -> Optional[List[dict]]:
    # Use regular expression to find JSON-like structures in the response
    match = re.search(r'\[.*\]', input_str, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            parsed_json = json.loads(json_str)
            return parsed_json
        except json.JSONDecodeError as e:
            print("JSON解析错误:", e)
            return None
    else:
        print("未找到有效的JSON数据")
        return None

# Format confidence scores to ensure they're long decimal numbers
def format_confidence(confidence):
    if isinstance(confidence, str) and "%" in confidence:
        # Convert percentage to decimal
        confidence = confidence.replace("%", "").strip()
        try:
            confidence_decimal = float(confidence) / 100
            return f"{confidence_decimal:.4f}"  # Format to 4 decimal places
        except ValueError:
            print("Invalid confidence format:", confidence)
            return None
    try:
        # If already a float, format to 6 decimal places
        return f"{float(confidence):.6f}"
    except ValueError:
        return None

def process_esg_data(txt_file: str, results_file: str, api_key: str, model: str = "gpt-4o-mini"):
    openai.api_key = api_key  # Set the OpenAI API key
    
    llm = create_open_llm(model=model)

    prompt = """
    (Only provide JSON output, with no extra text!) Extract any ESG-related 'metric' (indicator), 'value', 'unit', and 'confidence' (a decimal confidence score from 0 to 1, 
    with the actual precision level produced by the model, indicating how certain the model is about the accuracy of this extraction) from the semi-structured data below.
    Include metrics related to Environmental, Social, and Governance factors. Here are examples:

    - **Environmental**: Total GHG Emissions, Renewable Energy Usage, Water Consumption, Waste Generated, Air Quality, and other related indicators
    - **Social**: Employee Satisfaction, Diversity Ratio, Community Engagement Hours, Training and Development, and other related indicators
    - **Governance**: Board Diversity, Executive Compensation, Anti-Corruption Policies, Compliance Incidents, Corporate Donations, and other related indicators

    If no data is found, please return an empty JSON list ([]).

    """

    with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [line.strip() for line in f]

    results = []
    for line in lines:
        test_message = f"{prompt}\n\nData:\n{line}"
        content = [HumanMessage(content=test_message)]

        response = llm._call(test_message)
        print("Raw response:", response)

        json_result = extract_json(response)
        if json_result:
            for entry in json_result:
                entry['confidence'] = format_confidence(entry.get('confidence'))
                results.append(entry)

    df = pd.DataFrame(results)
    df.to_csv(results_file, index=False, encoding='utf-8-sig')
    print(f"Results saved to {results_file}")
    
# Directly call the function with required parameters 


def load_llm_model(txt_file):
    process_esg_data(txt_file, results_file, api_key)

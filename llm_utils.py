import os
import re
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

import streamlit as st

load_dotenv()

# Get API Key from Streamlit Secrets or Environment Variable
api_key = os.getenv("OPENAI_API_KEY")
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

if not api_key:
    # If no key is found, don't initialize yet, handle it in the function
    client = None
else:
    client = OpenAI(api_key=api_key)

def generate_python_code(question, df_summary):
    """Uses LLM to write Python code based on the user's question and dataframe schema."""
    if client is None:
        return "Error: OpenAI API Key not found. Please check your Streamlit Secrets."
    
    system_prompt = f"""You are a senior data analyst and Python expert working on "Talking Rabbitt", an executive intelligence layer.
Your job is to answer the user's question by writing Python code using pandas and, if appropriate, plotly.

A user uploaded a dataset with these characteristics:
Columns: {df_summary['columns']}
Info: {df_summary['info']}

Here are the first few rows:
{df_summary['sample']}

The user asked: "{question}"

Instructions:
1. Write Python code to answer the question.
2. The dataframe is already loaded as a variable named `df`. DO NOT reload or read the CSV file.
3. If the user asks for a comparison, trend, or if the resulting data is a series/aggregation, generate an interactive Plotly chart (e.g., using `plotly.express` as `px`). Save the plotly figure to a variable named `fig`.
4. Define a string variable named `answer_text` that contains the concise, business-friendly answer to the user's question (e.g., "The highest revenue was $5M in the North region.").
5. DO NOT print anything. Just define `answer_text` and optionally `fig`.
6. Return ONLY the valid, executable Python code inside a markdown code block (```python ... ```). Do not include any other conversational text or explanations.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview", # or gpt-3.5-turbo if cost is a concern, but 4 is much better at pandas
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.1
        )
        
        reply = response.choices[0].message.content
        return reply

    except Exception as e:
        return f"Error contacting LLM: {str(e)}"

def extract_code(llm_response):
    """Extracts python code from markdown block."""
    match = re.search(r"```python\n(.*?)\n```", llm_response, re.DOTALL)
    if match:
        return match.group(1)
    
    # Fallback if no markdown
    if "answer_text" in llm_response and "df" in llm_response:
         return llm_response
    
    return None

def execute_generated_code(code, df):
    """Executes the extracted code safely and returns the answer and figure."""
    if not code:
        return "Failed to generate valid code from LLM.", None
        
    # Setup the execution environment
    # Provide necessary libraries and the dataframe 'df'
    local_vars = {
        'df': df,
        'pd': pd,
        'px': px,
        'go': go,
        'plt': plt
    }
    
    # We restrict __builtins__ slightly for safety in a real app, but for this MVP 
    # we need standard builtins for pandas aggregations to work smoothly.
    # A true production app would use a more robust sandboxing environment like E2B.
    
    try:
        # Execute the code
        exec(code, globals(), local_vars)
        
        # Extract the required outputs
        answer_text = local_vars.get('answer_text', 'Code executed successfully but no answer_text was defined.')
        fig = local_vars.get('fig', None)
        
        return answer_text, fig
        
    except Exception as e:
        error_msg = f"Error executing generated code:\n{str(e)}\n\nCode attempted:\n```python\n{code}\n```"
        return error_msg, None

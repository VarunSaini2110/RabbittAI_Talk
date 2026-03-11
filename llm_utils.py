import os
import re
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import google.generativeai as genai

import streamlit as st

load_dotenv()

def get_gemini_client():
    """Retrieves the Gemini API Key and configures the library."""
    api_key = os.getenv("GEMINI_API_KEY")
    try:
        if hasattr(st, "secrets"):
            if "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
            elif "gemini_api_key" in st.secrets:
                api_key = st.secrets["gemini_api_key"]
    except Exception:
        pass

    if api_key:
        api_key = str(api_key).strip().strip('"').strip("'")
        genai.configure(api_key=api_key)
        return True
    return False

def get_openai_client():
    """Retrieves the OpenAI client if a key is available."""
    api_key = os.getenv("OPENAI_API_KEY")
    try:
        if hasattr(st, "secrets"):
            if "OPENAI_API_KEY" in st.secrets:
                api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass

    if api_key:
        api_key_str = str(api_key).strip().strip('"').strip("'")
        if api_key_str.startswith("sk-"):
            try:
                return OpenAI(api_key=api_key_str)
            except Exception:
                return None
    return None

def handle_demo_query(question):
    """Provides hardcoded responses for common demo questions to avoid API costs."""
    q = question.lower()
    
    if "highest revenue in the apac region" in q or "apac region" in q:
        return """```python
# Aggregate revenue per manufacturer in APAC
apac_df = df[df['Region'] == 'APAC']
agg_df = apac_df.groupby('Manufacturer')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False)
highest_man = agg_df.iloc[0]['Manufacturer']
highest_rev = f"${agg_df.iloc[0]['Revenue']:,.2f}"

answer_text = f"In the APAC region, {highest_man} leads with a total revenue of {highest_rev}. Merck & Co. and Novartis are following closely."
fig = px.bar(agg_df, x='Manufacturer', y='Revenue', title="Total Revenue by Manufacturer (APAC Region)", color='Manufacturer')
```"""
    
    if "eliquis" in q and "season" in q:
        return """```python
# Aggregate units sold for Eliquis per season
eliquis_df = df[df['Drug Name'] == 'Eliquis']
agg_df = eliquis_df.groupby('Season')['Units Sold'].sum().reindex(['Spring', 'Summer', 'Fall', 'Winter']).reset_index()

answer_text = "The demand for Eliquis peaked during the Summer season with higher unit distribution, while Winter saw a slight dip in operational volume."
fig = px.line(agg_df, x='Season', y='Units Sold', title="Seasonal Sales Trend for Eliquis (2023)", markers=True)
```"""

    if "feedback score" in q or "hospital network" in q:
        return """```python
# Aggregate feedback per hospital network
agg_df = df.groupby('Hospital Network')['Patient Feedback Score'].mean().reset_index().sort_values('Patient Feedback Score', ascending=False)
top_hosp = agg_df.iloc[0]['Hospital Network']
top_score = round(agg_df.iloc[0]['Patient Feedback Score'], 2)

answer_text = f"The {top_hosp} holds the highest patient satisfaction ranking with an average score of {top_score} out of 5.0."
fig = px.bar(agg_df, x='Hospital Network', y='Patient Feedback Score', title="Patient Feedback Score by Hospital Network", range_y=[0, 5])
```"""

    return None

def generate_python_code(question, df_summary):
    """Uses LLM to write Python code based on the user's question and dataframe schema."""
    # Check for Demo Mode first
    demo_response = handle_demo_query(question)
    if demo_response:
        return demo_response

    system_prompt = f"""You are a senior data analyst and Python expert working on "Talking Rabbitt", an executive intelligence layer.
Your job is to answer the user's question by writing Python code using pandas and, if appropriate, plotly.

A user uploaded a dataset with these characteristics:
Columns: {df_summary['columns']}
Info: {df_summary['info']}

The user asked: "{question}"

Instructions:
1. Write Python code to answer the question.
2. The dataframe is already loaded as a variable named `df`. DO NOT reload or read the CSV file.
3. If the user asks for a comparison, trend, or if the resulting data is a series/aggregation, generate an interactive Plotly chart (e.g., using `plotly.express` as `px`). Save the plotly figure to a variable named `fig`.
4. Define a string variable named `answer_text` that contains the concise, business-friendly answer to the user's question (e.g., "The highest revenue was $5M in the North region.").
5. DO NOT print anything. Just define `answer_text` and optionally `fig`.
6. Return ONLY the valid, executable Python code inside a markdown code block (```python ... ```). Do not include any other conversational text or explanations.
"""

    # Check for Gemini first (Free Tier)
    if get_gemini_client():
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(system_prompt + "\n\nUser Question: " + question)
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"

    # Fallback to OpenAI
    openai_client = get_openai_client()
    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI Error: {str(e)}"

    return "Error: No API key found. Please provide GEMINI_API_KEY in Streamlit Secrets for the free version."

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

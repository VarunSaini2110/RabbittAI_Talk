import streamlit as st
import pandas as pd
from data_utils import load_data, get_dataframe_summary
from llm_utils import generate_python_code, extract_code, execute_generated_code
from visualization import render_visualization

# App config
st.set_page_config(page_title="Talking Rabbitt MVP", layout="wide")

# Header
st.title("🐇 Talking Rabbitt")
st.subheader("Conversational Analytics for Executive Intelligence")
st.markdown("Upload your enterprise data and talk to it in plain English. No dashboards. No SQL. Just answers.")

# Session State
if 'df' not in st.session_state:
    st.session_state.df = None
if 'df_summary' not in st.session_state:
    st.session_state.df_summary = None
if 'history' not in st.session_state:
    st.session_state.history = []

# Section 1: File Upload
st.divider()
st.header("1. Upload Data")
uploaded_file = st.file_uploader("Upload a CSV file (Try our sample_data/pharma_sales_data.csv)", type=["csv"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is not None:
        st.session_state.df = df
        st.session_state.df_summary = get_dataframe_summary(df)
        
        st.success("File uploaded successfully!")
        with st.expander("Preview Data & Detected Columns", expanded=True):
            st.markdown(f"**Detected {len(df.columns)} Columns:**")
            st.write(df.columns.tolist())
            st.dataframe(df.head())
    else:
        st.error("Error connecting to the dataset.")

# Section 2: Conversational Interface
st.divider()
st.header("2. Ask Your Data")

if st.session_state.df is not None:
    
    # Optional: Guide the user with examples
    st.info("💡 **Try asking:** 'Compare gross revenue of Eliquis vs Keytruda in Summer vs Winter.' or 'Which Hospital Network had the lowest patient feedback score?'")
    
    question = st.text_input("What do you want to know about this data?", placeholder="e.g. Which region had the highest revenue in Q1?")
    
    if st.button("Generate Insight"):
        if question:
            with st.spinner("Talking Rabbitt is analyzing the data..."):
                # 1. Ask LLM to generate code
                llm_response = generate_python_code(question, st.session_state.df_summary)
                
                # 2. Extract code
                extracted_code = extract_code(llm_response)
                
                if extracted_code:
                    # 3. Execute code on the dataframe
                    answer_text, fig = execute_generated_code(extracted_code, st.session_state.df)
                    
                    # 4. Save to history
                    st.session_state.history.insert(0, {
                        'question': question,
                        'answer_text': answer_text,
                        'fig': fig,
                        'code': extracted_code # For transparency/debugging
                    })
                else:
                    st.error("The AI failed to generate executable code. Raw response:")
                    st.code(llm_response)
        else:
            st.warning("Please enter a question.")
else:
    st.warning("Please upload a CSV file above to start querying.")

# Section 3: Results & History
st.divider()
if st.session_state.history:
    st.header("3. Executive Insights")
    
    for i, interaction in enumerate(st.session_state.history):
        st.markdown(f"### Q: {interaction['question']}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### The Bottom Line:")
            st.success(interaction['answer_text'])
            
            with st.expander("View Code Execution (Audit Trail)"):
                st.code(interaction['code'], language="python")
                
        with col2:
            if interaction['fig']:
                st.markdown("#### Dynamic Visualization:")
                render_visualization(interaction['fig'])
        
        st.divider()

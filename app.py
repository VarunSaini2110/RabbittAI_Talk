import streamlit as st
import pandas as pd
from data_utils import load_data, get_dataframe_summary
from llm_utils import generate_python_code, extract_code, execute_generated_code
from visualization import render_visualization

# App config
st.set_page_config(page_title="Talking Rabbitt | Executive Intelligence", layout="wide", page_icon="🐇")

# Premium UI Styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: #ffffff; /* Fallback white */
    }
    .executive-card {
        padding: 20px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("Talking Rabbitt")
st.markdown("### **The Executive Intelligence Layer**")

st.markdown("---")

# Session State
if 'df' not in st.session_state:
    st.session_state.df = None
if 'df_summary' not in st.session_state:
    st.session_state.df_summary = None
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar Branding
with st.sidebar:
    st.image("assets/logo.png", width=150)
    st.title("Rabbitt AI")
    st.info("Conversational Data Intelligence for High-Growth Enterprises.")
    st.divider()
    if st.session_state.df is not None:
        st.success("Data Engine Active")
        st.write(f"Rows: {len(st.session_state.df):,}")
        st.write(f"Columns: {len(st.session_state.df.columns)}")

# Section 1: File Upload
st.header("1. Upload Data")
uploaded_file = st.file_uploader("Upload a CSV file (e.g., pharma_sales_data.csv)", type=["csv"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is not None:
        st.session_state.df = df
        st.session_state.df_summary = get_dataframe_summary(df)
        
        # KPI DASHBOARD (Only show when data is loaded)
        st.markdown("### 📊 Executive Snapshot")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        # Intelligent metrics if columns exist
        with kpi1:
            rev_col = [c for c in df.columns if 'Revenue' in c]
            if rev_col:
                total_rev = df[rev_col[0]].sum()
                st.metric("Total Revenue", f"${total_rev/1e6:.1f}M")
            else:
                st.metric("Total Rows", f"{len(df):,}")
        
        with kpi2:
            profit_col = [c for c in df.columns if 'Profit' in c]
            if profit_col:
                total_profit = df[profit_col[0]].sum()
                st.metric("Total Profit", f"${total_profit/1e6:.1f}M")
            else:
                st.metric("Data Columns", len(df.columns))
                
        with kpi3:
            hosp_col = [c for c in df.columns if 'Hospital_Network' in c]
            if hosp_col:
                unique_hosp = df[hosp_col[0]].nunique()
                st.metric("Partners", unique_hosp)
            else:
                st.metric("File Size", f"{uploaded_file.size/1024:.1f} KB")

        with kpi4:
            score_col = [c for c in df.columns if 'Score' in c]
            if score_col:
                avg_score = df[score_col[0]].mean()
                st.metric("Avg Score", f"{avg_score:.2f}/5")
            else:
                st.metric("Status", "Active")

        with st.expander("Explore Raw Dataset Infrastructure", expanded=False):
            st.dataframe(df.head(10))
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

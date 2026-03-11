import pandas as pd
import io

def load_data(file):
    """Loads CSV file into a Pandas DataFrame."""
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        return None

def get_dataframe_summary(df):
    """Extracts column names, types, and sample rows for the LLM prompt."""
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    
    sample_rows = df.head(3).to_markdown()
    
    columns_list = ", ".join(df.columns.tolist())
    
    return {
        "columns": columns_list,
        "info": info_str,
        "sample": sample_rows
    }

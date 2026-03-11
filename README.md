# Talking Rabbitt: The Executive Intelligence Layer

## The Vision
Enterprise data is broken. Traditional BI tools like PowerBI and Tableau are built for analysts, not executives. When a COO needs to know *"How did our new Pharma campaign perform in the Midwest vs. East Coast?"*, it becomes a Jira ticket that takes a week.

**Talking Rabbitt** is the conversational intelligence layer that sits *on top* of existing data structures. It reduces Time-To-Insight from 5 days to 5 seconds.

## The MVP
This repository contains a functional proof-of-concept (MVP) built in Python using Streamlit, Pandas, and OpenAI's API.

It demonstrates the "Magic Moment":
1. Upload a complex 15-column dataset (`sample_data/pharma_sales_data.csv`).
2. Ask an unstructured, complex business question.
3. The system generates a natural-language answer AND an interactive Plotly dashboard instantly directly.

### Architecture
User Prompt -> Streamlit Chatbox -> OpenAI LLM (Intent Parsing & Python Generation) -> Local Pandas Execution -> Plotly Chart Rendering -> Streamlit UI.

## How to Run Locally

### 1. Prerequisites
You need Python 3.9+ and pip installed. We highly recommend setting up a virtual environment.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API Key
You must have an OpenAI API Key. Create a `.env` file in the root directory and add your key:
```env
OPENAI_API_KEY=your_key_here
```

### 4. Run the Application
```bash
streamlit run app.py
```

### 5. Try the "Magic Moment"
- Upload the `pharma_sales_data.csv` found in the `sample_data` folder.
- Type: *"Compare the gross revenue of Pfizer vs Johnson & Johnson drugs in the Summer across all regions."*

## How to Deploy (Vercel/Streamlit Community Cloud)
To deploy this publicly (as required by the PM Challenge):

1. Commit this entire folder to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and connect your GitHub account.
3. Select your repository and point the "Main file path" to `app.py`.
4. **Crucial:** In the Streamlit Cloud advanced settings, paste your `OPENAI_API_KEY` into the Secrets management area.
5. Click Deploy!

# Talking Rabbitt: The Executive Intelligence Layer 🐇✨

## The Vision
Enterprise data is broken. Traditional BI tools like PowerBI and Tableau are built for analysts, not executives. Talking Rabbitt is the conversational intelligence layer that sits *on top* of existing data structures. It reduces Time-To-Insight from 5 days to **5 seconds**.

## The Product
This repository contains a functional, enterprise-grade MVP built in Python using Streamlit, Pandas, and **Google Gemini 1.5 Pro**.

### The "Magic Moment"
1. **Upload Data:** Upload the high-density `sample_data/pharma_sales_data.csv` (20 strategic columns, 2,500 rows).
2. **Executive Snapshot:** Instantly see a high-level KPI dashboard of your data.
3. **Conversational Query:** Ask complex business questions in plain English.
4. **Insights & Visuals:** Receive a clear "Bottom Line" answer AND an interactive Plotly dashboard instantly.

### Technical Architecture
- **Engine:** Google Gemini 1.5 Pro (via Vertex AI/AI Studio)
- **Frontend:** Streamlit with Custom Premium CSS (Glassmorphism aesthetics)
- **Data:** Pandas (Processing) & Plotly (Dynamic Visualization)
- **Fallback:** Logic handles both Gemini and OpenAI integration.

## How to Run Locally

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set API Keys:**
   Create a `.env` file or use Streamlit Secrets:
   ```env
   GEMINI_API_KEY=your_google_ai_key
   ```

3. **Launch:**
   ```bash
   streamlit run app.py
   ```

## How to Deploy (Streamlit Community Cloud)

1. Commit this folder to a GitHub repository.
2. Connect the repo to [share.streamlit.io](https://share.streamlit.io/).
3. **Important:** Add your `GEMINI_API_KEY` to the **Secrets** management in the app settings.

---
**Talking Rabbitt** | *Insight at the speed of thought.*

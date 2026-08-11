# AI-Powered Sales Insights Assistant

A Python project that turns raw sales data into plain-English business
insights using a generative AI model — built in stages, from a simple
script to a full interactive web app.

## Demo

A Streamlit web app where you can type any question about sales data
and get an instant, data-grounded answer — plus KPI cards and a
data explorer.

## Example output

> The East is currently our best performer with the highest overall
> profit, while the South trails as our weakest region in both sales
> and earnings. The biggest red flag is the West region, which
> generates massive sales volume but yields a shockingly low profit,
> indicating dangerously thin margins. I recommend auditing the West's
> pricing structure and discounting practices immediately.

## Project stages

| Stage | File | What it does |
|---|---|---|
| 1 | `stage1_insights_free_v2.py` | Fixed-metric summary: calculates region totals and gets one AI-written insight |
| 2 | `stage2_interactive_qa.py` | Terminal-based Q&A: ask any question, AI answers using precomputed data summaries |
| 3 | `stage3_streamlit_app.py` | Same Q&A logic wrapped in a basic Streamlit web app |
| 3b | `stage3b_streamlit_app_styled.py` | Polished dashboard-style version with KPI cards, custom styling, and tabbed data views |

## Tech stack

- Python
- pandas
- Google Gemini API (`google-genai`)
- Streamlit

## How it works

1. Loads sales data with pandas
2. Precomputes summaries across multiple dimensions (region, category,
   sub-category, month)
3. Sends the relevant summaries + your question to Google's Gemini API
4. Gemini answers using only the provided data (grounded, not guessed)
5. Answer is displayed either in the terminal or a Streamlit web page

## Setup

1. Clone this repo and install dependencies:
   ```
   pip install pandas google-genai streamlit
   ```

2. Get a free API key from [Google AI Studio](https://aistudio.google.com)
   (no credit card required)

3. Set it as an environment variable:
   ```
   # Windows (cmd)
   set GEMINI_API_KEY=your-key-here

   # Mac/Linux
   export GEMINI_API_KEY=your-key-here
   ```

4. Run whichever stage you want to try:
   ```
   python stage1_insights_free_v2.py
   python stage2_interactive_qa.py
   streamlit run stage3b_streamlit_app_styled.py
   ```

## Roadmap

- [x] Stage 1: fixed-metric summary generation
- [x] Stage 2: dynamic question answering
- [x] Stage 3: Streamlit UI
- [x] Stage 3b: polished dashboard-style UI
- [ ] Stage 4: swap in real Superstore dataset + MySQL integration

## Why this project

Built as part of exploring how generative AI fits into a data
analyst's toolkit — going beyond static dashboards toward
AI-assisted, natural-language explanations of data.

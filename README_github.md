# AI-Powered Sales Insights Assistant

A small Python project that turns raw sales data into a plain-English
business insight using a generative AI model — instead of just showing
numbers on a dashboard, it explains what they mean.

## What it does

1. Loads sales data (Superstore dataset) with pandas
2. Calculates region-wise total sales and profit
3. Sends those numbers to Google's Gemini API
4. Gets back a short, plain-English summary highlighting the
   best/worst performing regions and flagging any concerning
   sales-to-profit mismatches

## Example output

> The East is currently our best performer with the highest overall
> profit, while the South trails as our weakest region in both sales
> and earnings. The biggest red flag is the West region, which
> generates massive sales volume but yields a shockingly low profit,
> indicating dangerously thin margins. I recommend auditing the West's
> pricing structure and discounting practices immediately.

## Tech stack

- Python
- pandas
- Google Gemini API (`google-genai`)

## Setup

1. Clone this repo and install dependencies:
   ```
   pip install pandas google-genai
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

4. Run it:
   ```
   python stage1_insights_free_v2.py
   ```

## Roadmap

- [x] Stage 1: fixed-metric summary generation
- [ ] Stage 2: dynamic question answering (AI generates the query
      based on what you ask, instead of fixed metrics)
- [ ] Stage 3: Streamlit UI for interactive use
- [ ] Stage 4: integrate with the existing Power BI dashboard

## Why this project

Built as part of exploring how generative AI fits into a data
analyst's toolkit — going beyond static dashboards toward
AI-assisted, natural-language explanations of data.

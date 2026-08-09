"""
Stage 1: AI-Powered Sales Insights Assistant (FREE VERSION using Gemini)
--------------------------------------------------------------------------
Uses Google's NEWER official SDK (google-genai), which supports both the
old "AIza..." and new "AQ..." key formats from Google AI Studio.
"""

import os
import pandas as pd
from google import genai

# STEP 1: Load your API key
# Get one for free at https://aistudio.google.com (no credit card needed)
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "No API key found! Set the GEMINI_API_KEY environment variable first."
    )

client = genai.Client(api_key=api_key)

# STEP 2: Load your sales data
df = pd.read_csv("sample_superstore.csv")

print("Data loaded. Preview:")
print(df.head())
print("\n" + "=" * 50 + "\n")

# STEP 3: Calculate metrics with pandas
region_summary = df.groupby("Region")[["Sales", "Profit"]].sum().reset_index()

print("Region-wise summary:")
print(region_summary)
print("\n" + "=" * 50 + "\n")

# STEP 4: Turn the pandas table into plain text
summary_text = region_summary.to_string(index=False)

# STEP 5: Build the prompt
prompt = f"""You are a data analyst assistant. Below is a table showing
total sales and profit by region.

{summary_text}

Write a short, plain-English summary (3-4 sentences) explaining:
1. Which region is performing best and worst, and why that matters
2. Any region where profit looks concerning compared to its sales
3. One actionable suggestion for the sales manager

Keep it conversational, like you're briefing a manager who has no time
to read raw numbers."""

# STEP 6: Call the Gemini API using the new SDK
print("Asking Gemini to generate insights...\n")

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt
)

# STEP 7: Print the AI's text response
print("=" * 50)
print("AI-GENERATED INSIGHT:")
print("=" * 50)
print(response.text)

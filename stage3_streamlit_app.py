"""
Stage 3: AI-Powered Sales Insights Assistant (Streamlit Web App)
--------------------------------------------------------------------
Same brain as stage 2 (precomputed summaries + Gemini Q&A), but now
wrapped in a proper web interface using Streamlit instead of a
terminal window.

Streamlit turns a plain Python script into a web app just by adding
a few 'st.___' function calls - no HTML/CSS/JavaScript needed.

HOW TO RUN THIS FILE (different from stage 1 and 2!):
    streamlit run stage3_streamlit_app.py

Do NOT run it with plain 'python stage3_streamlit_app.py' - Streamlit
apps need to be launched with the 'streamlit run' command so it can
start a local web server and open your browser.
"""

import os
import pandas as pd
import streamlit as st
from google import genai

# STEP 1: Page setup
# This just controls the browser tab title and layout - purely cosmetic
st.set_page_config(page_title="AI Sales Insights Assistant", layout="centered")
st.title("AI-Powered Sales Insights Assistant")
st.write("Ask any question about your sales data and get a plain-English answer.")

# STEP 2: Load your API key
# Same idea as before, but Streamlit has its own way to show errors nicely
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("No API key found! Set the GEMINI_API_KEY environment variable "
              "in your terminal before running this app.")
    st.stop()  # stops the app here so nothing below tries to run without a key

client = genai.Client(api_key=api_key)

# STEP 3: Load and prepare the data
# @st.cache_data means: only reload/reprocess the data once, not every
# single time the page refreshes (which happens a lot in Streamlit).
# This makes the app faster.
@st.cache_data
def load_data():
    df = pd.read_csv("sample_superstore.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"] = df["Order_Date"].dt.strftime("%Y-%m")
    return df

df = load_data()

# STEP 4: Precompute summaries (same as stage 2)
@st.cache_data
def build_context(df):
    by_region = df.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
    by_category = df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
    by_subcategory = df.groupby("Sub_Category")[["Sales", "Profit"]].sum().reset_index()
    by_month = df.groupby("Month")[["Sales", "Profit"]].sum().reset_index()

    return f"""
SALES BY REGION:
{by_region.to_string(index=False)}

SALES BY CATEGORY:
{by_category.to_string(index=False)}

SALES BY SUB-CATEGORY:
{by_subcategory.to_string(index=False)}

SALES BY MONTH:
{by_month.to_string(index=False)}
"""

context = build_context(df)

# STEP 5: Show a preview of the raw data (nice touch for a demo)
with st.expander("View raw data"):
    st.dataframe(df)

# STEP 6: The question-answering function (same logic as stage 2)
def ask_question(question):
    prompt = f"""You are a data analyst assistant. You have access to the
following sales data summaries:

{context}

Using ONLY the data above, answer this question in plain English,
in 2-4 sentences. If the data above doesn't contain enough information
to answer confidently, say so honestly instead of guessing.

Question: {question}
"""
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    return response.text

# STEP 7: The interactive part - text input box + button
question = st.text_input("Your question:", placeholder="e.g. Which region has the best profit margin?")

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        answer = ask_question(question)
    st.markdown("### Answer")
    st.write(answer)

# STEP 8: A few example questions as clickable buttons (nice UX touch)
st.markdown("---")
st.write("Try an example:")
example_questions = [
    "Which category has the best profit margin?",
    "How did sales trend over the months?",
    "Is there any region we should be worried about?",
]

cols = st.columns(len(example_questions))
for col, eq in zip(cols, example_questions):
    if col.button(eq):
        with st.spinner("Thinking..."):
            answer = ask_question(eq)
        st.markdown("### Answer")
        st.write(answer)

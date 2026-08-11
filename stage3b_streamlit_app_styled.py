"""
Stage 3b: AI-Powered Sales Insights Assistant (Styled Streamlit App)
--------------------------------------------------------------------------
Same logic as stage 3, but with visual improvements:
- Custom page icon and wide layout
- KPI metric cards at the top (Total Sales, Total Profit, Best Region)
- Custom CSS for colors and spacing
- Icons and better visual hierarchy
- Chat-style display for question/answer history

Run with:
    streamlit run stage3b_streamlit_app_styled.py
"""

import os
import pandas as pd
import streamlit as st
from google import genai

# STEP 1: Page setup - wide layout looks more like a real dashboard
st.set_page_config(
    page_title="AI Sales Insights Assistant",
    page_icon="📊",
    layout="wide"
)

# STEP 2: Custom CSS
# Streamlit lets you inject raw CSS to restyle things beyond its defaults.
# This targets specific Streamlit component classes to add color, spacing,
# and rounded corners.
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fb;
    }
    .stButton>button {
        border-radius: 8px;
        border: 1px solid #4A90D9;
        color: #4A90D9;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #4A90D9;
        color: white;
    }
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e6e6e6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .answer-box {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #4A90D9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# STEP 3: Header
st.title("📊 AI-Powered Sales Insights Assistant")
st.caption("Ask questions about your sales data and get instant, plain-English answers powered by Gemini AI")

# STEP 4: Load API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("No API key found! Set the GEMINI_API_KEY environment variable in your terminal before running this app.")
    st.stop()

client = genai.Client(api_key=api_key)

# STEP 5: Load and prepare data
@st.cache_data
def load_data():
    df = pd.read_csv("sample_superstore.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"] = df["Order_Date"].dt.strftime("%Y-%m")
    return df

df = load_data()

# STEP 6: Precompute summaries
@st.cache_data
def build_summaries(df):
    by_region = df.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
    by_category = df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
    by_subcategory = df.groupby("Sub_Category")[["Sales", "Profit"]].sum().reset_index()
    by_month = df.groupby("Month")[["Sales", "Profit"]].sum().reset_index()
    return by_region, by_category, by_subcategory, by_month

by_region, by_category, by_subcategory, by_month = build_summaries(df)

context = f"""
SALES BY REGION:
{by_region.to_string(index=False)}

SALES BY CATEGORY:
{by_category.to_string(index=False)}

SALES BY SUB-CATEGORY:
{by_subcategory.to_string(index=False)}

SALES BY MONTH:
{by_month.to_string(index=False)}
"""

# STEP 7: KPI metric cards at the top
# st.metric() creates those clean stat boxes you see on real dashboards
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
best_region = by_region.loc[by_region["Profit"].idxmax(), "Region"]
best_region_profit = by_region["Profit"].max()

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🏆 Best Region", best_region)
col4.metric("Region Profit", f"${best_region_profit:,.0f}")

st.markdown("---")

# STEP 8: Two-column layout - chat on the left, data view on the right
left_col, right_col = st.columns([2, 1])

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

with left_col:
    st.subheader("💬 Ask a question")
    question = st.text_input("", placeholder="e.g. Which region has the best profit margin?", label_visibility="collapsed")

    ask_col, _ = st.columns([1, 4])
    ask_clicked = ask_col.button("Ask AI", type="primary")

    st.write("**Or try an example:**")
    example_questions = [
        "Which category has the best profit margin?",
        "How did sales trend over the months?",
        "Is there any region we should be worried about?",
    ]
    ex_cols = st.columns(len(example_questions))
    example_clicked = None
    for c, eq in zip(ex_cols, example_questions):
        if c.button(eq):
            example_clicked = eq

    final_question = question if (ask_clicked and question) else example_clicked

    if final_question:
        with st.spinner("Analyzing your data..."):
            answer = ask_question(final_question)
        st.markdown(f"""
            <div class="answer-box">
            <b>Q: {final_question}</b><br><br>
            {answer}
            </div>
        """, unsafe_allow_html=True)

with right_col:
    st.subheader("📁 Data snapshot")
    tab1, tab2, tab3 = st.tabs(["Region", "Category", "Monthly"])
    with tab1:
        st.dataframe(by_region, use_container_width=True, hide_index=True)
    with tab2:
        st.dataframe(by_category, use_container_width=True, hide_index=True)
    with tab3:
        st.dataframe(by_month, use_container_width=True, hide_index=True)

    with st.expander("View full raw data"):
        st.dataframe(df, use_container_width=True)

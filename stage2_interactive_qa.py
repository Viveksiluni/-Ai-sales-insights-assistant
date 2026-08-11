"""
Stage 2: AI-Powered Sales Insights Assistant (Interactive Q&A)
-----------------------------------------------------------------
Stage 1 only explained FIXED metrics (region totals).
This version lets YOU type any question, and the AI answers it
using several precomputed summaries of your data.

How it works (same idea as "RAG" - Retrieval Augmented Generation):
1. We precompute several useful summaries from your data ahead of time
   (by region, category, sub-category, and month)
2. When you ask a question, we send ALL of these summaries to Gemini
   along with your question
3. Gemini picks whichever summary is relevant and answers using it
   - instead of guessing from thin air, it's grounded in your real numbers
"""

import os
import pandas as pd
from google import genai

# STEP 1: Load your API key (same as stage 1)
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError(
        "No API key found! Set the GEMINI_API_KEY environment variable first."
    )

client = genai.Client(api_key=api_key)

# STEP 2: Load your sales data
df = pd.read_csv("sample_superstore.csv")

# Make sure Order_Date is treated as an actual date, not plain text,
# so we can group by month later
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Month"] = df["Order_Date"].dt.strftime("%Y-%m")

print("Data loaded successfully.\n")

# STEP 3: Precompute several summaries
# Each of these is a different "lens" on the same data.
# The AI will decide which one(s) are relevant to your question.

by_region = df.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
by_category = df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
by_subcategory = df.groupby("Sub_Category")[["Sales", "Profit"]].sum().reset_index()
by_month = df.groupby("Month")[["Sales", "Profit"]].sum().reset_index()

# STEP 4: Combine all summaries into one text block to give the AI context
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

# STEP 5: A function to ask one question
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

# STEP 6: Interactive loop - keep asking questions until user types 'exit'
print("=" * 60)
print("Ask me anything about your sales data!")
print("Type 'exit' to quit.")
print("=" * 60 + "\n")

while True:
    user_question = input("Your question: ")

    if user_question.strip().lower() == "exit":
        print("Goodbye!")
        break

    print("\nThinking...\n")
    answer = ask_question(user_question)
    print("AI Answer:")
    print(answer)
    print("\n" + "-" * 60 + "\n")

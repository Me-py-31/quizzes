import pandas as pd
import requests
import streamlit as st
from docx import Document

# ==============================================================================
# BACKEND CONFIGURATION
# Paste your Google Apps Script Webhook URL here so users don't see or enter it
# ==============================================================================
WEBHOOK_URL = "YOUR_GOOGLE_APPS_SCRIPT_WEBHOOK_URL_HERE"

st.set_page_config(
    page_title="MSPC335 IA 1 - Question Bank Collector",
    page_icon="📝",
    layout="centered",
)

st.title("📝 MSPC335 IA 1: Question Bank Collector")
st.caption("Enter your table identifier and questions below. Submissions sync automatically to the master sheet.")

with st.form("question_entry_form"):
    col1, col2 = st.columns(2)
    with col1:
        table_number = st.text_input("Table Number / Identifier", value="1")
    with col2:
        num_questions = st.number_input(
            "Number of Questions to Memorize",
            min_value=1,
            max_value=50,
            value=3,
            step=1,
        )

    st.markdown("---")
    st.subheader("Questions Input")

    questions_data = []
    for i in range(int(num_questions)):
        st.markdown(f"**Item #{i+1}**")
        q_col1, q_col2 = st.columns()
        with q_col1:
            q_num = st.text_input(
                "Question Number", value=f"Q{i+1}", key=f"q_num_{i}"
            )
        with q_col2:
            q_text = st.text_area(
                "Question Content",
                placeholder="Type question content here...",
                key=f"q_text_{i}",
                height=70,
            )

        questions_data.append(
            {
                "Table Number": table_number,
                "Question Number": q_num,
                "Question": q_text,
            }
        )

    st.markdown("---")
    submit_btn = st.form_submit_button("🚀 Submit Questions to Master Sheet")

if submit_btn:
    if WEBHOOK_URL == "YOUR_GOOGLE_APPS_SCRIPT_WEBHOOK_URL_HERE" or not WEBHOOK_URL:
        st.error("⚠️ Please set the `WEBHOOK_URL` variable in `app.py` first.")
    else:
        with st.spinner("Saving to Google Sheet..."):
            try:
                response = requests.post(WEBHOOK_URL, json=questions_data, timeout=10)
                if response.status_code == 200:
                    st.success("✅ Questions submitted and saved to the live Google Sheet!")
                else:
                    st.error(f"Failed to submit. Server status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error connecting to Google Sheet Webhook: {e}")

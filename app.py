import json
import requests
import streamlit as st

# ==============================================================================
# BACKEND CONFIGURATION
# Paste your deployed Google Apps Script Webhook URL here so it stays hidden from visitors.
# ==============================================================================
GOOGLE_DOC_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbw1Wdx0CACCMPXexjW1A5L5s9A25_nKYl-CplP8eKObe8G2OEd8DVmn-2EnFiFfN6PkXA/exec"

st.set_page_config(
    page_title="MSPC335 IA 1 - Question Collector",
    page_icon="📝",
    layout="centered",
)

st.title("📝 MSPC335 IA 1: Question & Options Collector")
st.caption(
    "Submit between 1 and 3 questions along with answer choices directly into"
    " the connected Google Doc."
)

with st.form("questions_form"):
    st.subheader("1. Submission Info")
    table_number = st.text_input("Table / Student Identifier", value="Table 1")

    # Enforces minimum 1 and maximum 3 questions per submission
    num_questions = st.number_input(
        "Number of Questions to Submit (Min: 1, Max: 3):",
        min_value=1,
        max_value=3,
        value=1,
        step=1,
    )

    st.markdown("---")
    st.subheader("2. Questions & Answer Options")

    submission_payload = []

    for i in range(int(num_questions)):
        st.markdown(f"### 📍 Question #{i+1}")

        q_num = st.text_input(
            f"Question Number / Label", value=f"Q{i+1}", key=f"q_num_{i}"
        )
        q_text = st.text_area(
            f"Question Text",
            placeholder="Type question content here...",
            key=f"q_text_{i}",
            height=80,
        )

        num_options = st.selectbox(
            f"Number of Answer Options for Question #{i+1}:",
            options=[2, 3, 4, 5],
            index=2,  # Default 4 options (A, B, C, D)
            key=f"num_opt_{i}",
        )

        options = []
        col_a, col_b = st.columns(2)
        for opt_idx in range(num_options):
            opt_label = chr(65 + opt_idx)  # A, B, C, D...
            target_col = col_a if opt_idx % 2 == 0 else col_b
            with target_col:
                opt_text = st.text_input(
                    f"Option {opt_label}",
                    placeholder=f"Choice {opt_label}",
                    key=f"opt_{i}_{opt_idx}",
                )
                options.append(f"Option {opt_label}: {opt_text}")

        submission_payload.append({
            "tableNumber": table_number,
            "questionNumber": q_num,
            "questionText": q_text,
            "options": options,
        })
        st.markdown("---")

    submit_button = st.form_submit_button("🚀 Submit to Google Doc")

if submit_button:
    if (
        GOOGLE_DOC_WEBHOOK_URL == "YOUR_GOOGLE_APPS_SCRIPT_WEBHOOK_URL_HERE"
        or not GOOGLE_DOC_WEBHOOK_URL
    ):
        st.error(
            "⚠️ Please configure GOOGLE_DOC_WEBHOOK_URL with your Google Apps"
            " Script Webhook URL."
        )
    else:
        with st.spinner("Saving questions and answer options to Google Doc..."):
            try:
                response = requests.post(
                    GOOGLE_DOC_WEBHOOK_URL,
                    data=json.dumps(submission_payload),
                    headers={"Content-Type": "application/json"},
                    timeout=15,
                )
                if response.status_code == 200:
                    st.success(
                        "✅ Questions and answer options successfully saved to"
                        " your connected Google Doc!"
                    )
                else:
                    st.error(
                        "Failed to submit. Server status code:"
                        f" {response.status_code}"
                    )
            except Exception as e:
                st.error(f"Error connecting to Google Webhook: {e}")

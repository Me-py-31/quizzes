import streamlit as st
import pandas as pd
import datetime
import uuid
from streamlit_gsheets import GSheetsConnection
conn = st.connection("gsheets", type=GSheetsConnection)
# Assign a unique session ID for each visitor
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]  # Short 8-character ID

def log_response(module_name, category, question_text, selected_option, correct_answer, is_correct):
    try:
        # ttl=0 prevents caching issues
        existing_df = conn.read(worksheet="Sheet1", ttl=0) 
        
        new_entry = pd.DataFrame([{
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "User_ID": st.session_state.user_id,
            "Module": module_name,
            "Category": category,
            "Question": question_text[:80],
            "Selected_Option": selected_option,
            "Correct_Answer": correct_answer,
            "Is_Correct": "Correct" if is_correct else "Incorrect"
        }])

        updated_df = pd.concat([existing_df, new_entry], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        st.toast("Response recorded to Google Sheets! ✅") # Visual confirmation
        
    except Exception as e:
        # Display the hidden error directly on screen
        st.error(f"Google Sheets Error: {e}")

# ------------------------------------------------------------------------------
# 3. EXAMPLE QUIZ QUESTION INTEGRATION
# ------------------------------------------------------------------------------
def render_question(q_id, module_name, category, question_dict):
    st.subheader(question_dict["question"])
    
    # Unique key for Streamlit state
    radio_key = f"{module_name}_{q_id}"
    
    user_choice = st.radio(
        "Select your answer:", 
        question_dict["options"], 
        key=radio_key, 
        index=None
    )
    
    if user_choice is not None:
        selected_letter = user_choice.split(".").strip()
        is_correct = (selected_letter == question_dict["answer"])
        
        # Display Result UI
        if is_correct:
            st.success(f"Correct! 🎉\n\n**Explanation:** {question_dict['explanation']}")
        else:
            st.error(f"Incorrect. Correct Answer: **{question_dict['answer']}**\n\n**Explanation:** {question_dict['explanation']}")
            
        # Log response to Google Sheets (triggers only once per radio button selection)
        if f"logged_{radio_key}" not in st.session_state:
            log_response(
                module_name=module_name,
                category=category,
                question_text=question_dict["question"],
                selected_option=selected_letter,
                correct_answer=question_dict["answer"],
                is_correct=is_correct
            )
            st.session_state[f"logged_{radio_key}"] = True
st.title("🧪 Google Sheets Connection Test")

try:
    st.write("1. Initializing connection...")
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.success("Connection initialized!")

    if st.button("Click to Test Write"):
        st.write("2. Reading current sheet...")
        df = conn.read(worksheet="Sheet1", ttl=0)
        st.write("Current rows found:", len(df))

        st.write("3. Attempting to write test row...")
        test_data = pd.DataFrame([{
            "Timestamp": str(datetime.datetime.now()),
            "User_ID": "TEST_USER",
            "Module": "TEST",
            "Category": "TEST",
            "Question": "Test question?",
            "Selected_Option": "A",
            "Correct_Answer": "A",
            "Is_Correct": "Correct"
        }])

        updated_df = pd.concat([df, test_data], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        st.success("🎉 SUCCESS! Check your Google Sheet now!")

except Exception as e:
        st.error(f"❌ FAILED AT STEP: {e}")
        st.exception(e)  # Prints the full stack trace on screen

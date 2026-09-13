import streamlit as st
import pandas as pd
import datetime
import uuid
from streamlit_gsheets import GSheetsConnection

# ------------------------------------------------------------------------------
# STREAMLIT CONFIG & GOOGLE SHEETS CONNECTION
# ------------------------------------------------------------------------------
st.set_page_config(page_title="💪🏼MSPC 235 Interactive Quiz & Tracker", layout="wide")

st.title("💪🏼 MSPC 235: Musculoskeletal & Locomotor Systems Question Bank")
st.caption("Categorized by Case Scenarios, True/False, Exceptions & Direct MCQs with Real-Time Response Logging")

# Initialize Google Sheets connection
# Initialize Google Sheets connection
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    conn = None
st.set_page_config(page_title="Medical Science Quiz", layout="wide")

# Input name for each visitor
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
except Exception:
    conn = None
if not st.session_state.user_name:
    st.title("🎓 Medical Science Exam Quiz")
    st.subheader("Welcome! Please enter your details to begin.")
    
    # Input field for Student Name / ID
    input_name = st.text_input("Enter your Full Name or Student ID:", placeholder="e.g. John Doe / ST12345")
    
    if st.button("Start Quiz 🚀"):
        if input_name.strip():
            st.session_state.user_name = input_name.strip()
            st.rerun()  # Refresh page to load quiz tabs
        else:
            st.warning("⚠️ Please enter your name before proceeding.")
            
    # Stop execution here until name is provided
    st.stop()
    
# Helper function to log responses
def log_response(module_name, category, question_text, selected_option, correct_answer, is_correct):
    if conn is None:
        return
    try:
        existing_df = conn.read(worksheet=module_name, ttl=0)
    except Exception:
        existing_df = pd.DataFrame(columns=[
            "Timestamp", "User_ID", "Module", "Category", 
            "Question", "Selected_Option", "Correct_Answer", "Is_Correct"
        ])

    new_entry = pd.DataFrame([{
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "User_ID": st.session_state.user_name,
        "Module": module_name,
        "Category": category,
        "Question": question_text[:80] + "...",
        "Selected_Option": selected_option,
        "Correct_Answer": correct_answer,
        "Is_Correct": "Correct" if is_correct else "Incorrect"
    }])

    updated_df = pd.concat([existing_df, new_entry], ignore_index=True)
    conn.update(worksheet=module_name, data=updated_df)
    st.toast("Response recorded to Google Sheets! ✅")
    
st.title("🎓 MSPC Interactive Exam Quiz")
st.sidebar.markdown(f"👤 **Student Logged In:**\n`{st.session_state.user_name}`")

if st.sidebar.button("Log Out / Change Name"):
    st.session_state.user_name = ""
    st.rerun()
# ------------------------------------------------------------------------------
# MSPC 235 QUESTION DATA
# ------------------------------------------------------------------------------
data_235 = {
    "case_scenarios": [
        {
            "question": "A 25-year-old construction worker falls from scaffolding and lands heavily on his shoulder, forcibly increasing the angle between his neck and shoulder. Physical exam reveals his right arm hangs adducted by his side, medially rotated, and the forearm pronated ('waiter's tip' posture). Which spinal roots were injured?",
            "options": ["A. C5 and C6 roots (Upper trunk)", "B. C7 root (Middle trunk)", "C. C8 and T1 roots (Lower trunk)", "D. T1 and T2 roots", "E. C5 and T1 roots"],
            "answer": "A",
            "explanation": "Erb-Duchenne palsy involves injury to upper roots C5-C6, paralyzing supraspinatus, infraspinatus, biceps brachii, and brachialis, leading to waiter's tip deformity."
        },
        {
            "question": "A 45-year-old woman undergoes chest tube insertion for a pleural effusion. The following day she complains of weakness pushing forward with her right arm. Exam shows protrusion of the medial border of her right scapula when pushing against a wall. Which nerve was injured?",
            "options": ["A. Thoracodorsal nerve", "B. Axillary nerve", "C. Long thoracic nerve", "D. Suprascapular nerve", "E. Radial nerve"],
            "answer": "C",
            "explanation": "Injury to the Long Thoracic nerve (C5-C7) paralyzes Serratus Anterior, causing 'winged scapula' and inability to abduct the arm above 90 degrees."
        },
        {
            "question": "A 26-year-old man slips and falls onto his outstretched hand. He presents to the ER with intense tenderness in the anatomical snuffbox. X-rays confirm a carpal bone fracture. Which bone is most commonly fractured in this mechanism?",
            "options": ["A. Lunate", "B. Scaphoid", "C. Hamate", "D. Pisiform", "E. Trapezium"],
            "answer": "B",
            "explanation": "Falling on an outstretched hand (FOOSH) most commonly causes a fracture of the scaphoid bone, manifesting with snuffbox tenderness."
        },
        {
            "question": "A 35-year-old female typist complains of numbness and tingling over the palmar aspect of her thumb, index, and middle fingers, accompanied by thenar muscle wasting. Which nerve is compressed in the carpal tunnel?",
            "options": ["A. Ulnar nerve", "B. Deep branch of radial nerve", "C. Median nerve", "D. Musculocutaneous nerve", "E. Superficial radial nerve"],
            "answer": "C",
            "explanation": "Carpal tunnel syndrome results from entrapment of the median nerve beneath the flexor retinaculum, sparing thenar sensation only over the palmar cutaneous branch."
        }
    ],
    "true_false": [
        {
            "question": "Cartilage tissue is highly vascularized, allowing rapid wound repair following traumatic fracture. (TRUE / FALSE)",
            "options": ["A. True", "B. False"],
            "answer": "B",
            "explanation": "FALSE. Cartilage is avascular; chondrocytes rely on slow nutrient diffusion through the hydrated proteoglycan matrix, resulting in poor regenerative capacity."
        },
        {
            "question": "The Long Thoracic nerve arises directly from the C5, C6, and C7 ventral rami (roots) of the brachial plexus. (TRUE / FALSE)",
            "options": ["A. True", "B. False"],
            "answer": "A",
            "explanation": "TRUE. Long thoracic nerve is a direct root branch (C5, C6, C7) supplying Serratus Anterior."
        },
        {
            "question": "The Clavicle is the first bone in the human body to begin ossification, developing via intramembranous ossification. (TRUE / FALSE)",
            "options": ["A. True", "B. False"],
            "answer": "A",
            "explanation": "TRUE. The clavicle is the first bone to ossify (week 5-6 fetal life) primarily through intramembranous ossification."
        }
    ],
    "exceptions": [
        {
            "question": "All of the following muscles form part of the Rotator Cuff surrounding the shoulder joint EXCEPT:",
            "options": ["A. Supraspinatus", "B. Infraspinatus", "C. Teres minor", "D. Subscapularis", "E. Teres major"],
            "answer": "E",
            "explanation": "The rotator cuff (SITS) comprises Supraspinatus, Infraspinatus, Teres minor, and Subscapularis. Teres major is NOT part of the cuff."
        },
        {
            "question": "Which of the following structures is NOT a constituent forming the boundaries of the anatomical snuffbox?",
            "options": ["A. Extensor pollicis longus tendon", "B. Extensor pollicis brevis tendon", "C. Abductor pollicis longus tendon", "D. Abductor pollicis brevis tendon", "E. Radial artery in the floor"],
            "answer": "D",
            "explanation": "The snuffbox is bounded medially by EPL tendon and laterally by EPB and APL tendons. Abductor pollicis brevis is a thenar muscle, not a border."
        }
    ],
    "direct_mcqs": [
        {
            "question": "Which muscle initiates the first 0 to 15 degrees of arm abduction at the glenohumeral joint?",
            "options": ["A. Deltoid", "B. Supraspinatus", "C. Infraspinatus", "D. Teres major", "E. Subscapularis"],
            "answer": "B",
            "explanation": "Supraspinatus initiates abduction (0-15°); Deltoid takes over for 15-90°; Serratus anterior and Trapezius rotate scapula above 90°."
        },
        {
            "question": "Which nerve provides motor innervation to the Deltoid and Teres minor muscles?",
            "options": ["A. Suprascapular nerve", "B. Radial nerve", "C. Axillary nerve", "D. Musculocutaneous nerve", "E. Thoracodorsal nerve"],
            "answer": "C",
            "explanation": "The Axillary nerve (C5-C6) passes through the quadrangular space to supply Deltoid and Teres minor."
        }
    ]
}

# ------------------------------------------------------------------------------
# RENDER QUIZ UI & TABS
# ------------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🩺 Case Scenarios", 
    "❌/✅ True or False", 
    "⚠️ Exception Questions", 
    "📚 Direct MCQs"
])

def render_category(questions, category_name, prefix):
    for idx, q in enumerate(questions):
        st.subheader(f"Q{idx+1}. {q['question']}")
        key = f"{prefix}_{idx}"
        
        user_choice = st.radio("Select your answer:", q["options"], key=key, index=None)
        
        if user_choice is not None:
            selected_letter = user_choice.split(".")[0].strip()
            is_correct = (selected_letter == q["answer"])
            
            if is_correct:
                st.success(f"Correct! 🎉\n\n**Explanation:** {q['explanation']}")
            else:
                st.error(f"Incorrect. Correct Answer: **{q['answer']}**\n\n**Explanation:** {q['explanation']}")
            
            # Log to Google Sheets
            if f"logged_{key}" not in st.session_state:
                log_response(
                    module_name="MSPC235",
                    category=category_name,
                    question_text=q["question"],
                    selected_option=selected_letter,
                    correct_answer=q["answer"],
                    is_correct=is_correct
                )
                st.session_state[f"logged_{key}"] = True
        st.divider()

with tab1:
    st.header("🩺 Clinical Case Scenarios")
    render_category(data_235["case_scenarios"], "Case Scenarios", "case")

with tab2:
    st.header("❌/✅ True or False Questions")
    render_category(data_235["true_false"], "True or False", "tf")

with tab3:
    st.header("⚠️ Exception & Negative Constraint Questions")
    render_category(data_235["exceptions"], "Exceptions", "exc")

with tab4:
    st.header("📚 Direct & Conceptual MCQs")
    render_category(data_235["direct_mcqs"], "Direct MCQs", "dir")

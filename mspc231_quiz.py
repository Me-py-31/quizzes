import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# ------------------------------------------------------------------------------
# STREAMLIT CONFIG & GOOGLE SHEETS CONNECTION
# ------------------------------------------------------------------------------
st.set_page_config(page_title="🧪MSPC 231 Interactive Quiz & Tracker", layout="wide")

st.title("💊 MSPC 231: Cell Biology, Histology & Physiology Question Bank")
st.caption("Categorized by Case Scenarios, True/False, Exceptions & Direct MCQs with Real-Time Response Logging")

# Initialize Google Sheets connection
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# Initialize session state for user authentication
if "verified_user" not in st.session_state:
    st.session_state.verified_user = None  # Stores verified student dict: {"name": ..., "id": ...}


# ------------------------------------------------------------------------------
# 2. STUDENT ROSTER VERIFICATION FUNCTION
# ------------------------------------------------------------------------------
def verify_student(input_identifier):
    """
    Checks if the entered Name or ID exists in the 'Student_Roster' sheet tab.
    Expected columns in roster sheet: 'Student_ID', 'Student_Name'
    """
    if conn is None:
        st.error("Google Sheets connection not configured.")
        return None

    try:
        # Read the Student_Roster tab (cached for 5 mins / 300s to keep it fast)
        roster_df = conn.read(worksheet="Student_Roster", ttl=300)
        
        # Clean and standardize search query
        search_query = str(input_identifier).strip().lower()

        # Check for match in either Student_ID or Student_Name columns
        match = roster_df[(roster_df["Student_ID"] == search_query) | (roster_df["Student_Name"] == search_query)]

        if not match.empty:
            matched_row = match.iloc
            return {
                "id": str(matched_row["Student_ID"]),
                "name": str(matched_row["Student_Name"])
            }
        else:
            return None

    except Exception as e:
        st.error(f"Error accessing Student Roster sheet: {e}")
        return None


# ------------------------------------------------------------------------------
# 3. VERIFICATION LOGIN GATE (LOCKS QUIZ UNTIL VERIFIED)
# ------------------------------------------------------------------------------
if not st.session_state.verified_user:
    st.title("🎓 Medical Science Professional Exam Portal")
    st.subheader("🔒 Student Identity Verification")
    st.caption("Please enter your official Student ID or Full Name to access the quiz.")

    with st.form("login_form"):
        user_input = st.text_input(
            "Student ID or Full Name:", 
            placeholder="e.g. ST10293 or Jane Doe"
        )
        submit_button = st.form_submit_button("Verify & Start Quiz 🚀")

    if submit_button:
        if user_input.strip():
            with st.spinner("Checking official student roster..."):
                student_info = verify_student(user_input)
                
            if student_info:
                st.session_state.verified_user = student_info
                st.success(f"✅ Identity Verified! Welcome, **{student_info['name']}** ({student_info['id']}).")
                st.rerun()  # Refresh page to load the quiz tabs
            else:
                st.error("❌ **Access Denied:** ID or Name not found in the official student roster. Please check for typos or contact your course administrator.")
        else:
            st.warning("⚠️ Please enter your Student ID or Name.")

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
# MSPC 231 QUESTION DATA
# ------------------------------------------------------------------------------
data_231 = {
    "case_scenarios": [
        {
            "question": "A 45-year-old mechanic was brought to the emergency department after being found unconscious in his closed garage with his car engine running. Blood gas analysis confirms severe carbon monoxide (CO) poisoning with O2 saturation under 10%. Which of the following is the most appropriate immediate intervention?",
            "options": ["A. Administer 100% high-flow oxygen immediately", "B. Perform an immediate emergency blood transfusion", "C. Administer IV bicarbonate", "D. Wait for specialist re-evaluation", "E. Hyperbaric nitric oxide"],
            "answer": "A",
            "explanation": "High-flow 100% oxygen decreases the half-life of carboxyhemoglobin by competing with CO for heme binding sites on hemoglobin."
        },
        {
            "question": "A patient with uncontrolled diabetes mellitus presents with severe hyperglycemia (blood glucose > 300 mg/dL). Which of the following changes is expected in the osmolality of their body fluids?",
            "options": ["A. Decreased ECF osmolality", "B. Increased ECF osmolality", "C. No change in osmolality", "D. Decreased ICF osmolality only", "E. Increased oncotic pressure only"],
            "answer": "B",
            "explanation": "Glucose is an effective osmole; severe hyperglycemia draws water out of cells into the ECF, elevating extracellular osmolality."
        },
        {
            "question": "A 16-year-old male presenting with severe watery diarrhea due to cholera loses a significant volume of water and electrolytes. What is the primary physiological effect on his body fluid compartments?",
            "options": ["A. Increased ICF volume", "B. Hyperosmotic expansion of ECF", "C. Isosmotic or hyposmotic fluid volume contraction", "D. Increased plasma oncotic pressure", "E. Zero fluid shift"],
            "answer": "C",
            "explanation": "Isotonic/hyposmotic electrolyte and water loss leads to volume contraction in the extracellular fluid compartment."
        },
        {
            "question": "A 28-year-old man presents with primary infertility. Physical examination reveals a left-sided varicocele. Semen analysis demonstrates oligozoospermia. What is the primary pathophysiological mechanism impairing his spermatogenesis?",
            "options": ["A. Autoimmune destruction of Sertoli cells", "B. Chromosomal nondisjunction", "C. Elevated testicular temperature due to venous stasis", "D. Pituitary insensitivity to GnRH", "E. Leydig cell necrosis"],
            "answer": "C",
            "explanation": "Venous stasis in varicoceles impairs countercurrent heat exchange, raising testicular temperature above optimal levels (~35°C)."
        },
        {
            "question": "A 60-year-old man with severe intellectual disability is evaluated. His urine yields a positive green color reaction upon addition of ferric chloride. Which amino acid metabolite is accumulated and detected in his urine?",
            "options": ["A. Homogentisic acid", "B. Phenylalanine / Phenylpyruvate", "C. Branched-chain alpha-ketoacids", "D. Methylmalonic acid", "E. Cystathionine"],
            "answer": "B",
            "explanation": "Ferric chloride reacts with phenylpyruvate (a phenylalanine metabolite in PKU) to produce a characteristic olive-green color."
        }
    ],
    "true_false": [
        {
            "question": "Regarding cell membrane fluidity, cells adapt to cold temperatures by increasing the proportion of saturated fatty acid chains in membrane phospholipids. (TRUE / FALSE)",
            "options": ["A. True", "B. False"],
            "answer": "B",
            "explanation": "FALSE. Cells adapt to cold temperatures by increasing unsaturated fatty acids (cis double bonds) to prevent membrane packing and maintain fluidity."
        },
        {
            "question": "The resting membrane potential of a neuron is primarily established and maintained by the passive leak of potassium ions out of the cell down its concentration gradient. (TRUE / FALSE)",
            "options": ["A. True", "B. False"],
            "answer": "A",
            "explanation": "TRUE. High resting K+ permeability via K+ leak channels brings the resting potential close to the Nernst equilibrium potential for potassium (-90 mV)."
        },
        {
            "question": "Primary structure of a protein refers to its amino acid sequence, and this level of organization is readily destroyed during heat-induced denaturation. (TRUE / FALSE)",
            "options": ["A. True", "B. False"],
            "answer": "B",
            "explanation": "FALSE. Denaturation disrupts non-covalent secondary, tertiary, and quaternary structures, but covalent peptide bonds maintaining primary structure remain intact."
        },
        {
            "question": "The absolute refractory period of an action potential prevents backward propagation and ensures unidirectional signal transmission down an axon. (TRUE / FALSE)",
            "options": ["A. True", "B. False"],
            "answer": "A",
            "explanation": "TRUE. Voltage-gated Na+ channel inactivation during the absolute refractory period prevents re-excitation of recently depolarized membrane segments."
        }
    ],
    "exceptions": [
        {
            "question": "All of the following are recognized physiological functions of the plasmalemma EXCEPT:",
            "options": ["A. Defining the outer physical boundary of the cell", "B. Regulating intracellular electrolyte composition", "C. Initiating the biochemical steps of nuclear DNA replication", "D. Mediating cell-cell recognition", "E. Transducing extracellular signals"],
            "answer": "C",
            "explanation": "Nuclear DNA replication initiation occurs inside the nucleus controlled by origin recognition complexes and cyclin-CDK complexes, not the plasmalemma."
        },
        {
            "question": "Which of the following transport processes does NOT require direct or indirect cellular energy expenditure (ATP)?",
            "options": ["A. Na+/K+ ATPase pump action", "B. Receptor-mediated endocytosis of LDL", "C. Glucose entry into neurons via GLUT-3 transport", "D. Calcium uptake into sarcoplasmic reticulum via SERCA", "E. Gastric proton pump action"],
            "answer": "C",
            "explanation": "GLUT transport is facilitated diffusion down a concentration gradient and requires no ATP."
        },
        {
            "question": "All of the following clinical conditions are direct consequences of primary organelle dysfunction EXCEPT:",
            "options": ["A. Tay-Sachs disease (Lysosomal defect)", "B. MELAS syndrome (Mitochondrial defect)", "C. Zellweger syndrome (Peroxisomal defect)", "D. Marfan syndrome (Extracellular matrix fibrillin mutation)", "E. I-cell disease (Golgi defect)"],
            "answer": "D",
            "explanation": "Marfan syndrome is caused by a genetic mutation in FBN1 encoding fibrillin-1 (an extracellular matrix protein), not an organelle defect."
        }
    ],
    "direct_mcqs": [
        {
            "question": "How many major physiological organ systems are conventionally classified within the human body?",
            "options": ["A. 9", "B. 10", "C. 11", "D. 12", "E. 14"],
            "answer": "C",
            "explanation": "There are 11 major organ systems in the human body."
        },
        {
            "question": "At the neuronal axon hillock, rapid action potential initiation is facilitated by a high density of which membrane channel type?",
            "options": ["A. Ligand-gated nicotinic channels", "B. Mechanically-gated cation channels", "C. Voltage-gated sodium channels", "D. Calcium-activated potassium channels", "E. Passive chloride leak channels"],
            "answer": "C",
            "explanation": "The axon hillock has the lowest threshold for action potential generation due to its exceptionally high concentration of voltage-gated Na+ channels."
        },
        {
            "question": "A membrane transport protein that moves two distinct solute species simultaneously in opposite directions across the lipid bilayer is termed a:",
            "options": ["A. Uniporter", "B. Symporter", "C. Antiporter", "D. ABC transporter", "E. Ion channel"],
            "answer": "C",
            "explanation": "Antiporters (exchangers) transport two different ions/molecules in opposite directions across a membrane."
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
                    module_name="MSPC231",
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
    render_category(data_231["case_scenarios"], "Case Scenarios", "case")

with tab2:
    st.header("❌/✅ True or False Questions")
    render_category(data_231["true_false"], "True or False", "tf")

with tab3:
    st.header("⚠️ Exception & Negative Constraint Questions")
    render_category(data_231["exceptions"], "Exceptions", "exc")

with tab4:
    st.header("📚 Direct & Conceptual MCQs")
    render_category(data_231["direct_mcqs"], "Direct MCQs", "dir")

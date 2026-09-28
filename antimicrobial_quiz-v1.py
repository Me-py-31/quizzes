import streamlit as st
import pandas as pd
import datetime
import time
from streamlit_gsheets import GSheetsConnection

# ------------------------------------------------------------------------------
# 1. STREAMLIT CONFIG & GOOGLE SHEETS INITIALIZATION
# ------------------------------------------------------------------------------
st.set_page_config(page_title="🧪 Antimicrobials & Drug Resistance Quiz (1-Min Timer)", layout="wide")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

if "verified_user" not in st.session_state:
    st.session_state.verified_user = None

# ------------------------------------------------------------------------------
# 2. ROSTER VERIFICATION GATE
# ------------------------------------------------------------------------------
def verify_student(input_identifier):
    search_query = str(input_identifier).strip().lower()
    if search_query.endswith(".0"):
        search_query = search_query[:-2]

    if not search_query or conn is None:
        return {"id": search_query.upper(), "name": search_query.title()}

    try:
        roster_df = conn.read(worksheet="Student_Roster", ttl=60)
        roster_df.columns = roster_df.columns.str.strip().str.lower()
        
        id_cols = [c for c in roster_df.columns if "id" in c]
        name_cols = [c for c in roster_df.columns if "name" in c]

        if id_cols and name_cols:
            id_col = id_cols[0]
            name_col = name_cols[0]
            
            id_series = (
                roster_df[id_col]
                .astype(str)
                .str.strip()
                .str.lower()
                .str.replace(r"\.0$", "", regex=True)
            )
            name_series = (
                roster_df[name_col]
                .astype(str)
                .str.strip()
                .str.lower()
            )
            
            match = roster_df[(id_series == search_query) | (name_series == search_query)]
            
            if not match.empty:
                row = match.iloc[0]
                clean_id = str(row[id_col]).strip()
                if clean_id.endswith(".0"):
                    clean_id = clean_id[:-2]
                    
                return {
                    "id": clean_id,
                    "name": str(row[name_col]).strip()
                }
    except Exception as e:
        pass
        
    return {"id": search_query.upper(), "name": search_query.title()}


if st.session_state.verified_user is None:
    st.title("🧪 Antimicrobials & Drug Resistance Exam Portal")
    st.subheader("⏱️ Timed Assessment (60 Seconds Per Question)")
    st.caption("Please enter your official Student ID or Full Name to begin.")

    user_input = st.text_input("Student ID or Full Name:", placeholder="e.g. ST203001, 203001, or Jane Doe", key="login_field")
    
    if st.button("Verify & Start Timed Quiz 🚀"):
        if user_input.strip():
            with st.spinner("Checking student roster..."):
                student_info = verify_student(user_input)
                
            st.session_state.verified_user = student_info
            st.rerun()
        else:
            st.warning("⚠️ Please enter your Student ID or Name.")

    st.stop()

# ------------------------------------------------------------------------------
# 3. RESPONSE LOGGING FUNCTION
# ------------------------------------------------------------------------------
def log_response(module_name, category, question_text, selected_option, correct_answer, is_correct, time_taken):
    if conn is None or st.session_state.verified_user is None:
        return
        
    student = st.session_state.verified_user
    
    try:
        existing_df = conn.read(worksheet=module_name, ttl=0)
    except Exception:
        existing_df = pd.DataFrame(columns=[
            "Timestamp", "Student_ID", "Student_Name", "Module", 
            "Category", "Question", "Selected_Option", "Correct_Answer", "Is_Correct", "Time_Taken_Sec"
        ])

    new_entry = pd.DataFrame([{
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Student_ID": student["id"],
        "Student_Name": student["name"],
        "Module": module_name,
        "Category": category,
        "Question": question_text[:80] + "...",
        "Selected_Option": selected_option if selected_option else "TIME EXPIRED",
        "Correct_Answer": correct_answer,
        "Is_Correct": "Correct" if is_correct else "Incorrect",
        "Time_Taken_Sec": time_taken
    }])

    try:
        updated_df = pd.concat([existing_df, new_entry], ignore_index=True)
        conn.update(worksheet=module_name, data=updated_df)
        st.toast("Response recorded to Google Sheets! ✅")
    except Exception:
        pass


# ------------------------------------------------------------------------------
# 4. QUESTION BANK (ANTIMICROBIALS & DRUG RESISTANCE)
# ------------------------------------------------------------------------------
ANTIMICROBIAL_QS = [
    {
        "id": 1,
        "category": "Cell Wall Inhibitors",
        "question": "Which of the following is the primary mechanism of action of beta-lactam antibiotics (e.g., Penicillins, Cephalosporins)?",
        "options": [
            "A. Inhibition of bacterial DNA gyrase",
            "B. Binding to 30S ribosomal subunit causing mRNA misreading",
            "C. Inhibition of transpeptidase enzymes (PBPs) preventing peptidoglycan cross-linking",
            "D. Binding to D-alanyl-D-alanine termini of cell wall peptidoglycan precursors"
        ],
        "answer": "C. Inhibition of transpeptidase enzymes (PBPs) preventing peptidoglycan cross-linking",
        "explanation": "Beta-lactam antibiotics covalently bind and inhibit Penicillin-Binding Proteins (PBPs), specifically transpeptidases, blocking the final cross-linking step of peptidoglycan cell wall synthesis in dividing bacteria."
    },
    {
        "id": 2,
        "category": "Drug Resistance Mechanisms",
        "question": "Methicillin-Resistant Staphylococcus aureus (MRSA) confers resistance to virtually all beta-lactams primarily through which genetic mechanism?",
        "options": [
            "A. Plasmid-mediated TEM-1 beta-lactamase secretion",
            "B. Acquisition of the mecA gene encoding an altered PBP2a with low affinity for beta-lactams",
            "C. Overexpression of ATP-binding cassette (ABC) efflux pumps",
            "D. D-alanyl-D-lactate replacement in cell wall precursor pentapeptides"
        ],
        "answer": "B. Acquisition of the mecA gene encoding an altered PBP2a with low affinity for beta-lactams",
        "explanation": "MRSA carries the mecA gene (located on the SCCmec element), which encodes PBP2a. PBP2a has a markedly reduced binding affinity for all beta-lactams except 5th-generation cephalosporins (e.g., ceftaroline)."
    },
    {
        "id": 3,
        "category": "Cell Wall Inhibitors",
        "question": "Vancomycin exerts its bactericidal effect by binding to which specific molecular target?",
        "options": [
            "A. Active site of transpeptidase enzymes",
            "B. D-alanyl-D-alanine terminus of cell wall peptidoglycan pentapeptide chains",
            "C. 50S ribosomal peptidyl transferase center",
            "D. Bacterial lipid II plasma membrane bilayer"
        ],
        "answer": "B. D-alanyl-D-alanine terminus of cell wall peptidoglycan pentapeptide chains",
        "explanation": "Vancomycin is a glycopeptide that binds directly to the D-Ala-D-Ala stem of cell wall precursors, sterically blocking both transglycosylase and transpeptidase reactions. Vancomycin-Resistant Enterococci (VRE) mutate this target to D-Ala-D-Lac."
    },
    {
        "id": 4,
        "category": "Protein Synthesis Inhibitors",
        "question": "Which class of protein synthesis inhibitors binds irreversibly to the 30S ribosomal subunit, is bactericidal, and requires oxygen for intracellular transport?",
        "options": [
            "A. Tetracyclines",
            "B. Macrolides",
            "C. Aminoglycosides",
            "D. Chloramphenicol"
        ],
        "answer": "C. Aminoglycosides",
        "explanation": "Aminoglycosides (e.g., Gentamicin, Amikacin) require an oxygen-dependent active transport mechanism to cross the inner bacterial membrane. They bind 30S ribosomal subunits, causing mRNA misreading and cell death. They are ineffective against anaerobes."
    },
    {
        "id": 5,
        "category": "Protein Synthesis Inhibitors",
        "question": "Which antibiotic binds to the 30S subunit to block aminoacyl-tRNA attachment, but is contraindicated in young children due to deposition in calcifying bones and teeth?",
        "options": [
            "A. Doxycycline / Tetracyclines",
            "B. Erythromycin / Macrolides",
            "C. Clindamycin",
            "D. Ciprofloxacin"
        ],
        "answer": "A. Doxycycline / Tetracyclines",
        "explanation": "Tetracyclines chelate divalent cations ($Ca^{2+}, Mg^{2+}$) and deposit in active bone growth plates and developing teeth, causing permanent tooth discoloration and enamel hypoplasia in children under 8 years."
    },
    {
        "id": 6,
        "category": "Protein Synthesis Inhibitors",
        "question": "Macrolides (e.g., Azithromycin, Erythromycin) inhibit protein synthesis by binding to which site?",
        "options": [
            "A. 30S subunit blocking aminoacyl-tRNA binding",
            "B. 50S subunit 23S rRNA blocking peptidyl translocation",
            "C. Bacterial RNA polymerase beta-subunit",
            "D. DNA Topoisomerase IV active site"
        ],
        "answer": "B. 50S subunit 23S rRNA blocking peptidyl translocation",
        "explanation": "Macrolides bind the 23S rRNA of the 50S ribosomal subunit, preventing the translocation step (peptidyl-tRNA movement from A site to P site) during peptide chain elongation."
    },
    {
        "id": 7,
        "category": "Nucleic Acid Synthesis Inhibitors",
        "question": "Fluoroquinolones (e.g., Ciprofloxacin, Levofloxacin) inhibit bacterial replication by targeting which enzymes?",
        "options": [
            "A. Dihydropteroate synthase and Dihydrofolate reductase",
            "B. DNA Gyrase (Topoisomerase II) and Topoisomerase IV",
            "C. DNA-dependent RNA polymerase",
            "D. Peptidyl transferase"
        ],
        "answer": "B. DNA Gyrase (Topoisomerase II) and Topoisomerase IV",
        "explanation": "Fluoroquinolones target bacterial DNA Gyrase (preventing relaxation of supercoiled DNA during replication in Gram-negative bacteria) and Topoisomerase IV (preventing decatenation/separation of daughter chromosomes in Gram-positive bacteria)."
    },
    {
        "id": 8,
        "category": "Antimetabolites",
        "question": "Co-trimoxazole (Trimethoprim-Sulfamethoxazole) produces a synergistic bactericidal effect through sequential inhibition of which pathway?",
        "options": [
            "A. Bacterial cell wall peptidoglycan synthesis",
            "B. Bacterial folic acid synthesis pathway",
            "C. Bacterial oxidative phosphorylation and ATP synthesis",
            "D. Ribosomal 50S and 30S subunit assembly"
        ],
        "answer": "B. Bacterial folic acid synthesis pathway",
        "explanation": "Sulfonamides structurally analog PABA to competitively inhibit Dihydropteroate Synthase. Trimethoprim selectively inhibits Dihydrofolate Reductase. Combined, they block sequential steps in bacterial purine and thymidine synthesis."
    },
    {
        "id": 9,
        "category": "RNA Synthesis Inhibitors",
        "question": "Rifampin exerts its antimicrobial activity by inhibiting which bacterial enzyme, and is notorious for causing orange-red discoloration of body fluids?",
        "options": [
            "A. DNA-dependent RNA polymerase",
            "B. Reverse transcriptase",
            "C. DNA ligase",
            "D. Thymidylate synthase"
        ],
        "answer": "A. DNA-dependent RNA polymerase",
        "explanation": "Rifampin binds the beta subunit of bacterial DNA-dependent RNA polymerase, suppressing mRNA transcription. It imparts a benign orange-red color to tears, urine, and sweat, and is a potent inducer of hepatic cytochrome P450 enzymes."
    },
    {
        "id": 10,
        "category": "Anaerobic & Membrane Agents",
        "question": "Metronidazole requires anaerobic intracellular reduction to form toxic nitro-free radicals that disrupt which cellular target?",
        "options": [
            "A. Peptidoglycan cell wall",
            "B. Bacterial DNA helical structure causing strand breakage",
            "C. 50S ribosomal subunit",
            "D. Folic acid enzymatic pathway"
        ],
        "answer": "B. Bacterial DNA helical structure causing strand breakage",
        "explanation": "Metronidazole is a prodrug taken up by anaerobic bacteria and protozoa. Pyruvate-ferredoxin oxidoreductase reduces its nitro group to reactive intermediate radicals that damage DNA, causing double-strand breaks."
    }
]

# ------------------------------------------------------------------------------
# 5. TIMED QUIZ RENDERER
# ------------------------------------------------------------------------------
student = st.session_state.verified_user

st.sidebar.markdown(f"👤 **Student Logged In:**\n- **Name:** {student['name']}\n- **ID:** `{student['id']}`")

if st.sidebar.button("Log Out / Reset"):
    st.session_state.verified_user = None
    st.session_state.current_index = 0
    st.session_state.user_score = 0
    st.session_state.quiz_finished = False
    st.rerun()

st.title("🧪 Antimicrobials & Drug Resistance: 60-Second Timed Quiz")

if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False

total_q = len(ANTIMICROBIAL_QS)

if st.session_state.quiz_finished or st.session_state.current_index >= total_q:
    st.balloons()
    st.header("🏆 Quiz Completed!")
    final_score = st.session_state.user_score
    pct = (final_score / total_q) * 100
    
    col1, col2 = st.columns(2)
    col1.metric("Final Score", f"{final_score} / {total_q}")
    col2.metric("Percentage", f"{pct:.1f}%")
    
    if pct >= 80:
        st.success("🌟 Outstanding Mastery of Antimicrobial Pharmacology & Resistance Mechanisms!")
    elif pct >= 60:
        st.info("👍 Good performance! Review the rationales to solidify weaker areas.")
    else:
        st.warning("📚 Keep practicing! Focus on cell wall vs protein synthesis inhibitors and resistance genes.")
        
    if st.button("Restart Quiz 🔄"):
        st.session_state.current_index = 0
        st.session_state.user_score = 0
        st.session_state.quiz_finished = False
        st.rerun()
    st.stop()

# Active Question
q = ANTIMICROBIAL_QS[st.session_state.current_index]
q_id = f"q_{q['id']}"

if f"start_time_{q_id}" not in st.session_state:
    st.session_state[f"start_time_{q_id}"] = time.time()

start_t = st.session_state[f"start_time_{q_id}"]
now_t = time.time()
elapsed = int(now_t - start_t)
remaining = max(0, 60 - elapsed)

# Top Bar Status
st.progress(st.session_state.current_index / total_q, text=f"Question {st.session_state.current_index + 1} of {total_q}")

col_q, col_timer = st.columns([3, 1])

with col_timer:
    if remaining > 20:
        st.markdown(f"### ⏳ Time: `<span style='color:green;'>{remaining}s</span>`", unsafe_allow_html=True)
    elif remaining > 10:
        st.markdown(f"### ⚠️ Time: `<span style='color:orange;'>{remaining}s</span>`", unsafe_allow_html=True)
    else:
        st.markdown(f"### 🚨 Time: `<span style='color:red;'>{remaining}s</span>`", unsafe_allow_html=True)

with col_q:
    st.caption(f"Category: {q['category']}")
    st.subheader(f"Q{q['id']}. {q['question']}")

is_answered = st.session_state.get(f"answered_{q_id}", False)
is_time_out = (remaining == 0 and not is_answered)

if is_time_out and not is_answered:
    st.session_state[f"answered_{q_id}"] = True
    st.session_state[f"selected_{q_id}"] = "TIME EXPIRED"
    log_response(
        module_name="Antimicrobials_Quiz",
        category=q["category"],
        question_text=q["question"],
        selected_option="TIME EXPIRED",
        correct_answer=q["answer"],
        is_correct=False,
        time_taken=60
    )
    st.rerun()

user_choice = st.radio(
    "Select your answer:",
    q["options"],
    key=f"radio_{q_id}",
    index=None,
    disabled=is_answered
)

col_sub, col_next = st.columns([1, 4])

if not is_answered:
    if col_sub.button("Submit Answer 🎯", key=f"btn_sub_{q_id}"):
        if user_choice:
            st.session_state[f"answered_{q_id}"] = True
            st.session_state[f"selected_{q_id}"] = user_choice
            is_corr = (user_choice == q["answer"])
            if is_corr:
                st.session_state.user_score += 1
            
            log_response(
                module_name="Antimicrobials_Quiz",
                category=q["category"],
                question_text=q["question"],
                selected_option=user_choice,
                correct_answer=q["answer"],
                is_correct=is_corr,
                time_taken=elapsed
            )
            st.rerun()
        else:
            st.warning("Please select an answer choice before submitting!")

if is_answered:
    selected = st.session_state.get(f"selected_{q_id}", "")
    if selected == q["answer"]:
        st.success(f"🎉 **Correct!**\n\n**Rationale:** {q['explanation']}")
    elif selected == "TIME EXPIRED":
        st.error(f"⏰ **Time Expired (60s Limit Reached)!**\n\n**Correct Answer:** `{q['answer']}`\n\n**Rationale:** {q['explanation']}")
    else:
        st.error(f"❌ **Incorrect.** You selected `{selected}`.\n\n**Correct Answer:** `{q['answer']}`\n\n**Rationale:** {q['explanation']}")
        
    if col_next.button("Next Question ➡️", key=f"btn_next_{q_id}"):
        st.session_state.current_index += 1
        st.rerun()

# Auto-refresh timer every 1 second while question is active and time remains
if not is_answered and remaining > 0:
    time.sleep(1)
    st.rerun()

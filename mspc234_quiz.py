import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# ------------------------------------------------------------------------------
# 1. STREAMLIT CONFIG & GOOGLE SHEETS INITIALIZATION
# ------------------------------------------------------------------------------
st.set_page_config(page_title="MSPC234 Interactive Quiz & Tracker", layout="wide")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# Initialize session state for user verification
if "verified_user" not in st.session_state:
    st.session_state.verified_user = None  # Dict: {"id": ..., "name": ...}


# ------------------------------------------------------------------------------
# 2. ROSTER VERIFICATION FUNCTION (HANDLES NUMBERS & LETTERS)
# ------------------------------------------------------------------------------
def verify_student(input_identifier):
    search_query = str(input_identifier).strip().lower()
    if search_query.endswith(".0"):
        search_query = search_query[:-2]

    if not search_query or conn is None:
        return None

    try:
        # Read the Student_Roster tab from Google Sheets
        roster_df = conn.read(worksheet="Student_Roster", ttl=60)
        roster_df.columns = roster_df.columns.str.strip().str.lower()
        
        # Locate ID and Name columns dynamically
        id_cols = [c for c in roster_df.columns if "id" in c]
        name_cols = [c for c in roster_df.columns if "name" in c]

        if id_cols and name_cols:
            id_col = id_cols[0]
            name_col = name_cols[0]
            
            # Clean ID series (removes trailing .0 from float conversions)
            id_series = (
                roster_df[id_col]
                .astype(str)
                .str.strip()
                .str.lower()
                .str.replace(r"\.0$", "", regex=True)
            )
            
            # Clean Name series
            name_series = (
                roster_df[name_col]
                .astype(str)
                .str.strip()
                .str.lower()
            )
            
            # Check for match in either ID or Name
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
        st.error(f"Roster check error: {e}")
        
    return None


# ------------------------------------------------------------------------------
# 3. SINGLE INPUT VERIFICATION GATE (LOCKS APP UNTIL VERIFIED)
# ------------------------------------------------------------------------------
if st.session_state.verified_user is None:
    st.title("🎓 Medical Science Professional Exam Portal")
    st.subheader("🔒 Student Identity Verification")
    st.caption("Please enter your official Student ID or Full Name once to unlock the quiz.")

    user_input = st.text_input("Student ID or Full Name:", placeholder="e.g. ST203001, 203001, or Jane Doe", key="login_field")
    
    if st.button("Verify & Enter Quiz 🚀"):
        if user_input.strip():
            with st.spinner("Verifying against official student roster..."):
                student_info = verify_student(user_input)
                
            if student_info:
                st.session_state.verified_user = student_info
                st.rerun()  # Instantly reloads page directly into the quiz
            else:
                st.error("❌ **Access Denied:** ID or Name not found in the official student roster. Please check for typos.")
        else:
            st.warning("⚠️ Please enter your Student ID or Name.")

    st.stop()  # Prevents unverified users from viewing questions below


# ------------------------------------------------------------------------------
# 4. RESPONSE LOGGING FUNCTION
# ------------------------------------------------------------------------------
def log_response(module_name, category, question_text, selected_option, correct_answer, is_correct):
    if conn is None or st.session_state.verified_user is None:
        return
        
    student = st.session_state.verified_user
    
    try:
        # Reads from the tab named after the module (e.g. "MSPC234")
        existing_df = conn.read(worksheet=module_name, ttl=0)
    except Exception:
        existing_df = pd.DataFrame(columns=[
            "Timestamp", "Student_ID", "Student_Name", "Module", 
            "Category", "Question", "Selected_Option", "Correct_Answer", "Is_Correct"
        ])

    new_entry = pd.DataFrame([{
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Student_ID": student["id"],
        "Student_Name": student["name"],
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


# ------------------------------------------------------------------------------
# 5. MAIN QUIZ INTERFACE & CATEGORY RENDERER
# ------------------------------------------------------------------------------
student = st.session_state.verified_user

# Sidebar Identity & Logout
st.sidebar.markdown(f"👤 **Logged-in Student:**\n- **Name:** {student['name']}\n- **ID:** `{student['id']}`")

if st.sidebar.button("Log Out / Switch Student"):
    st.session_state.verified_user = None
    st.rerun()

st.title("🎓 MSPC234: Head & Neck Anatomy, Neuroanatomy & Neuropharmacology")
st.caption("Interactive Comprehensive Question Bank grounded in Compiled Past Exam Questions.")

tab1, tab2, tab3 = st.tabs(["🫀 Part 1: Anatomy & Histology", "⚡ Part 2: Physiology & Pathophysiology", "🧪 Part 3: Biochemistry, Pharmacology & Clinical Scenarios"])

def render_question_list(questions, category_name, prefix):
    for idx, q in enumerate(questions):
        q_label = f"[{q.get('type', 'MCQ')}] {q['question']}" if 'type' in q else q['question']
        st.subheader(f"Q{idx+1}. {q_label}")
        key = f"{prefix}_{idx+1}"
        
        user_choice = st.radio("Select your answer:", q["options"], key=key, index=None)
        
        if user_choice is not None:
            selected_letter = user_choice[0]
            is_correct = (selected_letter == q["answer"])
            
            if is_correct:
                st.success(f"Correct! 🎉\n\n**Explanation:** {q['explanation']}")
            else:
                st.error(f"Incorrect. Correct Answer: **{q['answer']}**\n\n**Explanation:** {q['explanation']}")
            
            if f"logged_{key}" not in st.session_state:
                log_response(
                    module_name="MSPC234",
                    category=category_name,
                    question_text=q["question"],
                    selected_option=selected_letter,
                    correct_answer=q["answer"],
                    is_correct=is_correct
                )
                st.session_state[f"logged_{key}"] = True
        st.divider()

q_tab1 = [
    {
        "type": "Case Scenario",
        "question": "A 28-year-old patient undergoes surgical extraction of an impacted lower third molar. Postoperatively, she suffers complete loss of general tactile and taste sensation from the anterior two-thirds of the tongue on the affected side. Which nerve was injured?",
        "options": ["A. Lingual nerve", "B. Inferior alveolar nerve", "C. Glossopharyngeal nerve", "D. Chorda tympani alone"],
        "answer": "A",
        "explanation": "The lingual nerve runs immediately adjacent to the lingual periosteum of the mandibular third molar alveolus, carrying sensory fibers (V3) and taste fibers (Chorda tympani)."
    },
    {
        "type": "Direct Question",
        "question": "Which cranial foramina transmits the Mandibular division of the Trigeminal nerve (V3) through the greater wing of the sphenoid bone?",
        "options": ["A. Foramen ovale", "B. Foramen rotundum", "C. Foramen spinosum", "D. Jugular foramen"],
        "answer": "A",
        "explanation": "Foramen ovale transmits CN V3, accessory meningeal artery, lesser petrosal nerve, and emissary veins (MALE)."
    },
    {
        "type": "Exception Question",
        "question": "All of the following deep cerebellar nuclei are paired inside the white matter core EXCEPT:",
        "options": ["A. Dentate nucleus", "B. Emboliform nucleus", "C. Red nucleus", "D. Fastigial nucleus"],
        "answer": "C",
        "explanation": "The Red nucleus is located in the rostral midbrain tegmentum. Cerebellar nuclei laterally to medially are Dentate, Emboliform, Globose, and Fastigial (Don't Eat Greasy Foods)."
    },
    {
        "type": "True or False",
        "question": "Statement: Giant pyramidal cells of Betz are exclusively located within Layer V (Internal Pyramidal Layer) of the primary motor cortex (Brodmann Area 4).",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Betz cells are upper motor neurons situated in cortical Layer V of Brodmann Area 4, projecting long axons down the corticospinal tract."
    },
    {
        "type": "Case Scenario",
        "question": "A 65-year-old woman presents with sudden onset of contralateral face and upper limb weakness, sparing the lower extremity, with motor aphasia (Broca's). Which cerebral artery is occluded?",
        "options": ["A. Middle Cerebral Artery (MCA)", "B. Anterior Cerebral Artery (ACA)", "C. Posterior Cerebral Artery (PCA)", "D. Posterior Inferior Cerebellar Artery (PICA)"],
        "answer": "A",
        "explanation": "The MCA supplies the lateral precentral/postcentral gyri (face and arm areas) and Broca's area in the inferior frontal gyrus."
    },
    {
        "type": "Direct Question",
        "question": "Which developmental structure gives rise to melanocytes, schwann cells, meninges, and dentin-producing odontoblasts?",
        "options": ["A. Neural crest cells", "B. Neural tube neuroepithelium", "C. Paraxial mesoderm", "D. Surface ectoderm"],
        "answer": "A",
        "explanation": "Neural crest cells migrate extensively during neurulation, forming peripheral glia, adrenal medulla, melanocytes, meninges, and head mesenchymal structures."
    },
    {
        "type": "Exception Question",
        "question": "All of the following cranial nerve nuclei are located within the Pons EXCEPT:",
        "options": ["A. Abducens nucleus (CN VI)", "B. Facial motor nucleus (CN VII)", "C. Trigeminal motor nucleus (CN V)", "D. Hypoglossal nucleus (CN XII)"],
        "answer": "D",
        "explanation": "The Hypoglossal nucleus is located in the tegmentum of the Medulla Oblongata."
    },
    {
        "type": "True or False",
        "question": "Statement: The hippocampus forms a prominent elevation in the floor of the inferior (temporal) horn of the lateral ventricle.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "The hippocampus runs along the floor of the inferior horn, while the tail of the caudate nucleus runs along its roof."
    },
    {
        "type": "Case Scenario",
        "question": "An MRI scan of a newborn with an enlarged head reveals marked dilation of the lateral and third ventricles, with a normal fourth ventricle. Where is the anatomical obstruction located?",
        "options": ["A. Cerebral aqueduct of Sylvius", "B. Interventricular foramen of Monro", "C. Foramina of Luschka", "D. Foramen of Magendie"],
        "answer": "A",
        "explanation": "Aqueductal stenosis prevents CSF flow from the 3rd to 4th ventricle, causing non-communicating triventricular hydrocephalus."
    },
    {
        "type": "Direct Question",
        "question": "Which Parasympathetic ganglion receives preganglionic nerve fibers traveling via the greater petrosal nerve (branch of CN VII)?",
        "options": ["A. Pterygopalatine ganglion", "B. Otic ganglion", "C. Ciliary ganglion", "D. Submandibular ganglion"],
        "answer": "A",
        "explanation": "The greater petrosal nerve carries preganglionic parasympathetic fibers from the superior salivatory nucleus to the pterygopalatine ganglion for lacrimal secretion."
    },
    {
        "type": "Exception Question",
        "question": "All of the following dural venous sinuses drain directly or indirectly into the Internal Jugular Vein EXCEPT:",
        "options": ["A. Superior sagittal sinus", "B. Sigmoid sinus", "C. Cavernous sinus", "D. Inferior sagittal sinus (drains into Straight sinus)"],
        "answer": "D",
        "explanation": "Inferior sagittal sinus joins the Great Cerebral Vein (Galen) to form the Straight sinus, which then flows to the confluence."
    },
    {
        "type": "True or False",
        "question": "Statement: The Tentorium Cerebelli separates the occipital lobes of the cerebrum superiorly from the cerebellum inferiorly.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "The tentorium cerebelli is a horizontal dural fold roofed over the posterior cranial fossa."
    },
    {
        "type": "Case Scenario",
        "question": "A 45-year-old trauma patient exhibits bitemporal heteronymous hemianopia ('tunnel vision'). A skull base fracture has damaged which neural structure?",
        "options": ["A. Optic chiasm", "B. Left optic tract", "C. Right optic nerve", "D. Lateral geniculate nucleus"],
        "answer": "A",
        "explanation": "Lesions at the optic chiasm disrupt decussating nasal retinal fibers from both eyes, destroying peripheral temporal visual fields."
    },
    {
        "type": "Direct Question",
        "question": "Which cranial nerve provides general somatic sensation to the posterior one-third of the tongue?",
        "options": ["A. Glossopharyngeal nerve (CN IX)", "B. Lingual nerve (CN V3)", "C. Vagus nerve (CN X)", "D. Hypoglossal nerve (CN XII)"],
        "answer": "A",
        "explanation": "CN IX supplies BOTH general sensation and taste to the mucosal posterior third of the tongue."
    },
    {
        "type": "Exception Question",
        "question": "All of the following structures form part of the Basal Ganglia circuit EXCEPT:",
        "options": ["A. Caudate nucleus", "B. Putamen", "C. Globus pallidus", "D. Dentate nucleus"],
        "answer": "D",
        "explanation": "The Dentate nucleus is a deep Cerebellar nucleus involved in motor coordination, not part of the basal ganglia."
    },
    {
        "type": "True or False",
        "question": "Statement: The spinal cord in adult humans normally terminates at the L1-L2 vertebral level as the conus medullaris.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Due to differential growth, the adult spinal cord ends at L1-L2, whereas in newborns it terminates around L3."
    },
    {
        "type": "Case Scenario",
        "question": "A patient presents with a mid-shaft humeral fracture. Physical examination reveals wrist drop and sensory loss over the dorsum of the first web space. Which nerve was injured?",
        "options": ["A. Radial nerve", "B. Median nerve", "C. Ulnar nerve", "D. Axillary nerve"],
        "answer": "A",
        "explanation": "The radial nerve travels in the radial groove on the mid-shaft of the humerus, innervating forearm extensors."
    },
    {
        "type": "Direct Question",
        "question": "Which secondary brain vesicle develops into the thalamus, hypothalamus, and epithalamus?",
        "options": ["A. Diencephalon", "B. Telencephalon", "C. Mesencephalon", "D. Metencephalon"],
        "answer": "A",
        "explanation": "The Prosencephalon divides into Telencephalon (cerebral hemispheres) and Diencephalon (thalamic structures)."
    },
    {
        "type": "Exception Question",
        "question": "All of the following are clinical manifestations of an Upper Motor Neuron (UMN) lesion EXCEPT:",
        "options": ["A. Spastic paralysis", "B. Hyperreflexia", "C. Presence of Babinski sign", "D. Marked fasciculations and severe neurogenic muscle atrophy"],
        "answer": "D",
        "explanation": "Fasciculations and severe, rapid neurogenic atrophy are cardinal signs of Lower Motor Neuron (LMN) lesions."
    },
    {
        "type": "True or False",
        "question": "Statement: The anterolateral system (spinothalamic tract) decussates at the anterior white commissure within 1-2 spinal cord segments of entry.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Second-order spinothalamic neurons immediately cross in the anterior white commissure before ascending."
    },
    {
        "type": "Case Scenario",
        "question": "A 50-year-old man presents with Wallenberg syndrome (lateral medullary stroke). Which artery is occluded, causing loss of pain/temperature on the ipsilateral face and contralateral body?",
        "options": ["A. Posterior Inferior Cerebellar Artery (PICA)", "B. Anterior Spinal Artery", "C. Middle Cerebral Artery", "D. Basilar Artery"],
        "answer": "A",
        "explanation": "PICA supplies the anterolateral medulla, damaging the spinal trigeminal nucleus (ipsilateral face) and spinothalamic tract (contralateral body)."
    },
    {
        "type": "Direct Question",
        "question": "Which fiber bundle connects the vestibular nuclei with the oculomotor, trochlear, and abducens motor nuclei to coordinate conjugate eye movements?",
        "options": ["A. Medial Longitudinal Fasciculus (MLF)", "B. Medial lemniscus", "C. Lateral lemniscus", "D. Trapezoid body"],
        "answer": "A",
        "explanation": "The MLF coordinates vestibular stimuli with extraocular motor nuclei (CN III, IV, VI) for vestibulo-ocular reflexes."
    },
    {
        "type": "Exception Question",
        "question": "All of the following tracts descend through the pyramids of the medulla EXCEPT:",
        "options": ["A. Corticospinal tract", "B. Corticobulbar tract", "C. Spinothalamic tract", "D. None of the above"],
        "answer": "C",
        "explanation": "The spinothalamic tract is an ASCENDING sensory pathway located in the anterolateral tegmentum, not the motor pyramids."
    },
    {
        "type": "True or False",
        "question": "Statement: Spina bifida is the most common neural tube defect compatible with live birth.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Spina bifida results from failure of posterior neuropore closure around day 28; maternal folic acid reduces incidence."
    },
    {
        "type": "Direct Question",
        "question": "Which specific layer of the cerebral cortex contains the receptive granular cells receiving thalamocortical afferent projections?",
        "options": ["A. Layer IV (Internal Granular Layer)", "B. Layer I (Molecular)", "C. Layer III (External Pyramidal)", "D. Layer VI (Multiform)"],
        "answer": "A",
        "explanation": "Layer IV is the primary sensory input layer receiving dense projections from thalamic relay nuclei."
    }
]

# Tab 2 Questions (25 MCQs)
q_tab2 = [
    {
        "type": "Direct Question",
        "question": "Which extracellular ion concentration is the primary determinant of the neuronal resting membrane potential?",
        "options": ["A. Potassium (K+)", "B. Sodium (Na+)", "C. Calcium (Ca2+)", "D. Chloride (Cl-)"],
        "answer": "A",
        "explanation": "Neuronal resting membranes are highly permeable to K+ via leak channels; thus resting membrane potential (~ -70mV) is close to EK+."
    },
    {
        "type": "Case Scenario",
        "question": "A patient touches a hot stove and immediately withdraws his hand before feeling conscious pain. Which sensory fiber type conducts rapid sharp, localized nociceptive signals?",
        "options": ["A. A-delta fibers", "B. C fibers", "C. Ia fibers", "D. Ib fibers"],
        "answer": "A",
        "explanation": "A-delta fibers are small, myelinated axons conducting fast, sharp pain (~5-30 m/s), whereas C fibers are unmyelinated and conduct slow, dull aching pain."
    },
    {
        "type": "Exception Question",
        "question": "All of the following attributes are coded by sensory receptors EXCEPT:",
        "options": ["A. Sensory modality", "B. Stimulus location", "C. Stimulus intensity and duration", "D. Receptor quantum phase"],
        "answer": "D",
        "explanation": "The four fundamental coded sensory attributes are Modality, Location, Intensity, and Duration."
    },
    {
        "type": "Direct Question",
        "question": "Which divalent cation acts as an endogenous voltage-dependent blocker of the NMDA receptor channel at resting membrane potential?",
        "options": ["A. Magnesium (Mg2+)", "B. Calcium (Ca2+)", "C. Zinc (Zn2+)", "D. Sodium (Na+)"],
        "answer": "A",
        "explanation": "At resting membrane potentials (-70mV), extracellular Mg2+ plugs the pore of NMDA receptors; membrane depolarization is required to expel Mg2+."
    },
    {
        "type": "True or False",
        "question": "Statement: Activation of Golgi tendon organs by excessive muscle contraction triggers the Inverse Stretch Reflex, causing autogenic inhibition and muscle relaxation.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Golgi tendon organs (Ib afferents) sense tension and synapse on inhibitory interneurons in the spinal cord to protect against tendon tearing."
    },
    {
        "type": "Case Scenario",
        "question": "An ophthalmologist shines a light into a patient's right eye. The right pupil constricts (direct reflex) and the left pupil constricts simultaneously (consensual reflex). Which cranial nerve forms the afferent limb of this reflex?",
        "options": ["A. Optic nerve (CN II)", "B. Oculomotor nerve (CN III)", "C. Ophthalmic nerve (CN V1)", "D. Facial nerve (CN VII)"],
        "answer": "A",
        "explanation": "CN II carries light afferents to the pretectal nucleus; CN III carries parasympathetic efferents to the ciliary sphincter muscles."
    },
    {
        "type": "Direct Question",
        "question": "Which sensory receptor type detects sustained skin pressure and low-frequency stretch?",
        "options": ["A. Ruffini endings", "B. Pacinian corpuscles", "C. Meissner corpuscles", "D. Free nerve endings"],
        "answer": "A",
        "explanation": "Ruffini endings are slow-adapting mechanoreceptors detecting skin stretch; Pacinian corpuscles are fast-adapting high-frequency vibration sensors."
    },
    {
        "type": "Exception Question",
        "question": "All of the following sensory modalities relay through specific thalamic nuclei before reaching the primary sensory cortex EXCEPT:",
        "options": ["A. Olfaction (Smell)", "B. Vision", "C. Audition", "D. Gustation"],
        "answer": "A",
        "explanation": "Olfactory tracts project directly to the primary olfactory cortex (piriform cortex / uncus) without an obligate thalamic relay."
    },
    {
        "type": "True or False",
        "question": "Statement: Alpha motor neurons innervate extrafusal skeletal muscle fibers, while Gamma motor neurons innervate intrafusal muscle spindle fibers.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Alpha motor neurons drive force-producing extrafusal contraction; Gamma motor neurons adjust muscle spindle sensitivity during movement."
    },
    {
        "type": "Case Scenario",
        "question": "A Weber hearing test is performed on a patient complaining of right ear hearing loss. The sound lateralizes to the RIGHT (affected) ear. Rinne test shows bone conduction > air conduction in the right ear. What type of hearing loss is present?",
        "options": ["A. Right Conductive hearing loss", "B. Right Sensorineural hearing loss", "C. Left Sensorineural hearing loss", "D. Normal bilateral hearing"],
        "answer": "A",
        "explanation": "In conductive hearing loss, ambient room noise is masked in the affected ear, making bone-conducted sound louder (Weber lateralizes to affected ear; BC > AC)."
    },
    {
        "type": "Direct Question",
        "question": "Which ion influx triggers chemical neurotransmitter vesicle exocytosis at the presynaptic axon terminal upon action potential arrival?",
        "options": ["A. Calcium (Ca2+)", "B. Sodium (Na+)", "C. Potassium (K+)", "D. Chloride (Cl-)"],
        "answer": "A",
        "explanation": "Terminal depolarization opens voltage-gated Ca2+ channels; Ca2+ influx binds synaptotagmin to trigger SNARE-mediated vesicle fusion."
    },
    {
        "type": "Exception Question",
        "question": "All of the following proteins are essential components of the neuronal SNARE complex EXCEPT:",
        "options": ["A. Synaptobrevin (VAMP)", "B. Syntaxin-1", "C. SNAP-25", "D. Clathrin"],
        "answer": "D",
        "explanation": "SNAREs consist of Synaptobrevin (v-SNARE), Syntaxin, and SNAP-25 (t-SNAREs). Clathrin is involved in endocytic vesicle coat formation."
    },
    {
        "type": "True or False",
        "question": "Statement: Lateral inhibition in sensory processing suppresses lateral signal spread, enhancing spatial acuity and edge discrimination.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Inhibitory interneurons suppress adjacent sensory fields, sharpening spatial contrast at cortical levels."
    },
    {
        "type": "Case Scenario",
        "question": "An ENT specialist assesses a patient with vestibular neuritis. Warm water caloric irrigation of the right external auditory canal produces nystagmus with the fast phase beating to which side?",
        "options": ["A. RIGHT side", "B. LEFT side", "C. Upward", "D. Downward"],
        "answer": "A",
        "explanation": "Mnemonic COWS: Cold Opposite, Warm Same. Warm water irrigation stimulates the ipsilateral horizontal canal, producing fast-phase nystagmus to the SAME side."
    },
    {
        "type": "Direct Question",
        "question": "Which cell membrane ion channel family is activated by capsaicin and noxious thermal heat (>43°C)?",
        "options": ["A. TRPV1 channels", "B. TRPA1 channels", "C. TRPM8 channels", "D. ASIC channels"],
        "answer": "A",
        "explanation": "TRPV1 (Transient Receptor Potential Vanilloid 1) is a non-selective cation channel activated by heat, H+, and capsaicin."
    },
    {
        "type": "Exception Question",
        "question": "All of the following features characterize graded synaptic potentials EXCEPT:",
        "options": ["A. Summation (temporal and spatial)", "B. Proportional amplitude to stimulus strength", "C. Electrotonic decay over distance", "D. Constant 'All-or-None' amplitude"],
        "answer": "D",
        "explanation": "Action potentials are 'All-or-None'. Graded potentials (EPSPs/IPSPs) are variable in amplitude and decay with distance."
    },
    {
        "type": "True or False",
        "question": "Statement: High-frequency stimulation of excitatory synapses induces Long-Term Potentiation (LTP) through NMDA receptor activation and AMPA receptor insertion.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Ca2+ influx through NMDA channels triggers CaMKII cascades, recruiting additional AMPA receptors into the postsynaptic membrane."
    },
    {
        "type": "Case Scenario",
        "question": "A patient presents with extreme muscle rigidity, fever, and hyperthermia following halogenated anesthetic administration. Dantrolene is administered immediately. What is the molecular target of Dantrolene?",
        "options": ["A. Ryanodine Receptors (RyR1)", "B. Dihydropyridine Receptors (DHPR)", "C. Nicotinic Acetylcholine Receptors", "D. Sarcoplasmic Ca2+-ATPase (SERCA)"],
        "answer": "A",
        "explanation": "Dantrolene blocks RyR1 calcium-release channels in the sarcoplasmic reticulum, terminating uncontrolled cytosolic Ca2+ release in malignant hyperthermia."
    },
    {
        "type": "Direct Question",
        "question": "Which cranial nerve provides the afferent sensory limb for the Corneal Reflex when the cornea is touched with a cotton wisp?",
        "options": ["A. Ophthalmic nerve (CN V1)", "B. Optic nerve (CN II)", "C. Facial nerve (CN VII)", "D. Maxillary nerve (CN V2)"],
        "answer": "A",
        "explanation": "CN V1 carries corneal tactile afferents to the spinal trigeminal nucleus; CN VII interneurons activate orbicularis oculi efferents."
    },
    {
        "type": "Exception Question",
        "question": "All of the following parameters are measurable during electromyographic (EMG) evaluation of motor units EXCEPT:",
        "options": ["A. Motor unit action potential duration", "B. Peak-to-peak amplitude", "C. Polyphasic waveform count", "D. Direct myelin sheath thickness in millimeters"],
        "answer": "D",
        "explanation": "EMG measures electrical field potentials of motor units, not microscopic anatomical dimensions like myelin thickness."
    },
    {
        "type": "True or False",
        "question": "Statement: In the visual pathway, rod photoreceptors undergo hyperpolarization (not depolarization) in response to light absorption.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Light activates rhodopsin/transducin/PDE, breaking down cGMP and closing cGMP-gated Na+ channels, hyperpolarizing the rod cell."
    },
    {
        "type": "Direct Question",
        "question": "What is the function of the Sodium-Hydrogen Exchanger (NHE1) in central neurons?",
        "options": ["A. Extrude intracellular H+ to maintain cytosolic pH homeostasis", "B. Generate action potential depolarizations", "C. Reuptake glutamate from synaptic clefts", "D. Transport glucose across the blood-brain barrier"],
        "answer": "A",
        "explanation": "NHE1 exchanges intracellular H+ for extracellular Na+, protecting neuronal cytoplasm against metabolic acidosis."
    },
    {
        "type": "Case Scenario",
        "question": "A neurological examination demonstrates loss of two-point discrimination and joint position sense in the left lower limb. Pain and temperature sensations are completely intact. Where is the lesion?",
        "options": ["A. Left Fasciculus Gracilis in the posterior column", "B. Right Fasciculus Cuneatus", "C. Left Lateral Spinothalamic Tract", "D. Right Anterior Spinothalamic Tract"],
        "answer": "A",
        "explanation": "Fasciculus Gracilis carries conscious proprioception and fine touch from the ipsilateral lower body (below T6)."
    },
    {
        "type": "Exception Question",
        "question": "All of the following autonomic nervous system responses are mediated by Sympathetic activation EXCEPT:",
        "options": ["A. Pupillary dilation (Mydriasis - Alpha-1)", "B. Increased heart rate and contractility (Beta-1)", "C. Bronchodilating airway relaxation (Beta-2)", "D. Increased salivary secretion of abundant serous fluid"],
        "answer": "D",
        "explanation": "Abundant watery serous salivary secretion is driven by Parasympathetic stimulation; sympathetic stimulation yields viscous, protein-rich saliva."
    },
    {
        "type": "True or False",
        "question": "Statement: Pre-ganglionic autonomic sympathetic neurons originate exclusively within the Intermediolateral Gray Column (Lateral Horn) of spinal cord segments T1 through L2.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "The thoracolumbar outflow arises from lateral horn cell bodies between T1 and L2/L3."
    }
]

# Tab 3 Questions (25 MCQs)
q_tab3 = [
    {
        "type": "Case Scenario",
        "question": "A 45-year-old asthmatic patient is prescribed a long-acting inhaled bronchodilator for nocturnal symptoms. Which selective Beta-2 adrenergic receptor agonist is indicated?",
        "options": ["A. Formoterol", "B. Salbutamol", "C. Propranolol", "D. Atenolol"],
        "answer": "A",
        "explanation": "Formoterol and Salmeterol are long-acting selective Beta-2 agonists (LABAs) used for long-term asthma maintenance."
    },
    {
        "type": "Case Scenario",
        "question": "A patient presenting with acute muscle weakness undergoes a diagnostic test using Edrophonium (Tensilon). Immediate transient improvement in muscle strength confirms which diagnosis?",
        "options": ["A. Myasthenia Gravis", "B. Eaton-Lambert Syndrome", "C. Multiple Sclerosis", "D. Guillain-Barre Syndrome"],
        "answer": "A",
        "explanation": "Edrophonium is a ultra-short-acting acetylcholinesterase inhibitor that briefly increases ACh in the neuromuscular junction, reversing myasthenic crisis."
    },
    {
        "type": "Exception Question",
        "question": "Side effects of direct-acting or indirect-acting cholinomimetics (cholinergic excess) include all of the following EXCEPT:",
        "options": ["A. Miosis (pupillary constriction)", "B. Excessive lacrimation and salivation", "C. Bronchoconstriction and bradycardia", "D. Mydriasis and urinary retention"],
        "answer": "D",
        "explanation": "Mydriasis and urinary retention are ANTI-cholinergic (antimuscarinic) effects, as summarized by the DUMBBELSS toxidrome."
    },
    {
        "type": "Direct Question",
        "question": "Which central general anesthetic agent is a dissociative NMDA receptor antagonist that provides analgesia without cardiovascular depression?",
        "options": ["A. Ketamine", "B. Propofol", "C. Etomidate", "D. Halothane"],
        "answer": "A",
        "explanation": "Ketamine blocks NMDA receptors, producing dissociative anesthesia, catatonia, amnesia, and sympathetic stimulation."
    },
    {
        "type": "True or False",
        "question": "Statement: Etomidate is an intravenous general anesthetic that can cause transient adrenal suppression by inhibiting 11-beta-hydroxylase.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Etomidate inhibits mitochondrial 11-beta-hydroxylase, blocking cortisol synthesis; prolonged infusions can cause adrenal insufficiency."
    },
    {
        "type": "Case Scenario",
        "question": "A patient undergoing surgery receives Propofol for general anesthesia induction. In addition to rapid loss of consciousness, what beneficial postoperative side effect does Propofol possess?",
        "options": ["A. Potent antiemetic action (reduces PONV)", "B. Long-lasting analgesia", "C. Bronchodilation", "D. Hypertension"],
        "answer": "A",
        "explanation": "Propofol possesses inherent antiemetic properties, making it ideal for ambulatory surgery to prevent postoperative nausea and vomiting."
    },
    {
        "type": "Direct Question",
        "question": "By what mechanism does Cocaine produce intense euphoria and sympathetic activation in the central nervous system?",
        "options": ["A. Inhibits presynaptic dopamine and norepinephrine reuptake transporters (DAT/NET)", "B. Direct agonist at dopamine D2 receptors", "C. Stimulates monoamine oxidase (MAO)", "D. Enhances GABA-A receptor opening"],
        "answer": "A",
        "explanation": "Cocaine blocks DAT and NET, causing accumulation of dopamine and norepinephrine in the synaptic cleft."
    },
    {
        "type": "Exception Question",
        "question": "All of the following general anesthetics enhance GABA-A receptor-mediated chloride currents EXCEPT:",
        "options": ["A. Thiopental", "B. Propofol", "C. Midazolam", "D. Ketamine"],
        "answer": "D",
        "explanation": "Ketamine acts primarily as an NMDA receptor antagonist, unlike GABA-A potentiators such as barbiturates, propofol, and benzodiazepines."
    },
    {
        "type": "True or False",
        "question": "Statement: Local anesthetics (e.g., Lidocaine) are weak bases that become ionized in acidic infected tissue, reducing lipid membrane penetration and clinical efficacy.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Acidic extracellular pH shifts local anesthetics into their charged/ionized form, hindering diffusion across the uncharged nerve sheath."
    },
    {
        "type": "Case Scenario",
        "question": "A 35-year-old pregnant patient develops gestational hypertension. Which centrally acting alpha-2 adrenergic agonist is first-line for antihypertensive management in pregnancy?",
        "options": ["A. Alpha-methyldopa", "B. Clonidine", "C. Phenylephrine", "D. Prazosin"],
        "answer": "A",
        "explanation": "Alpha-methyldopa is converted to alpha-methylnorepinephrine in central neurons, stimulating presynaptic alpha-2 receptors to decrease sympathetic outflow safely during pregnancy."
    },
    {
        "type": "Direct Question",
        "question": "Which drug is administered alongside atropine as a specific cholinesterase reactivator in organophosphate poisoning?",
        "options": ["A. Pralidoxime (2-PAM)", "B. Physostigmine", "C. Neostigmine", "D. Pilocarpine"],
        "answer": "A",
        "explanation": "Pralidoxime cleaves the phosphate group from organophosphate-inhibited acetylcholinesterase before 'aging' occurs."
    },
    {
        "type": "Exception Question",
        "question": "Barbiturates (e.g., Phenobarbital, Thiopental) exhibit all of the following pharmacological properties EXCEPT:",
        "options": ["A. Prolong the opening duration of GABA-A chloride channels", "B. Cause respiratory depression at high doses", "C. Exacerbate Acute Intermittent Porphyria by inducing ALA synthase", "D. Act as direct antagonists at muscarinic M3 receptors"],
        "answer": "D",
        "explanation": "Barbiturates do not block muscarinic receptors; their toxicity stems from CNS/respiratory depression and hepatic CYP/ALA synthase induction."
    },
    {
        "type": "True or False",
        "question": "Statement: Co-administration of Epinephrine with local anesthetics delays systemic drug absorption through alpha-1 vasoconstriction, prolonging local anesthesia duration.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Epinephrine constricts local blood vessels, keeping the anesthetic localized and reducing systemic toxicity."
    },
    {
        "type": "Case Scenario",
        "question": "A 60-year-old Parkinson's disease patient experiences severe motor fluctuations and resting tremors. Which drug increases central dopamine synthesis by crossing the blood-brain barrier via L-amino acid transporters?",
        "options": ["A. Levodopa (L-DOPA)", "B. Dopamine", "C. Carbidopa", "D. Selegiline"],
        "answer": "A",
        "explanation": "Dopamine cannot cross the BBB. Levodopa (its precursor) crosses via LAT1 and is converted to dopamine by DOPA decarboxylase in the brain."
    },
    {
        "type": "Direct Question",
        "question": "Which non-depolarizing neuromuscular blocking agent undergoes spontaneous ester hydrolysis and Hofmann elimination independent of liver or renal function?",
        "options": ["A. Atracurium / Cisatracurium", "B. Vecuronium", "C. Pancuronium", "D. Succinylcholine"],
        "answer": "A",
        "explanation": "Cisatracurium breaks down spontaneously at physiological pH and temperature via Hofmann elimination, making it safe in organ failure."
    },
    {
        "type": "Exception Question",
        "question": "All of the following molecules cross the Blood-Brain Barrier (BBB) primarily via receptor-mediated transcytosis EXCEPT:",
        "options": ["A. Insulin", "B. Transferrin", "C. Leptin", "D. Small lipophilic molecules (e.g., Ethanol, Oxygen)"],
        "answer": "D",
        "explanation": "Small uncharged lipophilic gases and molecules cross the BBB via simple passive transcellular diffusion."
    },
    {
        "type": "True or False",
        "question": "Statement: Aripiprazole is a second-generation atypical antipsychotic that acts as a partial agonist at dopamine D2 receptors.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Aripiprazole stabilizes dopamine neurotransmission by acting as a partial D2 agonist (and 5-HT1A partial agonist / 5-HT2A antagonist)."
    },
    {
        "type": "Case Scenario",
        "question": "A patient presenting with acute postoperative urinary retention is given Bethanechol. What is the mechanism of action of Bethanechol?",
        "options": ["A. Direct Muscarinic (M3) receptor agonist", "B. Nicotinic receptor antagonist", "C. Alpha-1 adrenergic agonist", "D. Acetylcholinesterase inhibitor"],
        "answer": "A",
        "explanation": "Bethanechol is a synthetic choline ester selective for muscarinic receptors (M3), stimulating detrusor contraction and bladder emptying."
    },
    {
        "type": "Direct Question",
        "question": "Which intravenous general anesthetic enhances GABA-A currents and is notorious for causing post-anesthesia emergence delirium and visual hallucinations?",
        "options": ["A. Ketamine", "B. Propofol", "C. Midazolam", "D. Etomidate"],
        "answer": "A",
        "explanation": "Ketamine causes vivid dreams, out-of-body experiences, and emergence delirium upon awakening."
    },
    {
        "type": "Exception Question",
        "question": "All of the following drugs are useful in the management of Alzheimer's disease by inhibiting acetylcholinesterase EXCEPT:",
        "options": ["A. Donepezil", "B. Rivastigmine", "C. Galantamine", "D. Memantine"],
        "answer": "D",
        "explanation": "Memantine is an uncompetitive NMDA receptor antagonist, not a cholinesterase inhibitor."
    },
    {
        "type": "True or False",
        "question": "Statement: Glucocorticoids (e.g., Dexamethasone) preserve Blood-Brain Barrier structural integrity by upregulating endothelial tight junction proteins (Claudins/Occludins).",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Steroids decrease vasogenic brain edema around tumors/infections by tightening endothelial junctions."
    },
    {
        "type": "Case Scenario",
        "question": "An asthmatic patient takes high doses of non-selective Beta-agonists and develops palpitations and tachycardia. Which receptor mediates these cardiac side effects?",
        "options": ["A. Beta-1 adrenergic receptor", "B. Beta-2 adrenergic receptor", "C. Alpha-1 adrenergic receptor", "D. Muscarinic M2 receptor"],
        "answer": "A",
        "explanation": "Beta-1 receptors in the SA node and myocardium increase heart rate and contractility."
    },
    {
        "type": "Direct Question",
        "question": "Which class of antidepressant drugs inhibits Monoamine Oxidase-A (MAO-A), requiring strict dietary restriction of tyramine-rich foods (cheese, wine)?",
        "options": ["A. MAO inhibitors (e.g., Phenelzine, Tranylcypromine)", "B. SSRIs", "C. Tricyclic Antidepressants", "D. SNRIs"],
        "answer": "A",
        "explanation": "MAO-A breaks down intestinal tyramine; MAOIs allow tyramine entry into blood, triggering hypertensive crisis."
    },
    {
        "type": "Exception Question",
        "question": "All of the following statements regarding Benzodiazepines (e.g., Diazepam) are TRUE EXCEPT:",
        "options": ["A. They bind between alpha and gamma subunits of GABA-A receptors", "B. They increase the FREQUENCY of GABA-A channel opening", "C. Their overdose is rapidly reversed by Flumazenil", "D. They increase the DURATION of GABA-A channel opening"],
        "answer": "D",
        "explanation": "Benzodiazepines increase opening FREQUENCY; Barbiturates increase opening DURATION."
    },
    {
        "type": "True or False",
        "question": "Statement: Succinylcholine is a depolarizing neuromuscular blocker that acts as a persistent nicotinic agonist, causing initial muscle fasciculations followed by flaccid paralysis.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Succinylcholine depolarizes the motor endplate persistently, causing Phase I block (fasciculations followed by paralysis)."
    }
]



with tab1:
    st.header("🫀 Part 1: Anatomy & Histology")
    render_question_list(q_tab1, "Anatomy & Histology", "tab1")

with tab2:
    st.header("⚡ Part 2: Physiology & Pathophysiology")
    render_question_list(q_tab2, "Physiology", "tab2")

with tab3:
    st.header("🧪 Part 3: Biochemistry, Pharmacology & Clinical Scenarios")
    render_question_list(q_tab3, "Biochemistry & Clinical", "tab3")

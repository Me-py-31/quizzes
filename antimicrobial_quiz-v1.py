import streamlit as st
import pandas as pd
import datetime
import time
from streamlit_gsheets import GSheetsConnection

# ------------------------------------------------------------------------------
# 1. STREAMLIT CONFIG & GOOGLE SHEETS INITIALIZATION
# ------------------------------------------------------------------------------
st.set_page_config(page_title="🧪 Neoplasia & Tumors Quiz (1-Min Timer)", layout="wide")

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
    st.title("🧪 Neoplasia & Tumors Exam Portal")
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
# 4. QUESTION BANK (NEOPLASIA & TUMORS)
# ------------------------------------------------------------------------------
NEOPLASIA_QS = [
    {
        "id": 1,
        "category": "Disorders of Growth",
        "question": "Which disorder of development is defined as incomplete development or under-development of an organ resulting in a decreased cell count and reduced organ size?",
        "options": [
            "A. Aplasia",
            "B. Hypoplasia",
            "C. Atrophy",
            "D. Agenesis"
        ],
        "answer": "B. Hypoplasia",
        "explanation": "Hypoplasia is defined as the incomplete development or underdevelopment of an organ with a decreased number of cells, causing the organ to fail to reach normal size (e.g., renal hypoplasia)."
    },
    {
        "id": 2,
        "category": "Disorders of Growth",
        "question": "A localized, disorganized focal overgrowth of mature, specialized tissues indigenous to the particular organ site is termed a:",
        "options": [
            "A. Choristoma",
            "B. Hamartoma",
            "C. Teratoma",
            "D. Adenoma"
        ],
        "answer": "B. Hamartoma",
        "explanation": "A hamartoma is a benign, focal overgrowth of mature, specialized tissues indigenous (native) to the specific organ site (e.g., cartilage, blood vessels, and bronchial structures in a pulmonary hamartoma)."
    },
    {
        "id": 3,
        "category": "Disorders of Growth",
        "question": "An ectopic rest or heterotopic collection of histologically normal tissue found in an abnormal anatomical location (such as pancreatic tissue in the gastric mucosa) is known as a:",
        "options": [
            "A. Hamartoma",
            "B. Choristoma",
            "C. Teratoma",
            "D. Dysplasia"
        ],
        "answer": "B. Choristoma",
        "explanation": "A choristoma (or heterotopia) is a congenital anomaly consisting of a rest of normal cells or tissue located in an ectopic anatomical site (e.g., pancreatic rest in stomach or Meckel's diverticulum)."
    },
    {
        "id": 4,
        "category": "Disorders of Growth",
        "question": "Which term describes a disorderly, potentially reversible epithelial proliferation characterized by loss of cellular uniformity and loss of normal architectural orientation?",
        "options": [
            "A. Metaplasia",
            "B. Anaplasia",
            "C. Dysplasia",
            "D. Hypertrophy"
        ],
        "answer": "C. Dysplasia",
        "explanation": "Dysplasia refers to disorderly but potentially reversible cellular proliferation, usually in epithelia, characterized by loss of individual cell uniformity and architectural disorientation."
    },
    {
        "id": 5,
        "category": "Disorders of Growth",
        "question": "According to the classic definition by Rupert Willis, a neoplasm is an abnormal mass of tissue characterized by which key behavior?",
        "options": [
            "A. It regresses completely upon removal of the inciting inflammatory stimulus",
            "B. Its growth exceeds and is uncoordinated with normal tissues, persisting autonomously after cessation of the evoking stimulus",
            "C. It represents a non-clonal hyperplastic response to hormonal stimulation",
            "D. It is composed exclusively of primitive stem cells that cannot undergo mitosis"
        ],
        "answer": "B. Its growth exceeds and is uncoordinated with normal tissues, persisting autonomously after cessation of the evoking stimulus",
        "explanation": "Willis defined a neoplasm as an abnormal mass of tissue, the growth of which exceeds and is uncoordinated with that of normal tissues, and persists in the same excessive manner after cessation of the stimuli which evoked the change."
    },
    {
        "id": 6,
        "category": "Disorders of Growth",
        "question": "Which characteristic distinguishes a hypoplastic kidney from an atrophic, end-stage kidney?",
        "options": [
            "A. Presence of extensive cortical scarring",
            "B. Absence of parenchymal scars and a reduced number of renal pyramids (fewer than 6)",
            "C. Marked accumulation of lipofuscin pigment",
            "D. Hyperplasia of the contralateral adrenal gland"
        ],
        "answer": "B. Absence of parenchymal scars and a reduced number of renal pyramids (fewer than 6)",
        "explanation": "A hypoplastic kidney is differentiated from an atrophic kidney by the absence of inflammatory scars and a reduced count of lobes and pyramids (fewer than 6)."
    },
    {
        "id": 7,
        "category": "Disorders of Growth",
        "question": "Severe cervical dysplasia involving the full thickness of the epithelium without breaching the basement membrane is termed:",
        "options": [
            "A. Carcinoma in situ",
            "B. Invasive squamous cell carcinoma",
            "C. Squamous metaplasia",
            "D. Microinvasive carcinoma"
        ],
        "answer": "A. Carcinoma in situ",
        "explanation": "When dysplastic changes involve the entire thickness of the epithelium while remaining strictly confined above an intact basement membrane, it is termed carcinoma in situ (or intraepithelial carcinoma / CIN III)."
    },
    {
        "id": 8,
        "category": "Disorders of Growth",
        "question": "DiGeorge syndrome, characterized by thymic hypoplasia and congenital heart defects, results from a developmental failure of which pharyngeal pouches?",
        "options": [
            "A. First and second",
            "B. Third and fourth",
            "C. Fifth and sixth",
            "D. Second and third"
        ],
        "answer": "B. Third and fourth",
        "explanation": "Thymic hypoplasia in DiGeorge syndrome is a congenital disorder stemming from abnormal development of the 3rd and 4th pharyngeal pouches."
    },
    {
        "id": 9,
        "category": "Disorders of Growth",
        "question": "An adaptive replacement of one adult cell type by another adult cell type better suited to withstand chronic harsh environmental stress is defined as:",
        "options": [
            "A. Dysplasia",
            "B. Metaplasia",
            "C. Anaplasia",
            "D. Hyperplasia"
        ],
        "answer": "B. Metaplasia",
        "explanation": "Metaplasia is a reversible adaptive transformation in which one adult cell type is replaced by another adult cell type better able to endure the chronic irritation."
    },
    {
        "id": 10,
        "category": "Disorders of Growth",
        "question": "Unilateral renal agenesis leads to enlargement of the remaining solitary kidney through which mechanism?",
        "options": [
            "A. Pathologic hyperplasia",
            "B. Compensatory hypertrophy and hyperplasia",
            "C. Dysplastic regeneration",
            "D. Neoplastic transformation"
        ],
        "answer": "B. Compensatory hypertrophy and hyperplasia",
        "explanation": "When one kidney is absent, the remaining solitary kidney undergoes compensatory hypertrophy and cell proliferation to meet physiological functional demands."
    },
    {
        "id": 11,
        "category": "Disorders of Growth",
        "question": "Which of the following is TRUE regarding mild-to-moderate dysplastic lesions?",
        "options": [
            "A. They are irreversible genetic commitments to invasive cancer",
            "B. They always penetrate the basement membrane into the stroma",
            "C. They may completely revert to normal epithelium upon removal of the inciting cause",
            "D. They lack cellular pleomorphism and hyperchromasia"
        ],
        "answer": "C. They may completely revert to normal epithelium upon removal of the inciting cause",
        "explanation": "Mild to moderate dysplasia is a potentially reversible process; upon removal of the offending chronic irritant or toxic stimulus, the dysplastic epithelium may completely revert to normal."
    },
    {
        "id": 12,
        "category": "Disorders of Growth",
        "question": "A benign neoplasm composed of hair, teeth, skin, and sebaceous glands derived from more than one germ layer is classified as a:",
        "options": [
            "A. Choristoma",
            "B. Hamartoma",
            "C. Teratoma",
            "D. Leiomyoma"
        ],
        "answer": "C. Teratoma",
        "explanation": "A teratoma is a neoplasm composed of cell types derived from more than one germ cell layer (ectoderm, mesoderm, endoderm), commonly occurring in the ovaries (dermoid cyst) or testes."
    },
    {
        "id": 13,
        "category": "Disorders of Growth",
        "question": "Which suffix denotes a benign neoplasm of mesenchymal or epithelial origin, with notable non-neoplastic exceptions such as granuloma or tuberculoma?",
        "options": [
            "A. -itis",
            "B. -oma",
            "C. -sarcoma",
            "D. -carcinoma"
        ],
        "answer": "B. -oma",
        "explanation": "Benign tumors generally carry the suffix '-oma' attached to the cell of origin (e.g., fibroma, lipoma). Exceptions include non-neoplastic inflammatory masses like granuloma or tuberculoma."
    },
    {
        "id": 14,
        "category": "Disorders of Growth",
        "question": "A primary biological feature distinguishing neoplastic growth from non-neoplastic adaptive hyperplasia is:",
        "options": [
            "A. Monoclonality and autonomous replication independent of physiological signals",
            "B. Polyclonal composition responding to hormone withdrawal",
            "C. Absolute dependence on exogenous growth factor administration",
            "D. Complete absence of somatic genetic mutations"
        ],
        "answer": "A. Monoclonality and autonomous replication independent of physiological signals",
        "explanation": "Neoplasms are monoclonal (arising from a single genetically altered cell) and display autonomous growth that persists independently of physiological regulatory signals."
    },
    {
        "id": 15,
        "category": "Disorders of Growth",
        "question": "Which architectural feature is characteristic of epithelial dysplasia under light microscopy?",
        "options": [
            "A. Basal-like cells appearing in the upper/superficial layers with loss of normal polarity",
            "B. Dense fibrous pseudocapsule enclosing the epithelial sheet",
            "C. Diffuse invasion of lymphatic channels beneath the basement membrane",
            "D. Uniform cell size and low nuclear-to-cytoplasmic ratio"
        ],
        "answer": "A. Basal-like cells appearing in the upper/superficial layers with loss of normal polarity",
        "explanation": "Microscopically, dysplasia shows loss of cellular uniformity and architectural orientation (loss of polarity), with immature basal-like cells present in the upper layers of the epithelium."
    },
    {
        "id": 16,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "The most characteristic hallmark defining a malignant neoplasm compared to a benign tumor is the:",
        "options": [
            "A. High nuclear-to-cytoplasmic ratio",
            "B. Presence of metastases and local invasion",
            "C. Increased rate of mitotic figures",
            "D. Presence of cellular hyperchromasia"
        ],
        "answer": "B. Presence of metastases and local invasion",
        "explanation": "Metastasis and local tissue invasion are the definitive hallmarks of malignancy that unequivocally separate malignant neoplasms from benign tumors."
    },
    {
        "id": 17,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "Reversion of differentiated cells to a primitive, undifferentiated cellular state is termed:",
        "options": [
            "A. Metaplasia",
            "B. Anaplasia",
            "C. Dysplasia",
            "D. Desmoplasia"
        ],
        "answer": "B. Anaplasia",
        "explanation": "Anaplasia literally means 'to form backward' and represents a lack of cellular differentiation, serving as a hallmark of malignant transformation."
    },
    {
        "id": 18,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "Which morphological nuclear change is characteristic of anaplastic malignant tumor cells?",
        "options": [
            "A. Decreased nuclear-to-cytoplasmic (N/C) ratio approaching 1:6",
            "B. Hyperchromasia and nuclear-to-cytoplasmic ratio approaching 1:1",
            "C. Uniform, pale-staining vesicular chromatin",
            "D. Complete absence of mitotic spindles"
        ],
        "answer": "B. Hyperchromasia and nuclear-to-cytoplasmic ratio approaching 1:1",
        "explanation": "Anaplastic cells characteristically exhibit hyperchromatic (darkly staining) nuclei with an elevated N/C ratio approaching 1:1 (compared to 1:4 or 1:6 in normal cells)."
    },
    {
        "id": 19,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "Abundant collagenous stroma induced by parenchymal tumor cells, conferring a stony-hard consistency to a tumor mass, is called:",
        "options": [
            "A. Anaplasia",
            "B. Desmoplasia",
            "C. Dysplasia",
            "D. Metaplasia"
        ],
        "answer": "B. Desmoplasia",
        "explanation": "Desmoplasia refers to the proliferation of dense, collagenous fibrous stroma stimulated by parenchymal tumor cytokines, conferring a firm, 'scirrhous' consistency."
    },
    {
        "id": 20,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "Why are most benign mesenchymal tumors discrete, well-circumscribed, and readily movable on palpation?",
        "options": [
            "A. They metastasize early into adjacent lymphatic spaces",
            "B. They develop a fibrous capsule derived from stroma and compressed surrounding parenchyma",
            "C. They exhibit infiltrative, finger-like extensions into muscle planes",
            "D. They completely lack extracellular connective tissue"
        ],
        "answer": "B. They develop a fibrous capsule derived from stroma and compressed surrounding parenchyma",
        "explanation": "Benign tumors expand slowly and develop a rim of compressed fibrous tissue (capsule) that encapsulates the mass and provides a clean surgical cleavage plane."
    },
    {
        "id": 21,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "Tri-polar or quadripolar mitotic spindles observed during microscopic examination of tissue indicate:",
        "options": [
            "A. Physiological tissue repair",
            "B. Atypical mitotic figures characteristic of malignant neoplasms",
            "C. Normal hormonal hyperplasia",
            "D. Benign leiomyoma growth"
        ],
        "answer": "B. Atypical mitotic figures characteristic of malignant neoplasms",
        "explanation": "Atypical, bizarre mitotic figures (e.g., tri-polar, quadripolar, or multipolar spindles) reflect abnormal nuclear division and are strongly indicative of malignancy."
    },
    {
        "id": 22,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "Variation in size and shape among tumor cells and their nuclei is defined as:",
        "options": [
            "A. Hyperchromasia",
            "B. Pleomorphism",
            "C. Desmoplasia",
            "D. Polarity"
        ],
        "answer": "B. Pleomorphism",
        "explanation": "Pleomorphism describes marked variability in cell size and nuclear shape within a tumor mass."
    },
    {
        "id": 23,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "A malignant neoplasm arising from epithelial tissue is properly termed a:",
        "options": [
            "A. Sarcoma",
            "B. Carcinoma",
            "C. Papilloma",
            "D. Lymphoma"
        ],
        "answer": "B. Carcinoma",
        "explanation": "Malignant tumors derived from epithelial cell layers (ectoderm, endoderm, or mesoderm) are termed carcinomas."
    },
    {
        "id": 24,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "A malignant neoplasm arising from mesenchymal tissue (e.g., bone, fat, cartilage, muscle) is termed a:",
        "options": [
            "A. Carcinoma",
            "B. Adenoma",
            "C. Sarcoma",
            "D. Choristoma"
        ],
        "answer": "C. Sarcoma",
        "explanation": "Malignant neoplasms originating in fleshy mesenchymal tissues (connective tissue, bone, muscle, vessels) are named sarcomas (e.g., osteosarcoma, fibrosarcoma)."
    },
    {
        "id": 25,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "Which of the following neoplasms is malignant despite carrying the '-oma' suffix?",
        "options": [
            "A. Lipoma",
            "B. Melanoma",
            "C. Fibroma",
            "D. Leiomyoma"
        ],
        "answer": "B. Melanoma",
        "explanation": "Melanoma (and lymphoma, seminoma, hepatoma) is a highly malignant neoplasm despite the misleading '-oma' suffix."
    },
    {
        "id": 26,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "Which microscopic pattern is typically absent in carcinoma in situ?",
        "options": [
            "A. Hyperchromatic, pleomorphic nuclei",
            "B. High mitotic activity",
            "C. Penetration through the epithelial basement membrane into underlying stroma",
            "D. Loss of normal architectural maturation"
        ],
        "answer": "C. Penetration through the epithelial basement membrane into underlying stroma",
        "explanation": "Carcinoma in situ exhibits all cytological features of malignancy but lacks basement membrane invasion."
    },
    {
        "id": 27,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "Benign tumors can cause fatal clinical outcomes through which mechanism?",
        "options": [
            "A. Direct hematogenous metastasis to the liver",
            "B. Critical anatomical location causing compression of vital structures (e.g., intracranial ependymoma)",
            "C. Early diffuse lymphatic spread",
            "D. Widespread destruction of distant organs"
        ],
        "answer": "B. Critical anatomical location causing compression of vital structures (e.g., intracranial ependymoma)",
        "explanation": "Benign tumors do not metastasize, but can be lethal due to anatomical position (e.g., a meningioma compressing the brainstem or cardiac atrial myxoma blocking valvular flow)."
    },
    {
        "id": 28,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "A tumor displaying glandular differentiation or originating from glandular epithelium is classified as an:",
        "options": [
            "A. Adenoma (if benign) or Adenocarcinoma (if malignant)",
            "B. Papilloma",
            "C. Sarcoma",
            "D. Epithelioma"
        ],
        "answer": "A. Adenoma (if benign) or Adenocarcinoma (if malignant)",
        "explanation": "Glandular epithelial neoplasms are called adenomas when benign and adenocarcinomas when malignant."
    },
    {
        "id": 29,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "The orientation of anaplastic tumor cells growing in disorganized sheets with loss of normal structural relationship is described as loss of:",
        "options": [
            "A. Polarity",
            "B. Motility",
            "C. Mitosis",
            "D. Stroma"
        ],
        "answer": "A. Polarity",
        "explanation": "Anaplastic tumor cells lose normal cellular orientation and structural arrangement, a phenomenon called loss of polarity."
    },
    {
        "id": 30,
        "category": "Characteristics of Benign & Malignant Tumors",
        "question": "Ischemic central necrosis and ulceration are frequent gross features of malignant tumors because:",
        "options": [
            "A. Malignant cells cannot undergo anaerobic glycolysis",
            "B. Rapid tumor cell growth outpaces the vascular stroma supply",
            "C. Benign tumors possess higher metabolic demands than carcinomas",
            "D. Tumor capsules obstruct internal blood flow"
        ],
        "answer": "B. Rapid tumor cell growth outpaces the vascular stroma supply",
        "explanation": "Rapidly growing malignant tumors frequently outgrow their blood supply, resulting in central ischemic necrosis, hemorrhage, and surface ulceration."
    },
    {
        "id": 31,
        "category": "Metastasis, Staging & Survival",
        "question": "Which pathway of metastatic spread is most characteristic of carcinomas during initial dissemination?",
        "options": [
            "A. Hematogenous pathway",
            "B. Lymphatic pathway",
            "C. Transcoelomic seeding",
            "D. Direct intra-canalicular spread"
        ],
        "answer": "B. Lymphatic pathway",
        "explanation": "Carcinomas typically metastasize initially via the lymphatic system, whereas sarcomas characteristically spread via hematogenous routes."
    },
    {
        "id": 32,
        "category": "Metastasis, Staging & Survival",
        "question": "In a regional lymph node receiving lymphatic drainage from a primary carcinoma, where are the earliest metastatic tumor cell deposits typically found?",
        "options": [
            "A. Medullary cords",
            "B. Subcapsular sinus",
            "C. Germinal centers",
            "D. Efferent lymphatic vessel"
        ],
        "answer": "B. Subcapsular sinus",
        "explanation": "Lymphatic emboli enter the lymph node via afferent lymphatics and deposit first in the subcapsular (marginal) sinus of the node."
    },
    {
        "id": 33,
        "category": "Metastasis, Staging & Survival",
        "question": "A bilateral metastatic ovarian tumor originating from a primary mucin-secreting gastrointestinal adenocarcinoma (most commonly stomach) is known as a:",
        "options": [
            "A. Brenner tumor",
            "B. Krukenberg tumor",
            "C. Dysgerminoma",
            "D. Granulosa cell tumor"
        ],
        "answer": "B. Krukenberg tumor",
        "explanation": "Krukenberg tumors are bilateral metastatic signet-ring cell adenocarcinomas in the ovaries, usually originating from a gastric or colonic primary tumor via transcoelomic seeding or hematogenous spread."
    },
    {
        "id": 34,
        "category": "Metastasis, Staging & Survival",
        "question": "In the TNM staging system, what does the designation 'Tis' indicate?",
        "options": [
            "A. Small tumor less than 1 cm",
            "B. Carcinoma in situ (non-invasive, confined above basement membrane)",
            "C. Primary tumor cannot be assessed",
            "D. Tumor with early solitary lymph node involvement"
        ],
        "answer": "B. Carcinoma in situ (non-invasive, confined above basement membrane)",
        "explanation": "Tis stands for Carcinoma in situ, indicating non-invasive epithelial neoplasia confined strictly above the basement membrane."
    },
    {
        "id": 35,
        "category": "Metastasis, Staging & Survival",
        "question": "A pathologist reports a colonic tumor as T2N2M1. What does 'M1' signify?",
        "options": [
            "A. Microscopic local invasion",
            "B. Single regional lymph node involvement",
            "C. Presence of distant metastasis",
            "D. Margin of surgical excision is involved"
        ],
        "answer": "C. Presence of distant metastasis",
        "explanation": "In the UICC/AJCC TNM staging system, M0 indicates no distant metastasis, while M1 indicates the presence of distant hematogenous or visceral metastases."
    },
    {
        "id": 36,
        "category": "Metastasis, Staging & Survival",
        "question": "Comparing the clinical utility of tumor Grading versus tumor Staging, which statement is TRUE?",
        "options": [
            "A. Grading provides far superior prognostic value than Staging",
            "B. Staging has significantly greater clinical and prognostic value than Grading",
            "C. Grading measures anatomic extent of spread while Staging measures differentiation",
            "D. Staging is determined exclusively by microscopic mitotic counts"
        ],
        "answer": "B. Staging has significantly greater clinical and prognostic value than Grading",
        "explanation": "Staging (anatomic extent of spread) has proved to be of far greater clinical and prognostic value than histological grading (degree of differentiation)."
    },
    {
        "id": 37,
        "category": "Metastasis, Staging & Survival",
        "question": "Under the Dukes staging system for colorectal carcinoma, Dukes Stage C corresponds to:",
        "options": [
            "A. Invasion into but not through the bowel wall, no nodal involvement",
            "B. Invasion through the full thickness of the bowel wall, no nodal involvement",
            "C. Invasion through the bowel wall with regional lymph node involvement",
            "D. Distant hematogenous liver metastases"
        ],
        "answer": "C. Invasion through the bowel wall with regional lymph node involvement",
        "explanation": "Dukes A = limited to bowel wall; Dukes B = extension through wall, node negative; Dukes C = regional lymph node involvement; Dukes D = distant metastasis."
    },
    {
        "id": 38,
        "category": "Metastasis, Staging & Survival",
        "question": "Why are the liver and lungs the most frequent visceral sites of hematogenous metastatic deposition?",
        "options": [
            "A. They possess the lowest partial pressure of oxygen",
            "B. All portal and systemic venous drainage flows through their capillary beds",
            "C. Tumor cells specifically synthesize arterial receptors for hepatic parenchymal cells",
            "D. Lymphatic vessels drain directly into the bile ducts"
        ],
        "answer": "B. All portal and systemic venous drainage flows through their capillary beds",
        "explanation": "Venous blood draining primary organs flows directly into the portal circulation (to the liver) or systemic caval circulation (to the lungs), trapping tumor emboli in their capillary beds."
    },
    {
        "id": 39,
        "category": "Metastasis, Staging & Survival",
        "question": "What is the primary definition of the 'Sentinel Lymph Node' in surgical oncology?",
        "options": [
            "A. The largest lymph node detected on CT imaging",
            "B. The first regional lymph node that receives lymphatic drainage from a primary tumor site",
            "C. The supraclavicular lymph node draining the thoracic duct",
            "D. Any node containing necrotic tumor tissue"
        ],
        "answer": "B. The first regional lymph node that receives lymphatic drainage from a primary tumor site",
        "explanation": "The sentinel lymph node is the first node in a regional lymphatic basin that receives lymph flow from the primary tumor mass."
    },
    {
        "id": 40,
        "category": "Metastasis, Staging & Survival",
        "question": "Which endocrine gland is most frequently involved by hematogenous metastatic carcinoma deposits?",
        "options": [
            "A. Thyroid gland",
            "B. Adrenal gland",
            "C. Pituitary gland",
            "D. Parathyroid gland"
        ],
        "answer": "B. Adrenal gland",
        "explanation": "The adrenal gland is the most common endocrine site for hematogenous metastasis (frequently from lung, breast, and renal carcinomas)."
    },
    {
        "id": 41,
        "category": "Metastasis, Staging & Survival",
        "question": "Tumor grading evaluates which cellular parameters under light microscopy?",
        "options": [
            "A. Size of primary tumor and distant organ involvement",
            "B. Degree of cellular differentiation, nuclear pleomorphism, and mitotic activity",
            "C. Patient age and serum carcinoembryonic antigen levels",
            "D. Number of regional lymph nodes resected during surgery"
        ],
        "answer": "B. Degree of cellular differentiation, nuclear pleomorphism, and mitotic activity",
        "explanation": "Grading is based on histological differentiation of tumor cells and the frequency of mitoses/architectural atypia (Grades I to III or IV)."
    },
    {
        "id": 42,
        "category": "Metastasis, Staging & Survival",
        "question": "In the TNM system, 'NX' denotes that:",
        "options": [
            "A. Regional lymph nodes show no tumor involvement",
            "B. Regional lymph nodes cannot be clinically or pathologically assessed",
            "C. Distant metastases are present in non-regional nodes",
            "D. There are more than 10 positive lymph nodes"
        ],
        "answer": "B. Regional lymph nodes cannot be clinically or pathologically assessed",
        "explanation": "The suffix 'X' in TNM staging (e.g., TX, NX, MX) indicates that the parameter cannot be assessed."
    },
    {
        "id": 43,
        "category": "Metastasis, Staging & Survival",
        "question": "Transcoelomic metastasis (seeding of body cavities) occurs most commonly within which anatomical cavity?",
        "options": [
            "A. Peritoneal cavity",
            "B. Synovial joint space",
            "C. Subarachnoid space",
            "D. Pericardial cavity"
        ],
        "answer": "A. Peritoneal cavity",
        "explanation": "Seeding of body cavities occurs most frequently in the peritoneal cavity (e.g., ovarian, gastric, or appendiceal carcinomas spreading across peritoneal surfaces)."
    },
    {
        "id": 44,
        "category": "Metastasis, Staging & Survival",
        "question": "Virchow's node (Troisier sign) refers to a metastatic enlargement of which specific lymph node group?",
        "options": [
            "A. Right axillary lymph node",
            "B. Left supraclavicular lymph node",
            "C. Right inguinal lymph node",
            "D. Anterior cervical lymph node"
        ],
        "answer": "B. Left supraclavicular lymph node",
        "explanation": "Virchow's node is an enlarged left supraclavicular lymph node caused by metastatic spread of abdominal malignancies (e.g., gastric adenocarcinoma) via the thoracic duct."
    },
    {
        "id": 45,
        "category": "Metastasis, Staging & Survival",
        "question": "Which statistical parameter defines cancer 'survival rate' in clinical trials?",
        "options": [
            "A. The average age at which patients are diagnosed with cancer",
            "B. The percentage of patients with a specific cancer who remain alive after a specified time period (usually 5 years)",
            "C. The total time required for a primary tumor mass to double in volume",
            "D. The proportion of benign tumors that undergo malignant conversion"
        ],
        "answer": "B. The percentage of patients with a specific cancer who remain alive after a specified time period (usually 5 years)",
        "explanation": "Survival rate is defined as the percentage of patients alive after a designated follow-up milestone (typically 5-year overall survival) following diagnosis or treatment."
    },
    {
        "id": 46,
        "category": "Cancer Epidemiology",
        "question": "The steep rise in overall cancer incidence observed with advancing age (>55 years) is primarily explained by:",
        "options": [
            "A. Increased vascular diseases in elderly patients",
            "B. The multistep nature of carcinogenesis and accumulation of somatic mutations over time",
            "C. Rapid loss of basal epithelial basement membranes",
            "D. Decreased dietary consumption of procarcinogens"
        ],
        "answer": "B. The multistep nature of carcinogenesis and accumulation of somatic mutations over time",
        "explanation": "Cancer incidence increases exponentially with age due to the accumulation of multiple somatic mutations over decades and a decline in immune competence."
    },
    {
        "id": 47,
        "category": "Cancer Epidemiology",
        "question": "Geographic variation in cancer incidence (e.g., gastric cancer being 7 times more prevalent in Japan than in the USA) is primarily attributed to:",
        "options": [
            "A. Fixed racial genetic differences that persist across generations",
            "B. Environmental, dietary, and cultural exposure differences",
            "C. Differences in arterial anatomical branching",
            "D. Variations in basal metabolic oxygen consumption"
        ],
        "answer": "B. Environmental, dietary, and cultural exposure differences",
        "explanation": "Geographic variations in cancer incidence are largely driven by environmental, cultural, and dietary factors (proven by migration studies showing second-generation immigrants acquiring the cancer risks of their new home)."
    },
    {
        "id": 48,
        "category": "Cancer Epidemiology",
        "question": "Historical observations by Sir Percival Pott linked scrotum squamous cell carcinoma in chimney sweeps to occupational exposure to:",
        "options": [
            "A. Hardwood dust",
            "B. Polycyclic aromatic hydrocarbons in soot",
            "C. Silica particles",
            "D. Inorganic arsenic"
        ],
        "answer": "B. Polycyclic aromatic hydrocarbons in soot",
        "explanation": "Sir Percival Pott identified soot (containing polycyclic aromatic hydrocarbons) as the cause of scrotal squamous cell carcinoma in chimney sweeps."
    },
    {
        "id": 49,
        "category": "Cancer Epidemiology",
        "question": "Occupational exposure to vinyl chloride monomer in chemical plant workers is specifically associated with which rare malignancy?",
        "options": [
            "A. Bronchogenic carcinoma",
            "B. Angiosarcoma of the liver",
            "C. Renal cell carcinoma",
            "D. Mesothelioma of pleura"
        ],
        "answer": "B. Angiosarcoma of the liver",
        "explanation": "Vinyl chloride exposure in the plastics industry is strongly and specifically linked to hepatic angiosarcoma."
    },
    {
        "id": 50,
        "category": "Cancer Epidemiology",
        "question": "Occupational exposure to asbestos fibers significantly increases the risk of developing which combination of malignancies?",
        "options": [
            "A. Hepatic angiosarcoma and acute myelogenous leukemia",
            "B. Malignant mesothelioma and bronchogenic carcinoma",
            "C. Transitional cell bladder carcinoma and osteosarcoma",
            "D. Thyroid follicular carcinoma and pancreatic cancer"
        ],
        "answer": "B. Malignant mesothelioma and bronchogenic carcinoma",
        "explanation": "Asbestos exposure increases the risk of bronchogenic lung carcinoma (markedly multiplied by cigarette smoking) and pleural/peritoneal malignant mesothelioma."
    },
    {
        "id": 51,
        "category": "Cancer Epidemiology",
        "question": "Inherited cancer syndromes caused by germline mutations in tumor suppressor genes (e.g., familial Retinoblastoma) typically display which pattern of inheritance?",
        "options": [
            "A. Autosomal dominant",
            "B. Autosomal recessive",
            "C. X-linked recessive",
            "D. Mitochondrial inheritance"
        ],
        "answer": "A. Autosomal dominant",
        "explanation": "Inherited cancer susceptibility syndromes (such as familial retinoblastoma, Li-Fraumeni, or FAP) are inherited as autosomal dominant traits due to single germline mutant alleles."
    },
    {
        "id": 52,
        "category": "Cancer Epidemiology",
        "question": "Xeroderma pigmentosum is an autosomal recessive inherited disorder of DNA repair characterized by hypersensitivity to UV light due to defective:",
        "options": [
            "A. Mismatch repair (hMSH2)",
            "B. Nucleotide excision repair",
            "C. Non-homologous end joining",
            "D. Homologous recombination"
        ],
        "answer": "B. Nucleotide excision repair",
        "explanation": "Xeroderma pigmentosum results from inherited mutations in nucleotide excision repair enzymes required to repair UV-induced pyrimidine (thymine) dimers."
    },
    {
        "id": 53,
        "category": "Cancer Epidemiology",
        "question": "Which precursor condition predisposes to oral and genital squamous cell carcinoma?",
        "options": [
            "A. Solar keratosis",
            "B. Leukoplakia",
            "C. Chronic ulcerative colitis",
            "D. Barrett esophagus"
        ],
        "answer": "B. Leukoplakia",
        "explanation": "Leukoplakia (a white mucosal patch) is a well-recognized premalignant lesion that can progress to invasive squamous cell carcinoma in the oral cavity, vulva, or penis."
    },
    {
        "id": 54,
        "category": "Cancer Epidemiology",
        "question": "Long-standing chronic ulcerative colitis carries a markedly increased risk for the development of:",
        "options": [
            "A. Colonic adenocarcinoma",
            "B. Gastrointestinal stromal tumor (GIST)",
            "C. Leiomyosarcoma",
            "D. Squamous cell carcinoma of rectum"
        ],
        "answer": "A. Colonic adenocarcinoma",
        "explanation": "Chronic inflammatory bowel disease, particularly long-standing ulcerative colitis, is a well-established pre-neoplastic condition predisposing to colorectal adenocarcinoma."
    },
    {
        "id": 55,
        "category": "Cancer Epidemiology",
        "question": "Germline mutations in BRCA1 and BRCA2 genes significantly increase a woman's lifetime risk for developing:",
        "options": [
            "A. Breast and ovarian carcinomas",
            "B. Cervical and endometrial carcinomas",
            "C. Renal cell carcinoma and pheochromocytoma",
            "D. Thyroid carcinoma and gastric adenocarcinoma"
        ],
        "answer": "A. Breast and ovarian carcinomas",
        "explanation": "BRCA1 and BRCA2 mutations impair homologous recombination DNA repair, predisposing strongly to familial breast and ovarian cancers."
    },
    {
        "id": 56,
        "category": "Cancer Epidemiology",
        "question": "Which childhood tumor group accounts for a prominent fraction of cancers in the 0\u201315 year age bracket?",
        "options": [
            "A. Carcinomas of prostate and colon",
            "B. Embryonic blastomas (e.g., retinoblastoma, neuroblastoma, Wilms tumor) and leukemias/lymphomas",
            "C. Squamous cell carcinoma of skin",
            "D. Adenocarcinoma of stomach"
        ],
        "answer": "B. Embryonic blastomas (e.g., retinoblastoma, neuroblastoma, Wilms tumor) and leukemias/lymphomas",
        "explanation": "In infants and children (0\u201315 years), the predominant malignancies are leukemias/lymphomas, CNS tumors, and embryonic blastomas (retinoblastoma, neuroblastoma, nephroblastoma)."
    },
    {
        "id": 57,
        "category": "Cancer Epidemiology",
        "question": "Occupational exposure to aniline dyes and beta-naphthylamine in the rubber and chemical industry predisposes to:",
        "options": [
            "A. Angiosarcoma of liver",
            "B. Transitional cell carcinoma of the urinary bladder",
            "C. Adenocarcinoma of stomach",
            "D. Mesothelioma"
        ],
        "answer": "B. Transitional cell carcinoma of the urinary bladder",
        "explanation": "Azo dyes and beta-naphthylamine are metabolized to active carcinogens excreted in urine, strongly predisposing dye industry workers to urinary bladder carcinoma."
    },
    {
        "id": 58,
        "category": "Cancer Epidemiology",
        "question": "Actinic (solar) keratosis of sun-exposed skin is a recognized precursor lesion for:",
        "options": [
            "A. Basal cell carcinoma",
            "B. Squamous cell carcinoma of the skin",
            "C. Cutaneous angiosarcoma",
            "D. Dermatofibrosarcoma protuberans"
        ],
        "answer": "B. Squamous cell carcinoma of the skin",
        "explanation": "Actinic (solar) keratosis is a dysplastic, sun-induced cutaneous lesion that serves as a direct precursor to invasive squamous cell carcinoma."
    },
    {
        "id": 59,
        "category": "Cancer Epidemiology",
        "question": "Hereditary nonpolyposis colorectal cancer (HNPCC / Lynch syndrome) is caused by germline mutations in genes regulating:",
        "options": [
            "A. DNA mismatch repair (e.g., MSH2, MLH1)",
            "B. Nucleotide excision repair",
            "C. Telomerase activation",
            "D. Apoptosis (BCL2)"
        ],
        "answer": "A. DNA mismatch repair (e.g., MSH2, MLH1)",
        "explanation": "Lynch syndrome is an autosomal dominant cancer syndrome caused by germline mutations in DNA mismatch repair genes (MSH2, MLH1, PMS2, MSH6), leading to microsatellite instability."
    },
    {
        "id": 60,
        "category": "Cancer Epidemiology",
        "question": "Familial Adenomatous Polyposis (FAP) is an autosomal dominant syndrome characterized by hundreds of colonic adenomas due to germline mutations in the:",
        "options": [
            "A. APC gene on chromosome 5q21",
            "B. TP53 gene on chromosome 17p",
            "C. RB gene on chromosome 13q",
            "D. WT1 gene on chromosome 11p"
        ],
        "answer": "A. APC gene on chromosome 5q21",
        "explanation": "FAP is caused by germline loss-of-function mutations in the APC (Adenomatous Polyposis Coli) gene on chromosome 5q21."
    },
    {
        "id": 61,
        "category": "Molecular Basis of Cancer",
        "question": "The single most common oncogene mutation in human cancers involves point mutations in the:",
        "options": [
            "A. RAS gene family",
            "B. MYC gene",
            "C. ERBB2 gene",
            "D. ABL gene"
        ],
        "answer": "A. RAS gene family",
        "explanation": "Point mutations in the RAS gene family (KRAS, HRAS, NRAS) represent the single most frequent oncogenic abnormality in human tumors (~30% of all cancers)."
    },
    {
        "id": 62,
        "category": "Molecular Basis of Cancer",
        "question": "Activated RAS protein is normally converted back to its inactive GDP-bound state by which regulatory protein?",
        "options": [
            "A. Cyclin-dependent kinase 4 (CDK4)",
            "B. GTPase-Activating Protein (GAP)",
            "C. p53 transcription factor",
            "D. BCL-2 protein"
        ],
        "answer": "B. GTPase-Activating Protein (GAP)",
        "explanation": "GAPs (GTPase-Activating Proteins) accelerate GTP hydrolysis by RAS x 1000, acting as a brake. Mutated RAS resists GAP-mediated GTP hydrolysis and remains constitutively active."
    },
    {
        "id": 63,
        "category": "Molecular Basis of Cancer",
        "question": "The reciprocal translocation t(8;14)(q24;q32) characteristic of Burkitt lymphoma translocates which proto-oncogene to the immunoglobulin heavy chain locus?",
        "options": [
            "A. c-ABL",
            "B. c-MYC",
            "C. BCL-2",
            "D. CCND1 (Cyclin D1)"
        ],
        "answer": "B. c-MYC",
        "explanation": "t(8;14) translocates the c-MYC gene on chromosome 8 to the IgH locus on chromosome 14, driving constitutive MYC transcription."
    },
    {
        "id": 64,
        "category": "Molecular Basis of Cancer",
        "question": "The Philadelphia chromosome t(9;22)(q34;q11) characteristic of Chronic Myelogenous Leukemia (CML) creates a hybrid fusion gene encoding a constitutive:",
        "options": [
            "A. Receptor tyrosine kinase",
            "B. BCR-ABL non-receptor tyrosine kinase",
            "C. Serine-threonine phosphatase",
            "D. Nuclear transcription factor"
        ],
        "answer": "B. BCR-ABL non-receptor tyrosine kinase",
        "explanation": "t(9;22) fuses the ABL gene on chromosome 9 with the BCR gene on chromosome 22, producing a chimeric BCR-ABL protein with potent, unregulated tyrosine kinase activity."
    },
    {
        "id": 65,
        "category": "Molecular Basis of Cancer",
        "question": "Amplification of the HER2/neu (c-erbB2) gene is a critical predictive biomarker in a subset of which human carcinomas?",
        "options": [
            "A. Pancreatic adenocarcinoma",
            "B. Breast carcinoma",
            "C. Renal cell carcinoma",
            "D. Prostate adenocarcinoma"
        ],
        "answer": "B. Breast carcinoma",
        "explanation": "HER2/neu (ERBB2) gene amplification occurs in ~15-20% of breast cancers and predicts response to anti-HER2 targeted therapy (trastuzumab)."
    },
    {
        "id": 66,
        "category": "Molecular Basis of Cancer",
        "question": "The RB tumor suppressor gene located on chromosome 13q14 regulates cell cycle progression by inhibiting which transcription factor at the G1/S checkpoint?",
        "options": [
            "A. E2F",
            "B. AP-1",
            "C. NF-kB",
            "D. STAT3"
        ],
        "answer": "A. E2F",
        "explanation": "Hypophosphorylated RB binds and sequester E2F transcription factors, preventing transcription of genes needed for the G1 to S phase transition."
    },
    {
        "id": 67,
        "category": "Molecular Basis of Cancer",
        "question": "According to Knudson's 'two-hit' hypothesis for tumor suppressor genes, sporadic non-hereditary retinoblastoma requires:",
        "options": [
            "A. One inherited mutant allele and one post-natal somatic mutation",
            "B. Two sequential somatic mutational events in the same retinoblast cell",
            "C. Gene amplification of both RB alleles",
            "D. Viral integration into chromosome 13"
        ],
        "answer": "B. Two sequential somatic mutational events in the same retinoblast cell",
        "explanation": "In sporadic retinoblastoma, both RB alleles are inactivated through two separate somatic mutations in a single cell."
    },
    {
        "id": 68,
        "category": "Molecular Basis of Cancer",
        "question": "The p53 protein ('guardian of the genome') responds to DNA double-strand breaks by inducing cell cycle arrest through transcriptional upregulation of:",
        "options": [
            "A. Cyclin D1",
            "B. p21 (CDKN1A / WAF1)",
            "C. BCL-2",
            "D. MDM2"
        ],
        "answer": "B. p21 (CDKN1A / WAF1)",
        "explanation": "p53 transactivates p21, a cyclin-dependent kinase inhibitor (CDKI) that blocks cyclin-CDK complexes, arresting the cell cycle in late G1 to allow DNA repair."
    },
    {
        "id": 69,
        "category": "Molecular Basis of Cancer",
        "question": "If DNA damage is irreparable, p53 triggers intrinsic apoptotic cell death by upregulating which pro-apoptotic protein?",
        "options": [
            "A. BCL-2",
            "B. BAX",
            "C. BCL-xL",
            "D. Survivin"
        ],
        "answer": "B. BAX",
        "explanation": "When DNA repair fails, p53 transactivates BAX (and BAK), which permeabilize mitochondrial outer membranes to release cytochrome c and trigger apoptosis."
    },
    {
        "id": 70,
        "category": "Molecular Basis of Cancer",
        "question": "Overexpression of the BCL-2 anti-apoptotic protein in follicular lymphoma results from which chromosomal translocation?",
        "options": [
            "A. t(8;14)",
            "B. t(14;18)(q32;q21)",
            "C. t(9;22)",
            "D. t(11;14)"
        ],
        "answer": "B. t(14;18)(q32;q21)",
        "explanation": "t(14;18) translocates the BCL2 gene on chromosome 18 to the IgH locus on chromosome 14, overexpressing BCL-2 and protecting B-cells from apoptosis."
    },
    {
        "id": 71,
        "category": "Molecular Basis of Cancer",
        "question": "Telomerase reactivation in human tumor cells confers which hallmark of cancer?",
        "options": [
            "A. Induction of tumor desmoplasia",
            "B. Limitless replicative potential (cellular immortality)",
            "C. Enhanced basement membrane degradation",
            "D. Evasion of immune surveillance"
        ],
        "answer": "B. Limitless replicative potential (cellular immortality)",
        "explanation": "Telomerase maintains telomere length during cell division, preventing senescence and end-replication crisis to confer limitless replicative potential."
    },
    {
        "id": 72,
        "category": "Molecular Basis of Cancer",
        "question": "A solid tumor mass generally cannot expand beyond 1 to 2 mm in diameter without inducing:",
        "options": [
            "A. Capsular calcification",
            "B. Angiogenesis",
            "C. Eosinophilic infiltrate",
            "D. Squamous metaplasia"
        ],
        "answer": "B. Angiogenesis",
        "explanation": "Diffusion of oxygen and nutrients is limited to 1-2 mm; beyond this size, tumor growth requires neovascularization (angiogenesis)."
    },
    {
        "id": 73,
        "category": "Molecular Basis of Cancer",
        "question": "Merlin, a cytoskeletal scaffolding protein involved in contact inhibition, is encoded by which tumor suppressor gene?",
        "options": [
            "A. NF1",
            "B. NF2",
            "C. WT1",
            "D. VHL"
        ],
        "answer": "B. NF2",
        "explanation": "The NF2 tumor suppressor gene encodes Merlin (schwannomin); loss of NF2 predisposes to bilateral acoustic schwannomas."
    },
    {
        "id": 74,
        "category": "Molecular Basis of Cancer",
        "question": "The WT1 (Wilms Tumor-1) gene, essential for renal and gonadal differentiation, is located on which chromosome?",
        "options": [
            "A. Chromosome 11p13",
            "B. Chromosome 13q14",
            "C. Chromosome 17p13",
            "D. Chromosome 3p25"
        ],
        "answer": "A. Chromosome 11p13",
        "explanation": "The WT1 gene is located on chromosome 11p13; loss-of-function mutations cause Wilms tumor (nephroblastoma)."
    },
    {
        "id": 75,
        "category": "Molecular Basis of Cancer",
        "question": "Translocation t(11;14)(q13;q32) in mantle cell lymphoma upregulates which cell cycle regulatory protein?",
        "options": [
            "A. Cyclin D1 (CCND1)",
            "B. Cyclin E",
            "C. CDK2",
            "D. p16 INK4a"
        ],
        "answer": "A. Cyclin D1 (CCND1)",
        "explanation": "t(11;14) translocates the Cyclin D1 gene to the IgH locus, overexpressing Cyclin D1 and driving G1/S cell cycle progression in mantle cell lymphoma."
    },
    {
        "id": 76,
        "category": "Carcinogenesis",
        "question": "Chemical carcinogenesis is a multistep process divided into two mandatory phases known as:",
        "options": [
            "A. Progression and Regression",
            "B. Initiation and Promotion",
            "C. Mutation and Apoptosis",
            "D. Transformation and Differentiation"
        ],
        "answer": "B. Initiation and Promotion",
        "explanation": "Chemical carcinogenesis requires Initiation (permanent, irreversible DNA mutation caused by an initiator) followed by Promotion (stimulated cell proliferation of initiated cells)."
    },
    {
        "id": 77,
        "category": "Carcinogenesis",
        "question": "Which statement accurately describes chemical 'Initiators'?",
        "options": [
            "A. They are non-mutagenic agents that stimulate cell division",
            "B. They cause rapid, irreversible DNA damage and are mutagenic",
            "C. They must be applied repeatedly after promoters",
            "D. Their effect is completely reversible upon drug withdrawal"
        ],
        "answer": "B. They cause rapid, irreversible DNA damage and are mutagenic",
        "explanation": "Initiators are electrophilic mutagens that cause permanent, irreversible DNA damage in a single exposure."
    },
    {
        "id": 78,
        "category": "Carcinogenesis",
        "question": "Dietary exposure to Aflatoxin B1 produced by Aspergillus flavus in contaminated grains induces hepatocellular carcinoma by causing a specific point mutation in:",
        "options": [
            "A. Codon 249 of the p53 gene",
            "B. Codon 12 of the KRAS gene",
            "C. Exon 14 of the MET gene",
            "D. Codon 600 of the BRAF gene"
        ],
        "answer": "A. Codon 249 of the p53 gene",
        "explanation": "Aflatoxin B1 causes a characteristic G-to-T transversion at codon 249 of the TP53 gene, synergizing with HBV to cause hepatocellular carcinoma."
    },
    {
        "id": 79,
        "category": "Carcinogenesis",
        "question": "Procarcinogens (indirect-acting chemical carcinogens) require metabolic activation into ultimate carcinogens primarily by which host enzyme system?",
        "options": [
            "A. Cytochrome P-450 monooxygenases",
            "B. Glucuronosyltransferases",
            "C. Mitochondrial ATP synthase",
            "D. Lysosomal acid hydrolases"
        ],
        "answer": "A. Cytochrome P-450 monooxygenases",
        "explanation": "Indirect carcinogens require enzymatic conversion (chiefly by hepatic Cytochrome P-450 dependent monooxygenases) to generate active electrophilic ultimate carcinogens."
    },
    {
        "id": 80,
        "category": "Carcinogenesis",
        "question": "Ultraviolet (UVB) radiation induces cutaneous carcinogenesis by generating which specific form of DNA damage?",
        "options": [
            "A. Double-strand DNA breaks",
            "B. Formation of pyrimidine (specifically thymine) dimers",
            "C. Chromosomal translocations",
            "D. Alkylation of guanine bases"
        ],
        "answer": "B. Formation of pyrimidine (specifically thymine) dimers",
        "explanation": "UVB light induces covalent cross-linking between adjacent pyrimidine bases, forming thymine dimers that lead to skin cancers if un-repaired."
    },
    {
        "id": 81,
        "category": "Carcinogenesis",
        "question": "High-risk Human Papillomavirus (HPV) serotypes 16 and 18 promote cervical carcinogenesis through viral E6 and E7 oncoproteins which selectively bind and neutralize:",
        "options": [
            "A. E6 binds p53; E7 binds pRb",
            "B. E6 binds pRb; E7 binds p53",
            "C. E6 binds RAS; E7 binds MYC",
            "D. E6 binds BCL-2; E7 binds BAX"
        ],
        "answer": "A. E6 binds p53; E7 binds pRb",
        "explanation": "HPV E6 promotes ubiquitin-mediated degradation of p53, while E7 binds and inactivates pRb, releasing E2F to drive uncontrolled cell proliferation."
    },
    {
        "id": 82,
        "category": "Carcinogenesis",
        "question": "Epstein-Barr Virus (EBV) is etiologically linked to which spectrum of human malignancies?",
        "options": [
            "A. Hepatocellular carcinoma and Kaposi sarcoma",
            "B. African endemic Burkitt lymphoma, Nasopharyngeal carcinoma, and post-transplant B-cell lymphoproliferative disorders",
            "C. Adult T-cell leukemia/lymphoma and cervical carcinoma",
            "D. Merkel cell carcinoma and angiosarcoma"
        ],
        "answer": "B. African endemic Burkitt lymphoma, Nasopharyngeal carcinoma, and post-transplant B-cell lymphoproliferative disorders",
        "explanation": "EBV infects B-cells and nasopharyngeal epithelium, contributing to endemic Burkitt lymphoma, nasopharyngeal carcinoma, Hodgkin lymphoma, and post-transplant B-cell lymphomas."
    },
    {
        "id": 83,
        "category": "Carcinogenesis",
        "question": "Helicobacter pylori infection promotes gastric adenocarcinoma and gastric MALT lymphoma through chronic mucosal inflammation and secretion of:",
        "options": [
            "A. CagA oncoprotein and reactive oxygen species",
            "B. Enterotoxin B",
            "C. Alpha-toxin",
            "D. E6/E7 viral proteins"
        ],
        "answer": "A. CagA oncoprotein and reactive oxygen species",
        "explanation": "H. pylori introduces CagA into gastric epithelial cells and causes chronic gastritis, driving epithelial hyperproliferation and B-cell polyclonal expansion (MALT lymphoma)."
    },
    {
        "id": 84,
        "category": "Carcinogenesis",
        "question": "Human T-cell Leukemia Virus type 1 (HTLV-1) causes Adult T-cell Leukemia/Lymphoma (ATLL) by encoding which viral transactivator protein?",
        "options": [
            "A. Tax protein",
            "B. Tat protein",
            "C. EBNA-1",
            "D. LMP-1"
        ],
        "answer": "A. Tax protein",
        "explanation": "HTLV-1 encodes the Tax protein, which transactivates host cytokines (IL-2 and IL-2R) and inactivates the p16/INK4a CDKI, driving T-cell proliferation."
    },
    {
        "id": 85,
        "category": "Carcinogenesis",
        "question": "Infectious infection with Schistosoma haematobium in Sub-Saharan Africa predisposes to which specific bladder cancer?",
        "options": [
            "A. Transitional cell carcinoma",
            "B. Squamous cell carcinoma of the urinary bladder",
            "C. Adenocarcinoma of the urachus",
            "D. Small cell carcinoma"
        ],
        "answer": "B. Squamous cell carcinoma of the urinary bladder",
        "explanation": "Chronic vesical schistosomiasis causes squamous metaplasia of the bladder urothelium, leading to squamous cell carcinoma."
    },
    {
        "id": 86,
        "category": "Carcinogenesis",
        "question": "Nitrosamines and nitrosamides synthesized in the stomach from food nitrate preservatives are linked to:",
        "options": [
            "A. Gastric adenocarcinoma",
            "B. Renal cell carcinoma",
            "C. Bronchogenic carcinoma",
            "D. Hepatocellular carcinoma"
        ],
        "answer": "A. Gastric adenocarcinoma",
        "explanation": "Nitrosamines (formed by bacterial conversion of nitrates in preserved/smoked foods) are potent chemical carcinogens linked to gastric adenocarcinoma."
    },
    {
        "id": 87,
        "category": "Carcinogenesis",
        "question": "Ionizing radiation (X-rays, gamma-rays) causes genomic mutations primarily through:",
        "options": [
            "A. Formation of thymine-thymine crosslinks",
            "B. Generation of hydroxyl free radicals causing DNA double-strand breaks and chromosome translocations",
            "C. Direct inhibition of RNA polymerase",
            "D. Insertion of transposons"
        ],
        "answer": "B. Generation of hydroxyl free radicals causing DNA double-strand breaks and chromosome translocations",
        "explanation": "Ionizing radiation radiolyzes cellular water, producing free radicals that break DNA double-strands and induce chromosome aberrations."
    },
    {
        "id": 88,
        "category": "Carcinogenesis",
        "question": "Hepatitis B Virus (HBV) and Hepatitis C Virus (HCV) promote hepatocellular carcinoma primarily through:",
        "options": [
            "A. Direct insertion of viral v-onc genes into host hepatocytes",
            "B. Chronic immune-mediated liver injury, hepatocyte death, and compensatory oxidative-stress regeneration",
            "C. Synthesis of bacterial CagA proteins",
            "D. Translocation t(14;18)"
        ],
        "answer": "B. Chronic immune-mediated liver injury, hepatocyte death, and compensatory oxidative-stress regeneration",
        "explanation": "HBV/HCV cause chronic necroinflammation and regeneration (cirrhosis), increasing the cumulative risk of somatic mutations during hepatocyte division."
    },
    {
        "id": 89,
        "category": "Carcinogenesis",
        "question": "Human Herpesvirus 8 (HHV-8) is the direct oncogenic causative agent of which vascular neoplasm in HIV/AIDS patients?",
        "options": [
            "A. Angiosarcoma",
            "B. Kaposi sarcoma",
            "C. Glomangioma",
            "D. Hemangioendothelioma"
        ],
        "answer": "B. Kaposi sarcoma",
        "explanation": "HHV-8 (Kaposi Sarcoma-associated Herpesvirus) encodes viral homologs of cyclin D and cytokines, driving Kaposi sarcoma in immunocompromised patients."
    },
    {
        "id": 90,
        "category": "Carcinogenesis",
        "question": "Chemotherapeutic alkylating agents (e.g., Cyclophosphamide) used to treat primary tumors carry a recognized long-term risk for inducing secondary:",
        "options": [
            "A. Acute myelogenous leukemia (AML)",
            "B. Squamous cell carcinoma of the larynx",
            "C. Renal oncocytoma",
            "D. Medullary thyroid carcinoma"
        ],
        "answer": "A. Acute myelogenous leukemia (AML)",
        "explanation": "Alkylating chemotherapeutic agents damage DNA and carry a known late risk of inducing secondary acute myelogenous leukemia (AML)."
    },
    {
        "id": 91,
        "category": "Tumor Host Interactions",
        "question": "Cancer cachexia (progressive loss of body fat and lean muscle mass accompanied by profound weakness) is primarily mediated by host and tumor cytokines including:",
        "options": [
            "A. Tumor Necrosis Factor-alpha (TNF-a / Cachectin), IL-1, and IFN-gamma",
            "B. Insulin-like growth factor-1 (IGF-1)",
            "C. Erythropoietin and Thrombopoietin",
            "D. Parathyroid hormone-related peptide (PTHrP)"
        ],
        "answer": "A. Tumor Necrosis Factor-alpha (TNF-a / Cachectin), IL-1, and IFN-gamma",
        "explanation": "Cancer cachexia is a metabolic syndrome driven by systemic proinflammatory cytokines (TNF-a, IL-1, IL-6, IFN-g) that suppress appetite and stimulate muscle/fat catabolism."
    },
    {
        "id": 92,
        "category": "Tumor Host Interactions",
        "question": "A Paraneoplastic Syndrome is defined as a symptom complex in cancer patients that:",
        "options": [
            "A. Is directly caused by local invasion or distant anatomical metastases of the primary mass",
            "B. Cannot be readily explained by local/distant tumor spread or hormones typical of the tissue of origin",
            "C. Occurs exclusively in patients with benign adenomas",
            "D. Results directly from surgical excision margins"
        ],
        "answer": "B. Cannot be readily explained by local/distant tumor spread or hormones typical of the tissue of origin",
        "explanation": "Paraneoplastic syndromes are clinical complexes arising from ectopic hormone secretion or autoimmune cross-reactivity, not attributable to local/metastatic spread."
    },
    {
        "id": 93,
        "category": "Tumor Host Interactions",
        "question": "The most common paraneoplastic endocrine syndrome is hypercalcemia caused by tumor secretion of Parathyroid Hormone-Related Peptide (PTHrP) in:",
        "options": [
            "A. Small cell lung carcinoma",
            "B. Squamous cell carcinoma of the lung",
            "C. Colonic adenocarcinoma",
            "D. Gastric adenocarcinoma"
        ],
        "answer": "B. Squamous cell carcinoma of the lung",
        "explanation": "Hypercalcemia of malignancy via ectopic PTHrP secretion is most frequently associated with squamous cell carcinoma of the lung (and renal/breast cancers)."
    },
    {
        "id": 94,
        "category": "Tumor Host Interactions",
        "question": "Ectopic production of Adrenocorticotropic Hormone (ACTH) leading to paraneoplastic Cushing syndrome is most classic for:",
        "options": [
            "A. Small cell anaplastic carcinoma of the lung",
            "B. Renal cell carcinoma",
            "C. Prostatic adenocarcinoma",
            "D. Hepatocellular carcinoma"
        ],
        "answer": "A. Small cell anaplastic carcinoma of the lung",
        "explanation": "Small cell lung carcinoma frequently secretes ectopic ACTH (causing Cushing syndrome) or ADH (causing SIADH)."
    },
    {
        "id": 95,
        "category": "Tumor Host Interactions",
        "question": "Trousseau syndrome (migratory thrombophlebitis) associated with pancreatic or gastric mucin-secreting adenocarcinomas results from:",
        "options": [
            "A. Direct arterial wall destruction by tumor cells",
            "B. Release of procoagulant mucins and tissue factor into the circulation",
            "C. Autoimmune antibody destruction of platelets",
            "D. Ectopic calcitonin hypersecretion"
        ],
        "answer": "B. Release of procoagulant mucins and tissue factor into the circulation",
        "explanation": "Mucin-secreting adenocarcinomas release procoagulants into blood, causing venous thrombosis that migrates across different vascular beds (Trousseau sign)."
    },
    {
        "id": 96,
        "category": "Tumor Host Interactions",
        "question": "Which cell type in the host immune system provides the primary specific cellular immune defense against tumor cells carrying tumor-specific antigens?",
        "options": [
            "A. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "B. Neutrophils",
            "C. Eosinophils",
            "D. Mast cells"
        ],
        "answer": "A. CD8+ Cytotoxic T Lymphocytes (CTLs)",
        "explanation": "CD8+ Cytotoxic T Lymphocytes play the central role in cell-mediated immune surveillance by recognizing tumor antigens presented on MHC Class I molecules."
    },
    {
        "id": 97,
        "category": "Tumor Host Interactions",
        "question": "Natural Killer (NK) cells can destroy tumor cells without prior sensitization, particularly targeting cells that exhibit:",
        "options": [
            "A. Overexpression of MHC Class I molecules",
            "B. Downregulation or complete loss of MHC Class I surface expression",
            "C. High intracellular glycogen stores",
            "D. Dense capsular extracellular matrix"
        ],
        "answer": "B. Downregulation or complete loss of MHC Class I surface expression",
        "explanation": "MHC Class I molecules normally send inhibitory signals to NK cells. When tumor cells downregulate MHC Class I to escape CTLs, NK cells recognize and lyse them."
    },
    {
        "id": 98,
        "category": "Tumor Host Interactions",
        "question": "How do tumor cells escape immune surveillance by exploiting the PD-1 / PD-L1 pathway?",
        "options": [
            "A. Tumor PD-L1 binds PD-1 on T-cells, delivering an inhibitory signal that induces T-cell exhaustion/anergy",
            "B. Tumor cells secrete excess histamine to lyse T-cells",
            "C. PD-L1 activates complement MAC pore formation",
            "D. PD-1 enhances MHC Class II antigen presentation"
        ],
        "answer": "A. Tumor PD-L1 binds PD-1 on T-cells, delivering an inhibitory signal that induces T-cell exhaustion/anergy",
        "explanation": "Tumor cells express PD-L1, which binds PD-1 on CD8+ T-cells, suppressing T-cell receptor signaling and causing functional immune exhaustion."
    },
    {
        "id": 99,
        "category": "Tumor Host Interactions",
        "question": "Immunodeficient patients (e.g., organ transplant recipients on immunosuppressants or HIV/AIDS patients) exhibit a 200-fold increased risk primarily for which malignancies?",
        "options": [
            "A. Breast and prostate carcinomas",
            "B. Lymphomas and virus-associated carcinomas (e.g., Kaposi sarcoma, EBV lymphomas)",
            "C. Colorectal and pancreatic adenocarcinomas",
            "D. Osteosarcomas and chondrosarcomas"
        ],
        "answer": "B. Lymphomas and virus-associated carcinomas (e.g., Kaposi sarcoma, EBV lymphomas)",
        "explanation": "Immunodeficient hosts show a marked increase in malignancies, predominantly oncogenic virus-driven tumors such as EBV-related lymphomas and HHV-8 Kaposi sarcoma."
    },
    {
        "id": 100,
        "category": "Tumor Host Interactions",
        "question": "Non-bacterial thrombotic endocarditis (Marantic endocarditis) in advanced cancer patients is characterized by:",
        "options": [
            "A. Virulent bacterial destruction of the aortic valve",
            "B. Deposition of sterile fibrin and platelet vegetations on cardiac valves in hypercoagulable states",
            "C. Autoimmune antibody cross-reactivity with Streptococcal M protein",
            "D. Ectopic growth of cardiac myxoma tissue"
        ],
        "answer": "B. Deposition of sterile fibrin and platelet vegetations on cardiac valves in hypercoagulable states",
        "explanation": "Marantic endocarditis is the formation of small sterile fibrin/platelet thrombi on heart valves in hypercoagulable cancer patients (often accompanying cachexia)."
    },
    {
        "id": 101,
        "category": "Tumor Host Interactions",
        "question": "Which paraneoplastic manifestation is characteristically associated with renal cell carcinoma via ectopic erythropoietin secretion?",
        "options": [
            "A. Erythrocytosis (Polycythemia)",
            "B. Hypoglycemia",
            "C. Hyperthyroidism",
            "D. Thrombocytopenia"
        ],
        "answer": "A. Erythrocytosis (Polycythemia)",
        "explanation": "Renal cell carcinoma (and hepatocellular carcinoma or cerebellar hemangioblastoma) can secrete ectopic erythropoietin, stimulating RBC production."
    },
    {
        "id": 102,
        "category": "Tumor Host Interactions",
        "question": "Myasthenia gravis (muscle weakness improving with rest) is a paraneoplastic autoimmune syndrome strongly associated with neoplasms of the:",
        "options": [
            "A. Thyroid gland",
            "B. Thymus gland (Thymoma)",
            "C. Adrenal cortex",
            "D. Pancreatic islets"
        ],
        "answer": "B. Thymus gland (Thymoma)",
        "explanation": "Approximately 30-40% of patients with thymoma develop paraneoplastic Myasthenia Gravis due to autoantibodies against nicotinic acetylcholine receptors."
    },
    {
        "id": 103,
        "category": "Tumor Host Interactions",
        "question": "Tumor cells evade host immune destruction through which of the following immunosuppressive cytokines?",
        "options": [
            "A. Transforming Growth Factor-beta (TGF-b)",
            "B. Interleukin-2 (IL-2)",
            "C. Interferon-gamma",
            "D. Tumor Necrosis Factor-alpha"
        ],
        "answer": "A. Transforming Growth Factor-beta (TGF-b)",
        "explanation": "Tumors secrete TGF-beta, an immunosuppressive cytokine that inhibits T-cell proliferation and effector function."
    },
    {
        "id": 104,
        "category": "Tumor Host Interactions",
        "question": "Lambert-Eaton Myasthenic Syndrome is a paraneoplastic neurological disorder caused by autoantibodies directed against:",
        "options": [
            "A. Post-synaptic acetylcholine receptors",
            "B. Presynaptic voltage-gated calcium channels in small cell lung carcinoma patients",
            "C. Myelin basic protein",
            "D. Glial fibrillary acidic protein"
        ],
        "answer": "B. Presynaptic voltage-gated calcium channels in small cell lung carcinoma patients",
        "explanation": "Lambert-Eaton syndrome is a paraneoplastic autoimmune disease associated with small cell lung cancer, caused by antibodies to presynaptic P/Q-type calcium channels."
    },
    {
        "id": 105,
        "category": "Tumor Host Interactions",
        "question": "Hypertrophic Osteoarthropathy (periosteal new bone formation and digital clubbing) is a classic paraneoplastic feature of:",
        "options": [
            "A. Bronchogenic lung carcinoma",
            "B. Prostatic adenocarcinoma",
            "C. Acute lymphocytic leukemia",
            "D. Multiple myeloma"
        ],
        "answer": "A. Bronchogenic lung carcinoma",
        "explanation": "Hypertrophic pulmonary osteoarthropathy (digital clubbing, painful periostitis) is associated with lung carcinomas and intrathoracic disease."
    },
    {
        "id": 106,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "Alpha-Fetoprotein (AFP) is an oncofetal glycoprotein tumor marker synthesized during fetal life by the yolk sac and liver. Serum AFP is elevated in:",
        "options": [
            "A. Hepatocellular carcinoma and non-seminomatous germ cell testicular tumors (Yolk sac tumor)",
            "B. Prostatic adenocarcinoma and seminoma",
            "C. Choriocarcinoma and medullary thyroid carcinoma",
            "D. Colorectal carcinoma and leiomyosarcoma"
        ],
        "answer": "A. Hepatocellular carcinoma and non-seminomatous germ cell testicular tumors (Yolk sac tumor)",
        "explanation": "AFP is an oncofetal antigen elevated in 100% of yolk sac (endodermal sinus) tumors and in hepatocellular carcinoma (HCC)."
    },
    {
        "id": 107,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "Carcinoembryonic Antigen (CEA) is a cell-surface glycoprotein tumor marker primarily elevated in which malignant tumor group?",
        "options": [
            "A. Colorectal and gastrointestinal adenocarcinomas",
            "B. Multiple myeloma",
            "C. Choriocarcinoma",
            "D. Prostatic adenocarcinoma"
        ],
        "answer": "A. Colorectal and gastrointestinal adenocarcinomas",
        "explanation": "CEA is an oncofetal adhesion glycoprotein elevated in ~70% of colorectal carcinomas, as well as gastric, pancreatic, and breast cancers."
    },
    {
        "id": 108,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "Serum Human Chorionic Gonadotropin (hCG) is a diagnostic hormone tumor marker characteristically elevated in:",
        "options": [
            "A. Gestational trophoblastic disease (Choriocarcinoma, hydatidiform mole) and testicular germ cell tumors",
            "B. Medullary carcinoma of the thyroid",
            "C. Pheochromocytoma",
            "D. Adrenocortical adenoma"
        ],
        "answer": "A. Gestational trophoblastic disease (Choriocarcinoma, hydatidiform mole) and testicular germ cell tumors",
        "explanation": "hCG is secreted by syncytiotrophoblasts and serves as a marker for gestational choriocarcinoma, hydatidiform mole, and embryonal/germ cell tumors."
    },
    {
        "id": 109,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "Calcitonin is a specific hormonal tumor marker released by neuroendocrine C-cells in:",
        "options": [
            "A. Papillary thyroid carcinoma",
            "B. Medullary carcinoma of the thyroid",
            "C. Anaplastic thyroid carcinoma",
            "D. Parathyroid adenoma"
        ],
        "answer": "B. Medullary carcinoma of the thyroid",
        "explanation": "Medullary thyroid carcinoma arises from parafollicular C-cells and secretes calcitonin, serving as an ideal marker for diagnosis and monitoring."
    },
    {
        "id": 110,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "Measurement of 24-hour urinary Vanillylmandelic Acid (VMA) and metanephrines is diagnostic for:",
        "options": [
            "A. Carcinoid tumor",
            "B. Pheochromocytoma",
            "C. Insulinoma",
            "D. Gastrinoma"
        ],
        "answer": "B. Pheochromocytoma",
        "explanation": "Pheochromocytomas secrete catecholamines (epinephrine, norepinephrine), which break down into metanephrines and VMA excreted in urine."
    },
    {
        "id": 111,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "Urinary 5-Hydroxyindoleacetic Acid (5-HIAA) is the primary breakdown metabolite used to diagnose:",
        "options": [
            "A. Carcinoid syndrome / neuroendocrine carcinoid tumors",
            "B. Pheochromocytoma",
            "C. Neuroblastoma",
            "D. Multiple myeloma"
        ],
        "answer": "A. Carcinoid syndrome / neuroendocrine carcinoid tumors",
        "explanation": "Carcinoid tumors synthesize serotonin (5-HT), which is oxidized to 5-HIAA and excreted in urine."
    },
    {
        "id": 112,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "CA 19-9 is a carbohydrate tumor antigen primarily utilized for clinical monitoring of:",
        "options": [
            "A. Pancreatic carcinoma",
            "B. Ovarian serous cystadenocarcinoma",
            "C. Breast carcinoma",
            "D. Prostatic adenocarcinoma"
        ],
        "answer": "A. Pancreatic carcinoma",
        "explanation": "CA 19-9 is elevated in ~80-90% of pancreatic adenocarcinomas and is used to monitor treatment response and disease recurrence."
    },
    {
        "id": 113,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "CA 125 is a valuable serum tumor antigen marker used in the diagnosis and post-operative surveillance of:",
        "options": [
            "A. Ovarian epithelial carcinomas",
            "B. Endometrial leiomyosarcoma",
            "C. Cervical squamous cell carcinoma",
            "D. Choriocarcinoma"
        ],
        "answer": "A. Ovarian epithelial carcinomas",
        "explanation": "CA 125 is elevated in non-mucinous epithelial ovarian cancers and serves as a key biomarker for monitoring therapy response."
    },
    {
        "id": 114,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "Neuron-Specific Enolase (NSE) is an enzyme tumor marker elevated in neuroendocrine tumors and:",
        "options": [
            "A. Small cell anaplastic carcinoma of the lung and Neuroblastoma",
            "B. Renal cell carcinoma",
            "C. Squamous cell carcinoma of the esophagus",
            "D. Prostatic adenocarcinoma"
        ],
        "answer": "A. Small cell anaplastic carcinoma of the lung and Neuroblastoma",
        "explanation": "NSE is expressed by neural and neuroendocrine cells, serving as a circulating tumor marker for small cell lung cancer and pediatric neuroblastoma."
    },
    {
        "id": 115,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "Prostate-Specific Antigen (PSA) is an enzyme tumor marker specific for:",
        "options": [
            "A. Prostatic tissue (both benign hypertrophy and adenocarcinoma)",
            "B. Malignant prostate carcinoma exclusively",
            "C. Transitional cell bladder epithelium",
            "D. Testicular Leydig cells"
        ],
        "answer": "A. Prostatic tissue (both benign hypertrophy and adenocarcinoma)",
        "explanation": "PSA is organ-specific (produced by prostatic luminal epithelium) rather than cancer-specific; it is elevated in prostate cancer, BPH, and prostatitis."
    },
    {
        "id": 116,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "Monoclonal immunoglobulin spike (M-protein) and urinary Bence-Jones proteins (free Ig light chains) are diagnostic markers for:",
        "options": [
            "A. Multiple myeloma",
            "B. Hodgkin lymphoma",
            "C. Acute lymphocytic leukemia",
            "D. Chronic myelogenous leukemia"
        ],
        "answer": "A. Multiple myeloma",
        "explanation": "Multiple myeloma is a plasma cell neoplasm that secretes monoclonal immunoglobulins (M spike on serum protein electrophoresis) and urinary free light chains (Bence-Jones proteinuria)."
    },
    {
        "id": 117,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "Which laboratory technique provides the standard quantitative measurement for serum protein tumor markers?",
        "options": [
            "A. Column chromatography",
            "B. Gel electrophoresis",
            "C. Sandwich enzyme immunoassay (ELISA / Automated Immunoassay)",
            "D. Spectrophotometric blood gas analysis"
        ],
        "answer": "C. Sandwich enzyme immunoassay (ELISA / Automated Immunoassay)",
        "explanation": "Quantitative tumor marker testing (PSA, AFP, CEA, hCG) relies primarily on automated sandwich enzyme immunoassays."
    },
    {
        "id": 118,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "CA 15-3 and CA 27.29 are tumor antigen markers used clinically for monitoring treatment in patients with:",
        "options": [
            "A. Advanced breast carcinoma",
            "B. Pancreatic adenocarcinoma",
            "C. Renal cell carcinoma",
            "D. Gastric adenocarcinoma"
        ],
        "answer": "A. Advanced breast carcinoma",
        "explanation": "CA 15-3 and CA 27.29 are mucin-derived tumor markers used to monitor disease course and response to therapy in metastatic breast cancer."
    },
    {
        "id": 119,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "Chromogranin A is a secretory protein located in dense-core granules, serving as a universal biomarker for:",
        "options": [
            "A. Neuroendocrine tumors (e.g., carcinoids, pheochromocytomas, islet cell tumors)",
            "B. Sarcomas",
            "C. Squamous cell carcinomas",
            "D. Lymphomas"
        ],
        "answer": "A. Neuroendocrine tumors (e.g., carcinoids, pheochromocytomas, islet cell tumors)",
        "explanation": "Chromogranin A is contained in neuroendocrine secretory granules and is elevated in serum across diverse neuroendocrine neoplasms."
    },
    {
        "id": 120,
        "category": "Markers of Endocrine & Non-Endocrine Tumors",
        "question": "S-100 protein and HMB-45 (Human Melanoma Black 45) are immunohistochemical markers diagnostic for:",
        "options": [
            "A. Malignant Melanoma",
            "B. Squamous cell carcinoma",
            "C. Adenocarcinoma of colon",
            "D. Leiomyosarcoma"
        ],
        "answer": "A. Malignant Melanoma",
        "explanation": "S-100, HMB-45, and Melan-A/MART-1 are key immunohistochemical markers for establishing the diagnosis of malignant melanoma."
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

total_q = len(NEOPLASIA_QS)

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
q = NEOPLASIA_QS[st.session_state.current_index]
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

col_q, col_timer = st.columns([3, 1])

with col_timer:
  # 1. Dynamic color scheme based on remaining seconds
  if remaining > 20:
    border_color = "#28a745"  # Green
    bg_color = "#e8f5e9"
    text_color = "#1b5e20"
    icon = "⏳"
    label = "TIME REMAINING"
  elif remaining > 10:
    border_color = "#ff9800"  # Orange
    bg_color = "#fff3e0"
    text_color = "#e65100"
    icon = "⚠️"
    label = "HURRY UP!"
  else:
    border_color = "#dc3545"  # Red
    bg_color = "#ffebee"
    text_color = "#b71c1c"
    icon = "🚨"
    label = "CRITICAL TIME!"

  # 2. Custom HTML / CSS Styled Box 
  timer_box_html = f"""
    <div style="
        background-color: {bg_color};
        border: 2px solid {border_color};
        border-radius: 12px;
        padding: 10px 16px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08);
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        margin-bottom: 12px;
    ">
        <div style="font-size: 11px; font-weight: 700; letter-spacing: 1px; color: {text_color}; text-transform: uppercase;">
            {icon} {label}
        </div>
        <div style="font-size: 32px; font-weight: 800; color: {text_color}; line-height: 1.1; margin-top: 2px;">
            {remaining}<span style="font-size: 18px; font-weight: 600;">s</span>
        </div>
    </div>
    """
  st.markdown(timer_box_html, unsafe_allow_html=True)

with col_q:
    st.caption(f"Category: {q['category']}")
    st.subheader(f"Q{q['id']}. {q['question']}")

is_answered = st.session_state.get(f"answered_{q_id}", False)
is_time_out = (remaining == 0 and not is_answered)

if is_time_out and not is_answered:
    st.session_state[f"answered_{q_id}"] = True
    st.session_state[f"selected_{q_id}"] = "TIME EXPIRED"
    log_response(
        module_name="Neoplasia_331 Quiz",
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
                module_name="Neoplasia_331 Quiz",
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

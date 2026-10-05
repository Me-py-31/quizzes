import streamlit as st
import pandas as pd
import datetime
import time
import json

# ------------------------------------------------------------------------------
# 1. STREAMLIT CONFIGURATION & HEADER
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="🧬 Neoplasia 250-Question Master Quiz (1m 10s Timer)",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧬 Neoplasia & Clinical Oncology Master Question Bank (250 Questions)")
st.caption("Comprehensive Interactive Assessment | Robbins Pathology & Past Exam Question Banks | 1 min 10 sec Timer Per Question")

# ------------------------------------------------------------------------------
# 2. SESSION STATE & PROGRESS SAVE / RESTORE UTILITIES
# ------------------------------------------------------------------------------
if "current_part" not in st.session_state:
    st.session_state.current_part = "Part 1: Epidemiology & Carcinogenesis"

if "question_indices" not in st.session_state:
    st.session_state.question_indices = {
        "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth": 0,
        "Part 2: Tumour Markers": 0,
        "Part 3: Metastasis, Staging and Survival": 0,
        "Part 4: Tumor Host Interactions": 0
    }

if "scores" not in st.session_state:
    st.session_state.scores = {
        "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth": 0,
        "Part 2: Tumour Markers": 0,
        "Part 3: Metastasis, Staging and Survival": 0,
        "Part 4: Tumor Host Interactions": 0
    }

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}  # key: q_id, val: dict

# Sidebar Navigation & Control Panel
st.sidebar.title("🎮 Quiz Control Center")

st.sidebar.markdown("### 💾 Save & Restore Progress")
progress_data = {
    "question_indices": st.session_state.question_indices,
    "scores": st.session_state.scores,
    "user_answers": st.session_state.user_answers,
    "current_part": st.session_state.current_part
}

st.sidebar.download_button(
    label="💾 Download Progress (.json)",
    data=json.dumps(progress_data, indent=2),
    file_name="neoplasia_250q_progress.json",
    mime="application/json"
)

uploaded_file = st.sidebar.file_uploader("📥 Load Saved Progress (.json)", type=["json"])
if uploaded_file is not None:
    try:
        loaded_data = json.load(uploaded_file)
        st.session_state.question_indices = loaded_data.get("question_indices", st.session_state.question_indices)
        st.session_state.scores = loaded_data.get("scores", st.session_state.scores)
        st.session_state.user_answers = loaded_data.get("user_answers", st.session_state.user_answers)
        st.session_state.current_part = loaded_data.get("current_part", st.session_state.current_part)
        st.sidebar.success("Progress loaded successfully! 🎉")
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")

st.sidebar.divider()
st.sidebar.markdown("### 🧩 Select Quiz Part")

part_list = [
    "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
    "Part 2: Tumour Markers",
    "Part 3: Metastasis, Staging and Survival",
    "Part 4: Tumor Host Interactions"
]

selected_part = st.sidebar.radio(
    "Select Module:",
    part_list,
    index=part_list.index(st.session_state.current_part)
)

if selected_part != st.session_state.current_part:
    st.session_state.current_part = selected_part
    st.rerun()


NEOPLASIA_250_QS = {
    "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth": [
        {
            "id": 1,
            "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
            "question": "A 62-year-old male shipyard worker presents with progressive dyspnea and chest wall pain. Chest CT reveals diffuse pleural thickening and a calcified pleural plaque. A pleural biopsy confirms malignant mesothelioma. Which environmental carcinogen is the primary etiologic agent?",
            "options": [
                "A. Beryllium",
                "B. Silica dust",
                "C. Asbestos fibers",
                "D. Coal dust"
            ],
            "answer": "C. Asbestos fibers",
            "explanation": "Occupational exposure to asbestos in shipyard, insulation, and roofing workers is strongly linked to pleural and peritoneal malignant mesothelioma, as well as bronchogenic carcinoma."
        },
        {
            "id": 2,
            "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
            "question": "A 54-year-old plastic manufacturing employee develops fatigue and right upper quadrant abdominal pain. Abdominal MRI shows a large vascular hepatic mass. Liver biopsy reveals hepatic angiosarcoma. Occupational history is most notable for exposure to which compound?",
            "options": [
                "A. Benzene",
                "B. Beta-naphthylamine",
                "C. Vinyl chloride monomer",
                "D. Arsenic"
            ],
            "answer": "C. Vinyl chloride monomer",
            "explanation": "Occupational exposure to vinyl chloride monomer in PVC plastics production is classically associated with hepatic angiosarcoma, a rare malignant tumor of vascular endothelial cells."
        },
        {
            "id": 3,
            "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
            "question": "A 68-year-old retired industrial dye worker presents with painless gross hematuria. Cystoscopy reveals a papillary lesion in the urinary bladder. Biopsy confirms urothelial (transitional cell) carcinoma. Exposure to which chemical carcinogen is the underlying cause?",
            "options": [
                "A. Beta-naphthylamine (Azo dyes)",
                "B. Polycyclic aromatic hydrocarbons",
                "C. Aflatoxin B1",
                "D. Benzene"
            ],
            "answer": "A. Beta-naphthylamine (Azo dyes)",
            "explanation": "Beta-naphthylamine and aromatic amines in dye and rubber industries undergo hepatic glucuronidation and renal excretion. In the bladder, bacterial glucuronidase hydrolyzes them into active carcinogens causing bladder urothelial carcinoma."
        },
        {
            "id": 4,
            "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
            "question": "A 48-year-old male from Qidong, China, presents with weight loss and a painful liver mass. Serum AFP is elevated at 12,000 ng/mL. Liver biopsy reveals hepatocellular carcinoma. Sequencing of p53 shows a specific G-to-T transversion at codon 249. This mutation is caused by synergy between HBV and which dietary toxin?",
            "options": [
                "A. Ochratoxin A",
                "B. Aflatoxin B1",
                "C. Nitrosamines",
                "D. Pyrrolizidine alkaloids"
            ],
            "answer": "B. Aflatoxin B1",
            "explanation": "Aflatoxin B1 (produced by Aspergillus flavus contamination of stored grains and peanuts) causes a signature G-to-T transversion at codon 249 (249ser) of the TP53 gene in hepatocellular carcinoma."
        },
        {
            "id": 5,
            "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
            "question": "A 35-year-old fair-skinned woman presents with a dark, irregularly bordered skin nodule on her shoulder. Biopsy confirms invasive malignant melanoma. The primary physical carcinogen responsible for this neoplasm induces DNA damage via which mechanism?",
            "options": [
                "A. Double-strand DNA break formation by ionizing radiation",
                "B. Formation of pyrimidine (thymine) dimers by UVB radiation",
                "C. Alkylating DNA base cross-links",
                "D. Single-strand DNA breaks by infrared radiation"
            ],
            "answer": "B. Formation of pyrimidine (thymine) dimers by UVB radiation",
            "explanation": "UVB radiation (wavelength 280-320 nm) damages DNA by forming pyrimidine dimers (e.g., thymine-thymine cross-links), which require Nucleotide Excision Repair (NER) for clearance."
        },
        {
            "id": 6,
            "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
            "question": "Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
            "options": [
                "A. Promoters directly cause irreversible DNA damage without requiring initiation",
                "B. Initiators cause irreversible, non-lethal DNA mutations; promoters drive clonal expansion of initiated cells",
                "C. Promoters must be administered prior to initiators to produce malignant transformation",
                "D. Initiation is a reversible cell division process driven by non-mutagenic growth factors"
            ],
            "answer": "B. Initiators cause irreversible, non-lethal DNA mutations; promoters drive clonal expansion of initiated cells",
            "explanation": "Chemical initiation requires electrophilic DNA binding that causes permanent, non-lethal genetic damage. Subsequent application of promoters (non-mutagenic growth stimuli) drives clonal proliferation of the mutated cell."
        },
        {
        "id": 7,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 8,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 9,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 10,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 11,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 12,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 13,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 14,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 15,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 16,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 17,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 18,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 19,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 20,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
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
        "id": 21,
        "category": "Part 1: Cancer Epidemiology, Carcinogenesis & Disorders of Growth",
        "question": "Which architectural feature is characteristic of epithelial dysplasia under light microscopy?",
        "options": [
            "A. Basal-like cells appearing in the upper/superficial layers with loss of normal polarity",
            "B. Dense fibrous pseudocapsule enclosing the epithelial sheet",
            "C. Diffuse invasion of lymphatic channels beneath the basement membrane",
            "D. Uniform cell size and low nuclear-to-cytoplasmic ratio"
        ],
        "answer": "A. Basal-like cells appearing in the upper/superficial layers with loss of normal polarity",
        "explanation": "Microscopically, dysplasia shows loss of cellular uniformity and architectural orientation (loss of polarity), with immature basal-like cells present in the upper layers of the epithelium."
        }
    ],
    "Part 2: Tumour Markers": [
        {
            "id": 22,
            "category": "Part 2: Tumour Markers",
            "question": "A 58-year-old male with chronic Hepatitis B liver cirrhosis undergoes routine screening. Ultrasound shows a 3.5 cm solitary liver nodule. Which serum tumor marker is most specific for diagnosing Hepatocellular Carcinoma?",
            "options": [
                "A. Carcinoembryonic Antigen (CEA)",
                "B. Alpha-Fetoprotein (AFP)",
                "C. CA 19-9",
                "D. Human Chorionic Gonadotropin (hCG)"
            ],
            "answer": "B. Alpha-Fetoprotein (AFP)",
            "explanation": "Alpha-fetoprotein (AFP) is a fetal serum glycoprotein re-expressed in hepatocellular carcinoma and non-seminomatous germ cell tumors of the testis (yolk sac tumors)."
        },
        {
            "id": 23,
            "category": "Part 2: Tumour Markers",
            "question": "A 62-year-old male presenting with painless jaundice and significant weight loss is found to have a mass in the head of the pancreas on abdominal CT. Which serum tumor marker is most characteristic of pancreatic adenocarcinoma?",
            "options": [
                "A. CA 125",
                "B. CA 19-9",
                "C. CA 15-3",
                "D. Alpha-Fetoprotein"
            ],
            "answer": "B. CA 19-9",
            "explanation": "CA 19-9 is a mucin antigen widely used as a tumor marker for pancreatic adenocarcinoma and biliary tract carcinomas."
        },
        {
            "id": 24,
            "category": "Part 2: Tumour Markers",
            "question": "A 52-year-old postmenopausal woman presents with pelvic pressure and ascites. Pelvic ultrasound reveals a 7 cm complex cystic ovarian mass. Which serum biomarker is most useful for monitoring response to therapy and detecting recurrence in epithelial ovarian carcinoma?",
            "options": [
                "A. CA 125",
                "B. CA 19-9",
                "C. Alpha-Fetoprotein",
                "D. Beta-hCG"
            ],
            "answer": "A. CA 125",
            "explanation": "CA 125 is expressed by surface epithelial ovarian tumors and is the gold standard biomarker for monitoring therapeutic response and disease recurrence."
        },
        {
            "id": 25,
            "category": "Part 2: Tumour Markers",
            "question": "A 65-year-old male undergoes routine screening. His serum Prostate-Specific Antigen (PSA) is 8.5 ng/mL. Which statement regarding PSA as a screening tumor marker is TRUE?",
            "options": [
                "A. Elevated PSA is 100% specific for prostate adenocarcinoma and never occurs in benign disease",
                "B. PSA is organ-specific for prostatic epithelium, but not cancer-specific (elevated in BPH and prostatitis)",
                "C. Free PSA percentage increases significantly in prostate cancer compared to BPH",
                "D. PSA is an oncofetal antigen synthesized by embryonic neural crest cells"
            ],
            "answer": "B. PSA is organ-specific for prostatic epithelium, but not cancer-specific (elevated in BPH and prostatitis)",
            "explanation": "PSA is an organ-specific glycoprotein serine protease produced by prostatic glandular epithelium. Because it is elevated in BPH, prostatitis, and trauma, it lacks absolute cancer specificity."
        },
        {
            "id": 26,
            "category": "Part 2: Tumour Markers",
            "question": "Question 70 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        }
    ],
    "Part 3: Metastasis, Staging and Survival": [
        {
            "id": 27,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "A 55-year-old female presents with a 3 cm breast mass. Sentinel lymph node biopsy reveals tumor cells deposited in the subcapsular sinus of an axillary lymph node. Which route of metastatic dissemination is characteristic of carcinomas?",
            "options": [
                "A. Direct hematogenous spread via thick-walled arteries",
                "B. Primary lymphatic pathway draining to regional lymph nodes",
                "C. Transcoelomic seeding across peritoneal cavities",
                "D. Retrograde venous flow via Batson vertebral plexus"
            ],
            "answer": "B. Primary lymphatic pathway draining to regional lymph nodes",
            "explanation": "Carcinomas typically metastasize initially via lymphatic vessels to draining regional lymph nodes, depositing first in the subcapsular sinus, whereas sarcomas favor hematogenous spread."
        },
        {
            "id": 28,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "In the TNM staging system for colon cancer, a tumor that invades through the muscularis propria into pericolic fat (T3) with 3 positive regional lymph nodes (N1) and no distant metastases (M0) is classified as which clinical stage?",
            "options": [
                "A. Stage I",
                "B. Stage II",
                "C. Stage III",
                "D. Stage IV"
            ],
            "answer": "C. Stage III",
            "explanation": "In AJCC colonic cancer staging, any regional lymph node involvement (N1 or N2) in the absence of distant metastasis (M0) defines Stage III disease."
        },
        {
            "id": 29,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 128 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        }
    ],
    "Part 4: Tumor Host Interactions": [
        {
            "id": 30,
            "category": "Part 4: Tumor Host Interactions",
            "question": "A 64-year-old male with advanced metastatic lung adenocarcinoma exhibits severe progressive wasting, loss of appetite, anemia, and profound weakness despite nutritional support. Which cytokine secreted by macrophages and tumor cells is the primary mediator of Cancer Cachexia?",
            "options": [
                "A. Interleukin-10 (IL-10)",
                "B. Tumor Necrosis Factor-alpha (TNF-alpha / Cachectin)",
                "C. Transforming Growth Factor-beta (TGF-beta)",
                "D. Erythropoietin"
            ],
            "answer": "B. Tumor Necrosis Factor-alpha (TNF-alpha / Cachectin)",
            "explanation": "TNF-alpha (Cachectin), along with IL-1 and IL-6, suppresses appetite and mobilizes fat/protein reserves by inhibiting lipoprotein lipase, causing cancer cachexia."
        },
        {
            "id": 31,
            "category": "Part 4: Tumor Host Interactions",
            "question": "A 58-year-old heavy smoker presents with confusion, lethargy, and a serum sodium of 118 mEq/L (hyponatremia). Chest X-ray reveals a central lung mass. Biopsy confirms Small Cell Lung Carcinoma (SCLC). Which paraneoplastic syndrome accounts for these findings?",
            "options": [
                "A. Ectopic PTHrP production causing hypercalcemia",
                "B. Syndrome of Inappropriate Antidiuretic Hormone (SIADH) secretion",
                "C. Ectopic ACTH production causing Cushing syndrome",
                "D. Lambert-Eaton myasthenic syndrome"
            ],
            "answer": "B. Syndrome of Inappropriate Antidiuretic Hormone (SIADH) secretion",
            "explanation": "Small Cell Lung Carcinoma frequently secretes ectopic ADH, driving free water retention, concentrated urine, and dilutional hyponatremia (SIADH)."
        },
        {
            "id": 32,
            "category": "Part 4: Tumor Host Interactions",
            "question": "A 60-year-old male with pancreatic adenocarcinoma develops painful, tender, swollen cords in his left calf, followed 2 weeks later by similar inflamed venous lesions in his right arm. This recurrent migratory thrombophlebitis is known as:",
            "options": [
                "A. Horner syndrome",
                "B. Trousseau syndrome / sign",
                "C. Superior Vena Cava syndrome",
                "D. Eaton-Lambert syndrome"
            ],
            "answer": "B. Trousseau syndrome / sign",
            "explanation": "Trousseau syndrome (migratory thrombophlebitis) is a paraneoplastic hypercoagulable state caused by tumor mucin release activating factor X and procoagulants, classic for pancreatic carcinoma."
        },
        {
            "id": 33,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 194 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        }
    ]
}


# ------------------------------------------------------------------------------
# 4. TIMED QUIZ RENDER ENGINE (70 SECONDS / 1 MIN 10 SEC PER QUESTION)
# ------------------------------------------------------------------------------
active_part = st.session_state.current_part
part_questions = NEOPLASIA_33_QS[active_part]
total_q_in_part = len(part_questions)
current_idx = st.session_state.question_indices[active_part]

# Top Part Progress Summary
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Current Progress ({active_part}):**")
st.sidebar.progress(current_idx / total_q_in_part if total_q_in_part > 0 else 1.0)
st.sidebar.caption(f"Question {current_idx + 1} of {total_q_in_part} | Score: {st.session_state.scores[active_part]} / {current_idx if current_idx > 0 else 0}")

if current_idx >= total_q_in_part:
    st.balloons()
    st.header(f"🏆 Completed {active_part}!")
    part_score = st.session_state.scores[active_part]
    pct = (part_score / total_q_in_part) * 100 if total_q_in_part > 0 else 0
    
    col1, col2 = st.columns(2)
    col1.metric("Score for this Part", f"{part_score} / {total_q_in_part}")
    col2.metric("Percentage", f"{pct:.1f}%")
    
    if pct >= 80:
        st.success("🌟 Mastery Level Performance! Excellent grasp of Neoplasia Concepts.")
    elif pct >= 60:
        st.info("👍 Solid score! Review the explanations for incorrect questions to lock in key facts.")
    else:
        st.warning("📚 Keep practicing! Focus on high-yield Robbins Pathology figures and tables.")
        
    if st.button("Restart This Module 🔄"):
        st.session_state.question_indices[active_part] = 0
        st.session_state.scores[active_part] = 0
        st.rerun()
    st.stop()

# Active Question
q = part_questions[current_idx]
q_id = f"q_{q['id']}"

if f"start_time_{q_id}" not in st.session_state:
    st.session_state[f"start_time_{q_id}"] = time.time()

start_t = st.session_state[f"start_time_{q_id}"]
now_t = time.time()
elapsed = int(now_t - start_t)
remaining = max(0, 70 - elapsed)  # 1 min 10 sec limit

st.progress(current_idx / total_q_in_part, text=f"Progress: Question {current_idx + 1} of {total_q_in_part} ({active_part})")

col_q, col_timer = st.columns([3, 1])

with col_timer:
    if remaining > 30:
        border_color = "#28a745"  # Green
        bg_color = "#e8f5e9"
        text_color = "#1b5e20"
        icon = "⏳"
        label = "TIME REMAINING"
    elif remaining > 15:
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
    st.session_state.user_answers[q_id] = {
        "selected": "TIME EXPIRED",
        "correct": q["answer"],
        "is_correct": False
    }
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
            is_corr = (user_choice == q["answer"])
            if is_corr:
                st.session_state.scores[active_part] += 1
            
            st.session_state.user_answers[q_id] = {
                "selected": user_choice,
                "correct": q["answer"],
                "is_correct": is_corr
            }
            st.rerun()
        else:
            st.warning("Please select an option before submitting!")

if is_answered:
    user_record = st.session_state.user_answers.get(q_id, {})
    selected = user_record.get("selected", "")
    if selected == q["answer"]:
        st.success(f"🎉 **Correct!**\n\n**Rationale:** {q['explanation']}")
    elif selected == "TIME EXPIRED":
        st.error(f"⏰ **Time Expired (70s Limit Reached)!**\n\n**Correct Answer:** `{q['answer']}`\n\n**Rationale:** {q['explanation']}")
    else:
        st.error(f"❌ **Incorrect.** You selected `{selected}`.\n\n**Correct Answer:** `{q['answer']}`\n\n**Rationale:** {q['explanation']}")
        
    if col_next.button("Next Question ➡️", key=f"btn_next_{q_id}"):
        st.session_state.question_indices[active_part] += 1
        st.rerun()

if not is_answered and remaining > 0:
    time.sleep(1)
    st.rerun()

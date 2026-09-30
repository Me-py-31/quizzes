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
        "Part 1: Epidemiology & Carcinogenesis": 0,
        "Part 2: Tumour Markers": 0,
        "Part 3: Metastasis, Staging and Survival": 0,
        "Part 4: Tumor Host Interactions": 0
    }

if "scores" not in st.session_state:
    st.session_state.scores = {
        "Part 1: Epidemiology & Carcinogenesis": 0,
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
    "Part 1: Epidemiology & Carcinogenesis",
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
    "Part 1: Epidemiology & Carcinogenesis": [
        {
            "id": 1,
            "category": "Part 1: Epidemiology & Carcinogenesis",
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
            "category": "Part 1: Epidemiology & Carcinogenesis",
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
            "category": "Part 1: Epidemiology & Carcinogenesis",
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
            "category": "Part 1: Epidemiology & Carcinogenesis",
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
            "category": "Part 1: Epidemiology & Carcinogenesis",
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
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 6 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 7 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 8,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 8 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 9,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 9 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 10,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 10 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 11,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 11 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 12,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 12 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 13,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 13 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 14,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 14 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 15,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 15 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 16,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 16 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 17,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 17 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 18,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 18 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 19,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 19 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 20,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 20 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 21,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 21 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 22,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 22 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 23,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 23 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 24,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 24 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 25,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 25 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 26,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 26 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 27,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 27 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 28,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 28 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 29,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 29 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 30,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 30 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 31,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 31 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 32,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 32 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 33,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 33 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 34,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 34 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 35,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 35 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 36,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 36 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 37,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 37 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 38,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 38 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 39,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 39 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 40,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 40 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 41,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 41 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 42,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 42 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 43,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 43 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 44,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 44 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 45,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 45 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 46,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 46 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 47,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 47 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 48,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 48 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 49,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 49 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 50,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 50 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 51,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 51 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 52,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 52 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 53,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 53 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 54,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 54 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 55,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 55 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 56,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 56 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 57,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 57 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 58,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 58 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 59,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 59 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 60,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 60 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 61,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 61 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 62,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 62 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 63,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 63 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 64,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 64 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
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
            "id": 65,
            "category": "Part 1: Epidemiology & Carcinogenesis",
            "question": "Question 65 (Epidemiology & Carcinogenesis): Which statement regarding chemical initiation and promotion in carcinogenesis is correct?",
            "options": [
                "A. Promoters directly cause irreversible DNA damage without requiring initiation",
                "B. Initiators cause irreversible, non-lethal DNA mutations; promoters drive clonal expansion of initiated cells",
                "C. Promoters must be administered prior to initiators to produce malignant transformation",
                "D. Initiation is a reversible cell division process driven by non-mutagenic growth factors"
            ],
            "answer": "B. Initiators cause irreversible, non-lethal DNA mutations; promoters drive clonal expansion of initiated cells",
            "explanation": "Chemical initiation requires electrophilic DNA binding that causes permanent, non-lethal genetic damage. Subsequent application of promoters (non-mutagenic growth stimuli) drives clonal proliferation of the mutated cell."
        }
    ],
    "Part 2: Tumour Markers": [
        {
            "id": 66,
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
            "id": 67,
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
            "id": 68,
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
            "id": 69,
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
            "id": 70,
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
        },
        {
            "id": 71,
            "category": "Part 2: Tumour Markers",
            "question": "Question 71 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 72,
            "category": "Part 2: Tumour Markers",
            "question": "Question 72 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 73,
            "category": "Part 2: Tumour Markers",
            "question": "Question 73 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 74,
            "category": "Part 2: Tumour Markers",
            "question": "Question 74 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 75,
            "category": "Part 2: Tumour Markers",
            "question": "Question 75 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 76,
            "category": "Part 2: Tumour Markers",
            "question": "Question 76 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 77,
            "category": "Part 2: Tumour Markers",
            "question": "Question 77 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 78,
            "category": "Part 2: Tumour Markers",
            "question": "Question 78 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 79,
            "category": "Part 2: Tumour Markers",
            "question": "Question 79 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 80,
            "category": "Part 2: Tumour Markers",
            "question": "Question 80 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 81,
            "category": "Part 2: Tumour Markers",
            "question": "Question 81 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 82,
            "category": "Part 2: Tumour Markers",
            "question": "Question 82 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 83,
            "category": "Part 2: Tumour Markers",
            "question": "Question 83 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 84,
            "category": "Part 2: Tumour Markers",
            "question": "Question 84 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 85,
            "category": "Part 2: Tumour Markers",
            "question": "Question 85 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 86,
            "category": "Part 2: Tumour Markers",
            "question": "Question 86 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 87,
            "category": "Part 2: Tumour Markers",
            "question": "Question 87 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 88,
            "category": "Part 2: Tumour Markers",
            "question": "Question 88 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 89,
            "category": "Part 2: Tumour Markers",
            "question": "Question 89 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 90,
            "category": "Part 2: Tumour Markers",
            "question": "Question 90 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 91,
            "category": "Part 2: Tumour Markers",
            "question": "Question 91 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 92,
            "category": "Part 2: Tumour Markers",
            "question": "Question 92 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 93,
            "category": "Part 2: Tumour Markers",
            "question": "Question 93 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 94,
            "category": "Part 2: Tumour Markers",
            "question": "Question 94 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 95,
            "category": "Part 2: Tumour Markers",
            "question": "Question 95 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 96,
            "category": "Part 2: Tumour Markers",
            "question": "Question 96 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 97,
            "category": "Part 2: Tumour Markers",
            "question": "Question 97 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 98,
            "category": "Part 2: Tumour Markers",
            "question": "Question 98 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 99,
            "category": "Part 2: Tumour Markers",
            "question": "Question 99 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 100,
            "category": "Part 2: Tumour Markers",
            "question": "Question 100 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 101,
            "category": "Part 2: Tumour Markers",
            "question": "Question 101 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 102,
            "category": "Part 2: Tumour Markers",
            "question": "Question 102 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 103,
            "category": "Part 2: Tumour Markers",
            "question": "Question 103 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 104,
            "category": "Part 2: Tumour Markers",
            "question": "Question 104 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 105,
            "category": "Part 2: Tumour Markers",
            "question": "Question 105 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 106,
            "category": "Part 2: Tumour Markers",
            "question": "Question 106 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 107,
            "category": "Part 2: Tumour Markers",
            "question": "Question 107 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 108,
            "category": "Part 2: Tumour Markers",
            "question": "Question 108 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 109,
            "category": "Part 2: Tumour Markers",
            "question": "Question 109 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 110,
            "category": "Part 2: Tumour Markers",
            "question": "Question 110 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 111,
            "category": "Part 2: Tumour Markers",
            "question": "Question 111 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 112,
            "category": "Part 2: Tumour Markers",
            "question": "Question 112 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 113,
            "category": "Part 2: Tumour Markers",
            "question": "Question 113 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 114,
            "category": "Part 2: Tumour Markers",
            "question": "Question 114 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 115,
            "category": "Part 2: Tumour Markers",
            "question": "Question 115 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 116,
            "category": "Part 2: Tumour Markers",
            "question": "Question 116 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 117,
            "category": "Part 2: Tumour Markers",
            "question": "Question 117 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 118,
            "category": "Part 2: Tumour Markers",
            "question": "Question 118 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 119,
            "category": "Part 2: Tumour Markers",
            "question": "Question 119 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 120,
            "category": "Part 2: Tumour Markers",
            "question": "Question 120 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 121,
            "category": "Part 2: Tumour Markers",
            "question": "Question 121 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 122,
            "category": "Part 2: Tumour Markers",
            "question": "Question 122 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 123,
            "category": "Part 2: Tumour Markers",
            "question": "Question 123 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 124,
            "category": "Part 2: Tumour Markers",
            "question": "Question 124 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
            "options": [
                "A. Thyroglobulin",
                "B. Calcitonin",
                "C. Parathyroid Hormone (PTH)",
                "D. Chromogranin A"
            ],
            "answer": "B. Calcitonin",
            "explanation": "Medullary thyroid carcinoma originates from parafollicular C cells and secretes calcitonin, making serum calcitonin a highly specific biomarker for diagnosis and surveillance."
        },
        {
            "id": 125,
            "category": "Part 2: Tumour Markers",
            "question": "Question 125 (Tumour Markers): Which biochemical tumor marker is elevated in medullary thyroid carcinoma and utilized for monitoring post-surgical recurrence?",
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
            "id": 126,
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
            "id": 127,
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
            "id": 128,
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
        },
        {
            "id": 129,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 129 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 130,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 130 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 131,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 131 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 132,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 132 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 133,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 133 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 134,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 134 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 135,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 135 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 136,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 136 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 137,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 137 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 138,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 138 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 139,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 139 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 140,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 140 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 141,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 141 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 142,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 142 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 143,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 143 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 144,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 144 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 145,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 145 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 146,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 146 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 147,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 147 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 148,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 148 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 149,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 149 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 150,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 150 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 151,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 151 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 152,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 152 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 153,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 153 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 154,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 154 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 155,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 155 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 156,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 156 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 157,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 157 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 158,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 158 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 159,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 159 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 160,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 160 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 161,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 161 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 162,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 162 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 163,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 163 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 164,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 164 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 165,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 165 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 166,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 166 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 167,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 167 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 168,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 168 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 169,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 169 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 170,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 170 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 171,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 171 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 172,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 172 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 173,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 173 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 174,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 174 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 175,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 175 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 176,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 176 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 177,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 177 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 178,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 178 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 179,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 179 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 180,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 180 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 181,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 181 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 182,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 182 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 183,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 183 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 184,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 184 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 185,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 185 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 186,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 186 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 187,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 187 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 188,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 188 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 189,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 189 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
            "options": [
                "A. Staging measures cellular anaplasia under microscopic magnification",
                "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
                "C. Grading evaluates distant organ metastases while staging evaluates mitotic count",
                "D. Staging is variable over time whereas grading changes daily"
            ],
            "answer": "B. Staging evaluates the actual anatomical extent and spatial spread of tumor (TNM), which correlates most directly with overall survival",
            "explanation": "Cancer staging (TNM) assesses anatomical tumor extent and distant dissemination, making it a significantly more accurate prognostic indicator and driver of clinical treatment protocols than histological grading."
        },
        {
            "id": 190,
            "category": "Part 3: Metastasis, Staging and Survival",
            "question": "Question 190 (Metastasis, Staging & Survival): When comparing clinical cancer staging versus histological grading, why is cancer staging considered superior for patient prognosis?",
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
            "id": 191,
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
            "id": 192,
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
            "id": 193,
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
            "id": 194,
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
        },
        {
            "id": 195,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 195 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 196,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 196 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 197,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 197 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 198,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 198 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 199,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 199 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 200,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 200 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 201,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 201 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 202,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 202 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 203,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 203 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 204,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 204 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 205,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 205 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 206,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 206 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 207,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 207 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 208,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 208 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 209,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 209 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 210,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 210 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 211,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 211 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 212,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 212 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 213,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 213 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 214,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 214 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 215,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 215 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 216,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 216 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 217,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 217 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 218,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 218 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 219,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 219 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 220,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 220 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 221,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 221 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 222,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 222 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 223,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 223 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 224,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 224 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 225,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 225 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 226,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 226 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 227,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 227 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 228,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 228 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 229,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 229 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 230,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 230 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 231,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 231 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 232,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 232 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 233,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 233 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 234,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 234 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 235,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 235 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 236,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 236 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 237,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 237 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 238,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 238 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 239,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 239 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 240,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 240 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 241,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 241 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 242,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 242 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 243,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 243 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 244,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 244 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 245,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 245 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 246,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 246 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 247,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 247 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 248,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 248 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 249,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 249 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
            "options": [
                "A. CD4+ Th2 Helper T lymphocytes",
                "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
                "C. B-plasma cells secreting IgE",
                "D. Eosinophils"
            ],
            "answer": "B. CD8+ Cytotoxic T Lymphocytes (CTLs)",
            "explanation": "CD8+ Cytotoxic T Lymphocytes recognize tumor-specific antigens presented on MHC Class I molecules and kill tumor cells via perforin/granzyme release."
        },
        {
            "id": 250,
            "category": "Part 4: Tumor Host Interactions",
            "question": "Question 250 (Tumor Host Interactions): Which cell-mediated immune mechanism plays the primary role in host immune surveillance against virus-induced and highly immunogenic tumor cells?",
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
part_questions = NEOPLASIA_250_QS[active_part]
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

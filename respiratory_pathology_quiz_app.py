import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Respiratory Pathology 450 MCQ Board Review",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- EMBEDDED QUIZ DATASET ---
QUIZ_DATA = [
  {
    "id": "urt_1",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q1): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_2",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q2): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_3",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q3): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_4",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q4): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_5",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q5): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_6",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q6): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_7",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q7): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_8",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q8): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_9",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q9): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_10",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q10): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_11",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q11): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_12",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q12): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_13",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q13): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_14",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q14): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_15",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q15): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_16",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q16): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_17",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q17): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_18",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q18): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_19",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q19): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_20",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q20): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_21",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q21): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_22",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q22): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_23",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q23): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_24",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q24): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_25",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q25): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_26",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q26): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_27",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q27): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_28",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q28): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_29",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q29): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_30",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q30): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_31",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q31): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_32",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q32): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_33",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q33): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_34",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q34): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_35",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q35): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_36",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q36): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_37",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q37): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_38",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q38): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_39",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q39): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_40",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q40): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_41",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q41): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_42",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q42): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_43",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q43): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_44",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q44): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_45",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q45): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_46",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q46): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_47",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q47): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_48",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q48): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_49",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q49): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_50",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q50): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_51",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q51): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_52",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q52): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_53",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q53): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_54",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q54): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_55",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q55): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_56",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q56): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_57",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q57): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_58",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q58): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_59",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q59): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_60",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q60): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_61",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q61): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_62",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q62): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_63",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q63): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_64",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q64): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_65",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q65): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_66",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q66): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_67",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q67): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_68",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q68): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_69",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q69): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_70",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q70): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_71",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q71): Which upper respiratory tract structure is lined by pseudostratified ciliated columnar epithelium with goblet cells?",
    "options": [
      "Oropharynx",
      "Nasal cavity and nasopharynx",
      "True vocal cords",
      "Laryngopharynx",
      "Anterior epiglottis"
    ],
    "answer": 1,
    "explanation": "The nasal cavity and nasopharynx are lined by respiratory epithelium (pseudostratified ciliated columnar epithelium).",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_72",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q72): An 8-year-old child presents with high fever, inspiratory stridor, drooling, and severe respiratory distress. Laryngoscopy reveals a cherry-red, swollen epiglottis. What is the most likely pathogen?",
    "options": [
      "Haemophilus influenzae type b",
      "Epstein-Barr Virus",
      "Streptococcus pneumoniae",
      "Corynebacterium diphtheriae",
      "Rhinovirus"
    ],
    "answer": 0,
    "explanation": "Acute epiglottitis is classically caused by Haemophilus influenzae type b in unimmunized children.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_73",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "URT Pathology (Q73): Nasopharyngeal carcinoma is strongly associated with which infectious agent?",
    "options": [
      "Human Papillomavirus type 16",
      "Epstein-Barr Virus (EBV)",
      "Cytomegalovirus",
      "Herpes Simplex Virus type 1",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Undifferentiated nasopharyngeal carcinoma has a strong epidemiological link with EBV infection.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_74",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "URT Pathology (Q74): Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "urt_75",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "URT Pathology (Q75): A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Singer's nodule (vocal cord polyp)",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain.",
    "citation": "Robbins Review / URT Pathology"
  },
  {
    "id": "lrt_1",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q1): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_2",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q2): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_3",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q3): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_4",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q4): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_5",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q5): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_6",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q6): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_7",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q7): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_8",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q8): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_9",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q9): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_10",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q10): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_11",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q11): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_12",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q12): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_13",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q13): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_14",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q14): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_15",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q15): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_16",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q16): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_17",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q17): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_18",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q18): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_19",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q19): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_20",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q20): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_21",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q21): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_22",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q22): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_23",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q23): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_24",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q24): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_25",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q25): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_26",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q26): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_27",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q27): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_28",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q28): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_29",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q29): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_30",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q30): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_31",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q31): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_32",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q32): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_33",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q33): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_34",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q34): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_35",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q35): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_36",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q36): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_37",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q37): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_38",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q38): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_39",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q39): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_40",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q40): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_41",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q41): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_42",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q42): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_43",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q43): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_44",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q44): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_45",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q45): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_46",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q46): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_47",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q47): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_48",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q48): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_49",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q49): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_50",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q50): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_51",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q51): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_52",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q52): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_53",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q53): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_54",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q54): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_55",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q55): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_56",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q56): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_57",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q57): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_58",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q58): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_59",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q59): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_60",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q60): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_61",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q61): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_62",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q62): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_63",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q63): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_64",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q64): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_65",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q65): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_66",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q66): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_67",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q67): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_68",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q68): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_69",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q69): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_70",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q70): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_71",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q71): Which stage of lobar pneumonia is characterized by alveolar spaces packed with neutrophils, red blood cells, and fibrin, giving the lung a liver-like consistency?",
    "options": [
      "Stage of Congestion",
      "Stage of Red Hepatization",
      "Stage of Grey Hepatization",
      "Stage of Resolution",
      "Stage of Fibrosis"
    ],
    "answer": 1,
    "explanation": "Red hepatization involves massive extravasation of RBCs, neutrophils, and fibrin into alveolar spaces.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_72",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q72): A 55-year-old chronic smoker presents with chronic productive cough lasting for at least 3 consecutive months in 2 consecutive years. What is the diagnosis?",
    "options": [
      "Centriacinar Emphysema",
      "Chronic Bronchitis",
      "Bronchiectasis",
      "Atopic Asthma",
      "Idiopathic Pulmonary Fibrosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis is clinically defined as a persistent productive cough for at least 3 consecutive months in at least 2 consecutive years.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_73",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "LRT Pathology (Q73): Which morphological feature is characteristic of bronchial asthma in sputum microscopy?",
    "options": [
      "Ferruginous bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Schaumann bodies",
      "Ghon complexes",
      "Negri bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs) and Charcot-Leyden crystals (crystallized eosinophil proteins) are hallmarks of asthma.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_74",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "LRT Pathology (Q74): Panacinar emphysema is classically associated with a genetic deficiency of:",
    "options": [
      "Alpha-1 Antitrypsin",
      "CFTR protein",
      "BMPR2 receptor",
      "Surfactant Protein B",
      "Dynein heavy chain"
    ],
    "answer": 0,
    "explanation": "Alpha-1 antitrypsin deficiency leads to uninhibited elastase activity resulting in panacinar emphysema, especially in lower lobes.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "lrt_75",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "LRT Pathology (Q75): Kartagener syndrome consists of bronchiectasis, primary ciliary dyskinesia, chronic sinusitis, and:",
    "options": [
      "Situs inversus",
      "Cor pulmonale",
      "Pulmonary hypertension",
      "Pleural effusion",
      "Hypercalcemia"
    ],
    "answer": 0,
    "explanation": "Kartagener syndrome triad: situs inversus, chronic sinusitis/bronchiectasis, and male infertility due to defective dynein arms.",
    "citation": "Robbins Review / LRT Pathology"
  },
  {
    "id": "tum_1",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q1): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_2",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q2): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_3",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q3): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_4",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q4): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_5",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q5): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_6",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q6): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_7",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q7): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_8",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q8): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_9",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q9): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_10",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q10): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_11",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q11): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_12",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q12): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_13",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q13): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_14",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q14): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_15",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q15): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_16",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q16): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_17",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q17): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_18",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q18): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_19",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q19): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_20",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q20): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_21",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q21): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_22",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q22): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_23",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q23): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_24",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q24): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_25",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q25): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_26",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q26): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_27",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q27): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_28",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q28): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_29",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q29): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_30",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q30): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_31",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q31): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_32",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q32): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_33",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q33): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_34",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q34): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_35",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q35): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_36",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q36): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_37",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q37): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_38",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q38): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_39",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q39): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_40",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q40): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_41",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q41): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_42",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q42): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_43",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q43): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_44",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q44): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_45",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q45): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_46",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q46): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_47",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q47): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_48",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q48): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_49",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q49): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_50",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q50): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_51",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q51): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_52",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q52): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_53",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q53): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_54",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q54): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_55",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q55): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_56",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q56): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_57",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q57): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_58",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q58): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_59",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q59): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_60",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q60): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_61",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q61): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_62",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q62): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_63",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q63): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_64",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q64): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_65",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q65): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_66",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q66): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_67",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q67): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_68",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q68): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_69",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q69): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_70",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q70): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_71",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q71): Which lung malignancy is most strongly linked to cigarette smoking and characteristically arises centrally in major bronchi with keratin pearl formation?",
    "options": [
      "Adenocarcinoma",
      "Squamous Cell Carcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Bronchial Carcinoid"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma arises centrally in major bronchi, is strongly smoking-associated, and shows keratin pearls and intercellular bridges.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_72",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q72): A central lung mass in a heavy smoker is found to be composed of small round/oval blue cells with dark nuclei, scant cytoplasm, and nuclear molding. What paraneoplastic syndrome is most associated with this tumor?",
    "options": [
      "Hypercalcemia due to PTHrp",
      "SIADH (Hyponatremia)",
      "Hyperthyroidism",
      "Cushingoid state due to ACTH",
      "Hypogammaglobulinemia"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma (neuroendocrine origin) frequently produces SIADH or ectopic ACTH.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_73",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Lung Tumours Pathology (Q73): Which subtype of lung cancer is currently the most common primary lung malignancy in non-smokers and females, typically located peripherally?",
    "options": [
      "Squamous Cell Carcinoma",
      "Adenocarcinoma",
      "Small Cell Carcinoma",
      "Large Cell Carcinoma",
      "Mesothelioma"
    ],
    "answer": 1,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, particularly in non-smokers and peripheral lung regions.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_74",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Lung Tumours Pathology (Q74): A apical lung tumor causing ipsilateral ptosis, miosis, anhidrosis, and arm pain (Horner syndrome & brachial plexus invasion) is known as a:",
    "options": [
      "Krukenberg tumor",
      "Pancoast tumor (Superior sulcus tumor)",
      "Brenner tumor",
      "Warthin tumor",
      "Wilms tumor"
    ],
    "answer": 1,
    "explanation": "Pancoast tumors at the apical sulcus invade cervical sympathetic ganglia (Horner syndrome) and brachial plexus.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "tum_75",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Lung Tumours Pathology (Q75): Which genetic mutation is frequently observed in lung adenocarcinoma, especially in non-smoking Asian females, rendering them responsive to tyrosine kinase inhibitors?",
    "options": [
      "EGFR mutation",
      "KRAS mutation",
      "TP53 mutation",
      "RB1 mutation",
      "c-KIT mutation"
    ],
    "answer": 0,
    "explanation": "EGFR mutations in adenocarcinoma predict favorable response to EGFR-targeted TKIs like erlotinib/gefitinib.",
    "citation": "Robbins Review / Lung Tumours"
  },
  {
    "id": "inf_1",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q1): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_2",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q2): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_3",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q3): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_4",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q4): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_5",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q5): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_6",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q6): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_7",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q7): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_8",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q8): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_9",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q9): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_10",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q10): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_11",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q11): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_12",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q12): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_13",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q13): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_14",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q14): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_15",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q15): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_16",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q16): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_17",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q17): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_18",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q18): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_19",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q19): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_20",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q20): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_21",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q21): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_22",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q22): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_23",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q23): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_24",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q24): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_25",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q25): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_26",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q26): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_27",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q27): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_28",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q28): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_29",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q29): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_30",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q30): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_31",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q31): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_32",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q32): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_33",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q33): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_34",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q34): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_35",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q35): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_36",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q36): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_37",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q37): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_38",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q38): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_39",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q39): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_40",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q40): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_41",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q41): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_42",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q42): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_43",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q43): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_44",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q44): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_45",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q45): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_46",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q46): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_47",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q47): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_48",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q48): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_49",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q49): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_50",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q50): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_51",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q51): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_52",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q52): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_53",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q53): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_54",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q54): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_55",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q55): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_56",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q56): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_57",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q57): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_58",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q58): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_59",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q59): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_60",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q60): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_61",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q61): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_62",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q62): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_63",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q63): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_64",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q64): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_65",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q65): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_66",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q66): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_67",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q67): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_68",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q68): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_69",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q69): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_70",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q70): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_71",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q71): Eggshell calcification of hilar lymph nodes on chest radiograph is a classic diagnostic feature of which pneumoconiosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis classically presents with delicate eggshell calcifications in hilar lymph nodes.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_72",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Infiltrative Lung Disease (Q72): Ferruginous bodies (golden-brown beaded fibers coated with iron-protein complexes) in sputum or lung tissue are characteristic of:",
    "options": [
      "Silicosis",
      "Asbestosis",
      "Anthracosis",
      "Berylliosis",
      "Byssinosis"
    ],
    "answer": 1,
    "explanation": "Asbestos bodies are ferruginous bodies formed when alveolar macrophages engulf inhaled asbestos fibers.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_73",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q73): Which occupational exposure is associated with non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Silica dust",
      "Beryllium exposure",
      "Coal dust",
      "Cotton dust (Byssinosis)",
      "Sugar cane fiber (Bagassosis)"
    ],
    "answer": 1,
    "explanation": "Berylliosis induces cell-mediated hypersensitivity resulting in non-caseating pulmonary granulomas identical to sarcoidosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_74",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Infiltrative Lung Disease (Q74): Idiopathic Pulmonary Fibrosis (IPF) characteristically exhibits which histological pattern on lung biopsy?",
    "options": [
      "Usual Interstitial Pneumonia (UIP) pattern with honeycomb lung",
      "Non-Specific Interstitial Pneumonia (NSIP) pattern",
      "Desquamative Interstitial Pneumonia (DIP) pattern",
      "Organizing Pneumonia pattern",
      "Granulomatous pattern"
    ],
    "answer": 0,
    "explanation": "IPF is defined by the histological UIP pattern featuring temporal heterogeneity, fibroblastic foci, and honeycomb fibrosis.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "inf_75",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Infiltrative Lung Disease (Q75): Farmer's lung is an example of Hypersensitivity Pneumonitis caused by inhalation of:",
    "options": [
      "Thermaphilic actinomycetes in moldy hay",
      "Cotton fibers in textile mills",
      "Sugar cane bagasse",
      "Bird droppings",
      "Beryllium dust"
    ],
    "answer": 0,
    "explanation": "Farmer's lung is an immunologically mediated reaction to Saccharopolyspora rectivirgula in moldy hay.",
    "citation": "Robbins Review / Infiltrative Lung Diseases"
  },
  {
    "id": "ple_1",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q1): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_2",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q2): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_3",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q3): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_4",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q4): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_5",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q5): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_6",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q6): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_7",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q7): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_8",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q8): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_9",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q9): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_10",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q10): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_11",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q11): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_12",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q12): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_13",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q13): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_14",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q14): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_15",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q15): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_16",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q16): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_17",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q17): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_18",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q18): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_19",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q19): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_20",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q20): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_21",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q21): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_22",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q22): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_23",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q23): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_24",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q24): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_25",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q25): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_26",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q26): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_27",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q27): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_28",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q28): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_29",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q29): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_30",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q30): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_31",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q31): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_32",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q32): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_33",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q33): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_34",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q34): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_35",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q35): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_36",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q36): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_37",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q37): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_38",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q38): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_39",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q39): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_40",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q40): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_41",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q41): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_42",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q42): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_43",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q43): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_44",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q44): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_45",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q45): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_46",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q46): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_47",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q47): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_48",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q48): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_49",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q49): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_50",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q50): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_51",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q51): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_52",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q52): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_53",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q53): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_54",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q54): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_55",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q55): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_56",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q56): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_57",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q57): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_58",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q58): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_59",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q59): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_60",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q60): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_61",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q61): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_62",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q62): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_63",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q63): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_64",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q64): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_65",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q65): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_66",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q66): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_67",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q67): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_68",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q68): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_69",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q69): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_70",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q70): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_71",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Diseases of the Pleura (Q71): According to Light's criteria, a pleural effusion is classified as an EXUDATE if:",
    "options": [
      "Pleural fluid protein to serum protein ratio > 0.5",
      "Pleural fluid LDH to serum LDH ratio < 0.6",
      "Pleural fluid LDH < 2/3 upper limit of normal serum LDH",
      "Pleural fluid protein < 2.5 g/dL",
      "Pleural fluid cell count < 100 cells/uL"
    ],
    "answer": 0,
    "explanation": "Light's criteria for exudate: Protein ratio >0.5, LDH ratio >0.6, or fluid LDH >2/3 upper limit of normal serum LDH.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_72",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q72): A 68-year-old male with prior asbestos exposure presents with chest pain, dyspnea, pleural thickening, and a large bloody pleural effusion. Tumor cells are positive for Calretinin and WT-1. What is the diagnosis?",
    "options": [
      "Pleural Adenocarcinoma",
      "Malignant Mesothelioma",
      "Solitary Fibrous Tumor",
      "Squamous Cell Ca Metastasis",
      "Pleural Lymphoma"
    ],
    "answer": 1,
    "explanation": "Malignant Mesothelioma arises from mesothelial cells, strongly linked to asbestos, positive for Calretinin and WT-1.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_73",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q73): A purulent bacterial infection of the pleural cavity leading to creamy pus accumulation is called:",
    "options": [
      "Hydrothorax",
      "Hemothorax",
      "Empyema thoracis",
      "Chylothorax",
      "Pneumothorax"
    ],
    "answer": 2,
    "explanation": "Empyema thoracis is a suppurative pleural effusion containing gross pus and neutrophils.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_74",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Diseases of the Pleura (Q74): Milky white pleural fluid rich in triglycerides due to thoracic duct obstruction or trauma is termed:",
    "options": [
      "Chylothorax",
      "Pseudochylothorax",
      "Empyema",
      "Hydrothorax",
      "Hemothorax"
    ],
    "answer": 0,
    "explanation": "Chylothorax is milky pleural fluid containing chylomicrons and triglycerides from thoracic duct rupture.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "ple_75",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Diseases of the Pleura (Q75): A tall thin 20-year-old male experiences sudden sharp chest pain and dyspnea while resting. Chest X-ray shows air in the pleural space with lung collapse. What is the cause?",
    "options": [
      "Rupture of subpleural paraseptal emphysematous blebs",
      "Thoracic trauma",
      "Asbestos exposure",
      "Aspiration pneumonia",
      "Surfactant deficiency"
    ],
    "answer": 0,
    "explanation": "Primary spontaneous pneumothorax in young tall males occurs due to rupture of subpleural apical blebs.",
    "citation": "Robbins Review / Diseases of Pleura"
  },
  {
    "id": "stb_1",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q1): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_2",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q2): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_3",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q3): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_4",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q4): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_5",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q5): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_6",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q6): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_7",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q7): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_8",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q8): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_9",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q9): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_10",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q10): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_11",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q11): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_12",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q12): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_13",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q13): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_14",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q14): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_15",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q15): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_16",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q16): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_17",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q17): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_18",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q18): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_19",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q19): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_20",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q20): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_21",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q21): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_22",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q22): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_23",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q23): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_24",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q24): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_25",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q25): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_26",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q26): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_27",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q27): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_28",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q28): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_29",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q29): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_30",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q30): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_31",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q31): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_32",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q32): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_33",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q33): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_34",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q34): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_35",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q35): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_36",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q36): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_37",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q37): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_38",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q38): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_39",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q39): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_40",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q40): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_41",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q41): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_42",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q42): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_43",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q43): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_44",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q44): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_45",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q45): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_46",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q46): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_47",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q47): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_48",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q48): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_49",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q49): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_50",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q50): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_51",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q51): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_52",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q52): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_53",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q53): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_54",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q54): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_55",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q55): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_56",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q56): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_57",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q57): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_58",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q58): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_59",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q59): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_60",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q60): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_61",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q61): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_62",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q62): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_63",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q63): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_64",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q64): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_65",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q65): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_66",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q66): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_67",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q67): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_68",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q68): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_69",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q69): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_70",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q70): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_71",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Sarcoidosis & TB Pathology (Q71): In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_72",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q72): When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_73",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q73): Secondary (Reactivation) Pulmonary Tuberculosis classically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_74",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q74): The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells.",
    "citation": "Robbins Review / Sarcoidosis & TB"
  },
  {
    "id": "stb_75",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Sarcoidosis & TB Pathology (Q75): Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions).",
    "citation": "Robbins Review / Sarcoidosis & TB"
  }
]

# --- CATEGORY DEFINITIONS ---
CATEGORIES = [
    "URT Diseases",
    "LRT Diseases",
    "Lung Tumours",
    "Infiltrative Lung Diseases",
    "Diseases of the Pleura",
    "Sarcoidosis & TB"
]

CATEGORY_ICONS = {
    "URT Diseases": "👃",
    "LRT Diseases": "🫁",
    "Lung Tumours": "🎗️",
    "Infiltrative Lung Diseases": "🌫️",
    "Diseases of the Pleura": "🫁",
    "Sarcoidosis & TB": "🔬"
}

# --- INITIALIZE SESSION STATE ---
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}  # q_id -> selected_option_index

if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = set()    # set of q_ids

if "active_category" not in st.session_state:
    st.session_state.active_category = CATEGORIES[0]

if "active_indices" not in st.session_state:
    st.session_state.active_indices = {cat: 0 for cat in CATEGORIES}

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

# --- CUSTOM CSS STYLING ---
st.markdown("""
<style>
    /* Global App Background */
    .stApp {
        background-color: #000000 !important;
        color: #f8fafc !important;
    }

    /* Main Container Padding & Background */
    [data-testid="stMain"], .stMainBlockContainer {
        background-color: #000000 !important;
        color: #f8fafc !important;
    }

    /* Main Area Headers & Text */
    [data-testid="stMain"] h1, [data-testid="stMain"] h2, [data-testid="stMain"] h3, 
    [data-testid="stMain"] h4, [data-testid="stMain"] h5, [data-testid="stMain"] h6,
    [data-testid="stMain"] p, [data-testid="stMain"] span, [data-testid="stMain"] label,
    [data-testid="stMain"] li, [data-testid="stMain"] ol, [data-testid="stMain"] ul,
    [data-testid="stMain"] div, [data-testid="stMain"] b, [data-testid="stMain"] strong {
        color: #ffffff;
    }

    
    /* Ensure markdown container background never overrides dark boxes */
    [data-testid="stMarkdownContainer"], 
    [data-testid="stMarkdownContainer"] > div {
        background-color: transparent !important;
    }

    /* Titles */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #38bdf8 !important;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #94a3b8 !important;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    /* Welcome Card Styling */
    .welcome-card {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 2rem 1.5rem !important;
        margin: 1.5rem 0 !important;
        text-align: center !important;
    }
    .welcome-card h2 {
        color: #38bdf8 !important;
        margin-bottom: 1rem !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
    }
    .welcome-card p {
        color: #e2e8f0 !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        max-width: 650px !important;
        margin: 0 auto 1.5rem auto !important;
    }

    /* Steps Box Inside Welcome Card */
    .steps-box {
        background-color: #1e293b !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 10px !important;
        padding: 1.5rem !important;
        text-align: left !important;
        max-width: 650px !important;
        margin: 0 auto !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
    }
    .steps-box h4 {
        color: #38bdf8 !important;
        margin-top: 0 !important;
        margin-bottom: 0.75rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    .steps-box ol {
        color: #ffffff !important;
        font-size: 0.98rem !important;
        margin-bottom: 0 !important;
        padding-left: 1.3rem !important;
        line-height: 1.7 !important;
    }
    .steps-box li {
        color: #ffffff !important;
        margin-bottom: 0.5rem !important;
    }
    .steps-box li b, .steps-box li strong {
        color: #7dd3fc !important;
    }

    /* Question Card */
    .q-card {
        background-color: #111827 !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        border: 1px solid #374151 !important;
        margin-bottom: 1rem !important;
    }
    .q-card h3 {
        color: #f8fafc !important;
    }

    /* Question Type Badges */
    .q-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .badge-vignette { background-color: #0284c7 !important; color: #ffffff !important; }
    .badge-exception { background-color: #e11d48 !important; color: #ffffff !important; }
    .badge-conceptual { background-color: #7c3aed !important; color: #ffffff !important; }
    .badge-recall { background-color: #059669 !important; color: #ffffff !important; }

    /* PERMANENT VISIBILITY FOR BUTTONS */
    div.stButton > button {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1.5px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.6) !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        border-color: #7dd3fc !important;
    }

    /* Primary Buttons (Begin Quiz, Submit) */
    div.stButton > button[kind="primary"] {
        background-color: #0284c7 !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #0369a1 !important;
        border-color: #7dd3fc !important;
    }

    /* SIDEBAR STYLING - LIGHT BACKGROUND WITH CRISP BLACK TEXT */
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #0f172a !important;
    }
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: #e2e8f0 !important;
        color: #0f172a !important;
        border: 1px solid #94a3b8 !important;
    }
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #cbd5e1 !important;
        color: #0f172a !important;
    }

    /* Selectbox, Radio & File Uploader */
    div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        border-color: #374151 !important;
        color: #ffffff !important;
    }
    div[role="listbox"] {
        background-color: #111827 !important;
        color: #ffffff !important;
    }
    [data-testid="stFileUploader"] {
        background-color: #111827 !important;
        border: 1px dashed #38bdf8 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR & GLOBAL METRICS ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/lungs.png", width=70)
    st.title("🫁 450 MCQ Review")
    st.caption("Pathology Board Prep • Robbins Review & Selected Banks")
    st.divider()

    total_q = len(QUIZ_DATA)
    answered_q = len(st.session_state.user_answers)
    
    correct_cnt = 0
    for q_id, sel in st.session_state.user_answers.items():
        q_obj = next((q for q in QUIZ_DATA if q["id"] == q_id), None)
        if q_obj and sel == q_obj["answer"]:
            correct_cnt += 1
            
    accuracy = (correct_cnt / answered_q * 100) if answered_q > 0 else 0.0

    st.subheader("📊 Session Statistics")
    st.metric("Total Progress", f"{answered_q} / {total_q}", f"{(answered_q/total_q)*100:.1f}%")
    st.progress(answered_q / total_q)

    col_acc, col_bm = st.columns(2)
    with col_acc:
        st.metric("Accuracy", f"{accuracy:.1f}%")
    with col_bm:
        st.metric("Bookmarked", f"{len(st.session_state.bookmarks)}")

    st.divider()
    st.markdown("#### 💾 Progress Data")
    
    # Download JSON
    export_data = {
        "user_answers": st.session_state.user_answers,
        "bookmarks": list(st.session_state.bookmarks),
        "total_questions": total_q,
        "answered": answered_q,
        "correct": correct_cnt,
        "accuracy": round(accuracy, 2)
    }
    st.download_button(
        label="📥 Download Saved Progress",
        data=json.dumps(export_data, indent=2),
        file_name="respiratory_pathology_results.json",
        mime="application/json",
        use_container_width=True
    )

    # Upload / Restore JSON
    uploaded_file = st.file_uploader("📤 Restore Saved Progress", type=["json"], key="json_uploader_sidebar")
    if uploaded_file is not None:
        try:
            imported_data = json.load(uploaded_file)
            if "user_answers" in imported_data:
                st.session_state.user_answers = imported_data["user_answers"]
                if "bookmarks" in imported_data:
                    st.session_state.bookmarks = set(imported_data["bookmarks"])
                st.success("✅ Progress restored successfully!")
                st.rerun()
        except Exception:
            st.error("⚠️ Invalid progress file.")

    # Reset Progress
    if st.button("🔄 Reset All Progress", type="secondary", use_container_width=True):
        st.session_state.user_answers = {}
        st.session_state.bookmarks = set()
        st.rerun()

# --- MAIN INTERFACE RENDERING ---
if not st.session_state.get("quiz_started", False):
    st.markdown('<div class="main-title">Respiratory Pathology Board Review</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Interactive 450 High-Yield Question Bank • Robbins Review & Selected Banks</div>', unsafe_allow_html=True)
    
    st.markdown('''
    <div style="background-color: #0f172a !important; border: 1px solid #1e293b !important; border-radius: 12px !important; padding: 2rem 1.5rem !important; margin: 1.5rem 0 !important; text-align: center !important;">
        <h2 style="color: #38bdf8 !important; background-color: transparent !important; margin-bottom: 1rem !important; font-size: 1.6rem !important; font-weight: 800 !important;">Welcome to the 450-Question Board Exam Prep</h2>
        <p style="color: #f8fafc !important; background-color: transparent !important; font-size: 1.05rem !important; line-height: 1.6 !important; max-width: 650px !important; margin: 0 auto 1.5rem auto !important;">
            Test your clinical reasoning across 6 core categories in Respiratory Pathology. Features include a 1-minute question timer, auto-advance, instant pathological rationale, and session progress saving.
        </p>
        <div style="display: flex; justify-content: center; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 1.5rem; background-color: transparent !important;">
            <span style="background-color: #1e293b !important; color: #38bdf8 !important; padding: 0.5rem 1rem !important; border-radius: 9999px !important; font-weight: 600 !important; font-size: 0.9rem !important;">⏱️ 1-Min Limit per Question</span>
            <span style="background-color: #1e293b !important; color: #38bdf8 !important; padding: 0.5rem 1rem !important; border-radius: 9999px !important; font-weight: 600 !important; font-size: 0.9rem !important;">📚 6 Core Pathology Categories</span>
            <span style="background-color: #1e293b !important; color: #38bdf8 !important; padding: 0.5rem 1rem !important; border-radius: 9999px !important; font-weight: 600 !important; font-size: 0.9rem !important;">📊 Saved Progress & Analytics</span>
        </div>
        
        <!-- HOW TO SAVE PROGRESS BOX: SOLID DARK NAVY/BLACK BACKGROUND WITH CRISP WHITE TEXT -->
        <div style="background-color: #020617 !important; border: 2px solid #38bdf8 !important; border-radius: 10px !important; padding: 1.5rem !important; text-align: left !important; max-width: 650px !important; margin: 0 auto !important; box-shadow: 0 4px 14px rgba(0, 0, 0, 0.9) !important;">
            <h4 style="color: #38bdf8 !important; background-color: #020617 !important; margin-top: 0 !important; margin-bottom: 0.75rem !important; font-weight: 700 !important; font-size: 1.1rem !important;">💾 How to Save and Restore Your Progress:</h4>
            <ol style="color: #f8fafc !important; background-color: #020617 !important; font-size: 0.98rem !important; margin-bottom: 0 !important; padding-left: 1.3rem !important; line-height: 1.7 !important;">
                <li style="color: #f8fafc !important; background-color: #020617 !important; margin-bottom: 0.6rem !important;">
                    <b style="color: #38bdf8 !important; background-color: #020617 !important;">Automatic In-Session Saving:</b> 
                    <span style="color: #f8fafc !important; background-color: #020617 !important;">Your selected answers and bookmarks save automatically as you move through questions.</span>
                </li>
                <li style="color: #f8fafc !important; background-color: #020617 !important; margin-bottom: 0.6rem !important;">
                    <b style="color: #38bdf8 !important; background-color: #020617 !important;">Saving to Your Device:</b> 
                    <span style="color: #f8fafc !important; background-color: #020617 !important;">At the end of a study session, click <b style="color: #38bdf8 !important; background-color: #020617 !important;">"📥 Download Saved Progress"</b> in the left Sidebar or <b style="color: #38bdf8 !important; background-color: #020617 !important;">📊 Analytics</b> tab to save your progress file to your phone, tablet, or computer.</span>
                </li>
                <li style="color: #f8fafc !important; background-color: #020617 !important; margin-bottom: 0.2rem !important;">
                    <b style="color: #38bdf8 !important; background-color: #020617 !important;">Restoring Your Study Progress:</b> 
                    <span style="color: #f8fafc !important; background-color: #020617 !important;">Whenever you open the quiz again on any device, click <b style="color: #38bdf8 !important; background-color: #020617 !important;">"📤 Restore Saved Progress"</b> in the left Sidebar to upload your saved file and continue right where you left off!</span>
                </li>
            </ol>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
    with col_s2:
        if st.button("🚀 Begin Quiz", type="primary", key="begin_quiz_btn"):
            st.session_state.quiz_started = True
            st.rerun()
else:
    # --- MAIN INTERFACE HEADER ---
    st.markdown('<div class="main-title">Respiratory Pathology Board Review</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Interactive 450 High-Yield Question Bank with 1-Min Time Limit & Instant Rationale</div>', unsafe_allow_html=True)

    # --- CATEGORY TABS ---
    tab_names = [f"{CATEGORY_ICONS[cat]} {cat}" for cat in CATEGORIES] + ["📊 Analytics & Review"]
    tabs = st.tabs(tab_names)

    # Callbacks for Navigation
    def go_prev_cb(cat_name, prev_tuple):
        if prev_tuple:
            select_key = f"select_{cat_name}"
            st.session_state[select_key] = prev_tuple
            st.session_state.active_indices[cat_name] = prev_tuple[0]

    def go_next_cb(cat_name, next_tuple):
        if next_tuple:
            select_key = f"select_{cat_name}"
            st.session_state[select_key] = next_tuple
            st.session_state.active_indices[cat_name] = next_tuple[0]

    def toggle_bm_cb(q_id_to_bm):
        if q_id_to_bm in st.session_state.bookmarks:
            st.session_state.bookmarks.remove(q_id_to_bm)
        else:
            st.session_state.bookmarks.add(q_id_to_bm)

    def render_category_quiz(category_name, tab_idx):
        cat_questions = [q for q in QUIZ_DATA if q["category"] == category_name]
        num_cat_q = len(cat_questions)

        # Navigation Header
        col_nav, col_filter = st.columns([3, 2])
        
        with col_filter:
            q_filter = st.selectbox(
                "Filter Questions:",
                ["All Questions", "Unanswered", "Incorrect", "Bookmarked"],
                key=f"filter_{category_name}"
            )

        # Apply filter
        filtered_questions = []
        for idx, q in enumerate(cat_questions):
            q_id = q["id"]
            is_answered = q_id in st.session_state.user_answers
            user_sel = st.session_state.user_answers.get(q_id)
            is_correct = is_answered and (user_sel == q["answer"])
            is_bookmarked = q_id in st.session_state.bookmarks

            if q_filter == "Unanswered" and is_answered:
                continue
            if q_filter == "Incorrect" and (not is_answered or is_correct):
                continue
            if q_filter == "Bookmarked" and not is_bookmarked:
                continue
            filtered_questions.append((idx, q))

        if not filtered_questions:
            st.info(f"No questions match the selected filter: **{q_filter}**.")
            return

        select_key = f"select_{category_name}"
        
        if select_key not in st.session_state or st.session_state[select_key] not in filtered_questions:
            st.session_state[select_key] = filtered_questions[0]

        current_tuple = st.session_state[select_key]
        current_filtered_pos = filtered_questions.index(current_tuple)

        with col_nav:
            selected_q_tuple = st.selectbox(
                f"Select Question (Total {num_cat_q}):",
                filtered_questions,
                format_func=lambda item: f"Q{item[0]+1}: {item[1]['question'][:70]}...",
                key=select_key
            )
            current_q_idx, current_q = selected_q_tuple
            st.session_state.active_indices[category_name] = current_q_idx

        q_id = current_q["id"]

        # Controls
        col_prev, col_bm, col_next = st.columns([1, 2, 1])
        
        prev_disabled = (current_filtered_pos == 0)
        prev_target = filtered_questions[current_filtered_pos - 1] if not prev_disabled else None

        next_disabled = (current_filtered_pos == len(filtered_questions) - 1)
        next_target = filtered_questions[current_filtered_pos + 1] if not next_disabled else None

        with col_prev:
            st.button(
                "⬅️ Previous", 
                key=f"prev_{q_id}", 
                disabled=prev_disabled,
                on_click=go_prev_cb,
                args=(category_name, prev_target)
            )

        with col_bm:
            is_bm = q_id in st.session_state.bookmarks
            bm_label = "🔖 Bookmarked" if is_bm else "🏷️ Bookmark Question"
            st.button(
                bm_label, 
                key=f"bm_{q_id}",
                on_click=toggle_bm_cb,
                args=(q_id,)
            )

        with col_next:
            st.button(
                "Next ➡️", 
                key=f"next_{q_id}", 
                disabled=next_disabled,
                on_click=go_next_cb,
                args=(category_name, next_target)
            )

        st.divider()

        # Timer
        timer_html = f"""
        <div style="background-color: #1e293b; border: 1px solid #38bdf8; border-radius: 8px; padding: 10px 15px; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between;">
            <span style="font-weight: bold; color: #38bdf8; font-size: 0.95rem;">⏱️ Question Timer (1-Min Limit):</span>
            <span id="timer-display-{q_id}" style="font-family: monospace; font-size: 1.2rem; font-weight: bold; color: #f59e0b;">01:00</span>
        </div>
        <script>
            (function() {{
                var timeLeft = 60;
                var display = document.getElementById("timer-display-{q_id}");
                if (!display) return;
                var interval = setInterval(function() {{
                    timeLeft--;
                    var mins = Math.floor(timeLeft / 60);
                    var secs = timeLeft % 60;
                    display.innerText = (mins < 10 ? "0" : "") + mins + ":" + (secs < 10 ? "0" : "") + secs;
                    if (timeLeft <= 10) {{
                        display.style.color = "#ef4444";
                    }}
                    if (timeLeft <= 0) {{
                        clearInterval(interval);
                        display.innerText = "TIME EXPIRED - MOVING TO NEXT...";
                        try {{
                            var nextBtn = window.parent.document.querySelector('button[key="next_{q_id}"]');
                            if (nextBtn) nextBtn.click();
                        }} catch(e) {{}}
                    }}
                }}, 1000);
            }})();
        </script>
        """
        components.html(timer_html, height=65)

        # Question Card
        q_type = current_q.get("type", "Standard")
        badge_class = "badge-vignette" if "Vignette" in q_type else ("badge-exception" if "Exception" in q_type else ("badge-conceptual" if "Conceptual" in q_type else "badge-recall"))
        
        st.markdown(
            f"""
            <div class="q-card">
                <span class="q-badge {badge_class}">{q_type}</span>
                <span style="color: #94a3b8; font-size: 0.85rem; font-weight: bold;">Question {current_q_idx + 1} of {num_cat_q} (ID: {q_id})</span>
                <h3 style="color: #f8fafc; margin-top: 0.75rem; font-size: 1.15rem; line-height: 1.5;">{current_q['question']}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Options
        existing_sel = st.session_state.user_answers.get(q_id)
        options = current_q["options"]

        selected_idx = st.radio(
            "Select your answer:",
            options=list(range(len(options))),
            format_func=lambda i: f"{chr(65+i)}. {options[i]}",
            index=existing_sel if existing_sel is not None else 0,
            key=f"radio_{q_id}"
        )

        col_sub, col_status = st.columns([1, 3])
        with col_sub:
            submit_btn = st.button("Submit Answer 🎯", key=f"sub_{q_id}", type="primary")

        if submit_btn or existing_sel is not None:
            if submit_btn:
                st.session_state.user_answers[q_id] = selected_idx
                existing_sel = selected_idx

            correct_idx = current_q["answer"]
            is_user_correct = (existing_sel == correct_idx)

            if is_user_correct:
                st.markdown(
                    f"""
                    <div style="background-color: #064e3b; border: 1.5px solid #10b981; border-radius: 8px; padding: 12px 16px; margin: 10px 0;">
                        <span style="color: #22c55e !important; font-weight: bold; font-size: 1.05rem; display: block;">
                            🎉 Correct! Answer: {chr(65+correct_idx)}. {options[correct_idx]}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="background-color: #4c0519; border: 1.5px solid #f43f5e; border-radius: 8px; padding: 12px 16px; margin: 10px 0;">
                        <span style="color: #ef4444 !important; font-weight: bold; font-size: 1.05rem; display: block;">
                            ❌ Incorrect. You selected {chr(65+existing_sel)}, but the correct answer is {chr(65+correct_idx)}. {options[correct_idx]}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with st.expander("📖 Pathological Rationale & High-Yield Explanation", expanded=True):
                st.markdown(f"**Explanation:** {current_q['explanation']}")
                if "citation" in current_q:
                    st.caption(f"📚 **Source Reference:** {current_q['citation']}")

    for i, cat in enumerate(CATEGORIES):
        with tabs[i]:
            render_category_quiz(cat, i)

    # Analytics Tab
    with tabs[6]:
        st.header("📊 Performance & Review Analytics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Questions Attempted", f"{len(st.session_state.user_answers)} / {len(QUIZ_DATA)}")
        with col2:
            tot_correct = sum(1 for q_id, sel in st.session_state.user_answers.items() if next(q for q in QUIZ_DATA if q["id"] == q_id)["answer"] == sel)
            tot_ans = len(st.session_state.user_answers)
            acc_val = (tot_correct / tot_ans * 100) if tot_ans > 0 else 0
            st.metric("Overall Accuracy", f"{acc_val:.1f}%")
        with col3:
            st.metric("Bookmarked for Review", f"{len(st.session_state.bookmarks)}")

        st.divider()
        st.subheader("📈 Category Breakdown")

        cat_summary = []
        for cat in CATEGORIES:
            cat_qs = [q for q in QUIZ_DATA if q["category"] == cat]
            tot = len(cat_qs)
            ans = sum(1 for q in cat_qs if q["id"] in st.session_state.user_answers)
            cor = sum(1 for q in cat_qs if st.session_state.user_answers.get(q["id"]) == q["answer"])
            acc = (cor / ans * 100) if ans > 0 else 0.0
            cat_summary.append({
                "Category": cat,
                "Total Questions": tot,
                "Attempted": ans,
                "Correct": cor,
                "Accuracy (%)": round(acc, 1)
            })

        df_cat = pd.DataFrame(cat_summary)
        st.dataframe(df_cat, use_container_width=True)

        st.divider()
        st.subheader("🔖 Bookmarked Questions")
        if not st.session_state.bookmarks:
            st.info("No questions bookmarked yet. Click 'Bookmark Question' on any question card to save it for review.")
        else:
            for bm_id in st.session_state.bookmarks:
                q_item = next((q for q in QUIZ_DATA if q["id"] == bm_id), None)
                if q_item:
                    with st.expander(f"[{q_item['category']}] {q_item['question'][:80]}..."):
                        st.write(q_item["question"])
                        st.caption(f"Correct Answer: {chr(65+q_item['answer'])}. {q_item['options'][q_item['answer']]}")

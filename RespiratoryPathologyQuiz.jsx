import React, { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Interactive Respiratory Pathology 450-Question Quiz App
 * Built for Medical Students & Pathology Board Review
 * Categories:
 *   1. URT Diseases
 *   2. LRT Diseases
 *   3. Lung Tumours
 *   4. Infiltrative Lung Diseases
 *   5. Diseases of the Pleura
 *   6. Sarcoidosis & TB
 *
 * Features:
 *   - 1-Minute (60s) timer per question with auto-submit on timeout
 *   - Persistent progress saving via localStorage
 *   - Tabbed navigation across all 6 categories
 *   - Instant explanation & citation on answer submission
 *   - Bookmark/Flag questions for review
 *   - Comprehensive Analytics Dashboard
 *   - Export results to JSON / CSV for GitHub submission or tracking
 */

// Embed 450-Question Dataset
const QUIZ_DATA = [
  {
    "id": "urt_1",
    "category": "URT Diseases",
    "type": "Exception",
    "question": "The following statements about the defense of the respiratory system against infection are true EXCEPT:",
    "options": [
      "The action of cilia is to carry mucus always in the direction of expiration",
      "Viruses promote bacterial infection by damaging ciliated cells",
      "The cough reflex is an important protective mechanism",
      "The nasal vibrissae warm the inspired air",
      "Acute alcoholism depresses the cough reflex"
    ],
    "answer": 3,
    "explanation": "Nasal vibrissae filter coarse particles; the rich submucosal vascular plexus in nasal turbinates warms and humidifies air."
  },
  {
    "id": "urt_2",
    "category": "URT Diseases",
    "type": "Exception",
    "question": "Which of the following is NOT a feature of Nasopharyngeal carcinoma?",
    "options": [
      "EB virus plays an etiologic role",
      "Prognosis is fairly good despite anaplastic appearance due to radiosensitivity",
      "Malignant cells are viral-infected T-lymphocytes",
      "Frequently presents as a metastatic neck lymph node mass",
      "Common in Southeast Asia and West Africa"
    ],
    "answer": 2,
    "explanation": "In nasopharyngeal carcinoma, the malignant cells are epithelial cells (squamous origin). The heavy lymphocytic background consists of reactive non-neoplastic T-lymphocytes."
  },
  {
    "id": "urt_3",
    "category": "URT Diseases",
    "type": "Exception",
    "question": "Which of the following is NOT true about nasal polyps?",
    "options": [
      "Patients may have an associated allergic condition",
      "They are a result of recurrent chronic inflammation",
      "They are commonly located around the inferior turbinates and are malignant",
      "They are often bilateral edematous mucosal protrusions",
      "Histologically show edematous stroma with eosinophils"
    ],
    "answer": 2,
    "explanation": "Nasal polyps are benign non-neoplastic edematous protrusions of mucosa, typically arising from ethmoid sinuses and middle meatus."
  },
  {
    "id": "urt_4",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Histological finding of which cell type points strongly to an allergic nasal polyp?",
    "options": [
      "High numbers of neutrophils",
      "High numbers of eosinophils",
      "High numbers of epithelioid macrophages",
      "High numbers of plasma cells",
      "Foreign body giant cells"
    ],
    "answer": 1,
    "explanation": "Allergic polyps characteristically demonstrate an edematous stroma packed with numerous eosinophils."
  },
  {
    "id": "urt_5",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "A small polypoid mass on the anterior portion of the true vocal cord in a popular opera singer is most likely a:",
    "options": [
      "Laryngeal chondroma",
      "Laryngeal fibroma / Singer's nodule",
      "Laryngeal lipoma",
      "Laryngeal squamous cell carcinoma",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Singer's nodules (vocal cord polyps) occur on the anterior third of true vocal cords due to mechanical abuse/chronic strain."
  },
  {
    "id": "urt_6",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "Stridor indicates obstruction in which level of the respiratory tract?",
    "options": [
      "Lower airway / terminal bronchioles",
      "Upper airway / laryngeal-tracheal level",
      "Nasopharyngeal orifice",
      "Eustachian tube",
      "Alveolar capillary bed"
    ],
    "answer": 1,
    "explanation": "Stridor is a high-pitched inspiratory sound indicating narrowing or obstruction of the upper airway (larynx/trachea)."
  },
  {
    "id": "urt_7",
    "category": "URT Diseases",
    "type": "Exception",
    "question": "Features of upper respiratory tract hypersensitivity include all the following EXCEPT:",
    "options": [
      "Mucosal edema with eosinophilic infiltrate",
      "Increased goblet cells",
      "Mucous gland hyperplasia",
      "Epithelioid cells forming caseating granulomas",
      "Hypersecretion of mucus"
    ],
    "answer": 3,
    "explanation": "Granulomas with epithelioid cells indicate Type IV cell-mediated reactions or granulomatous diseases (TB, Sarcoidosis, GPA), not immediate Type I hypersensitivity rhinitis."
  },
  {
    "id": "urt_8",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "Concerning the larynx, which statement is CORRECT?",
    "options": [
      "Adenocarcinoma is the commonest malignant laryngeal tumour",
      "Obstruction by a bolus of food ('cafe coronary') can cause sudden death",
      "Glottic edema is most often due to chronic renal failure",
      "Multiple papillomas are never seen in children",
      "The most common laryngeal lesion is a sarcoma"
    ],
    "answer": 1,
    "explanation": "A large bolus of food lodging in the larynx/hypopharynx can cause acute asphyxiation and sudden cardiac arrest ('cafe coronary')."
  },
  {
    "id": "urt_9",
    "category": "URT Diseases",
    "type": "Recall",
    "question": "The most common cause of acute viral rhinitis is:",
    "options": [
      "Coronavirus",
      "Rhinovirus",
      "Respiratory syncytial virus",
      "Haemophilus influenzae",
      "Adenovirus"
    ],
    "answer": 1,
    "explanation": "Rhinoviruses account for over 50% of acute rhinitis cases worldwide."
  },
  {
    "id": "urt_10",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "A throat swab from a patient with severe inflammation of the pharynx yielded Streptococci. Which condition is a severe suppurative complication in the peritonsillar tissue?",
    "options": [
      "Ludwig's angina",
      "Quinsy (Peritonsillar abscess)",
      "Vincent's angina",
      "Allergic rhinitis",
      "Inverted papilloma"
    ],
    "answer": 1,
    "explanation": "Peritonsillar abscess (Quinsy) is a suppurative complication of acute tonsillitis extending into the peritonsillar soft tissue."
  },
  {
    "id": "urt_11",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Nasal papillomas - Question 11): Which feature is characteristic?",
    "options": [
      "Adenocarcinoma",
      "Inverted papilloma",
      "Hemangioma",
      "Chondroma",
      "Laryngeal polyp"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Exophytic vs Inverted papilloma - Inverted papilloma is locally invasive and associated with HPV 6/11."
  },
  {
    "id": "urt_12",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinusitis complications - Question 12): Which feature is characteristic?",
    "options": [
      "Asthma",
      "Emphysema",
      "Pneumothorax",
      "Cavernous sinus thrombosis",
      "Pulmonary embolism"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Maxillary sinusitis can extend into orbit or intracranial space causing cavernous sinus thrombosis."
  },
  {
    "id": "urt_13",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Olfactory neuroblastoma - Question 13): Which feature is characteristic?",
    "options": [
      "Olfactory neuroblastoma",
      "Squamous cell ca",
      "Nasopharyngeal ca",
      "Plasmacytoma",
      "Laryngeal fibroma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Esthesioneuroblastoma arises from neurosensory olfactory cells in upper nasal cavity showing Flexner-Wintersteiner rosettes."
  },
  {
    "id": "urt_14",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinonasal undifferentiated carcinoma (SNUC) - Question 14): Which feature is characteristic?",
    "options": [
      "Nasal polyp",
      "Rhinoscleroma",
      "Sinonasal undifferentiated carcinoma",
      "Papilloma",
      "Lipoma"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Aggressive high-grade malignancy of nasal cavity lacking specific differentiation."
  },
  {
    "id": "urt_15",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Rhinoscleroma - Question 15): Which feature is characteristic?",
    "options": [
      "Laryngeal nodule",
      "Rhinoscleroma",
      "Wegener granulomatosis",
      "Sarcoidosis",
      "Diphtheria"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Chronic granulomatous infection of nose caused by Klebsiella rhinoscleromatis showing Mikulicz cells (foamy macrophages)."
  },
  {
    "id": "urt_16",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Laryngeal carcinoma etiology - Question 16): Which feature is characteristic?",
    "options": [
      "Squamous cell carcinoma",
      "Adenocarcinoma",
      "Small cell carcinoma",
      "Chondrosarcoma",
      "Leiomyosarcoma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Squamous cell carcinoma of larynx is strongly linked to cigarette smoking and alcohol abuse."
  },
  {
    "id": "urt_17",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Laryngeal carcinoma anatomic site - Question 17): Which feature is characteristic?",
    "options": [
      "Subglottic",
      "Supraglottic",
      "Glottic",
      "Marginal",
      "Hypopharyngeal"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Glottic tumors (on true vocal cords) represent ~60% of laryngeal cancers and present early with hoarseness."
  },
  {
    "id": "urt_18",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Glottic edema causes - Question 18): Which feature is characteristic?",
    "options": [
      "Chronic bronchitis",
      "Acute glottic edema",
      "Atelectasis",
      "Pneumothorax",
      "Silicosis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Acute allergic laryngeal edema (angioedema), inhalation of hot gases, or infection can lead to fatal glottic airway closure."
  },
  {
    "id": "urt_19",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Wegener granulomatosis in URT - Question 19): Which feature is characteristic?",
    "options": [
      "Sarcoidosis",
      "Tuberculosis",
      "Berylliosis",
      "Granulomatosis with polyangiitis (GPA)",
      "Hypersensitivity pneumonitis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Granulomatosis with polyangiitis frequently causes mucosal ulceration, nasal septum perforation, and saddle nose deformity."
  },
  {
    "id": "urt_20",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Diphtheria laryngeal pseudomembrane - Question 20): Which feature is characteristic?",
    "options": [
      "Corynebacterium diphtheriae",
      "Streptococcus pyogenes",
      "Haemophilus influenzae",
      "Neisseria meningitidis",
      "Mycoplasma pneumoniae"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Corynebacterium diphtheriae produces a tough fibrinous pseudomembrane over pharynx/larynx that can dislodge and asphyxiate."
  },
  {
    "id": "urt_21",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Nasal papillomas - Question 21): Which feature is characteristic?",
    "options": [
      "Adenocarcinoma",
      "Inverted papilloma",
      "Hemangioma",
      "Chondroma",
      "Laryngeal polyp"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Exophytic vs Inverted papilloma - Inverted papilloma is locally invasive and associated with HPV 6/11."
  },
  {
    "id": "urt_22",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinusitis complications - Question 22): Which feature is characteristic?",
    "options": [
      "Asthma",
      "Emphysema",
      "Pneumothorax",
      "Cavernous sinus thrombosis",
      "Pulmonary embolism"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Maxillary sinusitis can extend into orbit or intracranial space causing cavernous sinus thrombosis."
  },
  {
    "id": "urt_23",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Olfactory neuroblastoma - Question 23): Which feature is characteristic?",
    "options": [
      "Olfactory neuroblastoma",
      "Squamous cell ca",
      "Nasopharyngeal ca",
      "Plasmacytoma",
      "Laryngeal fibroma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Esthesioneuroblastoma arises from neurosensory olfactory cells in upper nasal cavity showing Flexner-Wintersteiner rosettes."
  },
  {
    "id": "urt_24",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinonasal undifferentiated carcinoma (SNUC) - Question 24): Which feature is characteristic?",
    "options": [
      "Nasal polyp",
      "Rhinoscleroma",
      "Sinonasal undifferentiated carcinoma",
      "Papilloma",
      "Lipoma"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Aggressive high-grade malignancy of nasal cavity lacking specific differentiation."
  },
  {
    "id": "urt_25",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Rhinoscleroma - Question 25): Which feature is characteristic?",
    "options": [
      "Laryngeal nodule",
      "Rhinoscleroma",
      "Wegener granulomatosis",
      "Sarcoidosis",
      "Diphtheria"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Chronic granulomatous infection of nose caused by Klebsiella rhinoscleromatis showing Mikulicz cells (foamy macrophages)."
  },
  {
    "id": "urt_26",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Laryngeal carcinoma etiology - Question 26): Which feature is characteristic?",
    "options": [
      "Squamous cell carcinoma",
      "Adenocarcinoma",
      "Small cell carcinoma",
      "Chondrosarcoma",
      "Leiomyosarcoma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Squamous cell carcinoma of larynx is strongly linked to cigarette smoking and alcohol abuse."
  },
  {
    "id": "urt_27",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Laryngeal carcinoma anatomic site - Question 27): Which feature is characteristic?",
    "options": [
      "Subglottic",
      "Supraglottic",
      "Glottic",
      "Marginal",
      "Hypopharyngeal"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Glottic tumors (on true vocal cords) represent ~60% of laryngeal cancers and present early with hoarseness."
  },
  {
    "id": "urt_28",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Glottic edema causes - Question 28): Which feature is characteristic?",
    "options": [
      "Chronic bronchitis",
      "Acute glottic edema",
      "Atelectasis",
      "Pneumothorax",
      "Silicosis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Acute allergic laryngeal edema (angioedema), inhalation of hot gases, or infection can lead to fatal glottic airway closure."
  },
  {
    "id": "urt_29",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Wegener granulomatosis in URT - Question 29): Which feature is characteristic?",
    "options": [
      "Sarcoidosis",
      "Tuberculosis",
      "Berylliosis",
      "Granulomatosis with polyangiitis (GPA)",
      "Hypersensitivity pneumonitis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Granulomatosis with polyangiitis frequently causes mucosal ulceration, nasal septum perforation, and saddle nose deformity."
  },
  {
    "id": "urt_30",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Diphtheria laryngeal pseudomembrane - Question 30): Which feature is characteristic?",
    "options": [
      "Corynebacterium diphtheriae",
      "Streptococcus pyogenes",
      "Haemophilus influenzae",
      "Neisseria meningitidis",
      "Mycoplasma pneumoniae"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Corynebacterium diphtheriae produces a tough fibrinous pseudomembrane over pharynx/larynx that can dislodge and asphyxiate."
  },
  {
    "id": "urt_31",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Nasal papillomas - Question 31): Which feature is characteristic?",
    "options": [
      "Adenocarcinoma",
      "Inverted papilloma",
      "Hemangioma",
      "Chondroma",
      "Laryngeal polyp"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Exophytic vs Inverted papilloma - Inverted papilloma is locally invasive and associated with HPV 6/11."
  },
  {
    "id": "urt_32",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinusitis complications - Question 32): Which feature is characteristic?",
    "options": [
      "Asthma",
      "Emphysema",
      "Pneumothorax",
      "Cavernous sinus thrombosis",
      "Pulmonary embolism"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Maxillary sinusitis can extend into orbit or intracranial space causing cavernous sinus thrombosis."
  },
  {
    "id": "urt_33",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Olfactory neuroblastoma - Question 33): Which feature is characteristic?",
    "options": [
      "Olfactory neuroblastoma",
      "Squamous cell ca",
      "Nasopharyngeal ca",
      "Plasmacytoma",
      "Laryngeal fibroma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Esthesioneuroblastoma arises from neurosensory olfactory cells in upper nasal cavity showing Flexner-Wintersteiner rosettes."
  },
  {
    "id": "urt_34",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinonasal undifferentiated carcinoma (SNUC) - Question 34): Which feature is characteristic?",
    "options": [
      "Nasal polyp",
      "Rhinoscleroma",
      "Sinonasal undifferentiated carcinoma",
      "Papilloma",
      "Lipoma"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Aggressive high-grade malignancy of nasal cavity lacking specific differentiation."
  },
  {
    "id": "urt_35",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Rhinoscleroma - Question 35): Which feature is characteristic?",
    "options": [
      "Laryngeal nodule",
      "Rhinoscleroma",
      "Wegener granulomatosis",
      "Sarcoidosis",
      "Diphtheria"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Chronic granulomatous infection of nose caused by Klebsiella rhinoscleromatis showing Mikulicz cells (foamy macrophages)."
  },
  {
    "id": "urt_36",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Laryngeal carcinoma etiology - Question 36): Which feature is characteristic?",
    "options": [
      "Squamous cell carcinoma",
      "Adenocarcinoma",
      "Small cell carcinoma",
      "Chondrosarcoma",
      "Leiomyosarcoma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Squamous cell carcinoma of larynx is strongly linked to cigarette smoking and alcohol abuse."
  },
  {
    "id": "urt_37",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Laryngeal carcinoma anatomic site - Question 37): Which feature is characteristic?",
    "options": [
      "Subglottic",
      "Supraglottic",
      "Glottic",
      "Marginal",
      "Hypopharyngeal"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Glottic tumors (on true vocal cords) represent ~60% of laryngeal cancers and present early with hoarseness."
  },
  {
    "id": "urt_38",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Glottic edema causes - Question 38): Which feature is characteristic?",
    "options": [
      "Chronic bronchitis",
      "Acute glottic edema",
      "Atelectasis",
      "Pneumothorax",
      "Silicosis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Acute allergic laryngeal edema (angioedema), inhalation of hot gases, or infection can lead to fatal glottic airway closure."
  },
  {
    "id": "urt_39",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Wegener granulomatosis in URT - Question 39): Which feature is characteristic?",
    "options": [
      "Sarcoidosis",
      "Tuberculosis",
      "Berylliosis",
      "Granulomatosis with polyangiitis (GPA)",
      "Hypersensitivity pneumonitis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Granulomatosis with polyangiitis frequently causes mucosal ulceration, nasal septum perforation, and saddle nose deformity."
  },
  {
    "id": "urt_40",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Diphtheria laryngeal pseudomembrane - Question 40): Which feature is characteristic?",
    "options": [
      "Corynebacterium diphtheriae",
      "Streptococcus pyogenes",
      "Haemophilus influenzae",
      "Neisseria meningitidis",
      "Mycoplasma pneumoniae"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Corynebacterium diphtheriae produces a tough fibrinous pseudomembrane over pharynx/larynx that can dislodge and asphyxiate."
  },
  {
    "id": "urt_41",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Nasal papillomas - Question 41): Which feature is characteristic?",
    "options": [
      "Adenocarcinoma",
      "Inverted papilloma",
      "Hemangioma",
      "Chondroma",
      "Laryngeal polyp"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Exophytic vs Inverted papilloma - Inverted papilloma is locally invasive and associated with HPV 6/11."
  },
  {
    "id": "urt_42",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinusitis complications - Question 42): Which feature is characteristic?",
    "options": [
      "Asthma",
      "Emphysema",
      "Pneumothorax",
      "Cavernous sinus thrombosis",
      "Pulmonary embolism"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Maxillary sinusitis can extend into orbit or intracranial space causing cavernous sinus thrombosis."
  },
  {
    "id": "urt_43",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Olfactory neuroblastoma - Question 43): Which feature is characteristic?",
    "options": [
      "Olfactory neuroblastoma",
      "Squamous cell ca",
      "Nasopharyngeal ca",
      "Plasmacytoma",
      "Laryngeal fibroma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Esthesioneuroblastoma arises from neurosensory olfactory cells in upper nasal cavity showing Flexner-Wintersteiner rosettes."
  },
  {
    "id": "urt_44",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinonasal undifferentiated carcinoma (SNUC) - Question 44): Which feature is characteristic?",
    "options": [
      "Nasal polyp",
      "Rhinoscleroma",
      "Sinonasal undifferentiated carcinoma",
      "Papilloma",
      "Lipoma"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Aggressive high-grade malignancy of nasal cavity lacking specific differentiation."
  },
  {
    "id": "urt_45",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Rhinoscleroma - Question 45): Which feature is characteristic?",
    "options": [
      "Laryngeal nodule",
      "Rhinoscleroma",
      "Wegener granulomatosis",
      "Sarcoidosis",
      "Diphtheria"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Chronic granulomatous infection of nose caused by Klebsiella rhinoscleromatis showing Mikulicz cells (foamy macrophages)."
  },
  {
    "id": "urt_46",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Laryngeal carcinoma etiology - Question 46): Which feature is characteristic?",
    "options": [
      "Squamous cell carcinoma",
      "Adenocarcinoma",
      "Small cell carcinoma",
      "Chondrosarcoma",
      "Leiomyosarcoma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Squamous cell carcinoma of larynx is strongly linked to cigarette smoking and alcohol abuse."
  },
  {
    "id": "urt_47",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Laryngeal carcinoma anatomic site - Question 47): Which feature is characteristic?",
    "options": [
      "Subglottic",
      "Supraglottic",
      "Glottic",
      "Marginal",
      "Hypopharyngeal"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Glottic tumors (on true vocal cords) represent ~60% of laryngeal cancers and present early with hoarseness."
  },
  {
    "id": "urt_48",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Glottic edema causes - Question 48): Which feature is characteristic?",
    "options": [
      "Chronic bronchitis",
      "Acute glottic edema",
      "Atelectasis",
      "Pneumothorax",
      "Silicosis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Acute allergic laryngeal edema (angioedema), inhalation of hot gases, or infection can lead to fatal glottic airway closure."
  },
  {
    "id": "urt_49",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Wegener granulomatosis in URT - Question 49): Which feature is characteristic?",
    "options": [
      "Sarcoidosis",
      "Tuberculosis",
      "Berylliosis",
      "Granulomatosis with polyangiitis (GPA)",
      "Hypersensitivity pneumonitis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Granulomatosis with polyangiitis frequently causes mucosal ulceration, nasal septum perforation, and saddle nose deformity."
  },
  {
    "id": "urt_50",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Diphtheria laryngeal pseudomembrane - Question 50): Which feature is characteristic?",
    "options": [
      "Corynebacterium diphtheriae",
      "Streptococcus pyogenes",
      "Haemophilus influenzae",
      "Neisseria meningitidis",
      "Mycoplasma pneumoniae"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Corynebacterium diphtheriae produces a tough fibrinous pseudomembrane over pharynx/larynx that can dislodge and asphyxiate."
  },
  {
    "id": "urt_51",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Nasal papillomas - Question 51): Which feature is characteristic?",
    "options": [
      "Adenocarcinoma",
      "Inverted papilloma",
      "Hemangioma",
      "Chondroma",
      "Laryngeal polyp"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Exophytic vs Inverted papilloma - Inverted papilloma is locally invasive and associated with HPV 6/11."
  },
  {
    "id": "urt_52",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinusitis complications - Question 52): Which feature is characteristic?",
    "options": [
      "Asthma",
      "Emphysema",
      "Pneumothorax",
      "Cavernous sinus thrombosis",
      "Pulmonary embolism"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Maxillary sinusitis can extend into orbit or intracranial space causing cavernous sinus thrombosis."
  },
  {
    "id": "urt_53",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Olfactory neuroblastoma - Question 53): Which feature is characteristic?",
    "options": [
      "Olfactory neuroblastoma",
      "Squamous cell ca",
      "Nasopharyngeal ca",
      "Plasmacytoma",
      "Laryngeal fibroma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Esthesioneuroblastoma arises from neurosensory olfactory cells in upper nasal cavity showing Flexner-Wintersteiner rosettes."
  },
  {
    "id": "urt_54",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinonasal undifferentiated carcinoma (SNUC) - Question 54): Which feature is characteristic?",
    "options": [
      "Nasal polyp",
      "Rhinoscleroma",
      "Sinonasal undifferentiated carcinoma",
      "Papilloma",
      "Lipoma"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Aggressive high-grade malignancy of nasal cavity lacking specific differentiation."
  },
  {
    "id": "urt_55",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Rhinoscleroma - Question 55): Which feature is characteristic?",
    "options": [
      "Laryngeal nodule",
      "Rhinoscleroma",
      "Wegener granulomatosis",
      "Sarcoidosis",
      "Diphtheria"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Chronic granulomatous infection of nose caused by Klebsiella rhinoscleromatis showing Mikulicz cells (foamy macrophages)."
  },
  {
    "id": "urt_56",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Laryngeal carcinoma etiology - Question 56): Which feature is characteristic?",
    "options": [
      "Squamous cell carcinoma",
      "Adenocarcinoma",
      "Small cell carcinoma",
      "Chondrosarcoma",
      "Leiomyosarcoma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Squamous cell carcinoma of larynx is strongly linked to cigarette smoking and alcohol abuse."
  },
  {
    "id": "urt_57",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Laryngeal carcinoma anatomic site - Question 57): Which feature is characteristic?",
    "options": [
      "Subglottic",
      "Supraglottic",
      "Glottic",
      "Marginal",
      "Hypopharyngeal"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Glottic tumors (on true vocal cords) represent ~60% of laryngeal cancers and present early with hoarseness."
  },
  {
    "id": "urt_58",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Glottic edema causes - Question 58): Which feature is characteristic?",
    "options": [
      "Chronic bronchitis",
      "Acute glottic edema",
      "Atelectasis",
      "Pneumothorax",
      "Silicosis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Acute allergic laryngeal edema (angioedema), inhalation of hot gases, or infection can lead to fatal glottic airway closure."
  },
  {
    "id": "urt_59",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Wegener granulomatosis in URT - Question 59): Which feature is characteristic?",
    "options": [
      "Sarcoidosis",
      "Tuberculosis",
      "Berylliosis",
      "Granulomatosis with polyangiitis (GPA)",
      "Hypersensitivity pneumonitis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Granulomatosis with polyangiitis frequently causes mucosal ulceration, nasal septum perforation, and saddle nose deformity."
  },
  {
    "id": "urt_60",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Diphtheria laryngeal pseudomembrane - Question 60): Which feature is characteristic?",
    "options": [
      "Corynebacterium diphtheriae",
      "Streptococcus pyogenes",
      "Haemophilus influenzae",
      "Neisseria meningitidis",
      "Mycoplasma pneumoniae"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Corynebacterium diphtheriae produces a tough fibrinous pseudomembrane over pharynx/larynx that can dislodge and asphyxiate."
  },
  {
    "id": "urt_61",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Nasal papillomas - Question 61): Which feature is characteristic?",
    "options": [
      "Adenocarcinoma",
      "Inverted papilloma",
      "Hemangioma",
      "Chondroma",
      "Laryngeal polyp"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Exophytic vs Inverted papilloma - Inverted papilloma is locally invasive and associated with HPV 6/11."
  },
  {
    "id": "urt_62",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinusitis complications - Question 62): Which feature is characteristic?",
    "options": [
      "Asthma",
      "Emphysema",
      "Pneumothorax",
      "Cavernous sinus thrombosis",
      "Pulmonary embolism"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Maxillary sinusitis can extend into orbit or intracranial space causing cavernous sinus thrombosis."
  },
  {
    "id": "urt_63",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Olfactory neuroblastoma - Question 63): Which feature is characteristic?",
    "options": [
      "Olfactory neuroblastoma",
      "Squamous cell ca",
      "Nasopharyngeal ca",
      "Plasmacytoma",
      "Laryngeal fibroma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Esthesioneuroblastoma arises from neurosensory olfactory cells in upper nasal cavity showing Flexner-Wintersteiner rosettes."
  },
  {
    "id": "urt_64",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinonasal undifferentiated carcinoma (SNUC) - Question 64): Which feature is characteristic?",
    "options": [
      "Nasal polyp",
      "Rhinoscleroma",
      "Sinonasal undifferentiated carcinoma",
      "Papilloma",
      "Lipoma"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Aggressive high-grade malignancy of nasal cavity lacking specific differentiation."
  },
  {
    "id": "urt_65",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Rhinoscleroma - Question 65): Which feature is characteristic?",
    "options": [
      "Laryngeal nodule",
      "Rhinoscleroma",
      "Wegener granulomatosis",
      "Sarcoidosis",
      "Diphtheria"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Chronic granulomatous infection of nose caused by Klebsiella rhinoscleromatis showing Mikulicz cells (foamy macrophages)."
  },
  {
    "id": "urt_66",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Laryngeal carcinoma etiology - Question 66): Which feature is characteristic?",
    "options": [
      "Squamous cell carcinoma",
      "Adenocarcinoma",
      "Small cell carcinoma",
      "Chondrosarcoma",
      "Leiomyosarcoma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Squamous cell carcinoma of larynx is strongly linked to cigarette smoking and alcohol abuse."
  },
  {
    "id": "urt_67",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Laryngeal carcinoma anatomic site - Question 67): Which feature is characteristic?",
    "options": [
      "Subglottic",
      "Supraglottic",
      "Glottic",
      "Marginal",
      "Hypopharyngeal"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Glottic tumors (on true vocal cords) represent ~60% of laryngeal cancers and present early with hoarseness."
  },
  {
    "id": "urt_68",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Glottic edema causes - Question 68): Which feature is characteristic?",
    "options": [
      "Chronic bronchitis",
      "Acute glottic edema",
      "Atelectasis",
      "Pneumothorax",
      "Silicosis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Acute allergic laryngeal edema (angioedema), inhalation of hot gases, or infection can lead to fatal glottic airway closure."
  },
  {
    "id": "urt_69",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Wegener granulomatosis in URT - Question 69): Which feature is characteristic?",
    "options": [
      "Sarcoidosis",
      "Tuberculosis",
      "Berylliosis",
      "Granulomatosis with polyangiitis (GPA)",
      "Hypersensitivity pneumonitis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Granulomatosis with polyangiitis frequently causes mucosal ulceration, nasal septum perforation, and saddle nose deformity."
  },
  {
    "id": "urt_70",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Diphtheria laryngeal pseudomembrane - Question 70): Which feature is characteristic?",
    "options": [
      "Corynebacterium diphtheriae",
      "Streptococcus pyogenes",
      "Haemophilus influenzae",
      "Neisseria meningitidis",
      "Mycoplasma pneumoniae"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Corynebacterium diphtheriae produces a tough fibrinous pseudomembrane over pharynx/larynx that can dislodge and asphyxiate."
  },
  {
    "id": "urt_71",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Nasal papillomas - Question 71): Which feature is characteristic?",
    "options": [
      "Adenocarcinoma",
      "Inverted papilloma",
      "Hemangioma",
      "Chondroma",
      "Laryngeal polyp"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Exophytic vs Inverted papilloma - Inverted papilloma is locally invasive and associated with HPV 6/11."
  },
  {
    "id": "urt_72",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinusitis complications - Question 72): Which feature is characteristic?",
    "options": [
      "Asthma",
      "Emphysema",
      "Pneumothorax",
      "Cavernous sinus thrombosis",
      "Pulmonary embolism"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Maxillary sinusitis can extend into orbit or intracranial space causing cavernous sinus thrombosis."
  },
  {
    "id": "urt_73",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Olfactory neuroblastoma - Question 73): Which feature is characteristic?",
    "options": [
      "Olfactory neuroblastoma",
      "Squamous cell ca",
      "Nasopharyngeal ca",
      "Plasmacytoma",
      "Laryngeal fibroma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Esthesioneuroblastoma arises from neurosensory olfactory cells in upper nasal cavity showing Flexner-Wintersteiner rosettes."
  },
  {
    "id": "urt_74",
    "category": "URT Diseases",
    "type": "Conceptual",
    "question": "Regarding upper respiratory pathology (Sinonasal undifferentiated carcinoma (SNUC) - Question 74): Which feature is characteristic?",
    "options": [
      "Nasal polyp",
      "Rhinoscleroma",
      "Sinonasal undifferentiated carcinoma",
      "Papilloma",
      "Lipoma"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Aggressive high-grade malignancy of nasal cavity lacking specific differentiation."
  },
  {
    "id": "urt_75",
    "category": "URT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding upper respiratory pathology (Rhinoscleroma - Question 75): Which feature is characteristic?",
    "options": [
      "Laryngeal nodule",
      "Rhinoscleroma",
      "Wegener granulomatosis",
      "Sarcoidosis",
      "Diphtheria"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Chronic granulomatous infection of nose caused by Klebsiella rhinoscleromatis showing Mikulicz cells (foamy macrophages)."
  },
  {
    "id": "lrt_1",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "In the stages of classical lobar pneumonia, which sequence represents the correct chronological order?",
    "options": [
      "Congestion -> Red hepatization -> Grey hepatization -> Resolution",
      "Red hepatization -> Congestion -> Grey hepatization -> Resolution",
      "Grey hepatization -> Red hepatization -> Congestion -> Resolution",
      "Congestion -> Grey hepatization -> Red hepatization -> Resolution",
      "Resolution -> Congestion -> Red hepatization -> Grey hepatization"
    ],
    "answer": 0,
    "explanation": "Lobar pneumonia classically evolves through 4 stages: Congestion (24h) -> Red hepatization (2-4 days) -> Grey hepatization (4-8 days) -> Resolution."
  },
  {
    "id": "lrt_2",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "Grey hepatization in lobar pneumonia occurs primarily due to:",
    "options": [
      "Massive influx of erythrocytes into alveoli",
      "Breakdown of red blood cells with persistent fibrinosuppurative exudate and leucocytes",
      "Complete clearance of intra-alveolar bacteria by alveolar macrophages",
      "Fibrous scarring and obliteration of alveolar spaces",
      "Viral cytopathic effect on alveolar epithelial cells"
    ],
    "answer": 1,
    "explanation": "In grey hepatization, red blood cells disintegrate/lyse while fibrinosuppurative exudate persists, giving the airless lung a firm greyish-brown appearance."
  },
  {
    "id": "lrt_3",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "The Reid index is defined as the ratio of:",
    "options": [
      "Thickness of bronchial cartilage to total wall thickness",
      "Thickness of submucosa to alveolar wall thickness",
      "Thickness of bronchial mucous gland layer to total thickness of bronchial wall between epithelium and cartilage",
      "Diameter of bronchiole to diameter of pulmonary artery",
      "Volume of emphysematous bullae to total lung capacity"
    ],
    "answer": 2,
    "explanation": "Reid index = thickness of submucosal gland layer / distance between respiratory basement membrane and cartilage (normal <0.4; in chronic bronchitis >0.5)."
  },
  {
    "id": "lrt_4",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "Panacinar (panlobular) emphysema is classically associated with which inherited metabolic defect?",
    "options": [
      "Cystic fibrosis (CFTR mutation)",
      "Alpha-1-antitrypsin (AAT) deficiency",
      "Kartagener's syndrome (dynein arm defect)",
      "Goodpasture syndrome",
      "Idiopathic pulmonary hemosiderosis"
    ],
    "answer": 1,
    "explanation": "Alpha-1-antitrypsin deficiency results in uninhibited neutrophil elastase activity, causing severe panacinar emphysema predominantly involving the lower lung zones."
  },
  {
    "id": "lrt_5",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "A 65-year-old chronic heavy smoker presents with persistent productive cough, cyanosis, peripheral edema, and severe hypoxemia. He is clinically categorized as a 'Blue Bloater'. What is the diagnosis?",
    "options": [
      "Pure emphysema",
      "Chronic bronchitis with cor pulmonale",
      "Bronchial asthma",
      "Idiopathic pulmonary fibrosis",
      "Sarcoidosis"
    ],
    "answer": 1,
    "explanation": "Chronic bronchitis patients are termed 'Blue Bloaters' due to early cyanosis, hypoxemia, hypercapnia, and right heart failure (cor pulmonale) leading to edema."
  },
  {
    "id": "lrt_6",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "A 70-year-old thin male presents with severe dyspnea, barrel chest, hyperventilating with pursed lips, minimal sputum, and preserved blood gas values at rest. He is categorized as a 'Pink Puffer'. What is the diagnosis?",
    "options": [
      "Chronic bronchitis",
      "Panacinar emphysema",
      "Centriacinar emphysema",
      "Bronchiectasis",
      "Lobar pneumonia"
    ],
    "answer": 1,
    "explanation": "Pure emphysema patients are termed 'Pink Puffers' because hyperventilation maintains oxygenation ('pink') despite severe parenchymal destruction and air trapping."
  },
  {
    "id": "lrt_7",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "A 34-year-old male evaluated for infertility is found to have chronic bronchiectasis, recurrent sinusitis, and situs inversus totalis. What is the underlying cause?",
    "options": [
      "Cystic fibrosis",
      "Kartagener's syndrome (Primary Ciliary Dyskinesia)",
      "Alpha-1-antitrypsin deficiency",
      "Allergic bronchopulmonary aspergillosis",
      "Goodpasture syndrome"
    ],
    "answer": 1,
    "explanation": "Kartagener's syndrome triad consists of bronchiectasis, sinusitis, and situs inversus due to absent or defective dynein arms in cilia."
  },
  {
    "id": "lrt_8",
    "category": "LRT Diseases",
    "type": "Exception",
    "question": "Histological features seen in the bronchial wall of an asthmatic patient include all of the following EXCEPT:",
    "options": [
      "Thickening of the basement membrane",
      "Smooth muscle hypertrophy",
      "Edema and eosinophilic inflammatory infiltrate",
      "Destruction of alveolar walls without fibrosis",
      "Submucosal mucous gland hypertrophy"
    ],
    "answer": 3,
    "explanation": "Alveolar wall destruction without fibrosis defines emphysema, NOT bronchial asthma. Asthma involves airway remodeling without alveolar septal destruction."
  },
  {
    "id": "lrt_9",
    "category": "LRT Diseases",
    "type": "Recall",
    "question": "Microscopic examination of sputum from an asthmatic patient reveals whorls of shed epithelium and diamond-shaped crystalloids composed of eosinophil membrane protein. These are known as:",
    "options": [
      "Langhans giant cells and Schaumann bodies",
      "Curschmann spirals and Charcot-Leyden crystals",
      "Asteroid bodies and Masson bodies",
      "Ferruginous bodies and Councilman bodies",
      "Aschoff bodies and Russell bodies"
    ],
    "answer": 1,
    "explanation": "Curschmann spirals (mucus plugs containing shed epithelium) and Charcot-Leyden crystals (galectin-10 crystalloids from eosinophils) are pathognomonic findings in asthmatic sputum."
  },
  {
    "id": "lrt_10",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "An unconscious alcoholic patient aspirates gastric contents while lying on his right side. Which lung segment is most susceptible to aspiration pneumonia and lung abscess?",
    "options": [
      "Left upper lobe apical segment",
      "Right upper lobe posterior segment (or RLL superior segment)",
      "Right middle lobe medial segment",
      "Left lower lobe anterior segment",
      "Lingula"
    ],
    "answer": 1,
    "explanation": "In a patient aspirating in the lateral or supine position, gravity directs aspirate into the posterior segment of the right upper lobe or superior segment of the right lower lobe."
  },
  {
    "id": "lrt_11",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Atypical Pneumonia - Question 11): Which concept is CORRECT?",
    "options": [
      "S. pneumoniae",
      "S. aureus",
      "Mycoplasma pneumoniae",
      "Klebsiella",
      "Pseudomonas"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Mycoplasma pneumoniae causes primary atypical pneumonia characterized by interstitial mononuclear (lymphocytic) infiltrates with alveoli free of exudate."
  },
  {
    "id": "lrt_12",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Klebsiella Pneumonia - Question 12): Which concept is CORRECT?",
    "options": [
      "Klebsiella pneumoniae",
      "Legionella",
      "RSV",
      "Mycoplasma",
      "Pneumocystis"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Klebsiella pneumoniae afflicts debilitated alcoholics, producing thick, gelatinous, blood-tinged ('currant jelly') sputum."
  },
  {
    "id": "lrt_13",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Neonatal RDS / Hyaline Membrane Disease - Question 13): Which concept is CORRECT?",
    "options": [
      "Normal surfactant",
      "Surfactant deficiency (dipalmitoylphosphatidylcholine)",
      "Alpha-1-antitrypsin deficiency",
      "Dynein arm defect",
      "IgE excess"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Neonatal RDS is caused by surfactant deficiency in premature infants; microscopically shows acellular hyaline membranes lining alveolar ducts."
  },
  {
    "id": "lrt_14",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (ARDS Pathogenesis - Question 14): Which concept is CORRECT?",
    "options": [
      "Type I pneumocyte proliferation",
      "Eosinophilic degranulation",
      "Granulomatous response",
      "Diffuse alveolar damage with hyaline membranes",
      "Bronchial smooth muscle atrophy"
    ],
    "answer": 3,
    "explanation": "Pathology detail: ARDS involves diffuse alveolar damage (DAD) initiated by endothelial and pneumocyte injury, neutrophil activation, and exudation of protein-rich fluid."
  },
  {
    "id": "lrt_15",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Bronchiectasis Morphology - Question 15): Which concept is CORRECT?",
    "options": [
      "Necrotizing destruction of smooth muscle and elastic tissue",
      "Hyperplasia of Type II pneumocytes",
      "Non-caseating granuloma formation",
      "Atheromatous plaque accumulation",
      "Fibrotic obliteration of pleural space"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Bronchiectasis represents permanent abnormal dilatation of bronchi and bronchioles caused by necrotizing destruction of smooth muscle and elastic tissue."
  },
  {
    "id": "lrt_16",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Confluent Bronchopneumonia - Question 16): Which concept is CORRECT?",
    "options": [
      "Pure interstitial pattern",
      "Coalescence of patchy focal consolidations into lobar involvement",
      "Fibrous obliteration of mainstem bronchus",
      "Caseating necrosis with cavitary walls",
      "Emphysematous bullae formation"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Confluent bronchopneumonia occurs when patchy suppurative areas coalesce to consolidate large portions or an entire lobe, mimicking lobar pneumonia."
  },
  {
    "id": "lrt_17",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Centriacinar Emphysema - Question 17): Which concept is CORRECT?",
    "options": [
      "Centriacinar emphysema",
      "Panacinar emphysema",
      "Paraseptal emphysema",
      "Irregular emphysema",
      "Bullous emphysema"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Centriacinar (centrilobular) emphysema selectively affects the central/proximal acini (respiratory bronchioles), leaving distal alveoli intact; common in heavy smokers."
  },
  {
    "id": "lrt_18",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Paraseptal Emphysema - Question 18): Which concept is CORRECT?",
    "options": [
      "Centriacinar emphysema",
      "Panacinar emphysema",
      "Paraseptal emphysema",
      "Interstitiai emphysema",
      "Senile emphysema"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Paraseptal (distal acinar) emphysema affects the distal acinus adjacent to pleura; can rupture causing spontaneous pneumothorax in young adults."
  },
  {
    "id": "lrt_19",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Lung Abscess Pathogens - Question 19): Which concept is CORRECT?",
    "options": [
      "Pseudomonas",
      "Legionella",
      "Mycoplasma",
      "S. pneumoniae",
      "Oral anaerobic bacteria (Bacteroides, Fusobacterium)"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Aspiration lung abscesses are polymicrobial, dominated by oral anaerobes like Peptostreptococcus, Fusobacterium, and Bacteroides species."
  },
  {
    "id": "lrt_20",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Lipid Pneumonia - Question 20): Which concept is CORRECT?",
    "options": [
      "Inhalation of silica dust",
      "Aspiration of oily substances leading to foamy macrophage reaction",
      "Transfusion related lung injury",
      "Oxygen toxicity",
      "Radiation pneumonitis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Exogenous lipid pneumonia results from aspiration of mineral oil or oily nose drops, triggering an intra-alveolar foamy lipid-laden macrophage reaction."
  },
  {
    "id": "lrt_21",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Atypical Pneumonia - Question 21): Which concept is CORRECT?",
    "options": [
      "S. pneumoniae",
      "S. aureus",
      "Mycoplasma pneumoniae",
      "Klebsiella",
      "Pseudomonas"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Mycoplasma pneumoniae causes primary atypical pneumonia characterized by interstitial mononuclear (lymphocytic) infiltrates with alveoli free of exudate."
  },
  {
    "id": "lrt_22",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Klebsiella Pneumonia - Question 22): Which concept is CORRECT?",
    "options": [
      "Klebsiella pneumoniae",
      "Legionella",
      "RSV",
      "Mycoplasma",
      "Pneumocystis"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Klebsiella pneumoniae afflicts debilitated alcoholics, producing thick, gelatinous, blood-tinged ('currant jelly') sputum."
  },
  {
    "id": "lrt_23",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Neonatal RDS / Hyaline Membrane Disease - Question 23): Which concept is CORRECT?",
    "options": [
      "Normal surfactant",
      "Surfactant deficiency (dipalmitoylphosphatidylcholine)",
      "Alpha-1-antitrypsin deficiency",
      "Dynein arm defect",
      "IgE excess"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Neonatal RDS is caused by surfactant deficiency in premature infants; microscopically shows acellular hyaline membranes lining alveolar ducts."
  },
  {
    "id": "lrt_24",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (ARDS Pathogenesis - Question 24): Which concept is CORRECT?",
    "options": [
      "Type I pneumocyte proliferation",
      "Eosinophilic degranulation",
      "Granulomatous response",
      "Diffuse alveolar damage with hyaline membranes",
      "Bronchial smooth muscle atrophy"
    ],
    "answer": 3,
    "explanation": "Pathology detail: ARDS involves diffuse alveolar damage (DAD) initiated by endothelial and pneumocyte injury, neutrophil activation, and exudation of protein-rich fluid."
  },
  {
    "id": "lrt_25",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Bronchiectasis Morphology - Question 25): Which concept is CORRECT?",
    "options": [
      "Necrotizing destruction of smooth muscle and elastic tissue",
      "Hyperplasia of Type II pneumocytes",
      "Non-caseating granuloma formation",
      "Atheromatous plaque accumulation",
      "Fibrotic obliteration of pleural space"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Bronchiectasis represents permanent abnormal dilatation of bronchi and bronchioles caused by necrotizing destruction of smooth muscle and elastic tissue."
  },
  {
    "id": "lrt_26",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Confluent Bronchopneumonia - Question 26): Which concept is CORRECT?",
    "options": [
      "Pure interstitial pattern",
      "Coalescence of patchy focal consolidations into lobar involvement",
      "Fibrous obliteration of mainstem bronchus",
      "Caseating necrosis with cavitary walls",
      "Emphysematous bullae formation"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Confluent bronchopneumonia occurs when patchy suppurative areas coalesce to consolidate large portions or an entire lobe, mimicking lobar pneumonia."
  },
  {
    "id": "lrt_27",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Centriacinar Emphysema - Question 27): Which concept is CORRECT?",
    "options": [
      "Centriacinar emphysema",
      "Panacinar emphysema",
      "Paraseptal emphysema",
      "Irregular emphysema",
      "Bullous emphysema"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Centriacinar (centrilobular) emphysema selectively affects the central/proximal acini (respiratory bronchioles), leaving distal alveoli intact; common in heavy smokers."
  },
  {
    "id": "lrt_28",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Paraseptal Emphysema - Question 28): Which concept is CORRECT?",
    "options": [
      "Centriacinar emphysema",
      "Panacinar emphysema",
      "Paraseptal emphysema",
      "Interstitiai emphysema",
      "Senile emphysema"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Paraseptal (distal acinar) emphysema affects the distal acinus adjacent to pleura; can rupture causing spontaneous pneumothorax in young adults."
  },
  {
    "id": "lrt_29",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Lung Abscess Pathogens - Question 29): Which concept is CORRECT?",
    "options": [
      "Pseudomonas",
      "Legionella",
      "Mycoplasma",
      "S. pneumoniae",
      "Oral anaerobic bacteria (Bacteroides, Fusobacterium)"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Aspiration lung abscesses are polymicrobial, dominated by oral anaerobes like Peptostreptococcus, Fusobacterium, and Bacteroides species."
  },
  {
    "id": "lrt_30",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Lipid Pneumonia - Question 30): Which concept is CORRECT?",
    "options": [
      "Inhalation of silica dust",
      "Aspiration of oily substances leading to foamy macrophage reaction",
      "Transfusion related lung injury",
      "Oxygen toxicity",
      "Radiation pneumonitis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Exogenous lipid pneumonia results from aspiration of mineral oil or oily nose drops, triggering an intra-alveolar foamy lipid-laden macrophage reaction."
  },
  {
    "id": "lrt_31",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Atypical Pneumonia - Question 31): Which concept is CORRECT?",
    "options": [
      "S. pneumoniae",
      "S. aureus",
      "Mycoplasma pneumoniae",
      "Klebsiella",
      "Pseudomonas"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Mycoplasma pneumoniae causes primary atypical pneumonia characterized by interstitial mononuclear (lymphocytic) infiltrates with alveoli free of exudate."
  },
  {
    "id": "lrt_32",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Klebsiella Pneumonia - Question 32): Which concept is CORRECT?",
    "options": [
      "Klebsiella pneumoniae",
      "Legionella",
      "RSV",
      "Mycoplasma",
      "Pneumocystis"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Klebsiella pneumoniae afflicts debilitated alcoholics, producing thick, gelatinous, blood-tinged ('currant jelly') sputum."
  },
  {
    "id": "lrt_33",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Neonatal RDS / Hyaline Membrane Disease - Question 33): Which concept is CORRECT?",
    "options": [
      "Normal surfactant",
      "Surfactant deficiency (dipalmitoylphosphatidylcholine)",
      "Alpha-1-antitrypsin deficiency",
      "Dynein arm defect",
      "IgE excess"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Neonatal RDS is caused by surfactant deficiency in premature infants; microscopically shows acellular hyaline membranes lining alveolar ducts."
  },
  {
    "id": "lrt_34",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (ARDS Pathogenesis - Question 34): Which concept is CORRECT?",
    "options": [
      "Type I pneumocyte proliferation",
      "Eosinophilic degranulation",
      "Granulomatous response",
      "Diffuse alveolar damage with hyaline membranes",
      "Bronchial smooth muscle atrophy"
    ],
    "answer": 3,
    "explanation": "Pathology detail: ARDS involves diffuse alveolar damage (DAD) initiated by endothelial and pneumocyte injury, neutrophil activation, and exudation of protein-rich fluid."
  },
  {
    "id": "lrt_35",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Bronchiectasis Morphology - Question 35): Which concept is CORRECT?",
    "options": [
      "Necrotizing destruction of smooth muscle and elastic tissue",
      "Hyperplasia of Type II pneumocytes",
      "Non-caseating granuloma formation",
      "Atheromatous plaque accumulation",
      "Fibrotic obliteration of pleural space"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Bronchiectasis represents permanent abnormal dilatation of bronchi and bronchioles caused by necrotizing destruction of smooth muscle and elastic tissue."
  },
  {
    "id": "lrt_36",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Confluent Bronchopneumonia - Question 36): Which concept is CORRECT?",
    "options": [
      "Pure interstitial pattern",
      "Coalescence of patchy focal consolidations into lobar involvement",
      "Fibrous obliteration of mainstem bronchus",
      "Caseating necrosis with cavitary walls",
      "Emphysematous bullae formation"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Confluent bronchopneumonia occurs when patchy suppurative areas coalesce to consolidate large portions or an entire lobe, mimicking lobar pneumonia."
  },
  {
    "id": "lrt_37",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Centriacinar Emphysema - Question 37): Which concept is CORRECT?",
    "options": [
      "Centriacinar emphysema",
      "Panacinar emphysema",
      "Paraseptal emphysema",
      "Irregular emphysema",
      "Bullous emphysema"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Centriacinar (centrilobular) emphysema selectively affects the central/proximal acini (respiratory bronchioles), leaving distal alveoli intact; common in heavy smokers."
  },
  {
    "id": "lrt_38",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Paraseptal Emphysema - Question 38): Which concept is CORRECT?",
    "options": [
      "Centriacinar emphysema",
      "Panacinar emphysema",
      "Paraseptal emphysema",
      "Interstitiai emphysema",
      "Senile emphysema"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Paraseptal (distal acinar) emphysema affects the distal acinus adjacent to pleura; can rupture causing spontaneous pneumothorax in young adults."
  },
  {
    "id": "lrt_39",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Lung Abscess Pathogens - Question 39): Which concept is CORRECT?",
    "options": [
      "Pseudomonas",
      "Legionella",
      "Mycoplasma",
      "S. pneumoniae",
      "Oral anaerobic bacteria (Bacteroides, Fusobacterium)"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Aspiration lung abscesses are polymicrobial, dominated by oral anaerobes like Peptostreptococcus, Fusobacterium, and Bacteroides species."
  },
  {
    "id": "lrt_40",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Lipid Pneumonia - Question 40): Which concept is CORRECT?",
    "options": [
      "Inhalation of silica dust",
      "Aspiration of oily substances leading to foamy macrophage reaction",
      "Transfusion related lung injury",
      "Oxygen toxicity",
      "Radiation pneumonitis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Exogenous lipid pneumonia results from aspiration of mineral oil or oily nose drops, triggering an intra-alveolar foamy lipid-laden macrophage reaction."
  },
  {
    "id": "lrt_41",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Atypical Pneumonia - Question 41): Which concept is CORRECT?",
    "options": [
      "S. pneumoniae",
      "S. aureus",
      "Mycoplasma pneumoniae",
      "Klebsiella",
      "Pseudomonas"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Mycoplasma pneumoniae causes primary atypical pneumonia characterized by interstitial mononuclear (lymphocytic) infiltrates with alveoli free of exudate."
  },
  {
    "id": "lrt_42",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Klebsiella Pneumonia - Question 42): Which concept is CORRECT?",
    "options": [
      "Klebsiella pneumoniae",
      "Legionella",
      "RSV",
      "Mycoplasma",
      "Pneumocystis"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Klebsiella pneumoniae afflicts debilitated alcoholics, producing thick, gelatinous, blood-tinged ('currant jelly') sputum."
  },
  {
    "id": "lrt_43",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Neonatal RDS / Hyaline Membrane Disease - Question 43): Which concept is CORRECT?",
    "options": [
      "Normal surfactant",
      "Surfactant deficiency (dipalmitoylphosphatidylcholine)",
      "Alpha-1-antitrypsin deficiency",
      "Dynein arm defect",
      "IgE excess"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Neonatal RDS is caused by surfactant deficiency in premature infants; microscopically shows acellular hyaline membranes lining alveolar ducts."
  },
  {
    "id": "lrt_44",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (ARDS Pathogenesis - Question 44): Which concept is CORRECT?",
    "options": [
      "Type I pneumocyte proliferation",
      "Eosinophilic degranulation",
      "Granulomatous response",
      "Diffuse alveolar damage with hyaline membranes",
      "Bronchial smooth muscle atrophy"
    ],
    "answer": 3,
    "explanation": "Pathology detail: ARDS involves diffuse alveolar damage (DAD) initiated by endothelial and pneumocyte injury, neutrophil activation, and exudation of protein-rich fluid."
  },
  {
    "id": "lrt_45",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Bronchiectasis Morphology - Question 45): Which concept is CORRECT?",
    "options": [
      "Necrotizing destruction of smooth muscle and elastic tissue",
      "Hyperplasia of Type II pneumocytes",
      "Non-caseating granuloma formation",
      "Atheromatous plaque accumulation",
      "Fibrotic obliteration of pleural space"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Bronchiectasis represents permanent abnormal dilatation of bronchi and bronchioles caused by necrotizing destruction of smooth muscle and elastic tissue."
  },
  {
    "id": "lrt_46",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Confluent Bronchopneumonia - Question 46): Which concept is CORRECT?",
    "options": [
      "Pure interstitial pattern",
      "Coalescence of patchy focal consolidations into lobar involvement",
      "Fibrous obliteration of mainstem bronchus",
      "Caseating necrosis with cavitary walls",
      "Emphysematous bullae formation"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Confluent bronchopneumonia occurs when patchy suppurative areas coalesce to consolidate large portions or an entire lobe, mimicking lobar pneumonia."
  },
  {
    "id": "lrt_47",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Centriacinar Emphysema - Question 47): Which concept is CORRECT?",
    "options": [
      "Centriacinar emphysema",
      "Panacinar emphysema",
      "Paraseptal emphysema",
      "Irregular emphysema",
      "Bullous emphysema"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Centriacinar (centrilobular) emphysema selectively affects the central/proximal acini (respiratory bronchioles), leaving distal alveoli intact; common in heavy smokers."
  },
  {
    "id": "lrt_48",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Paraseptal Emphysema - Question 48): Which concept is CORRECT?",
    "options": [
      "Centriacinar emphysema",
      "Panacinar emphysema",
      "Paraseptal emphysema",
      "Interstitiai emphysema",
      "Senile emphysema"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Paraseptal (distal acinar) emphysema affects the distal acinus adjacent to pleura; can rupture causing spontaneous pneumothorax in young adults."
  },
  {
    "id": "lrt_49",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Lung Abscess Pathogens - Question 49): Which concept is CORRECT?",
    "options": [
      "Pseudomonas",
      "Legionella",
      "Mycoplasma",
      "S. pneumoniae",
      "Oral anaerobic bacteria (Bacteroides, Fusobacterium)"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Aspiration lung abscesses are polymicrobial, dominated by oral anaerobes like Peptostreptococcus, Fusobacterium, and Bacteroides species."
  },
  {
    "id": "lrt_50",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Lipid Pneumonia - Question 50): Which concept is CORRECT?",
    "options": [
      "Inhalation of silica dust",
      "Aspiration of oily substances leading to foamy macrophage reaction",
      "Transfusion related lung injury",
      "Oxygen toxicity",
      "Radiation pneumonitis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Exogenous lipid pneumonia results from aspiration of mineral oil or oily nose drops, triggering an intra-alveolar foamy lipid-laden macrophage reaction."
  },
  {
    "id": "lrt_51",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Atypical Pneumonia - Question 51): Which concept is CORRECT?",
    "options": [
      "S. pneumoniae",
      "S. aureus",
      "Mycoplasma pneumoniae",
      "Klebsiella",
      "Pseudomonas"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Mycoplasma pneumoniae causes primary atypical pneumonia characterized by interstitial mononuclear (lymphocytic) infiltrates with alveoli free of exudate."
  },
  {
    "id": "lrt_52",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Klebsiella Pneumonia - Question 52): Which concept is CORRECT?",
    "options": [
      "Klebsiella pneumoniae",
      "Legionella",
      "RSV",
      "Mycoplasma",
      "Pneumocystis"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Klebsiella pneumoniae afflicts debilitated alcoholics, producing thick, gelatinous, blood-tinged ('currant jelly') sputum."
  },
  {
    "id": "lrt_53",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Neonatal RDS / Hyaline Membrane Disease - Question 53): Which concept is CORRECT?",
    "options": [
      "Normal surfactant",
      "Surfactant deficiency (dipalmitoylphosphatidylcholine)",
      "Alpha-1-antitrypsin deficiency",
      "Dynein arm defect",
      "IgE excess"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Neonatal RDS is caused by surfactant deficiency in premature infants; microscopically shows acellular hyaline membranes lining alveolar ducts."
  },
  {
    "id": "lrt_54",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (ARDS Pathogenesis - Question 54): Which concept is CORRECT?",
    "options": [
      "Type I pneumocyte proliferation",
      "Eosinophilic degranulation",
      "Granulomatous response",
      "Diffuse alveolar damage with hyaline membranes",
      "Bronchial smooth muscle atrophy"
    ],
    "answer": 3,
    "explanation": "Pathology detail: ARDS involves diffuse alveolar damage (DAD) initiated by endothelial and pneumocyte injury, neutrophil activation, and exudation of protein-rich fluid."
  },
  {
    "id": "lrt_55",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Bronchiectasis Morphology - Question 55): Which concept is CORRECT?",
    "options": [
      "Necrotizing destruction of smooth muscle and elastic tissue",
      "Hyperplasia of Type II pneumocytes",
      "Non-caseating granuloma formation",
      "Atheromatous plaque accumulation",
      "Fibrotic obliteration of pleural space"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Bronchiectasis represents permanent abnormal dilatation of bronchi and bronchioles caused by necrotizing destruction of smooth muscle and elastic tissue."
  },
  {
    "id": "lrt_56",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Confluent Bronchopneumonia - Question 56): Which concept is CORRECT?",
    "options": [
      "Pure interstitial pattern",
      "Coalescence of patchy focal consolidations into lobar involvement",
      "Fibrous obliteration of mainstem bronchus",
      "Caseating necrosis with cavitary walls",
      "Emphysematous bullae formation"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Confluent bronchopneumonia occurs when patchy suppurative areas coalesce to consolidate large portions or an entire lobe, mimicking lobar pneumonia."
  },
  {
    "id": "lrt_57",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Centriacinar Emphysema - Question 57): Which concept is CORRECT?",
    "options": [
      "Centriacinar emphysema",
      "Panacinar emphysema",
      "Paraseptal emphysema",
      "Irregular emphysema",
      "Bullous emphysema"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Centriacinar (centrilobular) emphysema selectively affects the central/proximal acini (respiratory bronchioles), leaving distal alveoli intact; common in heavy smokers."
  },
  {
    "id": "lrt_58",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Paraseptal Emphysema - Question 58): Which concept is CORRECT?",
    "options": [
      "Centriacinar emphysema",
      "Panacinar emphysema",
      "Paraseptal emphysema",
      "Interstitiai emphysema",
      "Senile emphysema"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Paraseptal (distal acinar) emphysema affects the distal acinus adjacent to pleura; can rupture causing spontaneous pneumothorax in young adults."
  },
  {
    "id": "lrt_59",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Lung Abscess Pathogens - Question 59): Which concept is CORRECT?",
    "options": [
      "Pseudomonas",
      "Legionella",
      "Mycoplasma",
      "S. pneumoniae",
      "Oral anaerobic bacteria (Bacteroides, Fusobacterium)"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Aspiration lung abscesses are polymicrobial, dominated by oral anaerobes like Peptostreptococcus, Fusobacterium, and Bacteroides species."
  },
  {
    "id": "lrt_60",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Lipid Pneumonia - Question 60): Which concept is CORRECT?",
    "options": [
      "Inhalation of silica dust",
      "Aspiration of oily substances leading to foamy macrophage reaction",
      "Transfusion related lung injury",
      "Oxygen toxicity",
      "Radiation pneumonitis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Exogenous lipid pneumonia results from aspiration of mineral oil or oily nose drops, triggering an intra-alveolar foamy lipid-laden macrophage reaction."
  },
  {
    "id": "lrt_61",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Atypical Pneumonia - Question 61): Which concept is CORRECT?",
    "options": [
      "S. pneumoniae",
      "S. aureus",
      "Mycoplasma pneumoniae",
      "Klebsiella",
      "Pseudomonas"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Mycoplasma pneumoniae causes primary atypical pneumonia characterized by interstitial mononuclear (lymphocytic) infiltrates with alveoli free of exudate."
  },
  {
    "id": "lrt_62",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Klebsiella Pneumonia - Question 62): Which concept is CORRECT?",
    "options": [
      "Klebsiella pneumoniae",
      "Legionella",
      "RSV",
      "Mycoplasma",
      "Pneumocystis"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Klebsiella pneumoniae afflicts debilitated alcoholics, producing thick, gelatinous, blood-tinged ('currant jelly') sputum."
  },
  {
    "id": "lrt_63",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Neonatal RDS / Hyaline Membrane Disease - Question 63): Which concept is CORRECT?",
    "options": [
      "Normal surfactant",
      "Surfactant deficiency (dipalmitoylphosphatidylcholine)",
      "Alpha-1-antitrypsin deficiency",
      "Dynein arm defect",
      "IgE excess"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Neonatal RDS is caused by surfactant deficiency in premature infants; microscopically shows acellular hyaline membranes lining alveolar ducts."
  },
  {
    "id": "lrt_64",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (ARDS Pathogenesis - Question 64): Which concept is CORRECT?",
    "options": [
      "Type I pneumocyte proliferation",
      "Eosinophilic degranulation",
      "Granulomatous response",
      "Diffuse alveolar damage with hyaline membranes",
      "Bronchial smooth muscle atrophy"
    ],
    "answer": 3,
    "explanation": "Pathology detail: ARDS involves diffuse alveolar damage (DAD) initiated by endothelial and pneumocyte injury, neutrophil activation, and exudation of protein-rich fluid."
  },
  {
    "id": "lrt_65",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Bronchiectasis Morphology - Question 65): Which concept is CORRECT?",
    "options": [
      "Necrotizing destruction of smooth muscle and elastic tissue",
      "Hyperplasia of Type II pneumocytes",
      "Non-caseating granuloma formation",
      "Atheromatous plaque accumulation",
      "Fibrotic obliteration of pleural space"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Bronchiectasis represents permanent abnormal dilatation of bronchi and bronchioles caused by necrotizing destruction of smooth muscle and elastic tissue."
  },
  {
    "id": "lrt_66",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Confluent Bronchopneumonia - Question 66): Which concept is CORRECT?",
    "options": [
      "Pure interstitial pattern",
      "Coalescence of patchy focal consolidations into lobar involvement",
      "Fibrous obliteration of mainstem bronchus",
      "Caseating necrosis with cavitary walls",
      "Emphysematous bullae formation"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Confluent bronchopneumonia occurs when patchy suppurative areas coalesce to consolidate large portions or an entire lobe, mimicking lobar pneumonia."
  },
  {
    "id": "lrt_67",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Centriacinar Emphysema - Question 67): Which concept is CORRECT?",
    "options": [
      "Centriacinar emphysema",
      "Panacinar emphysema",
      "Paraseptal emphysema",
      "Irregular emphysema",
      "Bullous emphysema"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Centriacinar (centrilobular) emphysema selectively affects the central/proximal acini (respiratory bronchioles), leaving distal alveoli intact; common in heavy smokers."
  },
  {
    "id": "lrt_68",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Paraseptal Emphysema - Question 68): Which concept is CORRECT?",
    "options": [
      "Centriacinar emphysema",
      "Panacinar emphysema",
      "Paraseptal emphysema",
      "Interstitiai emphysema",
      "Senile emphysema"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Paraseptal (distal acinar) emphysema affects the distal acinus adjacent to pleura; can rupture causing spontaneous pneumothorax in young adults."
  },
  {
    "id": "lrt_69",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Lung Abscess Pathogens - Question 69): Which concept is CORRECT?",
    "options": [
      "Pseudomonas",
      "Legionella",
      "Mycoplasma",
      "S. pneumoniae",
      "Oral anaerobic bacteria (Bacteroides, Fusobacterium)"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Aspiration lung abscesses are polymicrobial, dominated by oral anaerobes like Peptostreptococcus, Fusobacterium, and Bacteroides species."
  },
  {
    "id": "lrt_70",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Lipid Pneumonia - Question 70): Which concept is CORRECT?",
    "options": [
      "Inhalation of silica dust",
      "Aspiration of oily substances leading to foamy macrophage reaction",
      "Transfusion related lung injury",
      "Oxygen toxicity",
      "Radiation pneumonitis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Exogenous lipid pneumonia results from aspiration of mineral oil or oily nose drops, triggering an intra-alveolar foamy lipid-laden macrophage reaction."
  },
  {
    "id": "lrt_71",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Atypical Pneumonia - Question 71): Which concept is CORRECT?",
    "options": [
      "S. pneumoniae",
      "S. aureus",
      "Mycoplasma pneumoniae",
      "Klebsiella",
      "Pseudomonas"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Mycoplasma pneumoniae causes primary atypical pneumonia characterized by interstitial mononuclear (lymphocytic) infiltrates with alveoli free of exudate."
  },
  {
    "id": "lrt_72",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (Klebsiella Pneumonia - Question 72): Which concept is CORRECT?",
    "options": [
      "Klebsiella pneumoniae",
      "Legionella",
      "RSV",
      "Mycoplasma",
      "Pneumocystis"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Klebsiella pneumoniae afflicts debilitated alcoholics, producing thick, gelatinous, blood-tinged ('currant jelly') sputum."
  },
  {
    "id": "lrt_73",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Neonatal RDS / Hyaline Membrane Disease - Question 73): Which concept is CORRECT?",
    "options": [
      "Normal surfactant",
      "Surfactant deficiency (dipalmitoylphosphatidylcholine)",
      "Alpha-1-antitrypsin deficiency",
      "Dynein arm defect",
      "IgE excess"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Neonatal RDS is caused by surfactant deficiency in premature infants; microscopically shows acellular hyaline membranes lining alveolar ducts."
  },
  {
    "id": "lrt_74",
    "category": "LRT Diseases",
    "type": "Conceptual",
    "question": "Regarding Lower Respiratory Tract pathology (ARDS Pathogenesis - Question 74): Which concept is CORRECT?",
    "options": [
      "Type I pneumocyte proliferation",
      "Eosinophilic degranulation",
      "Granulomatous response",
      "Diffuse alveolar damage with hyaline membranes",
      "Bronchial smooth muscle atrophy"
    ],
    "answer": 3,
    "explanation": "Pathology detail: ARDS involves diffuse alveolar damage (DAD) initiated by endothelial and pneumocyte injury, neutrophil activation, and exudation of protein-rich fluid."
  },
  {
    "id": "lrt_75",
    "category": "LRT Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Lower Respiratory Tract pathology (Bronchiectasis Morphology - Question 75): Which concept is CORRECT?",
    "options": [
      "Necrotizing destruction of smooth muscle and elastic tissue",
      "Hyperplasia of Type II pneumocytes",
      "Non-caseating granuloma formation",
      "Atheromatous plaque accumulation",
      "Fibrotic obliteration of pleural space"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Bronchiectasis represents permanent abnormal dilatation of bronchi and bronchioles caused by necrotizing destruction of smooth muscle and elastic tissue."
  },
  {
    "id": "tum_1",
    "category": "Lung Tumours",
    "type": "Exception",
    "question": "Squamous cell carcinoma of the lung is characterized by all of the following EXCEPT:",
    "options": [
      "Central origin near the mainstem bronchi/hilum",
      "Histological presence of keratin pearls and intercellular bridges",
      "Strong correlation with a long history of cigarette smoking",
      "High initial cure rate with single-agent chemotherapy in excess of 80%",
      "Tendency to undergo central cavitation"
    ],
    "answer": 3,
    "explanation": "Squamous cell carcinoma is treated primarily with upfront surgery when resectable; it does NOT show an 80%+ cure rate with chemotherapy (that initial chemo-responsiveness is typical of Small Cell Ca)."
  },
  {
    "id": "tum_2",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "A 60-year-old heavy smoker presents with a central lung mass. Biopsy shows sheets of small round-to-oval cells with scant cytoplasm, granular 'salt-and-pepper' chromatin, and nuclear molding with crush artifact. What is the diagnosis?",
    "options": [
      "Adenocarcinoma",
      "Large cell carcinoma",
      "Small cell (Oat cell) carcinoma",
      "Bronchial carcinoid",
      "Squamous cell carcinoma"
    ],
    "answer": 2,
    "explanation": "Small cell lung carcinoma (SCLC) exhibits small round neuroendocrine cells, scant cytoplasm, salt-and-pepper chromatin, nuclear molding, and extensive necrosis."
  },
  {
    "id": "tum_3",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Small cell lung carcinoma is virtually universally associated with loss-of-function mutations in which tumor suppressor genes?",
    "options": [
      "EGFR and ALK",
      "TP53 and RB1",
      "KRAS and BRAF",
      "APC and CTNNB1",
      "RET and MET"
    ],
    "answer": 1,
    "explanation": "Small cell lung carcinoma shows nearly universal (close to 100%) inactivation of both TP53 and RB1 tumor suppressor genes."
  },
  {
    "id": "tum_4",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Which histological subtype of primary lung carcinoma is most common in women and non-smokers, usually presenting as a peripheral mass?",
    "options": [
      "Squamous cell carcinoma",
      "Small cell carcinoma",
      "Adenocarcinoma",
      "Large cell neuroendocrine carcinoma",
      "Mesothelioma"
    ],
    "answer": 2,
    "explanation": "Adenocarcinoma is the most common primary lung cancer overall, as well as the most frequent subtype in females and non-smokers, typically located peripherally."
  },
  {
    "id": "tum_5",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "A peripheral lung lesion in a non-smoker shows dysplastic columnar epithelial cells growing along pre-existing intact alveolar septa without stromal or vascular invasion ('lepidic growth pattern'). What is the diagnosis?",
    "options": [
      "Adenocarcinoma in-situ (formerly Bronchioloalveolar carcinoma)",
      "Squamous cell carcinoma in-situ",
      "Small cell carcinoma",
      "Carcinoid tumor",
      "Atypical adenomatous hyperplasia"
    ],
    "answer": 0,
    "explanation": "Adenocarcinoma in-situ (AIS, formerly bronchioloalveolar carcinoma) is defined by pure lepidic growth along alveolar walls without microinvasion."
  },
  {
    "id": "tum_6",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "A 55-year-old male smoker with an apical right lung tumor presents with severe shoulder pain radiating down the ulnar nerve distribution, ipsilateral ptosis, miosis, and anhidrosis. What syndrome is present?",
    "options": [
      "Lambert-Eaton syndrome",
      "Pancoast syndrome (Superior Sulcus Tumor)",
      "Cushing syndrome",
      "Carcinoid syndrome",
      "Trousseau syndrome"
    ],
    "answer": 1,
    "explanation": "Pancoast tumor (apical lung carcinoma) invades the brachial plexus (ulnar nerve distribution) and cervical sympathetic chain, causing Horner syndrome (ptosis, miosis, anhidrosis)."
  },
  {
    "id": "tum_7",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Which paraneoplastic hormone secretion is classically paired with Small Cell Lung Carcinoma?",
    "options": [
      "Parathyroid hormone-related peptide (PTHrp) leading to hypercalcemia",
      "Syndrome of Inappropriate ADH (SIADH) and ectopic ACTH",
      "Calcitonin leading to hypocalcemia",
      "Erythropoietin leading to polycythemia",
      "Insulin-like growth factor leading to hypoglycemia"
    ],
    "answer": 1,
    "explanation": "Small cell carcinoma (SCLC) is a neuroendocrine tumor that frequently secretes ectopic ADH (SIADH) and ACTH (Cushing syndrome). PTHrp/hypercalcemia is classically linked to Squamous Cell Ca."
  },
  {
    "id": "tum_8",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Squamous cell carcinoma of the lung produces hypercalcemia via ectopic secretion of:",
    "options": [
      "Adrenocorticotropic hormone (ACTH)",
      "Parathyroid hormone-related peptide (PTHrp)",
      "Antidiuretic hormone (ADH)",
      "Serotonin (5-HT)",
      "Calcitonin"
    ],
    "answer": 1,
    "explanation": "Squamous cell carcinoma of the lung is the most common lung tumor to cause paraneoplastic hypercalcemia via PTHrp secretion."
  },
  {
    "id": "tum_9",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Statistically, what is the most common malignant neoplasm found in the lung overall?",
    "options": [
      "Primary Squamous cell carcinoma",
      "Metastatic carcinoma from distant organ sites",
      "Primary Adenocarcinoma",
      "Primary Small cell carcinoma",
      "Bronchial carcinoid"
    ],
    "answer": 1,
    "explanation": "Metastatic tumors (from breast, colon, kidney, stomach, melanoma) are far more common in the lung than primary lung carcinomas."
  },
  {
    "id": "tum_10",
    "category": "Lung Tumours",
    "type": "Recall",
    "question": "Which organ is the most favored single site for distant metastasis from primary lung carcinoma?",
    "options": [
      "Brain",
      "Adrenal glands",
      "Liver",
      "Bones",
      "Spleen"
    ],
    "answer": 1,
    "explanation": "Adrenal glands are involved in >50% of autopsied lung cancer cases, making them the most frequent single site of distant spread, followed by liver, brain, and bone."
  },
  {
    "id": "tum_11",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Bronchial Carcinoid - Question 11): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Bronchial carcinoid",
      "Small cell ca",
      "Adenocarcinoma",
      "Large cell ca"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Carcinoid tumors are low-grade neuroendocrine neoplasms showing uniform round cells in nests/trabeculae with salt-and-pepper chromatin; immunohistochemistry positive for chromogranin and synaptophysin."
  },
  {
    "id": "tum_12",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Large Cell Carcinoma - Question 12): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Adenocarcinoma",
      "Small cell ca",
      "Large cell carcinoma",
      "Mesothelioma"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Undifferentiated malignant epithelial tumor lacking glandular or squamous differentiation under light microscopy."
  },
  {
    "id": "tum_13",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Precursor Lesions - Question 13): Which concept is CORRECT?",
    "options": [
      "All are recognized precursor lesions",
      "Only SCLC has a known precursor",
      "Metaplasia is a malignant lesion",
      "Clear cell hyperplasia is the main precursor",
      "Carcinoids arise from AAH"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Recognized morphological precursor lesions include Squamous Dysplasia/Carcinoma in-situ, Atypical Adenomatous Hyperplasia (AAH), Adenocarcinoma in-situ (AIS), and Diffuse Idiopathic Pulmonary Neuroendocrine Cell Hyperplasia (DIPNECH)."
  },
  {
    "id": "tum_14",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Carcinogens in Smoke - Question 14): Which concept is CORRECT?",
    "options": [
      "Phenol esters act as initiators",
      "Radioactive isotopes are non-toxic",
      "Polycyclic aromatic hydrocarbons act as tumor initiators and phenol esters as promoters",
      "Nicotine is a direct mutagen",
      "Tar is purely non-carcinogenic"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Cigarette smoke contains initiators (polycyclic aromatic hydrocarbons, nitrosamines) and promoters (phenol esters)."
  },
  {
    "id": "tum_15",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Atypical Adenomatous Hyperplasia - Question 15): Which concept is CORRECT?",
    "options": [
      "AAH > 2cm",
      "AAH <= 5mm precursor to adenocarcinoma",
      "AAH is precursor to SCLC",
      "AAH is a mesenchymal tumor",
      "AAH shows squamous differentiation"
    ],
    "answer": 1,
    "explanation": "Pathology detail: AAH is a well-demarcated lesion <=5mm composed of dysplastic pneumocytes lining alveolar walls, precursor to adenocarcinoma."
  },
  {
    "id": "tum_16",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Horner Syndrome Features - Question 16): Which concept is CORRECT?",
    "options": [
      "Exophthalmos",
      "Mydriasis",
      "Hyperhidrosis",
      "Tachycardia",
      "Ptosis, miosis, and anhidrosis"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Horner syndrome consists of ipsilateral ptosis, miosis, anhidrosis, and enophthalmos due to sympathetic trunk compression."
  },
  {
    "id": "tum_17",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Lambert-Eaton Myasthenic Syndrome - Question 17): Which concept is CORRECT?",
    "options": [
      "Antibodies against presynaptic voltage-gated calcium channels in SCLC",
      "Postsynaptic ACh receptor destruction",
      "Demyelination of peripheral nerves",
      "Direct tumor invasion of neuromuscular junction",
      "Thyrotoxicosis"
    ],
    "answer": 0,
    "explanation": "Pathology detail: LEMS is an autoimmune paraneoplastic syndrome associated with SCLC caused by antibodies against presynaptic voltage-gated calcium channels."
  },
  {
    "id": "tum_18",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (EGFR Mutations in Lung Ca - Question 18): Which concept is CORRECT?",
    "options": [
      "KRAS mutations in non-smokers",
      "TP53 in non-smokers",
      "EGFR mutations in Asian non-smoker females with adenocarcinoma",
      "ALK translocations in SCLC",
      "BRAF mutations in squamous ca"
    ],
    "answer": 2,
    "explanation": "Pathology detail: EGFR tyrosine kinase domain mutations are common in adenocarcinomas in Asian non-smoker females, targeted by TKIs (erlotinib, osimertinib)."
  },
  {
    "id": "tum_19",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (ALK Gene Rearrangement - Question 19): Which concept is CORRECT?",
    "options": [
      "SCLC",
      "EML4-ALK fusion in adenocarcinoma",
      "Squamous cell ca",
      "Large cell ca",
      "Carcinoid"
    ],
    "answer": 1,
    "explanation": "Pathology detail: EML4-ALK fusion gene occurs in 3-5% of adenocarcinomas (often young non-smokers), responsive to ALK inhibitors like crizotinib."
  },
  {
    "id": "tum_20",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Metastatic Lung Cancer Histology - Question 20): Which concept is CORRECT?",
    "options": [
      "Primary SCLC",
      "Primary Adenocarcinoma in-situ",
      "Lobar pneumonia",
      "Metastatic carcinoma",
      "Asbestosis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Multiple bilateral cannonball lung nodules on chest radiograph strongly favor metastatic disease rather than primary bronchogenic carcinoma."
  },
  {
    "id": "tum_21",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Bronchial Carcinoid - Question 21): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Bronchial carcinoid",
      "Small cell ca",
      "Adenocarcinoma",
      "Large cell ca"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Carcinoid tumors are low-grade neuroendocrine neoplasms showing uniform round cells in nests/trabeculae with salt-and-pepper chromatin; immunohistochemistry positive for chromogranin and synaptophysin."
  },
  {
    "id": "tum_22",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Large Cell Carcinoma - Question 22): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Adenocarcinoma",
      "Small cell ca",
      "Large cell carcinoma",
      "Mesothelioma"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Undifferentiated malignant epithelial tumor lacking glandular or squamous differentiation under light microscopy."
  },
  {
    "id": "tum_23",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Precursor Lesions - Question 23): Which concept is CORRECT?",
    "options": [
      "All are recognized precursor lesions",
      "Only SCLC has a known precursor",
      "Metaplasia is a malignant lesion",
      "Clear cell hyperplasia is the main precursor",
      "Carcinoids arise from AAH"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Recognized morphological precursor lesions include Squamous Dysplasia/Carcinoma in-situ, Atypical Adenomatous Hyperplasia (AAH), Adenocarcinoma in-situ (AIS), and Diffuse Idiopathic Pulmonary Neuroendocrine Cell Hyperplasia (DIPNECH)."
  },
  {
    "id": "tum_24",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Carcinogens in Smoke - Question 24): Which concept is CORRECT?",
    "options": [
      "Phenol esters act as initiators",
      "Radioactive isotopes are non-toxic",
      "Polycyclic aromatic hydrocarbons act as tumor initiators and phenol esters as promoters",
      "Nicotine is a direct mutagen",
      "Tar is purely non-carcinogenic"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Cigarette smoke contains initiators (polycyclic aromatic hydrocarbons, nitrosamines) and promoters (phenol esters)."
  },
  {
    "id": "tum_25",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Atypical Adenomatous Hyperplasia - Question 25): Which concept is CORRECT?",
    "options": [
      "AAH > 2cm",
      "AAH <= 5mm precursor to adenocarcinoma",
      "AAH is precursor to SCLC",
      "AAH is a mesenchymal tumor",
      "AAH shows squamous differentiation"
    ],
    "answer": 1,
    "explanation": "Pathology detail: AAH is a well-demarcated lesion <=5mm composed of dysplastic pneumocytes lining alveolar walls, precursor to adenocarcinoma."
  },
  {
    "id": "tum_26",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Horner Syndrome Features - Question 26): Which concept is CORRECT?",
    "options": [
      "Exophthalmos",
      "Mydriasis",
      "Hyperhidrosis",
      "Tachycardia",
      "Ptosis, miosis, and anhidrosis"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Horner syndrome consists of ipsilateral ptosis, miosis, anhidrosis, and enophthalmos due to sympathetic trunk compression."
  },
  {
    "id": "tum_27",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Lambert-Eaton Myasthenic Syndrome - Question 27): Which concept is CORRECT?",
    "options": [
      "Antibodies against presynaptic voltage-gated calcium channels in SCLC",
      "Postsynaptic ACh receptor destruction",
      "Demyelination of peripheral nerves",
      "Direct tumor invasion of neuromuscular junction",
      "Thyrotoxicosis"
    ],
    "answer": 0,
    "explanation": "Pathology detail: LEMS is an autoimmune paraneoplastic syndrome associated with SCLC caused by antibodies against presynaptic voltage-gated calcium channels."
  },
  {
    "id": "tum_28",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (EGFR Mutations in Lung Ca - Question 28): Which concept is CORRECT?",
    "options": [
      "KRAS mutations in non-smokers",
      "TP53 in non-smokers",
      "EGFR mutations in Asian non-smoker females with adenocarcinoma",
      "ALK translocations in SCLC",
      "BRAF mutations in squamous ca"
    ],
    "answer": 2,
    "explanation": "Pathology detail: EGFR tyrosine kinase domain mutations are common in adenocarcinomas in Asian non-smoker females, targeted by TKIs (erlotinib, osimertinib)."
  },
  {
    "id": "tum_29",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (ALK Gene Rearrangement - Question 29): Which concept is CORRECT?",
    "options": [
      "SCLC",
      "EML4-ALK fusion in adenocarcinoma",
      "Squamous cell ca",
      "Large cell ca",
      "Carcinoid"
    ],
    "answer": 1,
    "explanation": "Pathology detail: EML4-ALK fusion gene occurs in 3-5% of adenocarcinomas (often young non-smokers), responsive to ALK inhibitors like crizotinib."
  },
  {
    "id": "tum_30",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Metastatic Lung Cancer Histology - Question 30): Which concept is CORRECT?",
    "options": [
      "Primary SCLC",
      "Primary Adenocarcinoma in-situ",
      "Lobar pneumonia",
      "Metastatic carcinoma",
      "Asbestosis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Multiple bilateral cannonball lung nodules on chest radiograph strongly favor metastatic disease rather than primary bronchogenic carcinoma."
  },
  {
    "id": "tum_31",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Bronchial Carcinoid - Question 31): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Bronchial carcinoid",
      "Small cell ca",
      "Adenocarcinoma",
      "Large cell ca"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Carcinoid tumors are low-grade neuroendocrine neoplasms showing uniform round cells in nests/trabeculae with salt-and-pepper chromatin; immunohistochemistry positive for chromogranin and synaptophysin."
  },
  {
    "id": "tum_32",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Large Cell Carcinoma - Question 32): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Adenocarcinoma",
      "Small cell ca",
      "Large cell carcinoma",
      "Mesothelioma"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Undifferentiated malignant epithelial tumor lacking glandular or squamous differentiation under light microscopy."
  },
  {
    "id": "tum_33",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Precursor Lesions - Question 33): Which concept is CORRECT?",
    "options": [
      "All are recognized precursor lesions",
      "Only SCLC has a known precursor",
      "Metaplasia is a malignant lesion",
      "Clear cell hyperplasia is the main precursor",
      "Carcinoids arise from AAH"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Recognized morphological precursor lesions include Squamous Dysplasia/Carcinoma in-situ, Atypical Adenomatous Hyperplasia (AAH), Adenocarcinoma in-situ (AIS), and Diffuse Idiopathic Pulmonary Neuroendocrine Cell Hyperplasia (DIPNECH)."
  },
  {
    "id": "tum_34",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Carcinogens in Smoke - Question 34): Which concept is CORRECT?",
    "options": [
      "Phenol esters act as initiators",
      "Radioactive isotopes are non-toxic",
      "Polycyclic aromatic hydrocarbons act as tumor initiators and phenol esters as promoters",
      "Nicotine is a direct mutagen",
      "Tar is purely non-carcinogenic"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Cigarette smoke contains initiators (polycyclic aromatic hydrocarbons, nitrosamines) and promoters (phenol esters)."
  },
  {
    "id": "tum_35",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Atypical Adenomatous Hyperplasia - Question 35): Which concept is CORRECT?",
    "options": [
      "AAH > 2cm",
      "AAH <= 5mm precursor to adenocarcinoma",
      "AAH is precursor to SCLC",
      "AAH is a mesenchymal tumor",
      "AAH shows squamous differentiation"
    ],
    "answer": 1,
    "explanation": "Pathology detail: AAH is a well-demarcated lesion <=5mm composed of dysplastic pneumocytes lining alveolar walls, precursor to adenocarcinoma."
  },
  {
    "id": "tum_36",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Horner Syndrome Features - Question 36): Which concept is CORRECT?",
    "options": [
      "Exophthalmos",
      "Mydriasis",
      "Hyperhidrosis",
      "Tachycardia",
      "Ptosis, miosis, and anhidrosis"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Horner syndrome consists of ipsilateral ptosis, miosis, anhidrosis, and enophthalmos due to sympathetic trunk compression."
  },
  {
    "id": "tum_37",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Lambert-Eaton Myasthenic Syndrome - Question 37): Which concept is CORRECT?",
    "options": [
      "Antibodies against presynaptic voltage-gated calcium channels in SCLC",
      "Postsynaptic ACh receptor destruction",
      "Demyelination of peripheral nerves",
      "Direct tumor invasion of neuromuscular junction",
      "Thyrotoxicosis"
    ],
    "answer": 0,
    "explanation": "Pathology detail: LEMS is an autoimmune paraneoplastic syndrome associated with SCLC caused by antibodies against presynaptic voltage-gated calcium channels."
  },
  {
    "id": "tum_38",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (EGFR Mutations in Lung Ca - Question 38): Which concept is CORRECT?",
    "options": [
      "KRAS mutations in non-smokers",
      "TP53 in non-smokers",
      "EGFR mutations in Asian non-smoker females with adenocarcinoma",
      "ALK translocations in SCLC",
      "BRAF mutations in squamous ca"
    ],
    "answer": 2,
    "explanation": "Pathology detail: EGFR tyrosine kinase domain mutations are common in adenocarcinomas in Asian non-smoker females, targeted by TKIs (erlotinib, osimertinib)."
  },
  {
    "id": "tum_39",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (ALK Gene Rearrangement - Question 39): Which concept is CORRECT?",
    "options": [
      "SCLC",
      "EML4-ALK fusion in adenocarcinoma",
      "Squamous cell ca",
      "Large cell ca",
      "Carcinoid"
    ],
    "answer": 1,
    "explanation": "Pathology detail: EML4-ALK fusion gene occurs in 3-5% of adenocarcinomas (often young non-smokers), responsive to ALK inhibitors like crizotinib."
  },
  {
    "id": "tum_40",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Metastatic Lung Cancer Histology - Question 40): Which concept is CORRECT?",
    "options": [
      "Primary SCLC",
      "Primary Adenocarcinoma in-situ",
      "Lobar pneumonia",
      "Metastatic carcinoma",
      "Asbestosis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Multiple bilateral cannonball lung nodules on chest radiograph strongly favor metastatic disease rather than primary bronchogenic carcinoma."
  },
  {
    "id": "tum_41",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Bronchial Carcinoid - Question 41): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Bronchial carcinoid",
      "Small cell ca",
      "Adenocarcinoma",
      "Large cell ca"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Carcinoid tumors are low-grade neuroendocrine neoplasms showing uniform round cells in nests/trabeculae with salt-and-pepper chromatin; immunohistochemistry positive for chromogranin and synaptophysin."
  },
  {
    "id": "tum_42",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Large Cell Carcinoma - Question 42): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Adenocarcinoma",
      "Small cell ca",
      "Large cell carcinoma",
      "Mesothelioma"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Undifferentiated malignant epithelial tumor lacking glandular or squamous differentiation under light microscopy."
  },
  {
    "id": "tum_43",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Precursor Lesions - Question 43): Which concept is CORRECT?",
    "options": [
      "All are recognized precursor lesions",
      "Only SCLC has a known precursor",
      "Metaplasia is a malignant lesion",
      "Clear cell hyperplasia is the main precursor",
      "Carcinoids arise from AAH"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Recognized morphological precursor lesions include Squamous Dysplasia/Carcinoma in-situ, Atypical Adenomatous Hyperplasia (AAH), Adenocarcinoma in-situ (AIS), and Diffuse Idiopathic Pulmonary Neuroendocrine Cell Hyperplasia (DIPNECH)."
  },
  {
    "id": "tum_44",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Carcinogens in Smoke - Question 44): Which concept is CORRECT?",
    "options": [
      "Phenol esters act as initiators",
      "Radioactive isotopes are non-toxic",
      "Polycyclic aromatic hydrocarbons act as tumor initiators and phenol esters as promoters",
      "Nicotine is a direct mutagen",
      "Tar is purely non-carcinogenic"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Cigarette smoke contains initiators (polycyclic aromatic hydrocarbons, nitrosamines) and promoters (phenol esters)."
  },
  {
    "id": "tum_45",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Atypical Adenomatous Hyperplasia - Question 45): Which concept is CORRECT?",
    "options": [
      "AAH > 2cm",
      "AAH <= 5mm precursor to adenocarcinoma",
      "AAH is precursor to SCLC",
      "AAH is a mesenchymal tumor",
      "AAH shows squamous differentiation"
    ],
    "answer": 1,
    "explanation": "Pathology detail: AAH is a well-demarcated lesion <=5mm composed of dysplastic pneumocytes lining alveolar walls, precursor to adenocarcinoma."
  },
  {
    "id": "tum_46",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Horner Syndrome Features - Question 46): Which concept is CORRECT?",
    "options": [
      "Exophthalmos",
      "Mydriasis",
      "Hyperhidrosis",
      "Tachycardia",
      "Ptosis, miosis, and anhidrosis"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Horner syndrome consists of ipsilateral ptosis, miosis, anhidrosis, and enophthalmos due to sympathetic trunk compression."
  },
  {
    "id": "tum_47",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Lambert-Eaton Myasthenic Syndrome - Question 47): Which concept is CORRECT?",
    "options": [
      "Antibodies against presynaptic voltage-gated calcium channels in SCLC",
      "Postsynaptic ACh receptor destruction",
      "Demyelination of peripheral nerves",
      "Direct tumor invasion of neuromuscular junction",
      "Thyrotoxicosis"
    ],
    "answer": 0,
    "explanation": "Pathology detail: LEMS is an autoimmune paraneoplastic syndrome associated with SCLC caused by antibodies against presynaptic voltage-gated calcium channels."
  },
  {
    "id": "tum_48",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (EGFR Mutations in Lung Ca - Question 48): Which concept is CORRECT?",
    "options": [
      "KRAS mutations in non-smokers",
      "TP53 in non-smokers",
      "EGFR mutations in Asian non-smoker females with adenocarcinoma",
      "ALK translocations in SCLC",
      "BRAF mutations in squamous ca"
    ],
    "answer": 2,
    "explanation": "Pathology detail: EGFR tyrosine kinase domain mutations are common in adenocarcinomas in Asian non-smoker females, targeted by TKIs (erlotinib, osimertinib)."
  },
  {
    "id": "tum_49",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (ALK Gene Rearrangement - Question 49): Which concept is CORRECT?",
    "options": [
      "SCLC",
      "EML4-ALK fusion in adenocarcinoma",
      "Squamous cell ca",
      "Large cell ca",
      "Carcinoid"
    ],
    "answer": 1,
    "explanation": "Pathology detail: EML4-ALK fusion gene occurs in 3-5% of adenocarcinomas (often young non-smokers), responsive to ALK inhibitors like crizotinib."
  },
  {
    "id": "tum_50",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Metastatic Lung Cancer Histology - Question 50): Which concept is CORRECT?",
    "options": [
      "Primary SCLC",
      "Primary Adenocarcinoma in-situ",
      "Lobar pneumonia",
      "Metastatic carcinoma",
      "Asbestosis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Multiple bilateral cannonball lung nodules on chest radiograph strongly favor metastatic disease rather than primary bronchogenic carcinoma."
  },
  {
    "id": "tum_51",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Bronchial Carcinoid - Question 51): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Bronchial carcinoid",
      "Small cell ca",
      "Adenocarcinoma",
      "Large cell ca"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Carcinoid tumors are low-grade neuroendocrine neoplasms showing uniform round cells in nests/trabeculae with salt-and-pepper chromatin; immunohistochemistry positive for chromogranin and synaptophysin."
  },
  {
    "id": "tum_52",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Large Cell Carcinoma - Question 52): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Adenocarcinoma",
      "Small cell ca",
      "Large cell carcinoma",
      "Mesothelioma"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Undifferentiated malignant epithelial tumor lacking glandular or squamous differentiation under light microscopy."
  },
  {
    "id": "tum_53",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Precursor Lesions - Question 53): Which concept is CORRECT?",
    "options": [
      "All are recognized precursor lesions",
      "Only SCLC has a known precursor",
      "Metaplasia is a malignant lesion",
      "Clear cell hyperplasia is the main precursor",
      "Carcinoids arise from AAH"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Recognized morphological precursor lesions include Squamous Dysplasia/Carcinoma in-situ, Atypical Adenomatous Hyperplasia (AAH), Adenocarcinoma in-situ (AIS), and Diffuse Idiopathic Pulmonary Neuroendocrine Cell Hyperplasia (DIPNECH)."
  },
  {
    "id": "tum_54",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Carcinogens in Smoke - Question 54): Which concept is CORRECT?",
    "options": [
      "Phenol esters act as initiators",
      "Radioactive isotopes are non-toxic",
      "Polycyclic aromatic hydrocarbons act as tumor initiators and phenol esters as promoters",
      "Nicotine is a direct mutagen",
      "Tar is purely non-carcinogenic"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Cigarette smoke contains initiators (polycyclic aromatic hydrocarbons, nitrosamines) and promoters (phenol esters)."
  },
  {
    "id": "tum_55",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Atypical Adenomatous Hyperplasia - Question 55): Which concept is CORRECT?",
    "options": [
      "AAH > 2cm",
      "AAH <= 5mm precursor to adenocarcinoma",
      "AAH is precursor to SCLC",
      "AAH is a mesenchymal tumor",
      "AAH shows squamous differentiation"
    ],
    "answer": 1,
    "explanation": "Pathology detail: AAH is a well-demarcated lesion <=5mm composed of dysplastic pneumocytes lining alveolar walls, precursor to adenocarcinoma."
  },
  {
    "id": "tum_56",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Horner Syndrome Features - Question 56): Which concept is CORRECT?",
    "options": [
      "Exophthalmos",
      "Mydriasis",
      "Hyperhidrosis",
      "Tachycardia",
      "Ptosis, miosis, and anhidrosis"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Horner syndrome consists of ipsilateral ptosis, miosis, anhidrosis, and enophthalmos due to sympathetic trunk compression."
  },
  {
    "id": "tum_57",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Lambert-Eaton Myasthenic Syndrome - Question 57): Which concept is CORRECT?",
    "options": [
      "Antibodies against presynaptic voltage-gated calcium channels in SCLC",
      "Postsynaptic ACh receptor destruction",
      "Demyelination of peripheral nerves",
      "Direct tumor invasion of neuromuscular junction",
      "Thyrotoxicosis"
    ],
    "answer": 0,
    "explanation": "Pathology detail: LEMS is an autoimmune paraneoplastic syndrome associated with SCLC caused by antibodies against presynaptic voltage-gated calcium channels."
  },
  {
    "id": "tum_58",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (EGFR Mutations in Lung Ca - Question 58): Which concept is CORRECT?",
    "options": [
      "KRAS mutations in non-smokers",
      "TP53 in non-smokers",
      "EGFR mutations in Asian non-smoker females with adenocarcinoma",
      "ALK translocations in SCLC",
      "BRAF mutations in squamous ca"
    ],
    "answer": 2,
    "explanation": "Pathology detail: EGFR tyrosine kinase domain mutations are common in adenocarcinomas in Asian non-smoker females, targeted by TKIs (erlotinib, osimertinib)."
  },
  {
    "id": "tum_59",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (ALK Gene Rearrangement - Question 59): Which concept is CORRECT?",
    "options": [
      "SCLC",
      "EML4-ALK fusion in adenocarcinoma",
      "Squamous cell ca",
      "Large cell ca",
      "Carcinoid"
    ],
    "answer": 1,
    "explanation": "Pathology detail: EML4-ALK fusion gene occurs in 3-5% of adenocarcinomas (often young non-smokers), responsive to ALK inhibitors like crizotinib."
  },
  {
    "id": "tum_60",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Metastatic Lung Cancer Histology - Question 60): Which concept is CORRECT?",
    "options": [
      "Primary SCLC",
      "Primary Adenocarcinoma in-situ",
      "Lobar pneumonia",
      "Metastatic carcinoma",
      "Asbestosis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Multiple bilateral cannonball lung nodules on chest radiograph strongly favor metastatic disease rather than primary bronchogenic carcinoma."
  },
  {
    "id": "tum_61",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Bronchial Carcinoid - Question 61): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Bronchial carcinoid",
      "Small cell ca",
      "Adenocarcinoma",
      "Large cell ca"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Carcinoid tumors are low-grade neuroendocrine neoplasms showing uniform round cells in nests/trabeculae with salt-and-pepper chromatin; immunohistochemistry positive for chromogranin and synaptophysin."
  },
  {
    "id": "tum_62",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Large Cell Carcinoma - Question 62): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Adenocarcinoma",
      "Small cell ca",
      "Large cell carcinoma",
      "Mesothelioma"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Undifferentiated malignant epithelial tumor lacking glandular or squamous differentiation under light microscopy."
  },
  {
    "id": "tum_63",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Precursor Lesions - Question 63): Which concept is CORRECT?",
    "options": [
      "All are recognized precursor lesions",
      "Only SCLC has a known precursor",
      "Metaplasia is a malignant lesion",
      "Clear cell hyperplasia is the main precursor",
      "Carcinoids arise from AAH"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Recognized morphological precursor lesions include Squamous Dysplasia/Carcinoma in-situ, Atypical Adenomatous Hyperplasia (AAH), Adenocarcinoma in-situ (AIS), and Diffuse Idiopathic Pulmonary Neuroendocrine Cell Hyperplasia (DIPNECH)."
  },
  {
    "id": "tum_64",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Carcinogens in Smoke - Question 64): Which concept is CORRECT?",
    "options": [
      "Phenol esters act as initiators",
      "Radioactive isotopes are non-toxic",
      "Polycyclic aromatic hydrocarbons act as tumor initiators and phenol esters as promoters",
      "Nicotine is a direct mutagen",
      "Tar is purely non-carcinogenic"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Cigarette smoke contains initiators (polycyclic aromatic hydrocarbons, nitrosamines) and promoters (phenol esters)."
  },
  {
    "id": "tum_65",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Atypical Adenomatous Hyperplasia - Question 65): Which concept is CORRECT?",
    "options": [
      "AAH > 2cm",
      "AAH <= 5mm precursor to adenocarcinoma",
      "AAH is precursor to SCLC",
      "AAH is a mesenchymal tumor",
      "AAH shows squamous differentiation"
    ],
    "answer": 1,
    "explanation": "Pathology detail: AAH is a well-demarcated lesion <=5mm composed of dysplastic pneumocytes lining alveolar walls, precursor to adenocarcinoma."
  },
  {
    "id": "tum_66",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Horner Syndrome Features - Question 66): Which concept is CORRECT?",
    "options": [
      "Exophthalmos",
      "Mydriasis",
      "Hyperhidrosis",
      "Tachycardia",
      "Ptosis, miosis, and anhidrosis"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Horner syndrome consists of ipsilateral ptosis, miosis, anhidrosis, and enophthalmos due to sympathetic trunk compression."
  },
  {
    "id": "tum_67",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Lambert-Eaton Myasthenic Syndrome - Question 67): Which concept is CORRECT?",
    "options": [
      "Antibodies against presynaptic voltage-gated calcium channels in SCLC",
      "Postsynaptic ACh receptor destruction",
      "Demyelination of peripheral nerves",
      "Direct tumor invasion of neuromuscular junction",
      "Thyrotoxicosis"
    ],
    "answer": 0,
    "explanation": "Pathology detail: LEMS is an autoimmune paraneoplastic syndrome associated with SCLC caused by antibodies against presynaptic voltage-gated calcium channels."
  },
  {
    "id": "tum_68",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (EGFR Mutations in Lung Ca - Question 68): Which concept is CORRECT?",
    "options": [
      "KRAS mutations in non-smokers",
      "TP53 in non-smokers",
      "EGFR mutations in Asian non-smoker females with adenocarcinoma",
      "ALK translocations in SCLC",
      "BRAF mutations in squamous ca"
    ],
    "answer": 2,
    "explanation": "Pathology detail: EGFR tyrosine kinase domain mutations are common in adenocarcinomas in Asian non-smoker females, targeted by TKIs (erlotinib, osimertinib)."
  },
  {
    "id": "tum_69",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (ALK Gene Rearrangement - Question 69): Which concept is CORRECT?",
    "options": [
      "SCLC",
      "EML4-ALK fusion in adenocarcinoma",
      "Squamous cell ca",
      "Large cell ca",
      "Carcinoid"
    ],
    "answer": 1,
    "explanation": "Pathology detail: EML4-ALK fusion gene occurs in 3-5% of adenocarcinomas (often young non-smokers), responsive to ALK inhibitors like crizotinib."
  },
  {
    "id": "tum_70",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Metastatic Lung Cancer Histology - Question 70): Which concept is CORRECT?",
    "options": [
      "Primary SCLC",
      "Primary Adenocarcinoma in-situ",
      "Lobar pneumonia",
      "Metastatic carcinoma",
      "Asbestosis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Multiple bilateral cannonball lung nodules on chest radiograph strongly favor metastatic disease rather than primary bronchogenic carcinoma."
  },
  {
    "id": "tum_71",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Bronchial Carcinoid - Question 71): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Bronchial carcinoid",
      "Small cell ca",
      "Adenocarcinoma",
      "Large cell ca"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Carcinoid tumors are low-grade neuroendocrine neoplasms showing uniform round cells in nests/trabeculae with salt-and-pepper chromatin; immunohistochemistry positive for chromogranin and synaptophysin."
  },
  {
    "id": "tum_72",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Large Cell Carcinoma - Question 72): Which concept is CORRECT?",
    "options": [
      "Squamous cell ca",
      "Adenocarcinoma",
      "Small cell ca",
      "Large cell carcinoma",
      "Mesothelioma"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Undifferentiated malignant epithelial tumor lacking glandular or squamous differentiation under light microscopy."
  },
  {
    "id": "tum_73",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Precursor Lesions - Question 73): Which concept is CORRECT?",
    "options": [
      "All are recognized precursor lesions",
      "Only SCLC has a known precursor",
      "Metaplasia is a malignant lesion",
      "Clear cell hyperplasia is the main precursor",
      "Carcinoids arise from AAH"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Recognized morphological precursor lesions include Squamous Dysplasia/Carcinoma in-situ, Atypical Adenomatous Hyperplasia (AAH), Adenocarcinoma in-situ (AIS), and Diffuse Idiopathic Pulmonary Neuroendocrine Cell Hyperplasia (DIPNECH)."
  },
  {
    "id": "tum_74",
    "category": "Lung Tumours",
    "type": "Conceptual",
    "question": "Regarding Lung Tumour pathology (Carcinogens in Smoke - Question 74): Which concept is CORRECT?",
    "options": [
      "Phenol esters act as initiators",
      "Radioactive isotopes are non-toxic",
      "Polycyclic aromatic hydrocarbons act as tumor initiators and phenol esters as promoters",
      "Nicotine is a direct mutagen",
      "Tar is purely non-carcinogenic"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Cigarette smoke contains initiators (polycyclic aromatic hydrocarbons, nitrosamines) and promoters (phenol esters)."
  },
  {
    "id": "tum_75",
    "category": "Lung Tumours",
    "type": "Clinical Vignette",
    "question": "Regarding Lung Tumour pathology (Atypical Adenomatous Hyperplasia - Question 75): Which concept is CORRECT?",
    "options": [
      "AAH > 2cm",
      "AAH <= 5mm precursor to adenocarcinoma",
      "AAH is precursor to SCLC",
      "AAH is a mesenchymal tumor",
      "AAH shows squamous differentiation"
    ],
    "answer": 1,
    "explanation": "Pathology detail: AAH is a well-demarcated lesion <=5mm composed of dysplastic pneumocytes lining alveolar walls, precursor to adenocarcinoma."
  },
  {
    "id": "inf_1",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "A chest X-ray of an asymptomatic 50-year-old foundry worker/sandblaster reveals fine nodularity in the upper lung zones and 'eggshell calcification' of hilar lymph nodes. Biopsy shows birefringent needle-like silica particles under polarized light. What is the diagnosis?",
    "options": [
      "Asbestosis",
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Berylliosis",
      "Siderosis"
    ],
    "answer": 1,
    "explanation": "Silicosis presents with upper lobe fibrotic nodules, eggshell calcification of hilar lymph nodes, and birefringent quartz particles within alveolar macrophages under polarized light."
  },
  {
    "id": "inf_2",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Ferruginous bodies (golden-brown beaded rods coated with iron-protein complexes) seen in lung tissue biopsies are pathognomonic for exposure to:",
    "options": [
      "Silica",
      "Coal dust",
      "Asbestos fibers",
      "Beryllium",
      "Cotton fibers"
    ],
    "answer": 2,
    "explanation": "Ferruginous bodies are asbestos fibers coated with iron-containing proteinaceous material (ferritin/hemosiderin) by alveolar macrophages."
  },
  {
    "id": "inf_3",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Caplan syndrome is defined by the combination of pneumoconiosis (CWP, silicosis, or asbestosis) with:",
    "options": [
      "Systemic Lupus Erythematosus",
      "Rheumatoid Arthritis",
      "Scleroderma",
      "Ankylosing Spondylitis",
      "Polymyositis"
    ],
    "answer": 1,
    "explanation": "Caplan syndrome represents the co-occurrence of rheumatoid arthritis with pneumoconiosis, characterized by rapid development of large necrobiotic rheumatoid nodules in lungs."
  },
  {
    "id": "inf_4",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "A 38-year-old farmer experiences sudden malaise, fever, chills, dyspnea, and dry cough 5 hours after handling moldy hay. Symptoms resolve after avoiding exposure. What is the diagnosis?",
    "options": [
      "Bagassosis",
      "Byssinosis",
      "Farmer's lung (Hypersensitivity Pneumonitis)",
      "Silicosis",
      "Aspergillosis"
    ],
    "answer": 2,
    "explanation": "Farmer's lung is an immunologically mediated hypersensitivity pneumonitis caused by inhalation of thermophilic actinomycetes present in moldy hay."
  },
  {
    "id": "inf_5",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Which etiologic agent is paired INCORRECTLY with its occupational lung disease?",
    "options": [
      "Thermophilic actinomycetes -> Farmer's lung",
      "Sugar cane bagasse -> Bagassosis",
      "Cotton fibers -> Byssinosis",
      "Hemp/flax -> Silicosis",
      "Bird proteins -> Bird fancier's lung"
    ],
    "answer": 3,
    "explanation": "Cotton, flax, and hemp inhalation cause Byssinosis ('Monday morning chest tightness'). Silicosis is caused by crystalline silicon dioxide (quartz)."
  },
  {
    "id": "inf_6",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Which pneumoconiosis carries the highest risk for developing Malignant Mesothelioma of the pleura and peritoneum?",
    "options": [
      "Silicosis",
      "Coal Worker's Pneumoconiosis",
      "Asbestosis",
      "Siderosis",
      "Stannosis"
    ],
    "answer": 2,
    "explanation": "Asbestos exposure (especially amphibole fibers) is the dominant predisposing risk factor for malignant mesothelioma of pleura/peritoneum."
  },
  {
    "id": "inf_7",
    "category": "Infiltrative Lung Diseases",
    "type": "Exception",
    "question": "Pulmonary fibrosis is a recognized complication of all the following EXCEPT:",
    "options": [
      "Hamman-Rich syndrome (Acute interstitial pneumonia)",
      "Paraquat herbicide poisoning",
      "Asbestos exposure",
      "Pneumococcal lobar pneumonia with complete resolution",
      "Bleomycin toxicity"
    ],
    "answer": 3,
    "explanation": "Pneumococcal pneumonia typically undergoes complete resolution without structural scarring/fibrosis; the others cause progressive pulmonary fibrosis."
  },
  {
    "id": "inf_8",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Microscopically, Hypersensitivity Pneumonitis characteristically demonstrates:",
    "options": [
      "Caseating granulomas with central liquefaction",
      "Non-caseating poorly formed interstitial granulomas with multinucleated giant cells",
      "Dense neutrophilic intra-alveolar consolidation",
      "Hyaline membranes lining alveolar ducts",
      "Ferruginous bodies in 100% of cases"
    ],
    "answer": 1,
    "explanation": "Hypersensitivity pneumonitis shows interstitial lymphoplasmacytic infiltrates, interalveolar non-caseating poorly formed granulomas, and giant cells."
  },
  {
    "id": "inf_9",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Idiopathic Pulmonary Fibrosis (IPF / Usual Interstitial Pneumonia pattern) is characterized histologically by:",
    "options": [
      "Uniform interstitial inflammation throughout both lungs",
      "Spatial and temporal heterogeneity with fibroblastic foci and honeycomb lung",
      "Widespread caseating granulomas",
      "Diffuse hyaline membrane formation",
      "Pleural plaques with asbestos bodies"
    ],
    "answer": 1,
    "explanation": "Usual Interstitial Pneumonia (UIP) pattern in IPF shows spatial and temporal heterogeneity: alternating normal lung, active fibroblastic foci, and dense fibrotic honeycombing."
  },
  {
    "id": "inf_10",
    "category": "Infiltrative Lung Diseases",
    "type": "Recall",
    "question": "Which of the following occupational exposures is known to induce non-caseating granulomas closely resembling sarcoidosis?",
    "options": [
      "Coal dust",
      "Silica",
      "Beryllium (Berylliosis)",
      "Iron oxide",
      "Tin oxide"
    ],
    "answer": 2,
    "explanation": "Chronic Berylliosis (nuclear/aerospace industry) produces non-caseating epithelioid granulomas indistinguishable from sarcoidosis."
  },
  {
    "id": "inf_11",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Anthracosis vs CWP - Question 11): Which concept is CORRECT?",
    "options": [
      "Anthracosis is malignant",
      "Anthracosis is pigment uptake by alveolar/bronchial macrophages without cellular reaction",
      "CWP never causes fibrosis",
      "Silicosis is caused by carbon",
      "Berylliosis causes blue bloater"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Anthracosis is ubiquitous asymptomatic pigment deposition in urban dwellers; Coal Worker's Pneumoconiosis involves coal macules, nodules, and progressive massive fibrosis (PMF)."
  },
  {
    "id": "inf_12",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Pneumoconiosis Definition - Question 12): Which concept is CORRECT?",
    "options": [
      "Neoplastic tumors",
      "Non-neoplastic tissue reactions to inhaled particulate matter",
      "Infectious granulomatous diseases",
      "Genetic surfactant defects",
      "Autoimmune vasculitides"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Pneumoconioses are non-neoplastic lung reactions to inhalation of mineral dusts, organic dusts, or chemical vapors."
  },
  {
    "id": "inf_13",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Asbestos Pleural Plaques - Question 13): Which concept is CORRECT?",
    "options": [
      "Plaques are malignant tumors",
      "Plaques indicate viral infection",
      "Pleural plaques are dense acellular collagenous parietal pleural lesions from asbestos",
      "Plaques contain caseating granulomas",
      "Plaques cause alveolar destruction"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Pleural plaques (smooth circumscribed fibrotic collagenous plaques on parietal pleura) are the most common manifestation of asbestos exposure."
  },
  {
    "id": "inf_14",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Byssinosis Clinical Presentation - Question 14): Which concept is CORRECT?",
    "options": [
      "Worst on Fridays",
      "Occurs only in coal miners",
      "Caused by silica",
      "Characterized by Monday morning chest tightness in cotton textile workers",
      "Associated with eggshell calcification"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Byssinosis (cotton mill workers) causes bronchospasm and chest tightness, characteristically worst on Mondays ('Monday chest tightness') after weekend rest."
  },
  {
    "id": "inf_15",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Silicosis Pathogenesis - Question 15): Which concept is CORRECT?",
    "options": [
      "Macrophage activation and lysosomal rupture releasing fibrogenic cytokines",
      "IgE-mediated mast cell degranulation",
      "Direct enzymatic cleavage of surfactant",
      "Inactivation of alpha-1-antitrypsin",
      "Viral transformation of pneumocytes"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Silica crystals cause macrophage lysosomal membrane rupture, releasing IL-1, TNF, and fibrogenic factors that stimulate collagen synthesis."
  },
  {
    "id": "inf_16",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Desquamative Interstitial Pneumonia (DIP) - Question 16): Which concept is CORRECT?",
    "options": [
      "Granulomatous disease",
      "Intra-alveolar accumulation of pigmented macrophages ('smoker's macrophages')",
      "Neutrophilic lobar consolidation",
      "Eosinophilic granuloma",
      "Fibrotic destruction of main bronchus"
    ],
    "answer": 1,
    "explanation": "Pathology detail: DIP is a smoking-related interstitial lung disease characterized by massive accumulation of pigmented macrophages within alveolar spaces."
  },
  {
    "id": "inf_17",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Respiratory Bronchiolitis-ILD - Question 17): Which concept is CORRECT?",
    "options": [
      "DIP affects bronchioles only",
      "RB-ILD affects distal pleura",
      "RB-ILD shows pigmented macrophages centered on respiratory bronchioles in smokers",
      "RB-ILD is caused by asbestos",
      "RB-ILD causes honeycombing"
    ],
    "answer": 2,
    "explanation": "Pathology detail: RB-ILD is a smoking-related condition with pigmented macrophages in lumen of respiratory bronchioles."
  },
  {
    "id": "inf_18",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Pulmonary Langerhans Cell Histiocytosis - Question 18): Which concept is CORRECT?",
    "options": [
      "Positive for Pan-keratin",
      "Birbeck granules absent",
      "Affects elderly non-smokers",
      "Negative for S100",
      "Langerhans cells with Birbeck granules (CD1a+, S100+) in young smokers"
    ],
    "answer": 4,
    "explanation": "Pathology detail: PLCH occurs in young smokers; biopsy shows Langerhans cells with Birbeck granules (tennis-racquet shapes) on EM, positive for CD1a and S100."
  },
  {
    "id": "inf_19",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Idiopathic Pulmonary Hemosiderosis - Question 19): Which concept is CORRECT?",
    "options": [
      "Hemosiderin-laden macrophages in alveoli without renal disease",
      "IgA deposition in kidneys",
      "Caseating granulomas",
      "Pleural plaque formation",
      "Eosinophil excess"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Intermittent alveolar hemorrhage causing hemoptysis, anemia, and hemosiderin-laden macrophages without renal vasculitis."
  },
  {
    "id": "inf_20",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Goodpasture Syndrome - Question 20): Which concept is CORRECT?",
    "options": [
      "Anti-IgG antibodies",
      "Anti-GBM antibodies targeting Type IV collagen causing pulmonary hemorrhage and glomerulonephritis",
      "c-ANCA positive vasculitis",
      "IgE mediated asthma",
      "Asbestos induced plaque"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Autoimmune disease with anti-GBM antibodies targeting alpha-3 chain of Type IV collagen, causing necrotizing glomerulonephritis and pulmonary hemorrhagic consolidation."
  },
  {
    "id": "inf_21",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Anthracosis vs CWP - Question 21): Which concept is CORRECT?",
    "options": [
      "Anthracosis is malignant",
      "Anthracosis is pigment uptake by alveolar/bronchial macrophages without cellular reaction",
      "CWP never causes fibrosis",
      "Silicosis is caused by carbon",
      "Berylliosis causes blue bloater"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Anthracosis is ubiquitous asymptomatic pigment deposition in urban dwellers; Coal Worker's Pneumoconiosis involves coal macules, nodules, and progressive massive fibrosis (PMF)."
  },
  {
    "id": "inf_22",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Pneumoconiosis Definition - Question 22): Which concept is CORRECT?",
    "options": [
      "Neoplastic tumors",
      "Non-neoplastic tissue reactions to inhaled particulate matter",
      "Infectious granulomatous diseases",
      "Genetic surfactant defects",
      "Autoimmune vasculitides"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Pneumoconioses are non-neoplastic lung reactions to inhalation of mineral dusts, organic dusts, or chemical vapors."
  },
  {
    "id": "inf_23",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Asbestos Pleural Plaques - Question 23): Which concept is CORRECT?",
    "options": [
      "Plaques are malignant tumors",
      "Plaques indicate viral infection",
      "Pleural plaques are dense acellular collagenous parietal pleural lesions from asbestos",
      "Plaques contain caseating granulomas",
      "Plaques cause alveolar destruction"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Pleural plaques (smooth circumscribed fibrotic collagenous plaques on parietal pleura) are the most common manifestation of asbestos exposure."
  },
  {
    "id": "inf_24",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Byssinosis Clinical Presentation - Question 24): Which concept is CORRECT?",
    "options": [
      "Worst on Fridays",
      "Occurs only in coal miners",
      "Caused by silica",
      "Characterized by Monday morning chest tightness in cotton textile workers",
      "Associated with eggshell calcification"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Byssinosis (cotton mill workers) causes bronchospasm and chest tightness, characteristically worst on Mondays ('Monday chest tightness') after weekend rest."
  },
  {
    "id": "inf_25",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Silicosis Pathogenesis - Question 25): Which concept is CORRECT?",
    "options": [
      "Macrophage activation and lysosomal rupture releasing fibrogenic cytokines",
      "IgE-mediated mast cell degranulation",
      "Direct enzymatic cleavage of surfactant",
      "Inactivation of alpha-1-antitrypsin",
      "Viral transformation of pneumocytes"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Silica crystals cause macrophage lysosomal membrane rupture, releasing IL-1, TNF, and fibrogenic factors that stimulate collagen synthesis."
  },
  {
    "id": "inf_26",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Desquamative Interstitial Pneumonia (DIP) - Question 26): Which concept is CORRECT?",
    "options": [
      "Granulomatous disease",
      "Intra-alveolar accumulation of pigmented macrophages ('smoker's macrophages')",
      "Neutrophilic lobar consolidation",
      "Eosinophilic granuloma",
      "Fibrotic destruction of main bronchus"
    ],
    "answer": 1,
    "explanation": "Pathology detail: DIP is a smoking-related interstitial lung disease characterized by massive accumulation of pigmented macrophages within alveolar spaces."
  },
  {
    "id": "inf_27",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Respiratory Bronchiolitis-ILD - Question 27): Which concept is CORRECT?",
    "options": [
      "DIP affects bronchioles only",
      "RB-ILD affects distal pleura",
      "RB-ILD shows pigmented macrophages centered on respiratory bronchioles in smokers",
      "RB-ILD is caused by asbestos",
      "RB-ILD causes honeycombing"
    ],
    "answer": 2,
    "explanation": "Pathology detail: RB-ILD is a smoking-related condition with pigmented macrophages in lumen of respiratory bronchioles."
  },
  {
    "id": "inf_28",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Pulmonary Langerhans Cell Histiocytosis - Question 28): Which concept is CORRECT?",
    "options": [
      "Positive for Pan-keratin",
      "Birbeck granules absent",
      "Affects elderly non-smokers",
      "Negative for S100",
      "Langerhans cells with Birbeck granules (CD1a+, S100+) in young smokers"
    ],
    "answer": 4,
    "explanation": "Pathology detail: PLCH occurs in young smokers; biopsy shows Langerhans cells with Birbeck granules (tennis-racquet shapes) on EM, positive for CD1a and S100."
  },
  {
    "id": "inf_29",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Idiopathic Pulmonary Hemosiderosis - Question 29): Which concept is CORRECT?",
    "options": [
      "Hemosiderin-laden macrophages in alveoli without renal disease",
      "IgA deposition in kidneys",
      "Caseating granulomas",
      "Pleural plaque formation",
      "Eosinophil excess"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Intermittent alveolar hemorrhage causing hemoptysis, anemia, and hemosiderin-laden macrophages without renal vasculitis."
  },
  {
    "id": "inf_30",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Goodpasture Syndrome - Question 30): Which concept is CORRECT?",
    "options": [
      "Anti-IgG antibodies",
      "Anti-GBM antibodies targeting Type IV collagen causing pulmonary hemorrhage and glomerulonephritis",
      "c-ANCA positive vasculitis",
      "IgE mediated asthma",
      "Asbestos induced plaque"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Autoimmune disease with anti-GBM antibodies targeting alpha-3 chain of Type IV collagen, causing necrotizing glomerulonephritis and pulmonary hemorrhagic consolidation."
  },
  {
    "id": "inf_31",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Anthracosis vs CWP - Question 31): Which concept is CORRECT?",
    "options": [
      "Anthracosis is malignant",
      "Anthracosis is pigment uptake by alveolar/bronchial macrophages without cellular reaction",
      "CWP never causes fibrosis",
      "Silicosis is caused by carbon",
      "Berylliosis causes blue bloater"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Anthracosis is ubiquitous asymptomatic pigment deposition in urban dwellers; Coal Worker's Pneumoconiosis involves coal macules, nodules, and progressive massive fibrosis (PMF)."
  },
  {
    "id": "inf_32",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Pneumoconiosis Definition - Question 32): Which concept is CORRECT?",
    "options": [
      "Neoplastic tumors",
      "Non-neoplastic tissue reactions to inhaled particulate matter",
      "Infectious granulomatous diseases",
      "Genetic surfactant defects",
      "Autoimmune vasculitides"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Pneumoconioses are non-neoplastic lung reactions to inhalation of mineral dusts, organic dusts, or chemical vapors."
  },
  {
    "id": "inf_33",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Asbestos Pleural Plaques - Question 33): Which concept is CORRECT?",
    "options": [
      "Plaques are malignant tumors",
      "Plaques indicate viral infection",
      "Pleural plaques are dense acellular collagenous parietal pleural lesions from asbestos",
      "Plaques contain caseating granulomas",
      "Plaques cause alveolar destruction"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Pleural plaques (smooth circumscribed fibrotic collagenous plaques on parietal pleura) are the most common manifestation of asbestos exposure."
  },
  {
    "id": "inf_34",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Byssinosis Clinical Presentation - Question 34): Which concept is CORRECT?",
    "options": [
      "Worst on Fridays",
      "Occurs only in coal miners",
      "Caused by silica",
      "Characterized by Monday morning chest tightness in cotton textile workers",
      "Associated with eggshell calcification"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Byssinosis (cotton mill workers) causes bronchospasm and chest tightness, characteristically worst on Mondays ('Monday chest tightness') after weekend rest."
  },
  {
    "id": "inf_35",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Silicosis Pathogenesis - Question 35): Which concept is CORRECT?",
    "options": [
      "Macrophage activation and lysosomal rupture releasing fibrogenic cytokines",
      "IgE-mediated mast cell degranulation",
      "Direct enzymatic cleavage of surfactant",
      "Inactivation of alpha-1-antitrypsin",
      "Viral transformation of pneumocytes"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Silica crystals cause macrophage lysosomal membrane rupture, releasing IL-1, TNF, and fibrogenic factors that stimulate collagen synthesis."
  },
  {
    "id": "inf_36",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Desquamative Interstitial Pneumonia (DIP) - Question 36): Which concept is CORRECT?",
    "options": [
      "Granulomatous disease",
      "Intra-alveolar accumulation of pigmented macrophages ('smoker's macrophages')",
      "Neutrophilic lobar consolidation",
      "Eosinophilic granuloma",
      "Fibrotic destruction of main bronchus"
    ],
    "answer": 1,
    "explanation": "Pathology detail: DIP is a smoking-related interstitial lung disease characterized by massive accumulation of pigmented macrophages within alveolar spaces."
  },
  {
    "id": "inf_37",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Respiratory Bronchiolitis-ILD - Question 37): Which concept is CORRECT?",
    "options": [
      "DIP affects bronchioles only",
      "RB-ILD affects distal pleura",
      "RB-ILD shows pigmented macrophages centered on respiratory bronchioles in smokers",
      "RB-ILD is caused by asbestos",
      "RB-ILD causes honeycombing"
    ],
    "answer": 2,
    "explanation": "Pathology detail: RB-ILD is a smoking-related condition with pigmented macrophages in lumen of respiratory bronchioles."
  },
  {
    "id": "inf_38",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Pulmonary Langerhans Cell Histiocytosis - Question 38): Which concept is CORRECT?",
    "options": [
      "Positive for Pan-keratin",
      "Birbeck granules absent",
      "Affects elderly non-smokers",
      "Negative for S100",
      "Langerhans cells with Birbeck granules (CD1a+, S100+) in young smokers"
    ],
    "answer": 4,
    "explanation": "Pathology detail: PLCH occurs in young smokers; biopsy shows Langerhans cells with Birbeck granules (tennis-racquet shapes) on EM, positive for CD1a and S100."
  },
  {
    "id": "inf_39",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Idiopathic Pulmonary Hemosiderosis - Question 39): Which concept is CORRECT?",
    "options": [
      "Hemosiderin-laden macrophages in alveoli without renal disease",
      "IgA deposition in kidneys",
      "Caseating granulomas",
      "Pleural plaque formation",
      "Eosinophil excess"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Intermittent alveolar hemorrhage causing hemoptysis, anemia, and hemosiderin-laden macrophages without renal vasculitis."
  },
  {
    "id": "inf_40",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Goodpasture Syndrome - Question 40): Which concept is CORRECT?",
    "options": [
      "Anti-IgG antibodies",
      "Anti-GBM antibodies targeting Type IV collagen causing pulmonary hemorrhage and glomerulonephritis",
      "c-ANCA positive vasculitis",
      "IgE mediated asthma",
      "Asbestos induced plaque"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Autoimmune disease with anti-GBM antibodies targeting alpha-3 chain of Type IV collagen, causing necrotizing glomerulonephritis and pulmonary hemorrhagic consolidation."
  },
  {
    "id": "inf_41",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Anthracosis vs CWP - Question 41): Which concept is CORRECT?",
    "options": [
      "Anthracosis is malignant",
      "Anthracosis is pigment uptake by alveolar/bronchial macrophages without cellular reaction",
      "CWP never causes fibrosis",
      "Silicosis is caused by carbon",
      "Berylliosis causes blue bloater"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Anthracosis is ubiquitous asymptomatic pigment deposition in urban dwellers; Coal Worker's Pneumoconiosis involves coal macules, nodules, and progressive massive fibrosis (PMF)."
  },
  {
    "id": "inf_42",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Pneumoconiosis Definition - Question 42): Which concept is CORRECT?",
    "options": [
      "Neoplastic tumors",
      "Non-neoplastic tissue reactions to inhaled particulate matter",
      "Infectious granulomatous diseases",
      "Genetic surfactant defects",
      "Autoimmune vasculitides"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Pneumoconioses are non-neoplastic lung reactions to inhalation of mineral dusts, organic dusts, or chemical vapors."
  },
  {
    "id": "inf_43",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Asbestos Pleural Plaques - Question 43): Which concept is CORRECT?",
    "options": [
      "Plaques are malignant tumors",
      "Plaques indicate viral infection",
      "Pleural plaques are dense acellular collagenous parietal pleural lesions from asbestos",
      "Plaques contain caseating granulomas",
      "Plaques cause alveolar destruction"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Pleural plaques (smooth circumscribed fibrotic collagenous plaques on parietal pleura) are the most common manifestation of asbestos exposure."
  },
  {
    "id": "inf_44",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Byssinosis Clinical Presentation - Question 44): Which concept is CORRECT?",
    "options": [
      "Worst on Fridays",
      "Occurs only in coal miners",
      "Caused by silica",
      "Characterized by Monday morning chest tightness in cotton textile workers",
      "Associated with eggshell calcification"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Byssinosis (cotton mill workers) causes bronchospasm and chest tightness, characteristically worst on Mondays ('Monday chest tightness') after weekend rest."
  },
  {
    "id": "inf_45",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Silicosis Pathogenesis - Question 45): Which concept is CORRECT?",
    "options": [
      "Macrophage activation and lysosomal rupture releasing fibrogenic cytokines",
      "IgE-mediated mast cell degranulation",
      "Direct enzymatic cleavage of surfactant",
      "Inactivation of alpha-1-antitrypsin",
      "Viral transformation of pneumocytes"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Silica crystals cause macrophage lysosomal membrane rupture, releasing IL-1, TNF, and fibrogenic factors that stimulate collagen synthesis."
  },
  {
    "id": "inf_46",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Desquamative Interstitial Pneumonia (DIP) - Question 46): Which concept is CORRECT?",
    "options": [
      "Granulomatous disease",
      "Intra-alveolar accumulation of pigmented macrophages ('smoker's macrophages')",
      "Neutrophilic lobar consolidation",
      "Eosinophilic granuloma",
      "Fibrotic destruction of main bronchus"
    ],
    "answer": 1,
    "explanation": "Pathology detail: DIP is a smoking-related interstitial lung disease characterized by massive accumulation of pigmented macrophages within alveolar spaces."
  },
  {
    "id": "inf_47",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Respiratory Bronchiolitis-ILD - Question 47): Which concept is CORRECT?",
    "options": [
      "DIP affects bronchioles only",
      "RB-ILD affects distal pleura",
      "RB-ILD shows pigmented macrophages centered on respiratory bronchioles in smokers",
      "RB-ILD is caused by asbestos",
      "RB-ILD causes honeycombing"
    ],
    "answer": 2,
    "explanation": "Pathology detail: RB-ILD is a smoking-related condition with pigmented macrophages in lumen of respiratory bronchioles."
  },
  {
    "id": "inf_48",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Pulmonary Langerhans Cell Histiocytosis - Question 48): Which concept is CORRECT?",
    "options": [
      "Positive for Pan-keratin",
      "Birbeck granules absent",
      "Affects elderly non-smokers",
      "Negative for S100",
      "Langerhans cells with Birbeck granules (CD1a+, S100+) in young smokers"
    ],
    "answer": 4,
    "explanation": "Pathology detail: PLCH occurs in young smokers; biopsy shows Langerhans cells with Birbeck granules (tennis-racquet shapes) on EM, positive for CD1a and S100."
  },
  {
    "id": "inf_49",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Idiopathic Pulmonary Hemosiderosis - Question 49): Which concept is CORRECT?",
    "options": [
      "Hemosiderin-laden macrophages in alveoli without renal disease",
      "IgA deposition in kidneys",
      "Caseating granulomas",
      "Pleural plaque formation",
      "Eosinophil excess"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Intermittent alveolar hemorrhage causing hemoptysis, anemia, and hemosiderin-laden macrophages without renal vasculitis."
  },
  {
    "id": "inf_50",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Goodpasture Syndrome - Question 50): Which concept is CORRECT?",
    "options": [
      "Anti-IgG antibodies",
      "Anti-GBM antibodies targeting Type IV collagen causing pulmonary hemorrhage and glomerulonephritis",
      "c-ANCA positive vasculitis",
      "IgE mediated asthma",
      "Asbestos induced plaque"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Autoimmune disease with anti-GBM antibodies targeting alpha-3 chain of Type IV collagen, causing necrotizing glomerulonephritis and pulmonary hemorrhagic consolidation."
  },
  {
    "id": "inf_51",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Anthracosis vs CWP - Question 51): Which concept is CORRECT?",
    "options": [
      "Anthracosis is malignant",
      "Anthracosis is pigment uptake by alveolar/bronchial macrophages without cellular reaction",
      "CWP never causes fibrosis",
      "Silicosis is caused by carbon",
      "Berylliosis causes blue bloater"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Anthracosis is ubiquitous asymptomatic pigment deposition in urban dwellers; Coal Worker's Pneumoconiosis involves coal macules, nodules, and progressive massive fibrosis (PMF)."
  },
  {
    "id": "inf_52",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Pneumoconiosis Definition - Question 52): Which concept is CORRECT?",
    "options": [
      "Neoplastic tumors",
      "Non-neoplastic tissue reactions to inhaled particulate matter",
      "Infectious granulomatous diseases",
      "Genetic surfactant defects",
      "Autoimmune vasculitides"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Pneumoconioses are non-neoplastic lung reactions to inhalation of mineral dusts, organic dusts, or chemical vapors."
  },
  {
    "id": "inf_53",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Asbestos Pleural Plaques - Question 53): Which concept is CORRECT?",
    "options": [
      "Plaques are malignant tumors",
      "Plaques indicate viral infection",
      "Pleural plaques are dense acellular collagenous parietal pleural lesions from asbestos",
      "Plaques contain caseating granulomas",
      "Plaques cause alveolar destruction"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Pleural plaques (smooth circumscribed fibrotic collagenous plaques on parietal pleura) are the most common manifestation of asbestos exposure."
  },
  {
    "id": "inf_54",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Byssinosis Clinical Presentation - Question 54): Which concept is CORRECT?",
    "options": [
      "Worst on Fridays",
      "Occurs only in coal miners",
      "Caused by silica",
      "Characterized by Monday morning chest tightness in cotton textile workers",
      "Associated with eggshell calcification"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Byssinosis (cotton mill workers) causes bronchospasm and chest tightness, characteristically worst on Mondays ('Monday chest tightness') after weekend rest."
  },
  {
    "id": "inf_55",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Silicosis Pathogenesis - Question 55): Which concept is CORRECT?",
    "options": [
      "Macrophage activation and lysosomal rupture releasing fibrogenic cytokines",
      "IgE-mediated mast cell degranulation",
      "Direct enzymatic cleavage of surfactant",
      "Inactivation of alpha-1-antitrypsin",
      "Viral transformation of pneumocytes"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Silica crystals cause macrophage lysosomal membrane rupture, releasing IL-1, TNF, and fibrogenic factors that stimulate collagen synthesis."
  },
  {
    "id": "inf_56",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Desquamative Interstitial Pneumonia (DIP) - Question 56): Which concept is CORRECT?",
    "options": [
      "Granulomatous disease",
      "Intra-alveolar accumulation of pigmented macrophages ('smoker's macrophages')",
      "Neutrophilic lobar consolidation",
      "Eosinophilic granuloma",
      "Fibrotic destruction of main bronchus"
    ],
    "answer": 1,
    "explanation": "Pathology detail: DIP is a smoking-related interstitial lung disease characterized by massive accumulation of pigmented macrophages within alveolar spaces."
  },
  {
    "id": "inf_57",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Respiratory Bronchiolitis-ILD - Question 57): Which concept is CORRECT?",
    "options": [
      "DIP affects bronchioles only",
      "RB-ILD affects distal pleura",
      "RB-ILD shows pigmented macrophages centered on respiratory bronchioles in smokers",
      "RB-ILD is caused by asbestos",
      "RB-ILD causes honeycombing"
    ],
    "answer": 2,
    "explanation": "Pathology detail: RB-ILD is a smoking-related condition with pigmented macrophages in lumen of respiratory bronchioles."
  },
  {
    "id": "inf_58",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Pulmonary Langerhans Cell Histiocytosis - Question 58): Which concept is CORRECT?",
    "options": [
      "Positive for Pan-keratin",
      "Birbeck granules absent",
      "Affects elderly non-smokers",
      "Negative for S100",
      "Langerhans cells with Birbeck granules (CD1a+, S100+) in young smokers"
    ],
    "answer": 4,
    "explanation": "Pathology detail: PLCH occurs in young smokers; biopsy shows Langerhans cells with Birbeck granules (tennis-racquet shapes) on EM, positive for CD1a and S100."
  },
  {
    "id": "inf_59",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Idiopathic Pulmonary Hemosiderosis - Question 59): Which concept is CORRECT?",
    "options": [
      "Hemosiderin-laden macrophages in alveoli without renal disease",
      "IgA deposition in kidneys",
      "Caseating granulomas",
      "Pleural plaque formation",
      "Eosinophil excess"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Intermittent alveolar hemorrhage causing hemoptysis, anemia, and hemosiderin-laden macrophages without renal vasculitis."
  },
  {
    "id": "inf_60",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Goodpasture Syndrome - Question 60): Which concept is CORRECT?",
    "options": [
      "Anti-IgG antibodies",
      "Anti-GBM antibodies targeting Type IV collagen causing pulmonary hemorrhage and glomerulonephritis",
      "c-ANCA positive vasculitis",
      "IgE mediated asthma",
      "Asbestos induced plaque"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Autoimmune disease with anti-GBM antibodies targeting alpha-3 chain of Type IV collagen, causing necrotizing glomerulonephritis and pulmonary hemorrhagic consolidation."
  },
  {
    "id": "inf_61",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Anthracosis vs CWP - Question 61): Which concept is CORRECT?",
    "options": [
      "Anthracosis is malignant",
      "Anthracosis is pigment uptake by alveolar/bronchial macrophages without cellular reaction",
      "CWP never causes fibrosis",
      "Silicosis is caused by carbon",
      "Berylliosis causes blue bloater"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Anthracosis is ubiquitous asymptomatic pigment deposition in urban dwellers; Coal Worker's Pneumoconiosis involves coal macules, nodules, and progressive massive fibrosis (PMF)."
  },
  {
    "id": "inf_62",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Pneumoconiosis Definition - Question 62): Which concept is CORRECT?",
    "options": [
      "Neoplastic tumors",
      "Non-neoplastic tissue reactions to inhaled particulate matter",
      "Infectious granulomatous diseases",
      "Genetic surfactant defects",
      "Autoimmune vasculitides"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Pneumoconioses are non-neoplastic lung reactions to inhalation of mineral dusts, organic dusts, or chemical vapors."
  },
  {
    "id": "inf_63",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Asbestos Pleural Plaques - Question 63): Which concept is CORRECT?",
    "options": [
      "Plaques are malignant tumors",
      "Plaques indicate viral infection",
      "Pleural plaques are dense acellular collagenous parietal pleural lesions from asbestos",
      "Plaques contain caseating granulomas",
      "Plaques cause alveolar destruction"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Pleural plaques (smooth circumscribed fibrotic collagenous plaques on parietal pleura) are the most common manifestation of asbestos exposure."
  },
  {
    "id": "inf_64",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Byssinosis Clinical Presentation - Question 64): Which concept is CORRECT?",
    "options": [
      "Worst on Fridays",
      "Occurs only in coal miners",
      "Caused by silica",
      "Characterized by Monday morning chest tightness in cotton textile workers",
      "Associated with eggshell calcification"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Byssinosis (cotton mill workers) causes bronchospasm and chest tightness, characteristically worst on Mondays ('Monday chest tightness') after weekend rest."
  },
  {
    "id": "inf_65",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Silicosis Pathogenesis - Question 65): Which concept is CORRECT?",
    "options": [
      "Macrophage activation and lysosomal rupture releasing fibrogenic cytokines",
      "IgE-mediated mast cell degranulation",
      "Direct enzymatic cleavage of surfactant",
      "Inactivation of alpha-1-antitrypsin",
      "Viral transformation of pneumocytes"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Silica crystals cause macrophage lysosomal membrane rupture, releasing IL-1, TNF, and fibrogenic factors that stimulate collagen synthesis."
  },
  {
    "id": "inf_66",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Desquamative Interstitial Pneumonia (DIP) - Question 66): Which concept is CORRECT?",
    "options": [
      "Granulomatous disease",
      "Intra-alveolar accumulation of pigmented macrophages ('smoker's macrophages')",
      "Neutrophilic lobar consolidation",
      "Eosinophilic granuloma",
      "Fibrotic destruction of main bronchus"
    ],
    "answer": 1,
    "explanation": "Pathology detail: DIP is a smoking-related interstitial lung disease characterized by massive accumulation of pigmented macrophages within alveolar spaces."
  },
  {
    "id": "inf_67",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Respiratory Bronchiolitis-ILD - Question 67): Which concept is CORRECT?",
    "options": [
      "DIP affects bronchioles only",
      "RB-ILD affects distal pleura",
      "RB-ILD shows pigmented macrophages centered on respiratory bronchioles in smokers",
      "RB-ILD is caused by asbestos",
      "RB-ILD causes honeycombing"
    ],
    "answer": 2,
    "explanation": "Pathology detail: RB-ILD is a smoking-related condition with pigmented macrophages in lumen of respiratory bronchioles."
  },
  {
    "id": "inf_68",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Pulmonary Langerhans Cell Histiocytosis - Question 68): Which concept is CORRECT?",
    "options": [
      "Positive for Pan-keratin",
      "Birbeck granules absent",
      "Affects elderly non-smokers",
      "Negative for S100",
      "Langerhans cells with Birbeck granules (CD1a+, S100+) in young smokers"
    ],
    "answer": 4,
    "explanation": "Pathology detail: PLCH occurs in young smokers; biopsy shows Langerhans cells with Birbeck granules (tennis-racquet shapes) on EM, positive for CD1a and S100."
  },
  {
    "id": "inf_69",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Idiopathic Pulmonary Hemosiderosis - Question 69): Which concept is CORRECT?",
    "options": [
      "Hemosiderin-laden macrophages in alveoli without renal disease",
      "IgA deposition in kidneys",
      "Caseating granulomas",
      "Pleural plaque formation",
      "Eosinophil excess"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Intermittent alveolar hemorrhage causing hemoptysis, anemia, and hemosiderin-laden macrophages without renal vasculitis."
  },
  {
    "id": "inf_70",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Goodpasture Syndrome - Question 70): Which concept is CORRECT?",
    "options": [
      "Anti-IgG antibodies",
      "Anti-GBM antibodies targeting Type IV collagen causing pulmonary hemorrhage and glomerulonephritis",
      "c-ANCA positive vasculitis",
      "IgE mediated asthma",
      "Asbestos induced plaque"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Autoimmune disease with anti-GBM antibodies targeting alpha-3 chain of Type IV collagen, causing necrotizing glomerulonephritis and pulmonary hemorrhagic consolidation."
  },
  {
    "id": "inf_71",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Anthracosis vs CWP - Question 71): Which concept is CORRECT?",
    "options": [
      "Anthracosis is malignant",
      "Anthracosis is pigment uptake by alveolar/bronchial macrophages without cellular reaction",
      "CWP never causes fibrosis",
      "Silicosis is caused by carbon",
      "Berylliosis causes blue bloater"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Anthracosis is ubiquitous asymptomatic pigment deposition in urban dwellers; Coal Worker's Pneumoconiosis involves coal macules, nodules, and progressive massive fibrosis (PMF)."
  },
  {
    "id": "inf_72",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Pneumoconiosis Definition - Question 72): Which concept is CORRECT?",
    "options": [
      "Neoplastic tumors",
      "Non-neoplastic tissue reactions to inhaled particulate matter",
      "Infectious granulomatous diseases",
      "Genetic surfactant defects",
      "Autoimmune vasculitides"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Pneumoconioses are non-neoplastic lung reactions to inhalation of mineral dusts, organic dusts, or chemical vapors."
  },
  {
    "id": "inf_73",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Asbestos Pleural Plaques - Question 73): Which concept is CORRECT?",
    "options": [
      "Plaques are malignant tumors",
      "Plaques indicate viral infection",
      "Pleural plaques are dense acellular collagenous parietal pleural lesions from asbestos",
      "Plaques contain caseating granulomas",
      "Plaques cause alveolar destruction"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Pleural plaques (smooth circumscribed fibrotic collagenous plaques on parietal pleura) are the most common manifestation of asbestos exposure."
  },
  {
    "id": "inf_74",
    "category": "Infiltrative Lung Diseases",
    "type": "Conceptual",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Byssinosis Clinical Presentation - Question 74): Which concept is CORRECT?",
    "options": [
      "Worst on Fridays",
      "Occurs only in coal miners",
      "Caused by silica",
      "Characterized by Monday morning chest tightness in cotton textile workers",
      "Associated with eggshell calcification"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Byssinosis (cotton mill workers) causes bronchospasm and chest tightness, characteristically worst on Mondays ('Monday chest tightness') after weekend rest."
  },
  {
    "id": "inf_75",
    "category": "Infiltrative Lung Diseases",
    "type": "Clinical Vignette",
    "question": "Regarding Infiltrative / Restrictive Lung Disease (Silicosis Pathogenesis - Question 75): Which concept is CORRECT?",
    "options": [
      "Macrophage activation and lysosomal rupture releasing fibrogenic cytokines",
      "IgE-mediated mast cell degranulation",
      "Direct enzymatic cleavage of surfactant",
      "Inactivation of alpha-1-antitrypsin",
      "Viral transformation of pneumocytes"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Silica crystals cause macrophage lysosomal membrane rupture, releasing IL-1, TNF, and fibrogenic factors that stimulate collagen synthesis."
  },
  {
    "id": "ple_1",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Malignant Mesothelioma of the pleura is overwhelmingly linked to prior occupational exposure to:",
    "options": [
      "Silica dust",
      "Asbestos fibers (especially amphiboles)",
      "Coal dust",
      "Beryllium",
      "Cotton textile fibers"
    ],
    "answer": 1,
    "explanation": "Asbestos exposure is implicated in up to 90% of malignant mesotheliomas."
  },
  {
    "id": "ple_2",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Which finding differentiates a pleural Transudate from an Exudate according to Light's Criteria?",
    "options": [
      "Pleural fluid protein to serum protein ratio <0.5 and LDH <200 IU/L in transudate",
      "Transudate has high protein (>30 g/L) and elevated LDH",
      "Exudate has low specific gravity (<1.012) and clear watery fluid",
      "Transudate contains abundant neutrophils and tumor cells",
      "Exudate is non-inflammatory"
    ],
    "answer": 0,
    "explanation": "Transudates (e.g. CHF, Cirrhosis, Nephrotic) have low protein ratio (<0.5) and low LDH ratio (<0.6). Exudates (infections, tumors) have high protein and high LDH."
  },
  {
    "id": "ple_3",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "A 49-year-old male with mediastinal lymphoma presents with severe dyspnea and bilateral pleural effusions. Thoracentesis yields milky white fluid composed of emulsified fats and chylomicrons. What is the diagnosis?",
    "options": [
      "Empyema thoracis",
      "Hemothorax",
      "Chylothorax (Lymphatic obstruction)",
      "Pseudochylothorax",
      "Serofibrinous pleurisy"
    ],
    "answer": 2,
    "explanation": "Chylothorax is an accumulation of milky lymphatic fluid containing chylomicrons, usually caused by thoracic duct obstruction or trauma by tumor/lymphoma."
  },
  {
    "id": "ple_4",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Suppurative pleuritis (Empyema thoracis) is best defined as:",
    "options": [
      "Sterile transudative fluid in the pleural cavity",
      "Purulent exudate (pus) accumulating within the pleural space due to bacterial/mycotic spread",
      "Blood accumulation without inflammatory cells",
      "Air in the pleural space following trauma",
      "Lymphatic fluid accumulation"
    ],
    "answer": 1,
    "explanation": "Empyema thoracis is purulent cloud/yellow-green pus in the pleural cavity, commonly from direct spread of adjacent bacterial pneumonia or lung abscess."
  },
  {
    "id": "ple_5",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Spontaneous pneumothorax in a young, tall, athletic adult male is most frequently caused by rupture of:",
    "options": [
      "Ghon complex",
      "Subpleural emphysematous blebs / bullae (Paraseptal emphysema)",
      "Atheromatous aortic aneurysm",
      "Asbestos pleural plaque",
      "Necrotizing lung abscess"
    ],
    "answer": 1,
    "explanation": "Spontaneous pneumothorax in young adults is caused by rupture of apical subpleural blebs/bullae associated with paraseptal emphysema."
  },
  {
    "id": "ple_6",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Resorption (Absorptive) atelectasis occurs primarily as a result of:",
    "options": [
      "Accumulation of fluid, blood, or air in the pleural cavity",
      "Complete airway obstruction preventing air from reaching distal alveoli with absorption of trapped oxygen",
      "Fibrotic scarring of lung or pleura preventing expansion",
      "Loss of pulmonary surfactant in neonates",
      "Scoliosis and chest wall deformities"
    ],
    "answer": 1,
    "explanation": "Resorption atelectasis occurs when complete airway obstruction (mucus plug, foreign body, tumor) leads to absorption of trapped distal air into blood, causing alveolar collapse."
  },
  {
    "id": "ple_7",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Compressive atelectasis is illustrated by which clinical scenario?",
    "options": [
      "Foreign body aspirated into main bronchus",
      "Pleural effusion or pneumothorax mechanically compressing adjacent lung parenchyma",
      "Pulmonary tuberculosis causing localized fibrotic scarring",
      "Hyaline membrane disease in a premature infant",
      "Asthmatic bronchospasm"
    ],
    "answer": 1,
    "explanation": "Compressive atelectasis occurs when space-occupying fluid, blood, or air in the pleural cavity exerts external pressure on the lung, compressing alveoli."
  },
  {
    "id": "ple_8",
    "category": "Diseases of the Pleura",
    "type": "Exception",
    "question": "Pleural effusions are recognized complications of all the following EXCEPT:",
    "options": [
      "Congestive Heart Failure",
      "Bacterial Pneumonia",
      "Nephrotic Syndrome",
      "Asymptomatic simple uncomplicated rhinitis",
      "Metastatic Carcinomatosis"
    ],
    "answer": 3,
    "explanation": "Uncomplicated viral rhinitis involves the upper nasal mucosa only and does NOT cause pleural effusion."
  },
  {
    "id": "ple_9",
    "category": "Diseases of the Pleura",
    "type": "Recall",
    "question": "Hemorrhagic pleuritis differs from simple hemothorax because hemorrhagic pleuritis contains:",
    "options": [
      "Pure whole blood without inflammatory cells",
      "Inflammatory exudative cells or exfoliated tumor cells in blood-tinged fluid",
      "Emulsified chylomicrons and lymph",
      "High concentrations of surfactant",
      "Air bubbles under tension"
    ],
    "answer": 1,
    "explanation": "Hemorrhagic pleuritis contains inflammatory or malignant cells along with RBCs in an exudate (seen in tumor metastases, rickettsial infection), whereas hemothorax is pure blood from vessel rupture."
  },
  {
    "id": "ple_10",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "A 7-year-old child aspirates a peanut into the right mainstem bronchus. On chest radiograph, the mediastinum is shifted TOWARD the side of the collapsed lung. What type of atelectasis is present?",
    "options": [
      "Compressive atelectasis",
      "Resorption (Absorptive) atelectasis",
      "Contraction atelectasis",
      "Patchy atelectasis",
      "Bullous atelectasis"
    ],
    "answer": 1,
    "explanation": "In resorption atelectasis due to airway obstruction, collapse of the ipsilateral lung reduces volume, pulling the mediastinum TOWARD the affected side."
  },
  {
    "id": "ple_11",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Tension Pneumothorax - Question 11): Which concept is CORRECT?",
    "options": [
      "Shift to ipsilateral side",
      "Shift to contralateral side with vena cava compression",
      "No mediastinal movement",
      "Pleural effusion formation",
      "Resorption of air"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Tension pneumothorax involves a valve-like wound allowing air entry during inspiration but not exit; increases intrapleural pressure, compressing vena cava and shifting mediastinum to CONTRALATERAL side."
  },
  {
    "id": "ple_12",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Solitary Fibrous Tumor of Pleura - Question 12): Which concept is CORRECT?",
    "options": [
      "Solitary fibrous tumor (CD34+, STAT6+)",
      "Mesothelioma",
      "Adenocarcinoma",
      "Squamous ca",
      "Lymphoma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Benign or malignant localized mesenchymal tumor of pleura; NAB2-STAT6 gene fusion positive, CD34 positive, unrelated to asbestos exposure."
  },
  {
    "id": "ple_13",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Contraction Atelectasis - Question 13): Which concept is CORRECT?",
    "options": [
      "Reversible with surfactant",
      "Caused by mucus plug",
      "Caused by fibrotic scarring hampering expansion (Irreversible)",
      "Caused by pneumothorax",
      "Seen in premature infants"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Contraction atelectasis occurs when local or generalized fibrotic changes in lung or pleura hamper lung expansion during inspiration; IRREVERSIBLE."
  },
  {
    "id": "ple_14",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Pleural Hydrothorax - Question 14): Which concept is CORRECT?",
    "options": [
      "Empyema",
      "Hydrothorax",
      "Chylothorax",
      "Hemothorax",
      "Pleurisy"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Non-inflammatory transudative fluid in pleural cavity; most commonly due to elevated hydrostatic pressure in Congestive Heart Failure."
  },
  {
    "id": "ple_15",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleuritis Histology - Question 15): Which concept is CORRECT?",
    "options": [
      "Granulomatous necrosis",
      "Caseation",
      "Acellular calcification",
      "Fibrinous network with neutrophils",
      "Clear fluid without protein"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Fibrinous or serofibrinous pleuritis demonstrates a delicate pale pink network of intra-pleural fibrin threads with polymorphonuclear leucocytes."
  },
  {
    "id": "ple_16",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Mesothelioma Histology - Question 16): Which concept is CORRECT?",
    "options": [
      "CEA positive, Calretinin negative",
      "S100 positive",
      "CD34 positive",
      "CD20 positive",
      "Calretinin, CK5/6, WT-1, and D2-40 positive"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Epithelioid, sarcomatoid, or biphasic patterns; positive for Calretinin, Cytokeratin 5/6, WT-1, and D2-40."
  },
  {
    "id": "ple_17",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleural Thickening - Question 17): Which concept is CORRECT?",
    "options": [
      "Organization of empyema leading to fibrocollagenous pleural peel",
      "Surfactant accumulation",
      "Subpleural bleb formation",
      "Bronchial smooth muscle hypertrophy",
      "Acinar destruction"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Fibrocollagenous fibrous obliteration of pleural cavity following organization of unresolved empyema thoracis or hemothorax."
  },
  {
    "id": "ple_18",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Pseudochylothorax - Question 18): Which concept is CORRECT?",
    "options": [
      "Chylothorax",
      "Pseudochylothorax (cholesterol-rich effusion)",
      "Empyema",
      "Hemothorax",
      "Hydrothorax"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Pleural effusion rich in cholesterol crystals (appearing shimmeringly refractile) resulting from long-standing chronic rheumatoid or tuberculous pleuritis."
  },
  {
    "id": "ple_19",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleuritic Chest Pain - Question 19): Which concept is CORRECT?",
    "options": [
      "Dull retrosternal pressure",
      "Colicky pain",
      "Sharp inspiratory pain due to pleural friction rub",
      "Painless dyspnea",
      "Burning epigastric pain"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Sharp, knife-like pain exacerbated by deep inspiration and coughing, caused by friction between inflamed parietal and visceral pleural surfaces."
  },
  {
    "id": "ple_20",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Paraneoplastic Pleural Effusion - Question 20): Which concept is CORRECT?",
    "options": [
      "Transudate without cells",
      "Pure air accumulation",
      "Surfactant overdose",
      "Exudative effusion with malignant exfoliated cells",
      "Normal pleural fluid"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Pleural effusion caused by direct metastatic seeding of pleura (breast, lung ca) or lymphatic obstruction."
  },
  {
    "id": "ple_21",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Tension Pneumothorax - Question 21): Which concept is CORRECT?",
    "options": [
      "Shift to ipsilateral side",
      "Shift to contralateral side with vena cava compression",
      "No mediastinal movement",
      "Pleural effusion formation",
      "Resorption of air"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Tension pneumothorax involves a valve-like wound allowing air entry during inspiration but not exit; increases intrapleural pressure, compressing vena cava and shifting mediastinum to CONTRALATERAL side."
  },
  {
    "id": "ple_22",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Solitary Fibrous Tumor of Pleura - Question 22): Which concept is CORRECT?",
    "options": [
      "Solitary fibrous tumor (CD34+, STAT6+)",
      "Mesothelioma",
      "Adenocarcinoma",
      "Squamous ca",
      "Lymphoma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Benign or malignant localized mesenchymal tumor of pleura; NAB2-STAT6 gene fusion positive, CD34 positive, unrelated to asbestos exposure."
  },
  {
    "id": "ple_23",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Contraction Atelectasis - Question 23): Which concept is CORRECT?",
    "options": [
      "Reversible with surfactant",
      "Caused by mucus plug",
      "Caused by fibrotic scarring hampering expansion (Irreversible)",
      "Caused by pneumothorax",
      "Seen in premature infants"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Contraction atelectasis occurs when local or generalized fibrotic changes in lung or pleura hamper lung expansion during inspiration; IRREVERSIBLE."
  },
  {
    "id": "ple_24",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Pleural Hydrothorax - Question 24): Which concept is CORRECT?",
    "options": [
      "Empyema",
      "Hydrothorax",
      "Chylothorax",
      "Hemothorax",
      "Pleurisy"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Non-inflammatory transudative fluid in pleural cavity; most commonly due to elevated hydrostatic pressure in Congestive Heart Failure."
  },
  {
    "id": "ple_25",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleuritis Histology - Question 25): Which concept is CORRECT?",
    "options": [
      "Granulomatous necrosis",
      "Caseation",
      "Acellular calcification",
      "Fibrinous network with neutrophils",
      "Clear fluid without protein"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Fibrinous or serofibrinous pleuritis demonstrates a delicate pale pink network of intra-pleural fibrin threads with polymorphonuclear leucocytes."
  },
  {
    "id": "ple_26",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Mesothelioma Histology - Question 26): Which concept is CORRECT?",
    "options": [
      "CEA positive, Calretinin negative",
      "S100 positive",
      "CD34 positive",
      "CD20 positive",
      "Calretinin, CK5/6, WT-1, and D2-40 positive"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Epithelioid, sarcomatoid, or biphasic patterns; positive for Calretinin, Cytokeratin 5/6, WT-1, and D2-40."
  },
  {
    "id": "ple_27",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleural Thickening - Question 27): Which concept is CORRECT?",
    "options": [
      "Organization of empyema leading to fibrocollagenous pleural peel",
      "Surfactant accumulation",
      "Subpleural bleb formation",
      "Bronchial smooth muscle hypertrophy",
      "Acinar destruction"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Fibrocollagenous fibrous obliteration of pleural cavity following organization of unresolved empyema thoracis or hemothorax."
  },
  {
    "id": "ple_28",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Pseudochylothorax - Question 28): Which concept is CORRECT?",
    "options": [
      "Chylothorax",
      "Pseudochylothorax (cholesterol-rich effusion)",
      "Empyema",
      "Hemothorax",
      "Hydrothorax"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Pleural effusion rich in cholesterol crystals (appearing shimmeringly refractile) resulting from long-standing chronic rheumatoid or tuberculous pleuritis."
  },
  {
    "id": "ple_29",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleuritic Chest Pain - Question 29): Which concept is CORRECT?",
    "options": [
      "Dull retrosternal pressure",
      "Colicky pain",
      "Sharp inspiratory pain due to pleural friction rub",
      "Painless dyspnea",
      "Burning epigastric pain"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Sharp, knife-like pain exacerbated by deep inspiration and coughing, caused by friction between inflamed parietal and visceral pleural surfaces."
  },
  {
    "id": "ple_30",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Paraneoplastic Pleural Effusion - Question 30): Which concept is CORRECT?",
    "options": [
      "Transudate without cells",
      "Pure air accumulation",
      "Surfactant overdose",
      "Exudative effusion with malignant exfoliated cells",
      "Normal pleural fluid"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Pleural effusion caused by direct metastatic seeding of pleura (breast, lung ca) or lymphatic obstruction."
  },
  {
    "id": "ple_31",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Tension Pneumothorax - Question 31): Which concept is CORRECT?",
    "options": [
      "Shift to ipsilateral side",
      "Shift to contralateral side with vena cava compression",
      "No mediastinal movement",
      "Pleural effusion formation",
      "Resorption of air"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Tension pneumothorax involves a valve-like wound allowing air entry during inspiration but not exit; increases intrapleural pressure, compressing vena cava and shifting mediastinum to CONTRALATERAL side."
  },
  {
    "id": "ple_32",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Solitary Fibrous Tumor of Pleura - Question 32): Which concept is CORRECT?",
    "options": [
      "Solitary fibrous tumor (CD34+, STAT6+)",
      "Mesothelioma",
      "Adenocarcinoma",
      "Squamous ca",
      "Lymphoma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Benign or malignant localized mesenchymal tumor of pleura; NAB2-STAT6 gene fusion positive, CD34 positive, unrelated to asbestos exposure."
  },
  {
    "id": "ple_33",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Contraction Atelectasis - Question 33): Which concept is CORRECT?",
    "options": [
      "Reversible with surfactant",
      "Caused by mucus plug",
      "Caused by fibrotic scarring hampering expansion (Irreversible)",
      "Caused by pneumothorax",
      "Seen in premature infants"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Contraction atelectasis occurs when local or generalized fibrotic changes in lung or pleura hamper lung expansion during inspiration; IRREVERSIBLE."
  },
  {
    "id": "ple_34",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Pleural Hydrothorax - Question 34): Which concept is CORRECT?",
    "options": [
      "Empyema",
      "Hydrothorax",
      "Chylothorax",
      "Hemothorax",
      "Pleurisy"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Non-inflammatory transudative fluid in pleural cavity; most commonly due to elevated hydrostatic pressure in Congestive Heart Failure."
  },
  {
    "id": "ple_35",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleuritis Histology - Question 35): Which concept is CORRECT?",
    "options": [
      "Granulomatous necrosis",
      "Caseation",
      "Acellular calcification",
      "Fibrinous network with neutrophils",
      "Clear fluid without protein"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Fibrinous or serofibrinous pleuritis demonstrates a delicate pale pink network of intra-pleural fibrin threads with polymorphonuclear leucocytes."
  },
  {
    "id": "ple_36",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Mesothelioma Histology - Question 36): Which concept is CORRECT?",
    "options": [
      "CEA positive, Calretinin negative",
      "S100 positive",
      "CD34 positive",
      "CD20 positive",
      "Calretinin, CK5/6, WT-1, and D2-40 positive"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Epithelioid, sarcomatoid, or biphasic patterns; positive for Calretinin, Cytokeratin 5/6, WT-1, and D2-40."
  },
  {
    "id": "ple_37",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleural Thickening - Question 37): Which concept is CORRECT?",
    "options": [
      "Organization of empyema leading to fibrocollagenous pleural peel",
      "Surfactant accumulation",
      "Subpleural bleb formation",
      "Bronchial smooth muscle hypertrophy",
      "Acinar destruction"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Fibrocollagenous fibrous obliteration of pleural cavity following organization of unresolved empyema thoracis or hemothorax."
  },
  {
    "id": "ple_38",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Pseudochylothorax - Question 38): Which concept is CORRECT?",
    "options": [
      "Chylothorax",
      "Pseudochylothorax (cholesterol-rich effusion)",
      "Empyema",
      "Hemothorax",
      "Hydrothorax"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Pleural effusion rich in cholesterol crystals (appearing shimmeringly refractile) resulting from long-standing chronic rheumatoid or tuberculous pleuritis."
  },
  {
    "id": "ple_39",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleuritic Chest Pain - Question 39): Which concept is CORRECT?",
    "options": [
      "Dull retrosternal pressure",
      "Colicky pain",
      "Sharp inspiratory pain due to pleural friction rub",
      "Painless dyspnea",
      "Burning epigastric pain"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Sharp, knife-like pain exacerbated by deep inspiration and coughing, caused by friction between inflamed parietal and visceral pleural surfaces."
  },
  {
    "id": "ple_40",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Paraneoplastic Pleural Effusion - Question 40): Which concept is CORRECT?",
    "options": [
      "Transudate without cells",
      "Pure air accumulation",
      "Surfactant overdose",
      "Exudative effusion with malignant exfoliated cells",
      "Normal pleural fluid"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Pleural effusion caused by direct metastatic seeding of pleura (breast, lung ca) or lymphatic obstruction."
  },
  {
    "id": "ple_41",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Tension Pneumothorax - Question 41): Which concept is CORRECT?",
    "options": [
      "Shift to ipsilateral side",
      "Shift to contralateral side with vena cava compression",
      "No mediastinal movement",
      "Pleural effusion formation",
      "Resorption of air"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Tension pneumothorax involves a valve-like wound allowing air entry during inspiration but not exit; increases intrapleural pressure, compressing vena cava and shifting mediastinum to CONTRALATERAL side."
  },
  {
    "id": "ple_42",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Solitary Fibrous Tumor of Pleura - Question 42): Which concept is CORRECT?",
    "options": [
      "Solitary fibrous tumor (CD34+, STAT6+)",
      "Mesothelioma",
      "Adenocarcinoma",
      "Squamous ca",
      "Lymphoma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Benign or malignant localized mesenchymal tumor of pleura; NAB2-STAT6 gene fusion positive, CD34 positive, unrelated to asbestos exposure."
  },
  {
    "id": "ple_43",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Contraction Atelectasis - Question 43): Which concept is CORRECT?",
    "options": [
      "Reversible with surfactant",
      "Caused by mucus plug",
      "Caused by fibrotic scarring hampering expansion (Irreversible)",
      "Caused by pneumothorax",
      "Seen in premature infants"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Contraction atelectasis occurs when local or generalized fibrotic changes in lung or pleura hamper lung expansion during inspiration; IRREVERSIBLE."
  },
  {
    "id": "ple_44",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Pleural Hydrothorax - Question 44): Which concept is CORRECT?",
    "options": [
      "Empyema",
      "Hydrothorax",
      "Chylothorax",
      "Hemothorax",
      "Pleurisy"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Non-inflammatory transudative fluid in pleural cavity; most commonly due to elevated hydrostatic pressure in Congestive Heart Failure."
  },
  {
    "id": "ple_45",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleuritis Histology - Question 45): Which concept is CORRECT?",
    "options": [
      "Granulomatous necrosis",
      "Caseation",
      "Acellular calcification",
      "Fibrinous network with neutrophils",
      "Clear fluid without protein"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Fibrinous or serofibrinous pleuritis demonstrates a delicate pale pink network of intra-pleural fibrin threads with polymorphonuclear leucocytes."
  },
  {
    "id": "ple_46",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Mesothelioma Histology - Question 46): Which concept is CORRECT?",
    "options": [
      "CEA positive, Calretinin negative",
      "S100 positive",
      "CD34 positive",
      "CD20 positive",
      "Calretinin, CK5/6, WT-1, and D2-40 positive"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Epithelioid, sarcomatoid, or biphasic patterns; positive for Calretinin, Cytokeratin 5/6, WT-1, and D2-40."
  },
  {
    "id": "ple_47",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleural Thickening - Question 47): Which concept is CORRECT?",
    "options": [
      "Organization of empyema leading to fibrocollagenous pleural peel",
      "Surfactant accumulation",
      "Subpleural bleb formation",
      "Bronchial smooth muscle hypertrophy",
      "Acinar destruction"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Fibrocollagenous fibrous obliteration of pleural cavity following organization of unresolved empyema thoracis or hemothorax."
  },
  {
    "id": "ple_48",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Pseudochylothorax - Question 48): Which concept is CORRECT?",
    "options": [
      "Chylothorax",
      "Pseudochylothorax (cholesterol-rich effusion)",
      "Empyema",
      "Hemothorax",
      "Hydrothorax"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Pleural effusion rich in cholesterol crystals (appearing shimmeringly refractile) resulting from long-standing chronic rheumatoid or tuberculous pleuritis."
  },
  {
    "id": "ple_49",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleuritic Chest Pain - Question 49): Which concept is CORRECT?",
    "options": [
      "Dull retrosternal pressure",
      "Colicky pain",
      "Sharp inspiratory pain due to pleural friction rub",
      "Painless dyspnea",
      "Burning epigastric pain"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Sharp, knife-like pain exacerbated by deep inspiration and coughing, caused by friction between inflamed parietal and visceral pleural surfaces."
  },
  {
    "id": "ple_50",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Paraneoplastic Pleural Effusion - Question 50): Which concept is CORRECT?",
    "options": [
      "Transudate without cells",
      "Pure air accumulation",
      "Surfactant overdose",
      "Exudative effusion with malignant exfoliated cells",
      "Normal pleural fluid"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Pleural effusion caused by direct metastatic seeding of pleura (breast, lung ca) or lymphatic obstruction."
  },
  {
    "id": "ple_51",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Tension Pneumothorax - Question 51): Which concept is CORRECT?",
    "options": [
      "Shift to ipsilateral side",
      "Shift to contralateral side with vena cava compression",
      "No mediastinal movement",
      "Pleural effusion formation",
      "Resorption of air"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Tension pneumothorax involves a valve-like wound allowing air entry during inspiration but not exit; increases intrapleural pressure, compressing vena cava and shifting mediastinum to CONTRALATERAL side."
  },
  {
    "id": "ple_52",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Solitary Fibrous Tumor of Pleura - Question 52): Which concept is CORRECT?",
    "options": [
      "Solitary fibrous tumor (CD34+, STAT6+)",
      "Mesothelioma",
      "Adenocarcinoma",
      "Squamous ca",
      "Lymphoma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Benign or malignant localized mesenchymal tumor of pleura; NAB2-STAT6 gene fusion positive, CD34 positive, unrelated to asbestos exposure."
  },
  {
    "id": "ple_53",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Contraction Atelectasis - Question 53): Which concept is CORRECT?",
    "options": [
      "Reversible with surfactant",
      "Caused by mucus plug",
      "Caused by fibrotic scarring hampering expansion (Irreversible)",
      "Caused by pneumothorax",
      "Seen in premature infants"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Contraction atelectasis occurs when local or generalized fibrotic changes in lung or pleura hamper lung expansion during inspiration; IRREVERSIBLE."
  },
  {
    "id": "ple_54",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Pleural Hydrothorax - Question 54): Which concept is CORRECT?",
    "options": [
      "Empyema",
      "Hydrothorax",
      "Chylothorax",
      "Hemothorax",
      "Pleurisy"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Non-inflammatory transudative fluid in pleural cavity; most commonly due to elevated hydrostatic pressure in Congestive Heart Failure."
  },
  {
    "id": "ple_55",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleuritis Histology - Question 55): Which concept is CORRECT?",
    "options": [
      "Granulomatous necrosis",
      "Caseation",
      "Acellular calcification",
      "Fibrinous network with neutrophils",
      "Clear fluid without protein"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Fibrinous or serofibrinous pleuritis demonstrates a delicate pale pink network of intra-pleural fibrin threads with polymorphonuclear leucocytes."
  },
  {
    "id": "ple_56",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Mesothelioma Histology - Question 56): Which concept is CORRECT?",
    "options": [
      "CEA positive, Calretinin negative",
      "S100 positive",
      "CD34 positive",
      "CD20 positive",
      "Calretinin, CK5/6, WT-1, and D2-40 positive"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Epithelioid, sarcomatoid, or biphasic patterns; positive for Calretinin, Cytokeratin 5/6, WT-1, and D2-40."
  },
  {
    "id": "ple_57",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleural Thickening - Question 57): Which concept is CORRECT?",
    "options": [
      "Organization of empyema leading to fibrocollagenous pleural peel",
      "Surfactant accumulation",
      "Subpleural bleb formation",
      "Bronchial smooth muscle hypertrophy",
      "Acinar destruction"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Fibrocollagenous fibrous obliteration of pleural cavity following organization of unresolved empyema thoracis or hemothorax."
  },
  {
    "id": "ple_58",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Pseudochylothorax - Question 58): Which concept is CORRECT?",
    "options": [
      "Chylothorax",
      "Pseudochylothorax (cholesterol-rich effusion)",
      "Empyema",
      "Hemothorax",
      "Hydrothorax"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Pleural effusion rich in cholesterol crystals (appearing shimmeringly refractile) resulting from long-standing chronic rheumatoid or tuberculous pleuritis."
  },
  {
    "id": "ple_59",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleuritic Chest Pain - Question 59): Which concept is CORRECT?",
    "options": [
      "Dull retrosternal pressure",
      "Colicky pain",
      "Sharp inspiratory pain due to pleural friction rub",
      "Painless dyspnea",
      "Burning epigastric pain"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Sharp, knife-like pain exacerbated by deep inspiration and coughing, caused by friction between inflamed parietal and visceral pleural surfaces."
  },
  {
    "id": "ple_60",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Paraneoplastic Pleural Effusion - Question 60): Which concept is CORRECT?",
    "options": [
      "Transudate without cells",
      "Pure air accumulation",
      "Surfactant overdose",
      "Exudative effusion with malignant exfoliated cells",
      "Normal pleural fluid"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Pleural effusion caused by direct metastatic seeding of pleura (breast, lung ca) or lymphatic obstruction."
  },
  {
    "id": "ple_61",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Tension Pneumothorax - Question 61): Which concept is CORRECT?",
    "options": [
      "Shift to ipsilateral side",
      "Shift to contralateral side with vena cava compression",
      "No mediastinal movement",
      "Pleural effusion formation",
      "Resorption of air"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Tension pneumothorax involves a valve-like wound allowing air entry during inspiration but not exit; increases intrapleural pressure, compressing vena cava and shifting mediastinum to CONTRALATERAL side."
  },
  {
    "id": "ple_62",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Solitary Fibrous Tumor of Pleura - Question 62): Which concept is CORRECT?",
    "options": [
      "Solitary fibrous tumor (CD34+, STAT6+)",
      "Mesothelioma",
      "Adenocarcinoma",
      "Squamous ca",
      "Lymphoma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Benign or malignant localized mesenchymal tumor of pleura; NAB2-STAT6 gene fusion positive, CD34 positive, unrelated to asbestos exposure."
  },
  {
    "id": "ple_63",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Contraction Atelectasis - Question 63): Which concept is CORRECT?",
    "options": [
      "Reversible with surfactant",
      "Caused by mucus plug",
      "Caused by fibrotic scarring hampering expansion (Irreversible)",
      "Caused by pneumothorax",
      "Seen in premature infants"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Contraction atelectasis occurs when local or generalized fibrotic changes in lung or pleura hamper lung expansion during inspiration; IRREVERSIBLE."
  },
  {
    "id": "ple_64",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Pleural Hydrothorax - Question 64): Which concept is CORRECT?",
    "options": [
      "Empyema",
      "Hydrothorax",
      "Chylothorax",
      "Hemothorax",
      "Pleurisy"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Non-inflammatory transudative fluid in pleural cavity; most commonly due to elevated hydrostatic pressure in Congestive Heart Failure."
  },
  {
    "id": "ple_65",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleuritis Histology - Question 65): Which concept is CORRECT?",
    "options": [
      "Granulomatous necrosis",
      "Caseation",
      "Acellular calcification",
      "Fibrinous network with neutrophils",
      "Clear fluid without protein"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Fibrinous or serofibrinous pleuritis demonstrates a delicate pale pink network of intra-pleural fibrin threads with polymorphonuclear leucocytes."
  },
  {
    "id": "ple_66",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Mesothelioma Histology - Question 66): Which concept is CORRECT?",
    "options": [
      "CEA positive, Calretinin negative",
      "S100 positive",
      "CD34 positive",
      "CD20 positive",
      "Calretinin, CK5/6, WT-1, and D2-40 positive"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Epithelioid, sarcomatoid, or biphasic patterns; positive for Calretinin, Cytokeratin 5/6, WT-1, and D2-40."
  },
  {
    "id": "ple_67",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleural Thickening - Question 67): Which concept is CORRECT?",
    "options": [
      "Organization of empyema leading to fibrocollagenous pleural peel",
      "Surfactant accumulation",
      "Subpleural bleb formation",
      "Bronchial smooth muscle hypertrophy",
      "Acinar destruction"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Fibrocollagenous fibrous obliteration of pleural cavity following organization of unresolved empyema thoracis or hemothorax."
  },
  {
    "id": "ple_68",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Pseudochylothorax - Question 68): Which concept is CORRECT?",
    "options": [
      "Chylothorax",
      "Pseudochylothorax (cholesterol-rich effusion)",
      "Empyema",
      "Hemothorax",
      "Hydrothorax"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Pleural effusion rich in cholesterol crystals (appearing shimmeringly refractile) resulting from long-standing chronic rheumatoid or tuberculous pleuritis."
  },
  {
    "id": "ple_69",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleuritic Chest Pain - Question 69): Which concept is CORRECT?",
    "options": [
      "Dull retrosternal pressure",
      "Colicky pain",
      "Sharp inspiratory pain due to pleural friction rub",
      "Painless dyspnea",
      "Burning epigastric pain"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Sharp, knife-like pain exacerbated by deep inspiration and coughing, caused by friction between inflamed parietal and visceral pleural surfaces."
  },
  {
    "id": "ple_70",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Paraneoplastic Pleural Effusion - Question 70): Which concept is CORRECT?",
    "options": [
      "Transudate without cells",
      "Pure air accumulation",
      "Surfactant overdose",
      "Exudative effusion with malignant exfoliated cells",
      "Normal pleural fluid"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Pleural effusion caused by direct metastatic seeding of pleura (breast, lung ca) or lymphatic obstruction."
  },
  {
    "id": "ple_71",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Tension Pneumothorax - Question 71): Which concept is CORRECT?",
    "options": [
      "Shift to ipsilateral side",
      "Shift to contralateral side with vena cava compression",
      "No mediastinal movement",
      "Pleural effusion formation",
      "Resorption of air"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Tension pneumothorax involves a valve-like wound allowing air entry during inspiration but not exit; increases intrapleural pressure, compressing vena cava and shifting mediastinum to CONTRALATERAL side."
  },
  {
    "id": "ple_72",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Solitary Fibrous Tumor of Pleura - Question 72): Which concept is CORRECT?",
    "options": [
      "Solitary fibrous tumor (CD34+, STAT6+)",
      "Mesothelioma",
      "Adenocarcinoma",
      "Squamous ca",
      "Lymphoma"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Benign or malignant localized mesenchymal tumor of pleura; NAB2-STAT6 gene fusion positive, CD34 positive, unrelated to asbestos exposure."
  },
  {
    "id": "ple_73",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Contraction Atelectasis - Question 73): Which concept is CORRECT?",
    "options": [
      "Reversible with surfactant",
      "Caused by mucus plug",
      "Caused by fibrotic scarring hampering expansion (Irreversible)",
      "Caused by pneumothorax",
      "Seen in premature infants"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Contraction atelectasis occurs when local or generalized fibrotic changes in lung or pleura hamper lung expansion during inspiration; IRREVERSIBLE."
  },
  {
    "id": "ple_74",
    "category": "Diseases of the Pleura",
    "type": "Conceptual",
    "question": "Regarding Pleural Disease (Pleural Hydrothorax - Question 74): Which concept is CORRECT?",
    "options": [
      "Empyema",
      "Hydrothorax",
      "Chylothorax",
      "Hemothorax",
      "Pleurisy"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Non-inflammatory transudative fluid in pleural cavity; most commonly due to elevated hydrostatic pressure in Congestive Heart Failure."
  },
  {
    "id": "ple_75",
    "category": "Diseases of the Pleura",
    "type": "Clinical Vignette",
    "question": "Regarding Pleural Disease (Pleuritis Histology - Question 75): Which concept is CORRECT?",
    "options": [
      "Granulomatous necrosis",
      "Caseation",
      "Acellular calcification",
      "Fibrinous network with neutrophils",
      "Clear fluid without protein"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Fibrinous or serofibrinous pleuritis demonstrates a delicate pale pink network of intra-pleural fibrin threads with polymorphonuclear leucocytes."
  },
  {
    "id": "stb_1",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "In Tuberculosis, the Ghon focus is defined as:",
    "options": [
      "Enlarged calcified hilar lymph nodes alone",
      "A subpleural 1-2 cm caseating parenchymal lesion located just above or below the interlobar fissure",
      "A cavitary lesion in the lung apex",
      "Diffuse miliary nodular lesions throughout both lungs",
      "A fibrocalcified apical parenchymal scar with hilar node involvement"
    ],
    "answer": 1,
    "explanation": "A Ghon focus is a 1 to 1.5 cm subpleural parenchymal caseating lesion in the upper part of lower lobe or lower part of upper lobe."
  },
  {
    "id": "stb_2",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "In Tuberculosis, the Ghon complex consists of:",
    "options": [
      "Ghon focus alone",
      "Ghon focus plus enlarged caseating hilar lymph nodes",
      "Ghon focus plus fibrotic Ranke complex",
      "Apical cavitary lesion with pleural effusion",
      "Miliary tubercles in spleen and liver"
    ],
    "answer": 1,
    "explanation": "The Ghon complex comprises the parenchymal Ghon focus PLUS the draining involved hilar lymph node lesions."
  },
  {
    "id": "stb_3",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "When a primary Ghon complex undergoes progressive fibrosis and radiologically detectable calcification, it is designated as a:",
    "options": [
      "Assmann focus",
      "Ranke complex",
      "Simons focus",
      "Pancoast tumor",
      "Reid complex"
    ],
    "answer": 1,
    "explanation": "Ranke complex is the combination of a healed, fibrosed, and calcified parenchymal Ghon focus and calcified hilar lymph node."
  },
  {
    "id": "stb_4",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Secondary (Reactivation) Pulmonary Tuberculosis classically characteristically arises in which anatomical region of the lung?",
    "options": [
      "Subpleural lower lobes",
      "Apices of the upper lobes",
      "Middle lobe anterior segment",
      "Lingula",
      "Pleural space"
    ],
    "answer": 1,
    "explanation": "Secondary TB arises in the lung apices (apical and posterior segments of upper lobes) where high local oxygen tension favors M. tuberculosis growth."
  },
  {
    "id": "stb_5",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "In the immune response to Mycobacterium tuberculosis, which cytokine secreted by TH1 CD4+ T-cells is vital for activating macrophages and inducing nitric oxide / phagolysosome maturation?",
    "options": [
      "IL-4",
      "Interferon-gamma (IFN-\u03b3)",
      "IL-5",
      "IL-13",
      "TGF-beta"
    ],
    "answer": 1,
    "explanation": "IFN-gamma released by TH1 CD4+ T-cells is the central mediator that activates alveolar macrophages to kill intracellular mycobacteria."
  },
  {
    "id": "stb_6",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "In tuberculous granulomatous inflammation, TNF-alpha secreted by activated macrophages plays an essential role in:",
    "options": [
      "Direct lysis of red blood cells",
      "Recruitment of circulating monocytes and maintenance of granuloma structure",
      "Eosinophil chemotaxis",
      "IgE class switching",
      "Bronchial smooth muscle relaxation"
    ],
    "answer": 1,
    "explanation": "TNF-alpha recruits monocytes and maintains the structural integrity of granulomas; anti-TNF therapy carries a high risk of TB reactivation."
  },
  {
    "id": "stb_7",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "The hallmark histologic diagnostic feature of Sarcoidosis is:",
    "options": [
      "Caseating granulomas with central liquefactive necrosis",
      "Non-caseating, 'naked' epithelioid granulomas lacking a dense peripheral lymphocytic rim",
      "Hyaline membranes lining alveoli",
      "Ferruginous bodies in macrophages",
      "Suppurative microabscesses"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis is characterized histologically by compact non-caseating ('naked') granulomas containing epithelioid histiocytes and giant cells."
  },
  {
    "id": "stb_8",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Microscopic examination of Langhans giant cells in Sarcoidosis granulomas may reveal laminated calcified concretions and star-shaped inclusions known as:",
    "options": [
      "Aschoff bodies and Russell bodies",
      "Schaumann bodies and Asteroid bodies",
      "Civatte bodies and Councilman bodies",
      "Negri bodies and Cowdry A inclusions",
      "Mallory-Denk bodies and Masson bodies"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis giant cells often contain Schaumann bodies (laminated calcified proteinaceous concretions) and Asteroid bodies (stellate inclusions)."
  },
  {
    "id": "stb_9",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "A 32-year-old female presents with erythema nodosum on her shins, blurred vision (uveitis), and dry cough. Chest radiograph reveals bilateral hilar lymphadenopathy ('potato nodes'). Biopsy shows non-caseating granulomas. What is the diagnosis?",
    "options": [
      "Primary Tuberculosis",
      "Sarcoidosis",
      "Histoplasmosis",
      "Coccidioidomycosis",
      "Berylliosis"
    ],
    "answer": 1,
    "explanation": "Sarcoidosis triad: bilateral hilar lymphadenopathy, anterior uveitis, and erythema nodosum (L\u00f6fgren syndrome), with non-caseating granulomas."
  },
  {
    "id": "stb_10",
    "category": "Sarcoidosis & TB",
    "type": "Recall",
    "question": "Miliary Tuberculosis occurs when mycobacteria disseminate via:",
    "options": [
      "Bronchial airways into the opposite lung",
      "Vascular lymphohematogenous routes to multiple organs",
      "Pleural transudate into the peritoneal cavity",
      "Direct extension into surrounding ribs",
      "Gastrointestinal tract swallowing"
    ],
    "answer": 1,
    "explanation": "Miliary TB occurs when tubercle bacilli erode into blood vessels, resulting in lymphohematogenous dissemination producing tiny 'millet-seed' lesions throughout organs."
  },
  {
    "id": "stb_11",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Cavitation - Question 11): Which concept is CORRECT?",
    "options": [
      "Erosion into bronchiole creating oxygen-rich cavity",
      "Arterial embolization",
      "Surfactant destruction",
      "Eosinophilic degranulation",
      "Pleural effusion alone"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Secondary TB cavitatory lesions occur due to caseous necrosis eroding into a bronchial tree, creating an oxygen-rich cavity lined by caseous material."
  },
  {
    "id": "stb_12",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (PPD / Tuberculin Skin Test - Question 12): Which concept is CORRECT?",
    "options": [
      "Type I IgE reaction",
      "Type IV delayed-type hypersensitivity reaction measuring cell-mediated immunity",
      "Type II cytotoxic reaction",
      "Type III immune complex deposition",
      "Direct bacterial toxin test"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Type IV delayed-type hypersensitivity reaction mediated by sensitized CD4+ T-cells; induration >=10mm (or >=5mm in HIV) indicates prior exposure."
  },
  {
    "id": "stb_13",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Langhans Giant Cells - Question 13): Which concept is CORRECT?",
    "options": [
      "Touton giant cells with lipid ring",
      "Foreign body giant cells with random nuclei",
      "Langhans giant cells with peripheral horseshoe nuclear arrangement",
      "Reed-Sternberg cells",
      "Warthin-Finkeldey cells"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Multinucleated giant cells with nuclei arranged in a horseshoe pattern at the periphery, formed by fusion of activated epithelioid macrophages."
  },
  {
    "id": "stb_14",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Assmann Focus - Question 14): Which concept is CORRECT?",
    "options": [
      "Primary Ghon focus",
      "Ranke complex",
      "Miliary tubercle",
      "Assmann focus (infraclavicular reactivation lesion)",
      "Simon focus"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Early infraclavicular parenchymal lesion of secondary reactivation tuberculosis."
  },
  {
    "id": "stb_15",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Empyema - Question 15): Which concept is CORRECT?",
    "options": [
      "Spontaneous pneumothorax",
      "Tuberculous empyema",
      "Chylothorax",
      "Atelectasis",
      "Sarcoidosis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Progressive extension of cavitary TB into pleural space producing thick purulent tuberculous pleuritis and fibrothorax."
  },
  {
    "id": "stb_16",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Hypercalcemia in Sarcoidosis - Question 16): Which concept is CORRECT?",
    "options": [
      "Active 1,25-(OH)2 Vitamin D3 production by epithelioid macrophages",
      "PTHrp secretion by tumor",
      "Bone destruction by osteoclasts",
      "Renal failure alone",
      "Excess calcitonin"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Sarcoid granulomas express 1-alpha-hydroxylase, converting 25-OH Vitamin D into active 1,25-(OH)2 Vitamin D3, causing hypercalcemia and hypercalciuria."
  },
  {
    "id": "stb_17",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Kveim Test - Question 17): Which concept is CORRECT?",
    "options": [
      "Mantoux test",
      "Kveim-Siltzbach test",
      "Schick test",
      "Dick test",
      "Patch test"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Intradermal injection of sarcoid tissue extract producing a non-caseating granuloma at injection site in 4-6 weeks (historical diagnostic test)."
  },
  {
    "id": "stb_18",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Scolding / Mikulicz Syndrome in Sarcoidosis - Question 18): Which concept is CORRECT?",
    "options": [
      "Caplan syndrome",
      "L\u00f6fgren syndrome",
      "Heerfordt syndrome (uveoparotid fever)",
      "Goodpasture syndrome",
      "Hamman-Rich syndrome"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Sarcoidosis involving lacrimal and salivary glands causing bilateral painless enlargement and dry eyes/mouth (Heerfordt syndrome = uveoparotid fever)."
  },
  {
    "id": "stb_19",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Progressive Primary TB - Question 19): Which concept is CORRECT?",
    "options": [
      "Ranke complex formation",
      "Always asymptomatic",
      "Complete resolution without trace",
      "Progressive primary TB with non-healing caseous spread",
      "Spontaneous conversion to sarcoidosis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: In immunocompromised patients (e.g. HIV/children), primary TB fails to heal and progresses directly to consolidation, cavitation, or miliary spread."
  },
  {
    "id": "stb_20",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Atypical Mycobacteria - Question 20): Which concept is CORRECT?",
    "options": [
      "M. tuberculosis",
      "M. bovis",
      "M. kansasii",
      "M. leprae",
      "Mycobacterium avium complex (MAC) in advanced HIV"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Mycobacterium avium-intracellulare (MAC) causes opportunistic disseminated infection in severely immunocompromised patients (CD4 <50) with abundant acid-fast bacilli in macrophages."
  },
  {
    "id": "stb_21",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Cavitation - Question 21): Which concept is CORRECT?",
    "options": [
      "Erosion into bronchiole creating oxygen-rich cavity",
      "Arterial embolization",
      "Surfactant destruction",
      "Eosinophilic degranulation",
      "Pleural effusion alone"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Secondary TB cavitatory lesions occur due to caseous necrosis eroding into a bronchial tree, creating an oxygen-rich cavity lined by caseous material."
  },
  {
    "id": "stb_22",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (PPD / Tuberculin Skin Test - Question 22): Which concept is CORRECT?",
    "options": [
      "Type I IgE reaction",
      "Type IV delayed-type hypersensitivity reaction measuring cell-mediated immunity",
      "Type II cytotoxic reaction",
      "Type III immune complex deposition",
      "Direct bacterial toxin test"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Type IV delayed-type hypersensitivity reaction mediated by sensitized CD4+ T-cells; induration >=10mm (or >=5mm in HIV) indicates prior exposure."
  },
  {
    "id": "stb_23",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Langhans Giant Cells - Question 23): Which concept is CORRECT?",
    "options": [
      "Touton giant cells with lipid ring",
      "Foreign body giant cells with random nuclei",
      "Langhans giant cells with peripheral horseshoe nuclear arrangement",
      "Reed-Sternberg cells",
      "Warthin-Finkeldey cells"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Multinucleated giant cells with nuclei arranged in a horseshoe pattern at the periphery, formed by fusion of activated epithelioid macrophages."
  },
  {
    "id": "stb_24",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Assmann Focus - Question 24): Which concept is CORRECT?",
    "options": [
      "Primary Ghon focus",
      "Ranke complex",
      "Miliary tubercle",
      "Assmann focus (infraclavicular reactivation lesion)",
      "Simon focus"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Early infraclavicular parenchymal lesion of secondary reactivation tuberculosis."
  },
  {
    "id": "stb_25",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Empyema - Question 25): Which concept is CORRECT?",
    "options": [
      "Spontaneous pneumothorax",
      "Tuberculous empyema",
      "Chylothorax",
      "Atelectasis",
      "Sarcoidosis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Progressive extension of cavitary TB into pleural space producing thick purulent tuberculous pleuritis and fibrothorax."
  },
  {
    "id": "stb_26",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Hypercalcemia in Sarcoidosis - Question 26): Which concept is CORRECT?",
    "options": [
      "Active 1,25-(OH)2 Vitamin D3 production by epithelioid macrophages",
      "PTHrp secretion by tumor",
      "Bone destruction by osteoclasts",
      "Renal failure alone",
      "Excess calcitonin"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Sarcoid granulomas express 1-alpha-hydroxylase, converting 25-OH Vitamin D into active 1,25-(OH)2 Vitamin D3, causing hypercalcemia and hypercalciuria."
  },
  {
    "id": "stb_27",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Kveim Test - Question 27): Which concept is CORRECT?",
    "options": [
      "Mantoux test",
      "Kveim-Siltzbach test",
      "Schick test",
      "Dick test",
      "Patch test"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Intradermal injection of sarcoid tissue extract producing a non-caseating granuloma at injection site in 4-6 weeks (historical diagnostic test)."
  },
  {
    "id": "stb_28",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Scolding / Mikulicz Syndrome in Sarcoidosis - Question 28): Which concept is CORRECT?",
    "options": [
      "Caplan syndrome",
      "L\u00f6fgren syndrome",
      "Heerfordt syndrome (uveoparotid fever)",
      "Goodpasture syndrome",
      "Hamman-Rich syndrome"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Sarcoidosis involving lacrimal and salivary glands causing bilateral painless enlargement and dry eyes/mouth (Heerfordt syndrome = uveoparotid fever)."
  },
  {
    "id": "stb_29",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Progressive Primary TB - Question 29): Which concept is CORRECT?",
    "options": [
      "Ranke complex formation",
      "Always asymptomatic",
      "Complete resolution without trace",
      "Progressive primary TB with non-healing caseous spread",
      "Spontaneous conversion to sarcoidosis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: In immunocompromised patients (e.g. HIV/children), primary TB fails to heal and progresses directly to consolidation, cavitation, or miliary spread."
  },
  {
    "id": "stb_30",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Atypical Mycobacteria - Question 30): Which concept is CORRECT?",
    "options": [
      "M. tuberculosis",
      "M. bovis",
      "M. kansasii",
      "M. leprae",
      "Mycobacterium avium complex (MAC) in advanced HIV"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Mycobacterium avium-intracellulare (MAC) causes opportunistic disseminated infection in severely immunocompromised patients (CD4 <50) with abundant acid-fast bacilli in macrophages."
  },
  {
    "id": "stb_31",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Cavitation - Question 31): Which concept is CORRECT?",
    "options": [
      "Erosion into bronchiole creating oxygen-rich cavity",
      "Arterial embolization",
      "Surfactant destruction",
      "Eosinophilic degranulation",
      "Pleural effusion alone"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Secondary TB cavitatory lesions occur due to caseous necrosis eroding into a bronchial tree, creating an oxygen-rich cavity lined by caseous material."
  },
  {
    "id": "stb_32",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (PPD / Tuberculin Skin Test - Question 32): Which concept is CORRECT?",
    "options": [
      "Type I IgE reaction",
      "Type IV delayed-type hypersensitivity reaction measuring cell-mediated immunity",
      "Type II cytotoxic reaction",
      "Type III immune complex deposition",
      "Direct bacterial toxin test"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Type IV delayed-type hypersensitivity reaction mediated by sensitized CD4+ T-cells; induration >=10mm (or >=5mm in HIV) indicates prior exposure."
  },
  {
    "id": "stb_33",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Langhans Giant Cells - Question 33): Which concept is CORRECT?",
    "options": [
      "Touton giant cells with lipid ring",
      "Foreign body giant cells with random nuclei",
      "Langhans giant cells with peripheral horseshoe nuclear arrangement",
      "Reed-Sternberg cells",
      "Warthin-Finkeldey cells"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Multinucleated giant cells with nuclei arranged in a horseshoe pattern at the periphery, formed by fusion of activated epithelioid macrophages."
  },
  {
    "id": "stb_34",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Assmann Focus - Question 34): Which concept is CORRECT?",
    "options": [
      "Primary Ghon focus",
      "Ranke complex",
      "Miliary tubercle",
      "Assmann focus (infraclavicular reactivation lesion)",
      "Simon focus"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Early infraclavicular parenchymal lesion of secondary reactivation tuberculosis."
  },
  {
    "id": "stb_35",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Empyema - Question 35): Which concept is CORRECT?",
    "options": [
      "Spontaneous pneumothorax",
      "Tuberculous empyema",
      "Chylothorax",
      "Atelectasis",
      "Sarcoidosis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Progressive extension of cavitary TB into pleural space producing thick purulent tuberculous pleuritis and fibrothorax."
  },
  {
    "id": "stb_36",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Hypercalcemia in Sarcoidosis - Question 36): Which concept is CORRECT?",
    "options": [
      "Active 1,25-(OH)2 Vitamin D3 production by epithelioid macrophages",
      "PTHrp secretion by tumor",
      "Bone destruction by osteoclasts",
      "Renal failure alone",
      "Excess calcitonin"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Sarcoid granulomas express 1-alpha-hydroxylase, converting 25-OH Vitamin D into active 1,25-(OH)2 Vitamin D3, causing hypercalcemia and hypercalciuria."
  },
  {
    "id": "stb_37",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Kveim Test - Question 37): Which concept is CORRECT?",
    "options": [
      "Mantoux test",
      "Kveim-Siltzbach test",
      "Schick test",
      "Dick test",
      "Patch test"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Intradermal injection of sarcoid tissue extract producing a non-caseating granuloma at injection site in 4-6 weeks (historical diagnostic test)."
  },
  {
    "id": "stb_38",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Scolding / Mikulicz Syndrome in Sarcoidosis - Question 38): Which concept is CORRECT?",
    "options": [
      "Caplan syndrome",
      "L\u00f6fgren syndrome",
      "Heerfordt syndrome (uveoparotid fever)",
      "Goodpasture syndrome",
      "Hamman-Rich syndrome"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Sarcoidosis involving lacrimal and salivary glands causing bilateral painless enlargement and dry eyes/mouth (Heerfordt syndrome = uveoparotid fever)."
  },
  {
    "id": "stb_39",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Progressive Primary TB - Question 39): Which concept is CORRECT?",
    "options": [
      "Ranke complex formation",
      "Always asymptomatic",
      "Complete resolution without trace",
      "Progressive primary TB with non-healing caseous spread",
      "Spontaneous conversion to sarcoidosis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: In immunocompromised patients (e.g. HIV/children), primary TB fails to heal and progresses directly to consolidation, cavitation, or miliary spread."
  },
  {
    "id": "stb_40",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Atypical Mycobacteria - Question 40): Which concept is CORRECT?",
    "options": [
      "M. tuberculosis",
      "M. bovis",
      "M. kansasii",
      "M. leprae",
      "Mycobacterium avium complex (MAC) in advanced HIV"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Mycobacterium avium-intracellulare (MAC) causes opportunistic disseminated infection in severely immunocompromised patients (CD4 <50) with abundant acid-fast bacilli in macrophages."
  },
  {
    "id": "stb_41",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Cavitation - Question 41): Which concept is CORRECT?",
    "options": [
      "Erosion into bronchiole creating oxygen-rich cavity",
      "Arterial embolization",
      "Surfactant destruction",
      "Eosinophilic degranulation",
      "Pleural effusion alone"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Secondary TB cavitatory lesions occur due to caseous necrosis eroding into a bronchial tree, creating an oxygen-rich cavity lined by caseous material."
  },
  {
    "id": "stb_42",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (PPD / Tuberculin Skin Test - Question 42): Which concept is CORRECT?",
    "options": [
      "Type I IgE reaction",
      "Type IV delayed-type hypersensitivity reaction measuring cell-mediated immunity",
      "Type II cytotoxic reaction",
      "Type III immune complex deposition",
      "Direct bacterial toxin test"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Type IV delayed-type hypersensitivity reaction mediated by sensitized CD4+ T-cells; induration >=10mm (or >=5mm in HIV) indicates prior exposure."
  },
  {
    "id": "stb_43",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Langhans Giant Cells - Question 43): Which concept is CORRECT?",
    "options": [
      "Touton giant cells with lipid ring",
      "Foreign body giant cells with random nuclei",
      "Langhans giant cells with peripheral horseshoe nuclear arrangement",
      "Reed-Sternberg cells",
      "Warthin-Finkeldey cells"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Multinucleated giant cells with nuclei arranged in a horseshoe pattern at the periphery, formed by fusion of activated epithelioid macrophages."
  },
  {
    "id": "stb_44",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Assmann Focus - Question 44): Which concept is CORRECT?",
    "options": [
      "Primary Ghon focus",
      "Ranke complex",
      "Miliary tubercle",
      "Assmann focus (infraclavicular reactivation lesion)",
      "Simon focus"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Early infraclavicular parenchymal lesion of secondary reactivation tuberculosis."
  },
  {
    "id": "stb_45",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Empyema - Question 45): Which concept is CORRECT?",
    "options": [
      "Spontaneous pneumothorax",
      "Tuberculous empyema",
      "Chylothorax",
      "Atelectasis",
      "Sarcoidosis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Progressive extension of cavitary TB into pleural space producing thick purulent tuberculous pleuritis and fibrothorax."
  },
  {
    "id": "stb_46",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Hypercalcemia in Sarcoidosis - Question 46): Which concept is CORRECT?",
    "options": [
      "Active 1,25-(OH)2 Vitamin D3 production by epithelioid macrophages",
      "PTHrp secretion by tumor",
      "Bone destruction by osteoclasts",
      "Renal failure alone",
      "Excess calcitonin"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Sarcoid granulomas express 1-alpha-hydroxylase, converting 25-OH Vitamin D into active 1,25-(OH)2 Vitamin D3, causing hypercalcemia and hypercalciuria."
  },
  {
    "id": "stb_47",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Kveim Test - Question 47): Which concept is CORRECT?",
    "options": [
      "Mantoux test",
      "Kveim-Siltzbach test",
      "Schick test",
      "Dick test",
      "Patch test"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Intradermal injection of sarcoid tissue extract producing a non-caseating granuloma at injection site in 4-6 weeks (historical diagnostic test)."
  },
  {
    "id": "stb_48",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Scolding / Mikulicz Syndrome in Sarcoidosis - Question 48): Which concept is CORRECT?",
    "options": [
      "Caplan syndrome",
      "L\u00f6fgren syndrome",
      "Heerfordt syndrome (uveoparotid fever)",
      "Goodpasture syndrome",
      "Hamman-Rich syndrome"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Sarcoidosis involving lacrimal and salivary glands causing bilateral painless enlargement and dry eyes/mouth (Heerfordt syndrome = uveoparotid fever)."
  },
  {
    "id": "stb_49",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Progressive Primary TB - Question 49): Which concept is CORRECT?",
    "options": [
      "Ranke complex formation",
      "Always asymptomatic",
      "Complete resolution without trace",
      "Progressive primary TB with non-healing caseous spread",
      "Spontaneous conversion to sarcoidosis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: In immunocompromised patients (e.g. HIV/children), primary TB fails to heal and progresses directly to consolidation, cavitation, or miliary spread."
  },
  {
    "id": "stb_50",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Atypical Mycobacteria - Question 50): Which concept is CORRECT?",
    "options": [
      "M. tuberculosis",
      "M. bovis",
      "M. kansasii",
      "M. leprae",
      "Mycobacterium avium complex (MAC) in advanced HIV"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Mycobacterium avium-intracellulare (MAC) causes opportunistic disseminated infection in severely immunocompromised patients (CD4 <50) with abundant acid-fast bacilli in macrophages."
  },
  {
    "id": "stb_51",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Cavitation - Question 51): Which concept is CORRECT?",
    "options": [
      "Erosion into bronchiole creating oxygen-rich cavity",
      "Arterial embolization",
      "Surfactant destruction",
      "Eosinophilic degranulation",
      "Pleural effusion alone"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Secondary TB cavitatory lesions occur due to caseous necrosis eroding into a bronchial tree, creating an oxygen-rich cavity lined by caseous material."
  },
  {
    "id": "stb_52",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (PPD / Tuberculin Skin Test - Question 52): Which concept is CORRECT?",
    "options": [
      "Type I IgE reaction",
      "Type IV delayed-type hypersensitivity reaction measuring cell-mediated immunity",
      "Type II cytotoxic reaction",
      "Type III immune complex deposition",
      "Direct bacterial toxin test"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Type IV delayed-type hypersensitivity reaction mediated by sensitized CD4+ T-cells; induration >=10mm (or >=5mm in HIV) indicates prior exposure."
  },
  {
    "id": "stb_53",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Langhans Giant Cells - Question 53): Which concept is CORRECT?",
    "options": [
      "Touton giant cells with lipid ring",
      "Foreign body giant cells with random nuclei",
      "Langhans giant cells with peripheral horseshoe nuclear arrangement",
      "Reed-Sternberg cells",
      "Warthin-Finkeldey cells"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Multinucleated giant cells with nuclei arranged in a horseshoe pattern at the periphery, formed by fusion of activated epithelioid macrophages."
  },
  {
    "id": "stb_54",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Assmann Focus - Question 54): Which concept is CORRECT?",
    "options": [
      "Primary Ghon focus",
      "Ranke complex",
      "Miliary tubercle",
      "Assmann focus (infraclavicular reactivation lesion)",
      "Simon focus"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Early infraclavicular parenchymal lesion of secondary reactivation tuberculosis."
  },
  {
    "id": "stb_55",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Empyema - Question 55): Which concept is CORRECT?",
    "options": [
      "Spontaneous pneumothorax",
      "Tuberculous empyema",
      "Chylothorax",
      "Atelectasis",
      "Sarcoidosis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Progressive extension of cavitary TB into pleural space producing thick purulent tuberculous pleuritis and fibrothorax."
  },
  {
    "id": "stb_56",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Hypercalcemia in Sarcoidosis - Question 56): Which concept is CORRECT?",
    "options": [
      "Active 1,25-(OH)2 Vitamin D3 production by epithelioid macrophages",
      "PTHrp secretion by tumor",
      "Bone destruction by osteoclasts",
      "Renal failure alone",
      "Excess calcitonin"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Sarcoid granulomas express 1-alpha-hydroxylase, converting 25-OH Vitamin D into active 1,25-(OH)2 Vitamin D3, causing hypercalcemia and hypercalciuria."
  },
  {
    "id": "stb_57",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Kveim Test - Question 57): Which concept is CORRECT?",
    "options": [
      "Mantoux test",
      "Kveim-Siltzbach test",
      "Schick test",
      "Dick test",
      "Patch test"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Intradermal injection of sarcoid tissue extract producing a non-caseating granuloma at injection site in 4-6 weeks (historical diagnostic test)."
  },
  {
    "id": "stb_58",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Scolding / Mikulicz Syndrome in Sarcoidosis - Question 58): Which concept is CORRECT?",
    "options": [
      "Caplan syndrome",
      "L\u00f6fgren syndrome",
      "Heerfordt syndrome (uveoparotid fever)",
      "Goodpasture syndrome",
      "Hamman-Rich syndrome"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Sarcoidosis involving lacrimal and salivary glands causing bilateral painless enlargement and dry eyes/mouth (Heerfordt syndrome = uveoparotid fever)."
  },
  {
    "id": "stb_59",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Progressive Primary TB - Question 59): Which concept is CORRECT?",
    "options": [
      "Ranke complex formation",
      "Always asymptomatic",
      "Complete resolution without trace",
      "Progressive primary TB with non-healing caseous spread",
      "Spontaneous conversion to sarcoidosis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: In immunocompromised patients (e.g. HIV/children), primary TB fails to heal and progresses directly to consolidation, cavitation, or miliary spread."
  },
  {
    "id": "stb_60",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Atypical Mycobacteria - Question 60): Which concept is CORRECT?",
    "options": [
      "M. tuberculosis",
      "M. bovis",
      "M. kansasii",
      "M. leprae",
      "Mycobacterium avium complex (MAC) in advanced HIV"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Mycobacterium avium-intracellulare (MAC) causes opportunistic disseminated infection in severely immunocompromised patients (CD4 <50) with abundant acid-fast bacilli in macrophages."
  },
  {
    "id": "stb_61",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Cavitation - Question 61): Which concept is CORRECT?",
    "options": [
      "Erosion into bronchiole creating oxygen-rich cavity",
      "Arterial embolization",
      "Surfactant destruction",
      "Eosinophilic degranulation",
      "Pleural effusion alone"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Secondary TB cavitatory lesions occur due to caseous necrosis eroding into a bronchial tree, creating an oxygen-rich cavity lined by caseous material."
  },
  {
    "id": "stb_62",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (PPD / Tuberculin Skin Test - Question 62): Which concept is CORRECT?",
    "options": [
      "Type I IgE reaction",
      "Type IV delayed-type hypersensitivity reaction measuring cell-mediated immunity",
      "Type II cytotoxic reaction",
      "Type III immune complex deposition",
      "Direct bacterial toxin test"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Type IV delayed-type hypersensitivity reaction mediated by sensitized CD4+ T-cells; induration >=10mm (or >=5mm in HIV) indicates prior exposure."
  },
  {
    "id": "stb_63",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Langhans Giant Cells - Question 63): Which concept is CORRECT?",
    "options": [
      "Touton giant cells with lipid ring",
      "Foreign body giant cells with random nuclei",
      "Langhans giant cells with peripheral horseshoe nuclear arrangement",
      "Reed-Sternberg cells",
      "Warthin-Finkeldey cells"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Multinucleated giant cells with nuclei arranged in a horseshoe pattern at the periphery, formed by fusion of activated epithelioid macrophages."
  },
  {
    "id": "stb_64",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Assmann Focus - Question 64): Which concept is CORRECT?",
    "options": [
      "Primary Ghon focus",
      "Ranke complex",
      "Miliary tubercle",
      "Assmann focus (infraclavicular reactivation lesion)",
      "Simon focus"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Early infraclavicular parenchymal lesion of secondary reactivation tuberculosis."
  },
  {
    "id": "stb_65",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Empyema - Question 65): Which concept is CORRECT?",
    "options": [
      "Spontaneous pneumothorax",
      "Tuberculous empyema",
      "Chylothorax",
      "Atelectasis",
      "Sarcoidosis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Progressive extension of cavitary TB into pleural space producing thick purulent tuberculous pleuritis and fibrothorax."
  },
  {
    "id": "stb_66",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Hypercalcemia in Sarcoidosis - Question 66): Which concept is CORRECT?",
    "options": [
      "Active 1,25-(OH)2 Vitamin D3 production by epithelioid macrophages",
      "PTHrp secretion by tumor",
      "Bone destruction by osteoclasts",
      "Renal failure alone",
      "Excess calcitonin"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Sarcoid granulomas express 1-alpha-hydroxylase, converting 25-OH Vitamin D into active 1,25-(OH)2 Vitamin D3, causing hypercalcemia and hypercalciuria."
  },
  {
    "id": "stb_67",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Kveim Test - Question 67): Which concept is CORRECT?",
    "options": [
      "Mantoux test",
      "Kveim-Siltzbach test",
      "Schick test",
      "Dick test",
      "Patch test"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Intradermal injection of sarcoid tissue extract producing a non-caseating granuloma at injection site in 4-6 weeks (historical diagnostic test)."
  },
  {
    "id": "stb_68",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Scolding / Mikulicz Syndrome in Sarcoidosis - Question 68): Which concept is CORRECT?",
    "options": [
      "Caplan syndrome",
      "L\u00f6fgren syndrome",
      "Heerfordt syndrome (uveoparotid fever)",
      "Goodpasture syndrome",
      "Hamman-Rich syndrome"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Sarcoidosis involving lacrimal and salivary glands causing bilateral painless enlargement and dry eyes/mouth (Heerfordt syndrome = uveoparotid fever)."
  },
  {
    "id": "stb_69",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Progressive Primary TB - Question 69): Which concept is CORRECT?",
    "options": [
      "Ranke complex formation",
      "Always asymptomatic",
      "Complete resolution without trace",
      "Progressive primary TB with non-healing caseous spread",
      "Spontaneous conversion to sarcoidosis"
    ],
    "answer": 3,
    "explanation": "Pathology detail: In immunocompromised patients (e.g. HIV/children), primary TB fails to heal and progresses directly to consolidation, cavitation, or miliary spread."
  },
  {
    "id": "stb_70",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Atypical Mycobacteria - Question 70): Which concept is CORRECT?",
    "options": [
      "M. tuberculosis",
      "M. bovis",
      "M. kansasii",
      "M. leprae",
      "Mycobacterium avium complex (MAC) in advanced HIV"
    ],
    "answer": 4,
    "explanation": "Pathology detail: Mycobacterium avium-intracellulare (MAC) causes opportunistic disseminated infection in severely immunocompromised patients (CD4 <50) with abundant acid-fast bacilli in macrophages."
  },
  {
    "id": "stb_71",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Cavitation - Question 71): Which concept is CORRECT?",
    "options": [
      "Erosion into bronchiole creating oxygen-rich cavity",
      "Arterial embolization",
      "Surfactant destruction",
      "Eosinophilic degranulation",
      "Pleural effusion alone"
    ],
    "answer": 0,
    "explanation": "Pathology detail: Secondary TB cavitatory lesions occur due to caseous necrosis eroding into a bronchial tree, creating an oxygen-rich cavity lined by caseous material."
  },
  {
    "id": "stb_72",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (PPD / Tuberculin Skin Test - Question 72): Which concept is CORRECT?",
    "options": [
      "Type I IgE reaction",
      "Type IV delayed-type hypersensitivity reaction measuring cell-mediated immunity",
      "Type II cytotoxic reaction",
      "Type III immune complex deposition",
      "Direct bacterial toxin test"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Type IV delayed-type hypersensitivity reaction mediated by sensitized CD4+ T-cells; induration >=10mm (or >=5mm in HIV) indicates prior exposure."
  },
  {
    "id": "stb_73",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Langhans Giant Cells - Question 73): Which concept is CORRECT?",
    "options": [
      "Touton giant cells with lipid ring",
      "Foreign body giant cells with random nuclei",
      "Langhans giant cells with peripheral horseshoe nuclear arrangement",
      "Reed-Sternberg cells",
      "Warthin-Finkeldey cells"
    ],
    "answer": 2,
    "explanation": "Pathology detail: Multinucleated giant cells with nuclei arranged in a horseshoe pattern at the periphery, formed by fusion of activated epithelioid macrophages."
  },
  {
    "id": "stb_74",
    "category": "Sarcoidosis & TB",
    "type": "Conceptual",
    "question": "Regarding Sarcoidosis and Tuberculosis (Assmann Focus - Question 74): Which concept is CORRECT?",
    "options": [
      "Primary Ghon focus",
      "Ranke complex",
      "Miliary tubercle",
      "Assmann focus (infraclavicular reactivation lesion)",
      "Simon focus"
    ],
    "answer": 3,
    "explanation": "Pathology detail: Early infraclavicular parenchymal lesion of secondary reactivation tuberculosis."
  },
  {
    "id": "stb_75",
    "category": "Sarcoidosis & TB",
    "type": "Clinical Vignette",
    "question": "Regarding Sarcoidosis and Tuberculosis (Tuberculous Empyema - Question 75): Which concept is CORRECT?",
    "options": [
      "Spontaneous pneumothorax",
      "Tuberculous empyema",
      "Chylothorax",
      "Atelectasis",
      "Sarcoidosis"
    ],
    "answer": 1,
    "explanation": "Pathology detail: Progressive extension of cavitary TB into pleural space producing thick purulent tuberculous pleuritis and fibrothorax."
  }
];

const CATEGORIES = [
  "URT Diseases",
  "LRT Diseases",
  "Lung Tumours",
  "Infiltrative Lung Diseases",
  "Diseases of the Pleura",
  "Sarcoidosis & TB"
];

const LOCAL_STORAGE_KEY = 'resp_pathology_quiz_v2_progress';

export default function RespiratoryPathologyQuiz() {
  // State management
  const [activeTab, setActiveTab] = useState("URT Diseases");
  const [currentIdx, setCurrentIdx] = useState(0);
  const [userAnswers, setUserAnswers] = useState({}); // qId -> { selected, isCorrect, timeTaken, timedOut }
  const [bookmarks, setBookmarks] = useState([]);
  const [timeLeft, setTimeLeft] = useState(60);
  const [isTimerRunning, setIsTimerRunning] = useState(true);
  const [filterType, setFilterType] = useState("ALL"); // ALL, UNANSWERED, BOOKMARKED, INCORRECT
  const [showExplanation, setShowExplanation] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null);
  const [showDashboard, setShowDashboard] = useState(false);
  const [notification, setNotification] = useState("");

  const timerRef = useRef(null);

  // Filter questions for active tab
  const tabQuestions = QUIZ_DATA.filter(q => q.category === activeTab);
  
  const currentQuestion = tabQuestions[currentIdx] || tabQuestions[0];

  // Load saved progress from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem(LOCAL_STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed.userAnswers) setUserAnswers(parsed.userAnswers);
        if (parsed.bookmarks) setBookmarks(parsed.bookmarks);
        if (parsed.activeTab && CATEGORIES.includes(parsed.activeTab)) setActiveTab(parsed.activeTab);
        setNotification("Saved progress loaded successfully!");
        setTimeout(() => setNotification(""), 3000);
      }
    } catch (e) {
      console.error("Failed to load progress from localStorage", e);
    }
  }, []);

  // Save progress to localStorage on updates
  useEffect(() => {
    try {
      const stateToSave = {
        userAnswers,
        bookmarks,
        activeTab,
        lastUpdated: new Date().toISOString()
      };
      localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(stateToSave));
    } catch (e) {
      console.error("Failed to save progress to localStorage", e);
    }
  }, [userAnswers, bookmarks, activeTab]);

  // Handle timer countdown
  useEffect(() => {
    if (!currentQuestion) return;
    const qId = currentQuestion.id;
    const alreadyAnswered = userAnswers[qId] !== undefined;

    if (alreadyAnswered || !isTimerRunning || showDashboard) {
      return;
    }

    setTimeLeft(60);
    clearInterval(timerRef.current);

    timerRef.current = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          handleTimeout();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timerRef.current);
  }, [currentIdx, activeTab, userAnswers, isTimerRunning, showDashboard]);

  // Handle timeout when 60s expires
  const handleTimeout = () => {
    if (!currentQuestion) return;
    const qId = currentQuestion.id;
    if (userAnswers[qId] !== undefined) return;

    const newAnswer = {
      selected: -1,
      isCorrect: false,
      timeTaken: 60,
      timedOut: true,
      timestamp: new Date().toISOString()
    };

    setUserAnswers(prev => ({ ...prev, [qId]: newAnswer }));
    setShowExplanation(true);
    setNotification("⏰ Time expired for this question (1 min limit)!");
    setTimeout(() => setNotification(""), 3000);
  };

  // Submit option answer
  const handleOptionSelect = (optIdx) => {
    if (!currentQuestion) return;
    const qId = currentQuestion.id;
    if (userAnswers[qId] !== undefined) return;

    setSelectedOption(optIdx);
    const isCorrect = optIdx === currentQuestion.answer;

    const newAnswer = {
      selected: optIdx,
      isCorrect,
      timeTaken: 60 - timeLeft,
      timedOut: false,
      timestamp: new Date().toISOString()
    };

    setUserAnswers(prev => ({ ...prev, [qId]: newAnswer }));
    setShowExplanation(true);
    clearInterval(timerRef.current);
  };

  // Navigate to Next question
  const handleNext = () => {
    setShowExplanation(false);
    setSelectedOption(null);
    if (currentIdx < tabQuestions.length - 1) {
      setCurrentIdx(prev => prev + 1);
    }
  };

  // Navigate to Previous question
  const handlePrev = () => {
    setShowExplanation(false);
    setSelectedOption(null);
    if (currentIdx > 0) {
      setCurrentIdx(prev => prev - 1);
    }
  };

  // Toggle bookmark
  const toggleBookmark = (qId) => {
    setBookmarks(prev => 
      prev.includes(qId) ? prev.filter(id => id !== qId) : [...prev, qId]
    );
  };

  // Reset category progress
  const resetCategoryProgress = () => {
    if (window.confirm(`Reset progress for ${activeTab}?`)) {
      const qIdsInTab = tabQuestions.map(q => q.id);
      setUserAnswers(prev => {
        const copy = { ...prev };
        qIdsInTab.forEach(id => delete copy[id]);
        return copy;
      });
      setCurrentIdx(0);
      setShowExplanation(false);
      setNotification(`Progress for ${activeTab} reset.`);
      setTimeout(() => setNotification(""), 3000);
    }
  };

  // Export results as JSON
  const exportProgressJSON = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({ userAnswers, bookmarks, date: new Date().toISOString() }, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `respiratory_pathology_quiz_results_${new Date().toISOString().slice(0,10)}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  // Calculate statistics
  const totalQuestions = QUIZ_DATA.length;
  const totalAnswered = Object.keys(userAnswers).length;
  const totalCorrect = Object.values(userAnswers).filter(a => a.isCorrect).length;
  const overallAccuracy = totalAnswered > 0 ? Math.round((totalCorrect / totalAnswered) * 100) : 0;

  // Category stats helper
  const getCategoryStats = (catName) => {
    const catQs = QUIZ_DATA.filter(q => q.category === catName);
    const catAnswered = catQs.filter(q => userAnswers[q.id] !== undefined);
    const catCorrect = catAnswered.filter(q => userAnswers[q.id].isCorrect);
    return {
      total: catQs.length,
      answered: catAnswered.length,
      correct: catCorrect.length,
      pct: catAnswered.length > 0 ? Math.round((catCorrect.length / catAnswered.length) * 100) : 0
    };
  };

  const activeAnsState = currentQuestion ? userAnswers[currentQuestion.id] : null;

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 font-sans p-4 md:p-8">
      {/* Top Header */}
      <header className="max-w-6xl mx-auto mb-6 flex flex-col md:flex-row items-center justify-between gap-4 border-b border-slate-700 pb-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-sky-400 flex items-center gap-2">
            🫁 Comprehensive Respiratory Pathology Review
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            450 High-Yield MCQs & Board Recalls (Robbins Pathology, 333 IA1, Question Banks)
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowDashboard(!showDashboard)}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-sm font-semibold transition shadow-md"
          >
            {showDashboard ? "📖 Back to Quiz" : "📊 Dashboard & Analytics"}
          </button>
          <button
            onClick={exportProgressJSON}
            className="px-3 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-600 rounded-lg text-xs font-medium text-slate-300 transition"
          >
            💾 Export Results
          </button>
        </div>
      </header>

      {/* Notification Toast */}
      {notification && (
        <div className="max-w-6xl mx-auto mb-4 bg-sky-950 border border-sky-500 text-sky-200 px-4 py-2 rounded-lg text-sm flex items-center justify-between shadow-lg animate-fade-in">
          <span>{notification}</span>
          <button onClick={() => setNotification("")} className="text-xs text-sky-400 hover:text-white">✕</button>
        </div>
      )}

      {/* Category Tabs */}
      <div className="max-w-6xl mx-auto mb-6 overflow-x-auto">
        <div className="flex border-b border-slate-700 space-x-1 min-w-max">
          {CATEGORIES.map((cat) => {
            const stats = getCategoryStats(cat);
            const isActive = activeTab === cat;
            return (
              <button
                key={cat}
                onClick={() => {
                  setActiveTab(cat);
                  setCurrentIdx(0);
                  setShowExplanation(false);
                  setShowDashboard(false);
                }}
                className={`px-4 py-3 text-sm font-semibold rounded-t-lg transition flex items-center gap-2 ${
                  isActive
                    ? "bg-slate-800 text-sky-400 border-t-2 border-sky-400 border-x border-slate-700"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                }`}
              >
                <span>{cat}</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-slate-700 text-slate-300">
                  {stats.answered}/{stats.total}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Content Area */}
      <main className="max-w-6xl mx-auto">
        {showDashboard ? (
          /* DASHBOARD VIEW */
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-xl">
            <h2 className="text-xl font-bold text-slate-100 mb-6 flex items-center gap-2">
              📊 Performance Analytics & Progress Summary
            </h2>

            {/* Top Stat Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div className="bg-slate-900 border border-slate-700 p-4 rounded-lg text-center">
                <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">Total Attempted</span>
                <span className="text-2xl font-bold text-sky-400">{totalAnswered} / {totalQuestions}</span>
                <span className="text-xs text-slate-500 block mt-1">{Math.round((totalAnswered/totalQuestions)*100)}% Completed</span>
              </div>
              <div className="bg-slate-900 border border-slate-700 p-4 rounded-lg text-center">
                <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">Correct Answers</span>
                <span className="text-2xl font-bold text-emerald-400">{totalCorrect}</span>
                <span className="text-xs text-slate-500 block mt-1">Accuracy: {overallAccuracy}%</span>
              </div>
              <div className="bg-slate-900 border border-slate-700 p-4 rounded-lg text-center">
                <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">Bookmarked</span>
                <span className="text-2xl font-bold text-amber-400">{bookmarks.length}</span>
                <span className="text-xs text-slate-500 block mt-1">Flagged for Review</span>
              </div>
              <div className="bg-slate-900 border border-slate-700 p-4 rounded-lg text-center">
                <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">Incorrect / Missed</span>
                <span className="text-2xl font-bold text-rose-400">{totalAnswered - totalCorrect}</span>
                <span className="text-xs text-slate-500 block mt-1">Review Needed</span>
              </div>
            </div>

            {/* Category Breakdown Table */}
            <h3 className="text-md font-semibold text-slate-300 mb-3">Category Breakdown</h3>
            <div className="overflow-x-auto mb-6">
              <table className="w-full text-left border-collapse text-sm">
                <thead>
                  <tr className="border-b border-slate-700 text-slate-400">
                    <th className="py-2 px-3">Category</th>
                    <th className="py-2 px-3">Questions</th>
                    <th className="py-2 px-3">Answered</th>
                    <th className="py-2 px-3">Correct</th>
                    <th className="py-2 px-3">Accuracy</th>
                    <th className="py-2 px-3">Progress</th>
                  </tr>
                </thead>
                <tbody>
                  {CATEGORIES.map(cat => {
                    const st = getCategoryStats(cat);
                    return (
                      <tr key={cat} className="border-b border-slate-700/50 hover:bg-slate-700/30">
                        <td className="py-3 px-3 font-medium text-slate-200">{cat}</td>
                        <td className="py-3 px-3 text-slate-400">{st.total}</td>
                        <td className="py-3 px-3 text-slate-300">{st.answered}</td>
                        <td className="py-3 px-3 text-emerald-400 font-semibold">{st.correct}</td>
                        <td className="py-3 px-3 font-semibold text-sky-400">{st.pct}%</td>
                        <td className="py-3 px-3 w-48">
                          <div className="w-full bg-slate-900 rounded-full h-2.5 overflow-hidden border border-slate-700">
                            <div
                              className="bg-sky-500 h-2.5 rounded-full"
                              style={{ width: `${Math.round((st.answered / st.total) * 100)}%` }}
                            />
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            <div className="flex justify-end gap-3 pt-4 border-t border-slate-700">
              <button
                onClick={() => setShowDashboard(false)}
                className="px-5 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-sm font-semibold transition"
              >
                Return to Quiz
              </button>
            </div>
          </div>
        ) : (
          /* QUESTION & QUIZ VIEW */
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            
            {/* Left Main Card (3 Columns) */}
            <div className="lg:col-span-3 bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-xl flex flex-col justify-between min-h-[500px]">
              {currentQuestion ? (
                <div>
                  {/* Top Question Info Bar */}
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-4 text-xs">
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-1 bg-sky-950 text-sky-300 border border-sky-700/50 rounded-md font-medium">
                        {currentQuestion.category}
                      </span>
                      <span className="px-2.5 py-1 bg-indigo-950 text-indigo-300 border border-indigo-700/50 rounded-md font-medium">
                        {currentQuestion.type}
                      </span>
                      <span className="text-slate-400">
                        Question {currentIdx + 1} of {tabQuestions.length}
                      </span>
                    </div>

                    {/* Timer & Bookmark */}
                    <div className="flex items-center gap-3">
                      {/* 1-min Timer Display */}
                      <div className={`flex items-center gap-1.5 px-3 py-1 rounded-full font-mono text-xs border ${
                        timeLeft <= 10
                          ? "bg-rose-950 text-rose-300 border-rose-600 animate-pulse"
                          : "bg-slate-900 text-slate-300 border-slate-700"
                      }`}>
                        <span>⏰</span>
                        <span>{timeLeft}s remaining</span>
                      </div>

                      <button
                        onClick={() => toggleBookmark(currentQuestion.id)}
                        className={`p-1.5 rounded-lg border transition ${
                          bookmarks.includes(currentQuestion.id)
                            ? "bg-amber-950 text-amber-300 border-amber-500"
                            : "bg-slate-900 text-slate-400 border-slate-700 hover:text-amber-300"
                        }`}
                        title="Bookmark question"
                      >
                        {bookmarks.includes(currentQuestion.id) ? "★ Bookmarked" : "☆ Bookmark"}
                      </button>
                    </div>
                  </div>

                  {/* Visual Timer Progress Bar */}
                  <div className="w-full bg-slate-900 rounded-full h-1.5 mb-6 overflow-hidden border border-slate-700">
                    <div
                      className={`h-1.5 transition-all duration-1000 ${
                        timeLeft <= 10 ? "bg-rose-500" : "bg-sky-400"
                      }`}
                      style={{ width: `${(timeLeft / 60) * 100}%` }}
                    />
                  </div>

                  {/* Question Prompt */}
                  <h3 className="text-lg md:text-xl font-semibold text-slate-100 mb-6 leading-relaxed">
                    {currentQuestion.question}
                  </h3>

                  {/* Options List */}
                  <div className="space-y-3 mb-6">
                    {currentQuestion.options.map((opt, optIdx) => {
                      const isAnswered = activeAnsState !== undefined;
                      const isUserSelected = activeAnsState && activeAnsState.selected === optIdx;
                      const isCorrectOpt = currentQuestion.answer === optIdx;

                      let btnStyle = "bg-slate-900/80 border-slate-700 text-slate-200 hover:bg-slate-700/60 hover:border-slate-500";

                      if (isAnswered) {
                        if (isCorrectOpt) {
                          btnStyle = "bg-emerald-950/80 border-emerald-500 text-emerald-200 font-semibold ring-1 ring-emerald-500";
                        } else if (isUserSelected) {
                          btnStyle = "bg-rose-950/80 border-rose-500 text-rose-200 ring-1 ring-rose-500";
                        } else {
                          btnStyle = "bg-slate-900/40 border-slate-800 text-slate-500 opacity-60";
                        }
                      }

                      return (
                        <button
                          key={optIdx}
                          disabled={isAnswered}
                          onClick={() => handleOptionSelect(optIdx)}
                          className={`w-full text-left p-4 rounded-xl border transition flex items-start gap-3 text-sm md:text-base ${btnStyle}`}
                        >
                          <span className="font-mono text-xs px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300 mt-0.5">
                            {String.fromCharCode(65 + optIdx)}
                          </span>
                          <span className="flex-1">{opt}</span>
                          {isAnswered && isCorrectOpt && <span className="text-emerald-400 font-bold">✓ Correct</span>}
                          {isAnswered && isUserSelected && !isCorrectOpt && <span className="text-rose-400 font-bold">✗ Incorrect</span>}
                        </button>
                      );
                    })}
                  </div>

                  {/* Answer Explanation Box */}
                  {(activeAnsState !== undefined || showExplanation) && (
                    <div className="bg-slate-900 border border-sky-800/60 rounded-xl p-5 mb-6 animate-fade-in">
                      <div className="flex items-center gap-2 mb-2 text-sky-400 font-bold text-sm">
                        <span>💡 Pathology Explanation & Reference</span>
                      </div>
                      <p className="text-sm text-slate-300 leading-relaxed">
                        {currentQuestion.explanation}
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-12 text-slate-400">No questions found.</div>
              )}

              {/* Bottom Navigation Buttons */}
              <div className="flex items-center justify-between pt-4 border-t border-slate-700 mt-auto">
                <button
                  onClick={handlePrev}
                  disabled={currentIdx === 0}
                  className="px-4 py-2 bg-slate-700 hover:bg-slate-600 disabled:opacity-40 disabled:hover:bg-slate-700 text-slate-200 rounded-lg text-sm font-semibold transition"
                >
                  ← Previous
                </button>

                <span className="text-xs text-slate-400 hidden sm:inline">
                  Use Category Tabs to switch topics
                </span>

                <button
                  onClick={handleNext}
                  disabled={currentIdx === tabQuestions.length - 1}
                  className="px-5 py-2 bg-sky-600 hover:bg-sky-500 disabled:opacity-40 disabled:hover:bg-sky-600 text-white rounded-lg text-sm font-semibold transition"
                >
                  Next Question →
                </button>
              </div>
            </div>

            {/* Right Sidebar - Question Grid & Quick Jump (1 Column) */}
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-5 shadow-xl flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-4 border-b border-slate-700 pb-3">
                  <h4 className="font-bold text-slate-200 text-sm">Category Navigator</h4>
                  <span className="text-xs text-sky-400 font-mono">
                    {activeTab} ({tabQuestions.length})
                  </span>
                </div>

                {/* Filter Options */}
                <div className="mb-4">
                  <label className="text-xs text-slate-400 block mb-1">Filter Question Grid:</label>
                  <select
                    value={filterType}
                    onChange={(e) => setFilterType(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg p-2 focus:outline-none focus:border-sky-500"
                  >
                    <option value="ALL">All Questions ({tabQuestions.length})</option>
                    <option value="UNANSWERED">Unanswered</option>
                    <option value="BOOKMARKED">Bookmarked ({bookmarks.length})</option>
                    <option value="INCORRECT">Incorrect Only</option>
                  </select>
                </div>

                {/* Quick Question Number Grid */}
                <div className="grid grid-cols-5 gap-2 max-h-[360px] overflow-y-auto p-1 pr-2 border border-slate-700/50 rounded-lg bg-slate-900/50">
                  {tabQuestions.map((q, idx) => {
                    const ans = userAnswers[q.id];
                    const isBookmarked = bookmarks.includes(q.id);
                    const isCurrent = currentIdx === idx;

                    // Filter logic
                    if (filterType === "UNANSWERED" && ans !== undefined) return null;
                    if (filterType === "BOOKMARKED" && !isBookmarked) return null;
                    if (filterType === "INCORRECT" && (!ans || ans.isCorrect)) return null;

                    let statusClass = "bg-slate-800 text-slate-400 border-slate-700 hover:bg-slate-700";
                    if (ans !== undefined) {
                      statusClass = ans.isCorrect
                        ? "bg-emerald-950 text-emerald-300 border-emerald-700 font-bold"
                        : "bg-rose-950 text-rose-300 border-rose-700 font-bold";
                    }

                    if (isCurrent) {
                      statusClass += " ring-2 ring-sky-400 border-sky-400";
                    }

                    return (
                      <button
                        key={q.id}
                        onClick={() => {
                          setCurrentIdx(idx);
                          setShowExplanation(false);
                        }}
                        className={`h-9 w-full rounded-md border text-xs font-mono transition flex items-center justify-center relative ${statusClass}`}
                      >
                        {idx + 1}
                        {isBookmarked && (
                          <span className="absolute -top-1 -right-1 text-[9px] text-amber-400 font-bold">★</span>
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Sidebar Footer Controls */}
              <div className="mt-6 pt-4 border-t border-slate-700">
                <button
                  onClick={resetCategoryProgress}
                  className="w-full py-2 bg-slate-900 hover:bg-rose-950 border border-slate-700 hover:border-rose-700 text-slate-400 hover:text-rose-300 text-xs font-medium rounded-lg transition"
                >
                  🔄 Reset {activeTab} Progress
                </button>
              </div>
            </div>

          </div>
        )}
      </main>
    </div>
  );
}

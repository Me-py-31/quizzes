import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# ------------------------------------------------------------------------------
# 1. STREAMLIT CONFIG & GOOGLE SHEETS INITIALIZATION
# ------------------------------------------------------------------------------
st.set_page_config(page_title="MSPC 237 Interactive Quiz & Tracker", layout="wide")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

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
        st.error(f"Roster check error: {e}")
        
    return None


# ------------------------------------------------------------------------------
# 3. SINGLE INPUT VERIFICATION GATE
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
                st.rerun()
            else:
                st.error("❌ **Access Denied:** ID or Name not found in official student roster. Please check for typos.")
        else:
            st.warning("⚠️ Please enter your Student ID or Name.")

    st.stop()


# ------------------------------------------------------------------------------
# 4. RESPONSE LOGGING FUNCTION
# ------------------------------------------------------------------------------
def log_response(module_name, category, question_text, selected_option, correct_answer, is_correct):
    if conn is None or st.session_state.verified_user is None:
        return
        
    student = st.session_state.verified_user
    
    try:
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
# 5. QUESTION BANK DATA (MSPC 237)
# ------------------------------------------------------------------------------
RESP_QS = [
    {
        "id": 1,
        "question": "A patient's predicted FVC is 3.0L. Spirometry reveals pre-bronchodilator FEV1 = 1.5L, FVC = 3.0L; post-bronchodilator FEV1 = 2.0L, FVC = 3.2L. What is his pre-bronchodilator FEV1/FVC ratio?",
        "options": [
            "A. 50.0%",
            "B. 62.5%",
            "C. 75.0%",
            "D. 80.0%",
            "E. 90.0%"
        ],
        "answer": "A. 50.0%",
        "explanation": "FEV1/FVC ratio = 1.5L / 3.0L = 0.50 (50.0%). An FEV1/FVC ratio below 70% defines an obstructive ventilatory defect."
    },
    {
        "id": 2,
        "question": "Based on the spirometry findings (pre-FEV1/FVC = 50.0%, FVC = 100% predicted), what is the primary respiratory pattern?",
        "options": [
            "A. Normal respiratory function",
            "B. Restrictive pulmonary defect",
            "C. Obstructive pulmonary defect",
            "D. Mixed obstructive and restrictive defect",
            "E. Lung cancer"
        ],
        "answer": "C. Obstructive pulmonary defect",
        "explanation": "Normal FVC with a reduced FEV1/FVC ratio is the hallmark signature of an obstructive pulmonary defect (airflow limitation)."
    },
    {
        "id": 3,
        "question": "In the same patient, what was the effect of inhaled salbutamol (bronchodilator) on respiratory function (FEV1 increased from 1.5L to 2.0L, a 33% increase)?",
        "options": [
            "A. Salbutamol had no significant effect",
            "B. Salbutamol reversed the airway obstruction",
            "C. Salbutamol improved lung restriction",
            "D. Salbutamol improved lung compliance",
            "E. Salbutamol decreased lung compliance"
        ],
        "answer": "B. Salbutamol reversed the airway obstruction",
        "explanation": "An increase in FEV1 > 12% and > 200 mL post-bronchodilator meets the diagnostic criteria for significant airway reversibility (e.g. asthma)."
    },
    {
        "id": 4,
        "question": "A C-section is planned at 33 weeks for a mother with severe lung disease. Which alveolar epithelial cells synthesize and secrete pulmonary surfactant?",
        "options": [
            "A. Alveolar neutrophils",
            "B. Type I pneumocytes",
            "C. Type II pneumocytes",
            "D. Alveolar macrophages",
            "E. Dust cells"
        ],
        "answer": "C. Type II pneumocytes",
        "explanation": "Type II pneumocytes synthesize, store (in lamellar bodies), and secrete pulmonary surfactant, and act as progenitor cells for Type I pneumocytes."
    },
    {
        "id": 5,
        "question": "Which of the following laboratory tests on amniotic fluid may be utilized to assess fetal lung maturity prior to premature delivery?",
        "options": [
            "A. Lamellar body count",
            "B. Phosphatidylglycerol test",
            "C. Foam stability (shake) test",
            "D. Surfactant/albumin ratio",
            "E. All the above are correct"
        ],
        "answer": "E. All the above are correct",
        "explanation": "Lamellar body counts, phosphatidylglycerol testing, foam stability assays, and surfactant-to-albumin ratios are all validated clinical tests for fetal lung maturity."
    },
    {
        "id": 6,
        "question": "Patient A has a Respiratory Rate (RR) of 14/min, Tidal Volume (TV) of 400 mL, and Anatomical Dead Space of 150 mL. Estimate his dead space ventilation.",
        "options": [
            "A. 2.0 L/min",
            "B. 2.1 L/min",
            "C. 3.5 L/min",
            "D. 3.6 L/min",
            "E. 5.6 L/min"
        ],
        "answer": "B. 2.1 L/min",
        "explanation": "Dead space ventilation = RR x Dead Space Volume = 14/min x 150 mL = 2,100 mL/min = 2.1 L/min."
    },
    {
        "id": 7,
        "question": "Patient B has a Respiratory Rate (RR) of 10/min, Tidal Volume (TV) of 560 mL, and Anatomical Dead Space of 200 mL. Estimate his alveolar minute ventilation.",
        "options": [
            "A. 3.5 L/min",
            "B. 3.6 L/min",
            "C. 4.5 L/min",
            "D. 4.6 L/min",
            "E. 5.6 L/min"
        ],
        "answer": "B. 3.6 L/min",
        "explanation": "Alveolar minute ventilation = RR x (TV - Dead Space) = 10/min x (560 - 200 mL) = 10 x 360 mL = 3.6 L/min."
    },
    {
        "id": 8,
        "question": "Comparing Patient A (Alveolar ventilation = 3.5 L/min) and Patient B (Alveolar ventilation = 3.6 L/min), which patient will present with a higher PaCO2 and lower arterial pH?",
        "options": [
            "A. Patient A",
            "B. Patient B",
            "C. Depends on barometric pressure",
            "D. Depends on cardiac output",
            "E. Insufficient information"
        ],
        "answer": "A. Patient A",
        "explanation": "PaCO2 is inversely proportional to alveolar ventilation. Patient A has lower alveolar ventilation (3.5 L/min vs 3.6 L/min), so he retains more CO2, leading to respiratory acidosis."
    },
    {
        "id": 9,
        "question": "On the oxygen-carbon dioxide (Rahn-Fenn) diagram, point D corresponds to a V/Q ratio approaching infinity (V/Q = \u221e). Point D represents:",
        "options": [
            "A. Anatomic dead space",
            "B. Alveolar dead space",
            "C. Pulmonary shunt",
            "D. Right-to-left intracardiac shunt",
            "E. Mixed venous point"
        ],
        "answer": "B. Alveolar dead space",
        "explanation": "V/Q = \u221e represents ventilated alveoli that receive no blood perfusion, defining alveolar dead space."
    },
    {
        "id": 10,
        "question": "If blood is sampled from pulmonary capillary blood close to region C (V/Q = 1), what is the typical mixed venous oxygen saturation of incoming blood before exchange?",
        "options": [
            "A. 25%",
            "B. 40%",
            "C. 50%",
            "D. 75%",
            "E. 100%"
        ],
        "answer": "D. 75%",
        "explanation": "Mixed venous oxygen saturation entering pulmonary capillaries is normally ~75% (PvO2 ~40 mmHg), dictated by systemic tissue oxygen extraction."
    },
    {
        "id": 11,
        "question": "On the O2-CO2 diagram, the region representing optimal, ideal gas exchange matching is labeled:",
        "options": [
            "A. Point A (V/Q = 0)",
            "B. Point B",
            "C. Point C (V/Q = 1)",
            "D. Point D (V/Q = \u221e)",
            "E. None of the above"
        ],
        "answer": "C. Point C (V/Q = 1)",
        "explanation": "Point C represents a V/Q ratio near 1, where ventilation and perfusion are ideally matched for maximum gas exchange efficiency."
    },
    {
        "id": 12,
        "question": "If the right main bronchus is completely obstructed, what will be the partial pressures of O2 and CO2 in blood leaving that affected lung region?",
        "options": [
            "A. pO2 = 150, pCO2 = 0 mmHg",
            "B. pO2 = 40, pCO2 = 46 mmHg",
            "C. pO2 = 100, pCO2 = 40 mmHg",
            "D. Similar to inspired air",
            "E. Unknown"
        ],
        "answer": "B. pO2 = 40, pCO2 = 46 mmHg",
        "explanation": "Complete bronchial obstruction creates a pure shunt (V/Q = 0). Unventilated perfused blood exits with unchanged mixed venous values (pO2 = 40, pCO2 = 46 mmHg)."
    },
    {
        "id": 13,
        "question": "Administration of neostigmine increases airway acetylcholine. What is the primary physiological determinant of resting airway smooth muscle tone?",
        "options": [
            "A. Sympathetic innervation",
            "B. Parasympathetic innervation",
            "C. Non-adrenergic, non-cholinergic system",
            "D. Histamine H1 action",
            "E. Histamine H2 action"
        ],
        "answer": "B. Parasympathetic innervation",
        "explanation": "Resting bronchial tone is predominantly maintained by parasympathetic (vagal) cholinergic input acting on muscarinic receptors."
    },
    {
        "id": 14,
        "question": "According to Poiseuille's Law (R \u221d 1/r^4), if bronchoconstriction halves the airway radius, airway resistance will change by what factor?",
        "options": [
            "A. Airway resistance is doubled",
            "B. Airway resistance increases by a factor of 16",
            "C. Airway resistance decreases by a factor of 16",
            "D. Airway resistance increases by a factor of 4",
            "E. Airway resistance decreases by a factor of 4"
        ],
        "answer": "B. Airway resistance increases by a factor of 16",
        "explanation": "Resistance is inversely proportional to the 4th power of radius. Halving radius increases resistance by 2^4 = 16-fold."
    },
    {
        "id": 15,
        "question": "Which specific cholinergic muscarinic receptor subtype on airway smooth muscle mediates acetylcholine-induced bronchoconstriction?",
        "options": [
            "A. M1",
            "B. M2",
            "C. M3",
            "D. M4",
            "E. M5"
        ],
        "answer": "C. M3",
        "explanation": "M3 muscarinic receptors on airway smooth muscle couple to Gq proteins to increase intracellular calcium, driving bronchoconstriction."
    },
    {
        "id": 16,
        "question": "A pregnant patient with recurrent hypoxemia has PaO2 = 60 mmHg while receiving 50% O2 (FiO2 = 0.5). What is her calculated PaO2/FiO2 ratio?",
        "options": [
            "A. 80",
            "B. 120",
            "C. 200",
            "D. 300",
            "E. 400"
        ],
        "answer": "B. 120",
        "explanation": "PaO2/FiO2 ratio = 60 / 0.5 = 120 (indicating moderate-to-severe acute hypoxemic respiratory failure/ARDS)."
    },
    {
        "id": 17,
        "question": "In the same patient, hypoxemia refractory to 100% supplemental O2 (PaO2 remains low at 60 mmHg) identifies which primary pathophysiological mechanism?",
        "options": [
            "A. Hypoventilation",
            "B. Anatomic or physiological shunt",
            "C. Diffusion limitation",
            "D. High V/Q mismatch",
            "E. Decreased atmospheric pressure"
        ],
        "answer": "B. Anatomic or physiological shunt",
        "explanation": "Refractory hypoxemia that fails to respond to supplemental oxygen is the clinical hallmark of a true right-to-left shunt."
    },
    {
        "id": 18,
        "question": "An aspirated foreign body is most likely to lodge in the _____ lung because the _____ main bronchus is wider, shorter, and makes an angle of _____ to the vertical.",
        "options": [
            "A. left, left, 20-25\u00b0",
            "B. right, right, 20-25\u00b0",
            "C. left, left, 40-45\u00b0",
            "D. right, right, 40-45\u00b0",
            "E. left, right, 20-25\u00b0"
        ],
        "answer": "B. right, right, 20-25\u00b0",
        "explanation": "The right main bronchus is wider, shorter, and more steeply vertical (20-25\u00b0 off the vertical carina), making foreign body aspiration more common on the right."
    },
    {
        "id": 19,
        "question": "Which of the following arterial blood gas parameters directly indicates severely impaired alveolar gas exchange?",
        "options": [
            "A. Arterial pH of 7.38",
            "B. Bicarbonate concentration of 24 mmol/L",
            "C. PaO2 of 90 mmHg",
            "D. PaCO2 of 60 mmHg",
            "E. PaO2/FiO2 ratio of 400"
        ],
        "answer": "D. PaCO2 of 60 mmHg",
        "explanation": "A PaCO2 of 60 mmHg is markedly elevated above normal (35-45 mmHg), directly demonstrating alveolar hypoventilation and impaired gas exchange."
    },
    {
        "id": 20,
        "question": "All of the following conditions or pharmacological agents cause an increase in pulmonary vascular resistance (PVR) EXCEPT:",
        "options": [
            "A. Alveolar hypoxia",
            "B. Hypercapnia",
            "C. Hyperventilation",
            "D. Acidosis",
            "E. Infusion of milrinone"
        ],
        "answer": "E. Infusion of milrinone",
        "explanation": "Milrinone is a phosphodiesterase-3 inhibitor that induces pulmonary vasodilation (lowering PVR), whereas hypoxia, hypercapnia, and acidosis cause pulmonary vasoconstriction."
    },
    {
        "id": 21,
        "question": "According to West's lung zonal physiology, which pressure relationship defines Zone 2 of the lung?",
        "options": [
            "A. Alveolar > arterial > venous",
            "B. Arterial > alveolar > venous",
            "C. Arterial > venous > alveolar",
            "D. Total dead space",
            "E. No blood flow"
        ],
        "answer": "B. Arterial > alveolar > venous",
        "explanation": "Zone 2 (mid-zone) is defined by Arterial Pressure > Alveolar Pressure > Venous Pressure, producing waterfall-like intermittent blood flow."
    },
    {
        "id": 22,
        "question": "How does the ventilation-perfusion (V/Q) ratio vary in an upright human lung from Zone 1 (apex) down to Zone 3 (base)?",
        "options": [
            "A. Increases linearly from Zone 3 to Zone 1",
            "B. Increases non-linearly from Zone 3 to Zone 1",
            "C. Decreases linearly from Zone 3 to Zone 1",
            "D. Decreases non-linearly from Zone 3 to Zone 1",
            "E. Remains relatively constant throughout"
        ],
        "answer": "B. Increases non-linearly from Zone 3 to Zone 1",
        "explanation": "V/Q increases non-linearly from ~0.6 at the base (Zone 3) up to ~3.3 at the apex (Zone 1) because perfusion decreases more steeply with height than ventilation."
    },
    {
        "id": 23,
        "question": "Postnatal alveolar development (increase in total alveolar number and surface area) continues actively until approximately what age?",
        "options": [
            "A. Up to 24 weeks of fetal development",
            "B. Up to 30 weeks of fetal development",
            "C. Up to 36 weeks of fetal development",
            "D. Up to 8 years of age",
            "E. Throughout late adolescence"
        ],
        "answer": "D. Up to 8 years of age",
        "explanation": "Alveolarization continues postnatally until ~8 years of age, after which lung enlargement occurs primarily through expansion of existing alveoli."
    },
    {
        "id": 24,
        "question": "How does the respiratory system primarily compensate for acute metabolic acidosis?",
        "options": [
            "A. Increase in alveolar dead space",
            "B. Decrease in alveolar dead space",
            "C. Hypoventilation",
            "D. Hyperventilation",
            "E. Increasing surface area"
        ],
        "answer": "D. Hyperventilation",
        "explanation": "Metabolic acidosis stimulates chemoreceptors to drive alveolar hyperventilation (Kussmaul breathing), blowing off CO2 to restore blood pH."
    },
    {
        "id": 25,
        "question": "What is the volume of air remaining in the lungs after a maximal forced exhalation?",
        "options": [
            "A. Functional residual capacity",
            "B. Total lung capacity",
            "C. Residual volume",
            "D. Vital capacity",
            "E. Expiratory reserve volume"
        ],
        "answer": "C. Residual volume",
        "explanation": "Residual Volume (RV) is the air remaining in the lungs following a maximal forced expiration and cannot be exhaled voluntarily."
    },
    {
        "id": 26,
        "question": "How is static lung compliance calculated from a graph plotting lung volume on the y-axis against transpulmonary pressure on the x-axis?",
        "options": [
            "A. Area under the curve",
            "B. Reciprocal of area under the curve",
            "C. Gradient (slope) of the curve",
            "D. Reciprocal of the gradient",
            "E. Negative logarithm of peak pressure"
        ],
        "answer": "C. Gradient (slope) of the curve",
        "explanation": "Compliance is defined as \u0394V / \u0394P, which corresponds directly to the gradient (slope) of the pressure-volume curve."
    },
    {
        "id": 27,
        "question": "Which anatomical structure forms the posterior boundary of the anterior mediastinum?",
        "options": [
            "A. Thoracic vertebrae",
            "B. Pericardium",
            "C. Pleura",
            "D. Sternum",
            "E. Prevertebral fascia"
        ],
        "answer": "B. Pericardium",
        "explanation": "The anterior mediastinum lies between the sternum anteriorly and the fibrous pericardium posteriorly."
    },
    {
        "id": 28,
        "question": "During surgical ligation or clamping of a patent ductus arteriosus, which nerve is at high risk of iatrogenic injury?",
        "options": [
            "A. Accessory hemiazygos vein",
            "B. Left recurrent laryngeal nerve",
            "C. Left internal thoracic artery",
            "D. Left phrenic nerve",
            "E. Thoracic duct"
        ],
        "answer": "B. Left recurrent laryngeal nerve",
        "explanation": "The left recurrent laryngeal nerve loops under the aortic arch immediately adjacent to the ductus arteriosus / ligamentum arteriosum."
    },
    {
        "id": 29,
        "question": "Along the mid-axillary line, the inferior margin of the visceral pleura extends down to which rib level?",
        "options": [
            "A. 6th rib",
            "B. 8th rib",
            "C. 10th rib",
            "D. 12th rib",
            "E. 4th rib"
        ],
        "answer": "B. 8th rib",
        "explanation": "The visceral pleura extends to the 6th rib (midclavicular), 8th rib (midaxillary), and 10th rib (paravertebral)."
    },
    {
        "id": 30,
        "question": "The middle lobe of the right lung is bounded by fissures running along which anterior rib levels?",
        "options": [
            "A. 3rd and 6th ribs",
            "B. 4th and 6th ribs",
            "C. 5th and 6th ribs",
            "D. 6th and 7th ribs",
            "E. 2nd and 4th ribs"
        ],
        "answer": "B. 4th and 6th ribs",
        "explanation": "The horizontal fissure lies along the 4th rib and the oblique fissure crosses the 6th rib, demarcating the right middle lobe."
    },
    {
        "id": 31,
        "question": "The thoracic diaphragm develops embryologically from all of the following structures EXCEPT:",
        "options": [
            "A. Septum transversum",
            "B. Pleuroperitoneal membrane",
            "C. Dorsal mesogastrium",
            "D. Dorsal body wall",
            "E. Dorsal mesentery of esophagus"
        ],
        "answer": "C. Dorsal mesogastrium",
        "explanation": "The diaphragm develops from septum transversum, pleuroperitoneal membranes, dorsal esophageal mesentery, and body wall ingrowth. Dorsal mesogastrium forms peritoneal ligaments."
    },
    {
        "id": 32,
        "question": "What embryonic structure partitions the respiratory diverticulum from the primitive foregut?",
        "options": [
            "A. Laryngopharyngeal groove",
            "B. Tracheoesophageal septum",
            "C. Laryngopharyngeal diverticulum",
            "D. Bronchopulmonary segment",
            "E. Septum transversum"
        ],
        "answer": "B. Tracheoesophageal septum",
        "explanation": "The tracheoesophageal septum fuses to separate the ventral laryngotracheal tube from the dorsal esophagus."
    },
    {
        "id": 33,
        "question": "Which transcription factor expressed in splanchnic mesoderm directly induces the initial budding of the respiratory diverticulum?",
        "options": [
            "A. VEGF",
            "B. FGF",
            "C. TBX4",
            "D. Retinoic acid",
            "E. Wnt"
        ],
        "answer": "C. TBX4",
        "explanation": "TBX4 expression in splanchnic mesoderm induces respiratory bud outgrowth and directs branching morphogenesis."
    },
    {
        "id": 34,
        "question": "Congenital choanal atresia results from the failure of breakdown of which embryonic membrane?",
        "options": [
            "A. Buccopharyngeal membrane",
            "B. Oronasal membrane",
            "C. Pleuroperitoneal membrane",
            "D. Pericardioperitoneal fold",
            "E. Laryngotracheal groove"
        ],
        "answer": "B. Oronasal membrane",
        "explanation": "Persistence of the oronasal membrane prevents opening of the posterior nasal apertures (choanae)."
    },
    {
        "id": 35,
        "question": "Esophageal atresia with tracheoesophageal fistula in a neonate is characteristically associated with which antenatal maternal condition?",
        "options": [
            "A. Oligohydramnios",
            "B. Pregnancy-induced hypertension",
            "C. Gestational diabetes",
            "D. Postmature delivery",
            "E. Polyhydramnios"
        ],
        "answer": "E. Polyhydramnios",
        "explanation": "Inability of the fetus to swallow and absorb amniotic fluid leads to polyhydramnios."
    },
    {
        "id": 36,
        "question": "Which statement regarding lung development and embryology is INCORRECT?",
        "options": [
            "A. Laryngotracheal diverticulum develops from the foregut",
            "B. Cartilage, smooth muscle, and connective tissue derive from endoderm",
            "C. Only 1/6 of adult alveoli are present at birth",
            "D. Lung bud formation is induced by TBX4",
            "E. Laryngotracheal septum separates lung buds from esophagus"
        ],
        "answer": "B. Cartilage, smooth muscle, and connective tissue derive from endoderm",
        "explanation": "Airway connective tissues, cartilage, and smooth muscle derive from splanchnic mesoderm, NOT endoderm (endoderm forms epithelial lining only)."
    },
    {
        "id": 37,
        "question": "What is the principal muscle of quiet inspiration, and what percentage of tidal volume does it provide?",
        "options": [
            "A. Diaphragm, 90%",
            "B. Diaphragm, 75%",
            "C. External intercostals, 90%",
            "D. Internal intercostals, 75%",
            "E. Abdominal recti, 90%"
        ],
        "answer": "B. Diaphragm, 75%",
        "explanation": "The diaphragm is the main inspiratory muscle, contributing ~75% of quiet inspiratory effort."
    },
    {
        "id": 38,
        "question": "Transection of the spinal cord above which level abolishes phrenic nerve output, causing complete respiratory paralysis?",
        "options": [
            "A. C3",
            "B. C7",
            "C. T3",
            "D. T7",
            "E. S1"
        ],
        "answer": "A. C3",
        "explanation": "The phrenic nerve arises from C3-C5 ('C3, 4, 5 keep the diaphragm alive'). Transection above C3 stops all diaphragmatic respiration."
    },
    {
        "id": 39,
        "question": "What is the true distending pressure gradient driving lung expansion and volume changes?",
        "options": [
            "A. Atmospheric pressure",
            "B. Alveolar pressure",
            "C. Intrapleural pressure",
            "D. Transpulmonary pressure",
            "E. Airway pressure gradient"
        ],
        "answer": "D. Transpulmonary pressure",
        "explanation": "Transpulmonary pressure (Alveolar pressure minus Intrapleural pressure) is the net distending pressure across the lung wall."
    },
    {
        "id": 40,
        "question": "At what point in the respiratory cycle does airflow velocity into the respiratory tract reach its peak?",
        "options": [
            "A. Start of inspiration",
            "B. Start of expiration",
            "C. End of inspiration",
            "D. End of expiration",
            "E. Mid-inspiration"
        ],
        "answer": "E. Mid-inspiration",
        "explanation": "Airflow velocity is proportional to the rate of volume change, reaching its peak roughly midway through inspiration."
    },
    {
        "id": 41,
        "question": "In an uncompensated open pneumothorax, which of the following physiological events occurs?",
        "options": [
            "A. Intrapleural pressure rises toward atmospheric",
            "B. Transpulmonary pressure decreases",
            "C. Ipsilateral lung collapses",
            "D. Chest wall on affected side expands outward",
            "E. All of the above are true"
        ],
        "answer": "E. All of the above are true",
        "explanation": "Loss of negative intrapleural pressure abolishes transpulmonary pressure, collapsing the lung and allowing the chest wall to spring outward."
    },
    {
        "id": 42,
        "question": "Standard bedside spirometry CANNOT directly measure which of the following lung volumes?",
        "options": [
            "A. Tidal volume",
            "B. Inspiratory reserve volume",
            "C. Expiratory reserve volume",
            "D. Residual volume",
            "E. Vital capacity"
        ],
        "answer": "D. Residual volume",
        "explanation": "Residual volume cannot be exhaled voluntarily and thus cannot be measured by direct spirometry (requires plethysmography or gas dilution)."
    },
    {
        "id": 43,
        "question": "A patient breathing 100% O2 has FRC = 2500 mL. Assuming O2 consumption = 250 mL/min, estimate non-hypoxic apnea duration.",
        "options": [
            "A. 2.5 minutes",
            "B. 5 minutes",
            "C. 7.5 minutes",
            "D. 10 minutes",
            "E. 25 minutes"
        ],
        "answer": "D. 10 minutes",
        "explanation": "Apnea duration = FRC / O2 consumption = 2500 mL / 250 mL/min = 10 minutes."
    },
    {
        "id": 44,
        "question": "If severe bronchoconstriction reduces airway radius to 1/2 its baseline value, airway resistance will:",
        "options": [
            "A. Decrease by a factor of 16",
            "B. Increase by a factor of 16",
            "C. Decrease by a factor of 2",
            "D. Increase by a factor of 2",
            "E. Remain unchanged"
        ],
        "answer": "B. Increase by a factor of 16",
        "explanation": "By Poiseuille's Law, resistance is inversely proportional to r^4. Halving radius increases resistance 16-fold."
    },
    {
        "id": 45,
        "question": "Subject A has RR = 5/min and TV = 1000 mL. What is Subject A's minute ventilation?",
        "options": [
            "A. 3 L/min",
            "B. 4 L/min",
            "C. 5 L/min",
            "D. 6 L/min",
            "E. 8 L/min"
        ],
        "answer": "C. 5 L/min",
        "explanation": "Minute ventilation = RR x TV = 5/min x 1000 mL = 5,000 mL/min = 5 L/min."
    },
    {
        "id": 46,
        "question": "Subject B has RR = 10/min, TV = 500 mL, and Dead Space = 200 mL. What is Subject B's alveolar minute ventilation?",
        "options": [
            "A. 3 L/min",
            "B. 4 L/min",
            "C. 5 L/min",
            "D. 6 L/min",
            "E. 8 L/min"
        ],
        "answer": "A. 3 L/min",
        "explanation": "Alveolar ventilation = RR x (TV - Dead Space) = 10 x (500 - 200) = 3,000 mL/min = 3 L/min."
    },
    {
        "id": 47,
        "question": "Comparing Subject A (Alveolar vent = 4 L/min) and Subject B (Alveolar vent = 3 L/min), which subject will retain more CO2 and have lower pH?",
        "options": [
            "A. Subject A",
            "B. Subject B",
            "C. Both identical",
            "D. Depends on barometric pressure",
            "E. Cannot be determined"
        ],
        "answer": "B. Subject B",
        "explanation": "Lower alveolar ventilation in Subject B (3 L/min vs 4 L/min) causes CO2 retention, higher PaCO2, and lower arterial pH."
    },
    {
        "id": 48,
        "question": "A ventilation-perfusion ratio equal to zero (V/Q = 0) defines:",
        "options": [
            "A. True intrapulmonary shunt",
            "B. Anatomic dead space",
            "C. Alveolar dead space",
            "D. Physiological dead space",
            "E. Ideal gas exchange unit"
        ],
        "answer": "A. True intrapulmonary shunt",
        "explanation": "V/Q = 0 represents perfused alveoli receiving no ventilation, defining a true shunt."
    },
    {
        "id": 49,
        "question": "What primary physical mechanism directs greater pulmonary blood flow toward the lung bases in an upright human?",
        "options": [
            "A. Alveolar surface tension",
            "B. Hydrostatic gravitational effect",
            "C. Chest wall compliance",
            "D. Hypoxic vasoconstriction",
            "E. Anatomic shunting"
        ],
        "answer": "B. Hydrostatic gravitational effect",
        "explanation": "Gravity increases hydrostatic intravascular pressure in dependent lung regions, recruiting and distending basal capillaries."
    },
    {
        "id": 50,
        "question": "Mycobacterium tuberculosis reactivation shows a striking predilection for lung apices because:",
        "options": [
            "A. Ventilation is highest at apex",
            "B. Perfusion is highest at apex",
            "C. V/Q ratio and PO2 are highest at apex",
            "D. Lymphatics absent at apex",
            "E. Airway resistance lowest at apex"
        ],
        "answer": "C. V/Q ratio and PO2 are highest at apex",
        "explanation": "High V/Q ratio at the lung apex produces high tissue PO2, favoring growth of obligate aerobic M. tuberculosis."
    },
    {
        "id": 51,
        "question": "Why are true vocal folds lined by stratified squamous epithelium rather than pseudostratified ciliated columnar epithelium?",
        "options": [
            "A. Exposure to unconditioned pollutants",
            "B. Mechanical friction and stress during phonation",
            "C. Rapid mucosal absorption",
            "D. Lack of lamina propria",
            "E. Lack of sensory nerves"
        ],
        "answer": "B. Mechanical friction and stress during phonation",
        "explanation": "Stratified squamous epithelium protects against severe mechanical abrasion and friction during vocal cord vibration."
    },
    {
        "id": 52,
        "question": "What is the primary physiological function of the blood-air barrier in interalveolar septa?",
        "options": [
            "A. Passive diffusion of gases while preventing fluid leakage",
            "B. Passage of RBCs into alveoli",
            "C. Prevent macrophage systemic entry",
            "D. Filter plasma into airways",
            "E. Structural anchorage"
        ],
        "answer": "A. Passive diffusion of gases while preventing fluid leakage",
        "explanation": "Extremely thin barrier permits rapid passive gas exchange while tight junctions prevent plasma leakage into alveoli."
    },
    {
        "id": 53,
        "question": "How does olfactory epithelium structurally differ from standard respiratory epithelium?",
        "options": [
            "A. Complete absence of cilia",
            "B. Absence of goblet cells",
            "C. Absence of basal stem cells",
            "D. Absence of supporting cells",
            "E. Non-vascular basement membrane"
        ],
        "answer": "B. Absence of goblet cells",
        "explanation": "Olfactory epithelium lacks goblet cells; mucosal fluid is secreted by underlying serous Bowman's glands."
    },
    {
        "id": 54,
        "question": "Which cell type acts as the resident stem/progenitor cell for epithelial repair in terminal bronchioles?",
        "options": [
            "A. Basal cell",
            "B. Club cell (Bronchiolar exocrine cell)",
            "C. Ciliated columnar cell",
            "D. Goblet cell",
            "E. Type I pneumocyte"
        ],
        "answer": "B. Club cell (Bronchiolar exocrine cell)",
        "explanation": "Club cells (Clara cells) regenerate bronchiolar epithelium, replacing themselves and ciliated cells after injury."
    },
    {
        "id": 55,
        "question": "Metabolic oxygen consumption by mitochondrial enzymes inside tissue cells is defined as:",
        "options": [
            "A. External respiration",
            "B. Pulmonary ventilation",
            "C. Cellular respiration",
            "D. Gas transport",
            "E. Internal ventilation"
        ],
        "answer": "C. Cellular respiration",
        "explanation": "Mitochondrial ATP generation consuming O2 is cellular (internal) respiration."
    },
    {
        "id": 56,
        "question": "The pleural cavity is anatomically defined as the potential space between:",
        "options": [
            "A. Visceral pleura and parietal pleura",
            "B. Lung parenchyma and visceral pleura",
            "C. Parietal pleura and thoracic wall",
            "D. Mediastinum and pericardium",
            "E. Costal cartilages and intercostals"
        ],
        "answer": "A. Visceral pleura and parietal pleura",
        "explanation": "The pleural cavity is the serous fluid-filled potential space between visceral and parietal pleura."
    },
    {
        "id": 57,
        "question": "In the costal groove of a rib, what is the superior-to-inferior arrangement of the neurovascular bundle?",
        "options": [
            "A. Nerve, Artery, Vein (NAV)",
            "B. Vein, Artery, Nerve (VAN)",
            "C. Artery, Vein, Nerve (AVN)",
            "D. Nerve, Vein, Artery (NVA)",
            "E. Artery, Nerve, Vein (ANV)"
        ],
        "answer": "B. Vein, Artery, Nerve (VAN)",
        "explanation": "From top to bottom in the costal groove, structures lie in VAN order: Vein, Artery, Nerve."
    },
    {
        "id": 58,
        "question": "The phrenic nerve provides sensory/motor innervation to all the following structures EXCEPT:",
        "options": [
            "A. Diaphragmatic central tendon",
            "B. Mediastinal parietal pleura",
            "C. Diaphragmatic parietal pleura",
            "D. Fibrous pericardium",
            "E. Left ventricular myocardium"
        ],
        "answer": "E. Left ventricular myocardium",
        "explanation": "Myocardium is innervated by cardiac autonomic plexuses, NOT the phrenic nerve."
    },
    {
        "id": 59,
        "question": "Where is the intercostal nerve positioned in relation to the costal groove of a rib?",
        "options": [
            "A. Deep to superior border",
            "B. Superficial to superior border",
            "C. Immediately deep to inferior border in costal groove",
            "D. Superficial to inferior border",
            "E. In marrow space"
        ],
        "answer": "C. Immediately deep to inferior border in costal groove",
        "explanation": "The intercostal nerve runs along the inferior border of the costal groove, below the vein and artery."
    },
    {
        "id": 60,
        "question": "What anatomical site on a rib shaft is most susceptible to traumatic structural fracture?",
        "options": [
            "A. Head of rib",
            "B. Neck of rib",
            "C. Tubercle of rib",
            "D. Angle of rib shaft",
            "E. Costochondral junction"
        ],
        "answer": "D. Angle of rib shaft",
        "explanation": "The angle of the rib is the point of maximum curvature and structural weakness."
    },
    {
        "id": 61,
        "question": "Which statement regarding sternal anatomy is INCORRECT?",
        "options": [
            "A. Manubrium articulates with clavicles and 1st costal cartilage",
            "B. Sternal angle lies at T4/T5 disc level",
            "C. Xiphoid process remains cartilaginous in youth",
            "D. Sternal angle is marker for 1st costal cartilage",
            "E. Tracheal bifurcation occurs near sternal angle"
        ],
        "answer": "D. Sternal angle is marker for 1st costal cartilage",
        "explanation": "The sternal angle marks the articulation of the 2nd costal cartilage (1st costal cartilage attaches to the manubrium)."
    },
    {
        "id": 62,
        "question": "Which diaphragmatic aperture is correctly matched with its thoracic vertebral level?",
        "options": [
            "A. Vena cava foramen \u2014 T8",
            "B. Esophageal hiatus \u2014 T8",
            "C. Aortic hiatus \u2014 T10",
            "D. Vena cava foramen \u2014 T12",
            "E. Esophageal hiatus \u2014 T12"
        ],
        "answer": "A. Vena cava foramen \u2014 T8",
        "explanation": "T8 = Caval foramen, T10 = Esophageal hiatus, T12 = Aortic hiatus ('I ate 8, ten 10, eggs 12')."
    },
    {
        "id": 63,
        "question": "Relative to the root (hilum) of the lung, what are the precise anatomical paths of the vagus and phrenic nerves?",
        "options": [
            "A. Vagus anterior; Phrenic posterior",
            "B. Vagus posterior; Phrenic anterior",
            "C. Both anterior",
            "D. Both posterior",
            "E. Vagus through root"
        ],
        "answer": "B. Vagus posterior; Phrenic anterior",
        "explanation": "Vagus passes POSTERIOR to the lung root; Phrenic passes ANTERIOR to the lung root."
    },
    {
        "id": 64,
        "question": "Which of the following structures is NOT located in the posterior mediastinum?",
        "options": [
            "A. Descending thoracic aorta",
            "B. Thoracic duct",
            "C. Phrenic nerves",
            "D. Azygos veins",
            "E. Esophagus"
        ],
        "answer": "C. Phrenic nerves",
        "explanation": "Phrenic nerves traverse the middle mediastinum over the fibrous pericardium."
    },
    {
        "id": 65,
        "question": "A patient with pleurisy feels sharp inspiratory pain. Which nerves transmit somatic pain from the costal parietal pleura?",
        "options": [
            "A. Phrenic nerve",
            "B. Intercostal nerves",
            "C. Vagus nerve",
            "D. Sympathetic splanchnic nerves",
            "E. Pulmonary plexus"
        ],
        "answer": "B. Intercostal nerves",
        "explanation": "Costal parietal pleura receives somatic pain innervation via intercostal nerves."
    },
    {
        "id": 66,
        "question": "Which anatomical feature is present on the right lung but absent on the left lung?",
        "options": [
            "A. Cardiac notch",
            "B. Lingula",
            "C. Middle lobe separated by horizontal fissure",
            "D. Aortic groove",
            "E. Eight segments"
        ],
        "answer": "C. Middle lobe separated by horizontal fissure",
        "explanation": "The right lung has 3 lobes separated by oblique and horizontal fissures."
    },
    {
        "id": 67,
        "question": "All the following are anatomical subdivisions of parietal pleura EXCEPT:",
        "options": [
            "A. Costal pleura",
            "B. Diaphragmatic pleura",
            "C. Mediastinal pleura",
            "D. Cervical pleura (Cupula)",
            "E. Bronchopulmonary pleura"
        ],
        "answer": "E. Bronchopulmonary pleura",
        "explanation": "Parietal pleura consists of costal, diaphragmatic, mediastinal, and cervical parts. 'Bronchopulmonary' is not a parietal subdivision."
    },
    {
        "id": 68,
        "question": "Which structure does NOT pass through the hilum (root) of the lung?",
        "options": [
            "A. Main bronchus",
            "B. Pulmonary artery",
            "C. Pulmonary veins",
            "D. Bronchial vessels",
            "E. Phrenic nerve"
        ],
        "answer": "E. Phrenic nerve",
        "explanation": "The phrenic nerve runs anterior to the lung root."
    },
    {
        "id": 69,
        "question": "According to Laplace's Law (P = 2T/r), surfactant's reduction of surface tension is essential because it:",
        "options": [
            "A. Prevents smaller alveoli from collapsing into larger alveoli",
            "B. Increases pressure needed for small alveoli",
            "C. Reduces compliance",
            "D. Increases transpulmonary pressure",
            "E. Causes fluid transudation"
        ],
        "answer": "A. Prevents smaller alveoli from collapsing into larger alveoli",
        "explanation": "Surfactant reduces surface tension proportionally more in smaller alveoli, preventing small-alveolus collapse into larger ones."
    },
    {
        "id": 70,
        "question": "Central chemoreceptors on the ventral medulla respond primarily to changes in:",
        "options": [
            "A. Arterial PO2 directly",
            "B. Arterial pH directly",
            "C. CSF pH altered by arterial PCO2",
            "D. Mixed venous PCO2",
            "E. Alveolar-arterial gradient"
        ],
        "answer": "C. CSF pH altered by arterial PCO2",
        "explanation": "CO2 crosses the blood-brain barrier into CSF, forming H+ that directly stimulates central chemoreceptors."
    },
    {
        "id": 71,
        "question": "Peripheral chemoreceptors in carotid and aortic bodies are primarily activated by:",
        "options": [
            "A. Marked decrease in arterial PaO2 (< 60 mmHg)",
            "B. Small decrease in O2 content (anemia)",
            "C. Mild pH increase",
            "D. Decrease in BP",
            "E. Increase in blood glucose"
        ],
        "answer": "A. Marked decrease in arterial PaO2 (< 60 mmHg)",
        "explanation": "Peripheral chemoreceptors fire rapidly when PaO2 drops below 60 mmHg."
    },
    {
        "id": 72,
        "question": "During exercise, the oxygen-hemoglobin dissociation curve shifts rightward (Bohr effect) due to increased:",
        "options": [
            "A. Decreased temperature",
            "B. Decreased PCO2",
            "C. Increased pH",
            "D. Increased 2,3-BPG, H+, PCO2, and temp",
            "E. Decreased metabolic rate"
        ],
        "answer": "D. Increased 2,3-BPG, H+, PCO2, and temp",
        "explanation": "Increases in H+ (low pH), PCO2, 2,3-BPG, and temperature shift the O2 curve right, promoting oxygen unloading."
    },
    {
        "id": 73,
        "question": "What is the physiological mechanism of the Haldane effect in pulmonary capillaries?",
        "options": [
            "A. Oxygen binding to hemoglobin promotes CO2 unloading",
            "B. CO2 binding increases O2 affinity",
            "C. High PCO2 promotes O2 release",
            "D. H+ accumulation shifts curve left",
            "E. Carbonic anhydrase inhibition"
        ],
        "answer": "A. Oxygen binding to hemoglobin promotes CO2 unloading",
        "explanation": "Oxygenation of hemoglobin in lungs reduces its affinity for CO2 and H+, enhancing CO2 clearance."
    },
    {
        "id": 74,
        "question": "In a resting healthy adult, what percentage of delivered arterial oxygen is extracted during capillary transit?",
        "options": [
            "A. 10%",
            "B. 25%",
            "C. 50%",
            "D. 75%",
            "E. 90%"
        ],
        "answer": "B. 25%",
        "explanation": "Arterial SaO2 (~98%) minus Mixed Venous SvO2 (~75%) = 25% systemic oxygen extraction at rest."
    },
    {
        "id": 75,
        "question": "An acute increase in physiological dead space at constant minute ventilation leads directly to:",
        "options": [
            "A. Hypercapnia and decreased alveolar ventilation",
            "B. Hypocapnia and increased alveolar ventilation",
            "C. Increased pH",
            "D. Decreased A-a gradient",
            "E. Increased O2 delivery"
        ],
        "answer": "A. Hypercapnia and decreased alveolar ventilation",
        "explanation": "Increased dead space wastes ventilation, reducing alveolar ventilation and causing blood CO2 accumulation (hypercapnia)."
    }
]

CV_QS = [
    {
        "id": 76,
        "question": "The epicardium layer of the heart wall is synonymous with the:",
        "options": [
            "A. Endocardium",
            "B. Visceral layer of serous pericardium",
            "C. Modified myocardium",
            "D. Fibrous pericardium",
            "E. Subendocardium"
        ],
        "answer": "B. Visceral layer of serous pericardium",
        "explanation": "The epicardium is the outer layer of the heart, identical to the visceral layer of the serous pericardium."
    },
    {
        "id": 77,
        "question": "Atrial myocytes produce Atrial Natriuretic Peptide (ANP) in response to stretch. ANP acts to:",
        "options": [
            "A. Decrease blood pressure",
            "B. Increase blood pressure",
            "C. Cause vasoconstriction",
            "D. Facilitate renin release",
            "E. Promote renal Na+ reabsorption"
        ],
        "answer": "A. Decrease blood pressure",
        "explanation": "ANP induces natriuresis, diuresis, and vasodilation, lowering blood volume and arterial blood pressure."
    },
    {
        "id": 78,
        "question": "Normal intrinsic cardiac impulse initiation is the primary responsibility of which structure?",
        "options": [
            "A. AV node",
            "B. Bundle of His",
            "C. Sympathetic nerves",
            "D. Sinoatrial (SA) node",
            "E. Purkinje fibers"
        ],
        "answer": "D. Sinoatrial (SA) node",
        "explanation": "The SA node possesses the fastest spontaneous depolarization rate and acts as the normal cardiac pacemaker."
    },
    {
        "id": 79,
        "question": "In which histological layer of the heart wall are Purkinje conduction fibers located?",
        "options": [
            "A. Pericardium",
            "B. Myocardium",
            "C. Subendocardium",
            "D. Epicardium",
            "E. Adventitia"
        ],
        "answer": "C. Subendocardium",
        "explanation": "Purkinje fibers run in the subendocardial layer before penetrating ventricular cardiac muscle."
    },
    {
        "id": 80,
        "question": "Cardiac Purkinje cells are specialized primarily for:",
        "options": [
            "A. Elasticity",
            "B. Rapid electrical impulse conduction",
            "C. High force contraction",
            "D. Valve stabilization",
            "E. Wall strengthening"
        ],
        "answer": "B. Rapid electrical impulse conduction",
        "explanation": "Purkinje cells have large diameters and abundant gap junctions tailored for high-speed electrical impulse conduction."
    },
    {
        "id": 81,
        "question": "Which layer of the heart wall is in direct contact with intraventricular blood?",
        "options": [
            "A. Epicardium",
            "B. Endocardium",
            "C. Myocardium",
            "D. Pericardium",
            "E. Vasa vasorum"
        ],
        "answer": "B. Endocardium",
        "explanation": "The endocardium lines the internal surface of all heart chambers and valves."
    },
    {
        "id": 82,
        "question": "Which single layer is present throughout ALL parts of the cardiovascular system, from aorta to capillaries?",
        "options": [
            "A. Tunica media",
            "B. Tunica adventitia",
            "C. Endothelial cell layer",
            "D. Vasa vasorum",
            "E. Internal elastic lamina"
        ],
        "answer": "C. Endothelial cell layer",
        "explanation": "Endothelium is the universal inner lining present in every blood vessel."
    },
    {
        "id": 83,
        "question": "In atherosclerosis, which layer of the vessel wall undergoes primary lipid accumulation and thickening?",
        "options": [
            "A. Tunica intima",
            "B. Tunica media",
            "C. Tunica adventitia",
            "D. Externa",
            "E. Subserosa"
        ],
        "answer": "A. Tunica intima",
        "explanation": "Atherosclerotic plaque development occurs within the tunica intima."
    },
    {
        "id": 84,
        "question": "Smooth muscle in the tunica media of blood vessels is arranged predominantly in what orientation?",
        "options": [
            "A. Longitudinal",
            "B. Circular",
            "C. Transverse",
            "D. Radial",
            "E. Random"
        ],
        "answer": "B. Circular",
        "explanation": "Vascular smooth muscle is arranged circularly around the vessel lumen to regulate vessel diameter."
    },
    {
        "id": 85,
        "question": "What is the principal physiological function of lymphatic vessels?",
        "options": [
            "A. Immune surveillance site",
            "B. Lymph filtration",
            "C. Transport leaked fluid/proteins back to blood",
            "D. Gas exchange",
            "E. Hormone transport"
        ],
        "answer": "C. Transport leaked fluid/proteins back to blood",
        "explanation": "Lymphatics drain excess interstitial fluid and extravasated plasma proteins back into the venous system."
    },
    {
        "id": 86,
        "question": "The dilated, saclike origin of the thoracic duct in the abdomen is the:",
        "options": [
            "A. Lacteal",
            "B. Right lymphatic duct",
            "C. Cisterna chyli",
            "D. Lymph sac",
            "E. Chyle node"
        ],
        "answer": "C. Cisterna chyli",
        "explanation": "The cisterna chyli receives lumbar and intestinal lymph trunks to form the thoracic duct."
    },
    {
        "id": 87,
        "question": "Prominent longitudinal smooth muscle bundles in the tunica adventitia are a characteristic feature of:",
        "options": [
            "A. Arterioles",
            "B. Venules",
            "C. Muscular arteries",
            "D. Elastic arteries",
            "E. Large veins (e.g. IVC)"
        ],
        "answer": "E. Large veins (e.g. IVC)",
        "explanation": "Large veins (like the vena cava) contain longitudinal smooth muscle in the adventitia to aid venous return."
    },
    {
        "id": 88,
        "question": "Which histological feature is most characteristic of a medium-sized (muscular) artery?",
        "options": [
            "A. Endothelial valves",
            "B. Longitudinal adventitial muscle",
            "C. Media elastic lamellae",
            "D. Well-defined internal elastic lamina",
            "E. Vasa vasorum"
        ],
        "answer": "D. Well-defined internal elastic lamina",
        "explanation": "A prominent, wavy internal elastic lamina separates the intima and media in muscular arteries."
    },
    {
        "id": 89,
        "question": "In which organ would you expect to find continuous (non-fenestrated) capillaries rather than fenestrated ones?",
        "options": [
            "A. Liver",
            "B. Endocrine pancreas",
            "C. Lung",
            "D. Kidney glomerulus",
            "E. Intestinal villi"
        ],
        "answer": "C. Lung",
        "explanation": "Pulmonary capillaries have continuous endothelium to maintain the blood-air barrier and prevent fluid transudation."
    },
    {
        "id": 90,
        "question": "Extracellular matrix (elastin and collagen) in the tunica media of large elastic arteries is synthesized by:",
        "options": [
            "A. Endothelial cells",
            "B. Vascular smooth muscle cells",
            "C. Fibroblasts",
            "D. Macrophages",
            "E. Pericytes"
        ],
        "answer": "B. Vascular smooth muscle cells",
        "explanation": "Arterial smooth muscle cells in the tunica media synthesize elastin, collagen, and ground substance."
    },
    {
        "id": 91,
        "question": "Which type of capillary possesses an incomplete or discontinuous basement membrane?",
        "options": [
            "A. Continuous",
            "B. Fenestrated with diaphragm",
            "C. Fenestrated without diaphragm",
            "D. HEV",
            "E. Sinusoidal"
        ],
        "answer": "E. Sinusoidal",
        "explanation": "Sinusoidal (discontinuous) capillaries in liver, spleen, and marrow have large intercellular gaps and incomplete basement membranes."
    },
    {
        "id": 92,
        "question": "Which structural feature distinguishes somatic capillaries from visceral capillaries?",
        "options": [
            "A. Presence or absence of fenestrae",
            "B. Lumen size",
            "C. Wall thickness",
            "D. Pericytes",
            "E. Basal lamina thickness"
        ],
        "answer": "A. Presence or absence of fenestrae",
        "explanation": "Somatic capillaries are continuous (non-fenestrated); visceral capillaries are fenestrated."
    },
    {
        "id": 93,
        "question": "Vasa vasorum in large vessel walls function analogously to which cardiac structure?",
        "options": [
            "A. AV valves",
            "B. Semilunar valves",
            "C. Coronary arteries",
            "D. Elastic arteries",
            "E. Metarterioles"
        ],
        "answer": "C. Coronary arteries",
        "explanation": "Vasa vasorum nourish the outer walls of large vessels, just as coronary arteries supply the heart wall."
    },
    {
        "id": 94,
        "question": "Which is the thickest structural layer in the wall of a large artery?",
        "options": [
            "A. Subepithelial",
            "B. Adventitia",
            "C. Externa",
            "D. Intima",
            "E. Tunica media"
        ],
        "answer": "E. Tunica media",
        "explanation": "The tunica media is the thickest layer in arteries, containing smooth muscle and elastic fibers."
    },
    {
        "id": 95,
        "question": "Large veins have more abundant vasa vasorum than corresponding arteries primarily because veins:",
        "options": [
            "A. Slow flow",
            "B. Wide lumen",
            "C. Require more oxygen",
            "D. Thicker walls",
            "E. Carry deoxygenated blood"
        ],
        "answer": "E. Carry deoxygenated blood",
        "explanation": "Deoxygenated luminal blood cannot supply outer wall cells, necessitating extensive vasa vasorum in veins."
    },
    {
        "id": 96,
        "question": "Which histological feature is strictly exclusive to cardiomyocytes among muscle tissue types?",
        "options": [
            "A. Single nucleus",
            "B. Smooth ER network",
            "C. Central nucleus",
            "D. Striations",
            "E. Intercalated discs"
        ],
        "answer": "E. Intercalated discs",
        "explanation": "Intercalated discs with desmosomes and gap junctions are unique to cardiac muscle."
    },
    {
        "id": 97,
        "question": "Which statement regarding cardiac muscle contraction is most accurate?",
        "options": [
            "A. T-tubules store less Ca2+",
            "B. Contraction strength depends on extracellular Ca2+",
            "C. Action potential opens slow Ca2+ immediately",
            "D. Repolarization caused by Na+",
            "E. Mucopolysaccharides bind Cl-"
        ],
        "answer": "B. Contraction strength depends on extracellular Ca2+",
        "explanation": "Cardiac contraction relies on Calcium-Induced Calcium Release (CICR) triggered by extracellular Ca2+ influx via L-type channels."
    },
    {
        "id": 98,
        "question": "Which electrolyte imbalance causes the heart to go into spastic (tetanic) contraction?",
        "options": [
            "A. Elevated body temp",
            "B. Sympathetic stimulation",
            "C. Hypokalemia",
            "D. Hyperkalemia",
            "E. Excess extracellular Ca2+"
        ],
        "answer": "E. Excess extracellular Ca2+",
        "explanation": "Severe hypercalcemia prolongs excitation-contraction coupling, locking cardiac muscle in spastic contraction."
    },
    {
        "id": 99,
        "question": "Which electrolyte imbalance leads to a dilated, flaccid heart that arrests in diastole?",
        "options": [
            "A. Excess Ca2+",
            "B. Excess K+ (Hyperkalemia)",
            "C. Excess Na+",
            "D. Sympathetic stimulation",
            "E. Norepinephrine"
        ],
        "answer": "B. Excess K+ (Hyperkalemia)",
        "explanation": "Hyperkalemia depolarizes resting potential, impairing conduction and causing a dilated, flaccid heart."
    },
    {
        "id": 100,
        "question": "According to the Frank-Starling law, increasing end-diastolic volume (preload) within physiological limits causes:",
        "options": [
            "A. Decreased contraction",
            "B. Increased force of contraction",
            "C. No change in CO",
            "D. Constant force",
            "E. Decreased SV"
        ],
        "answer": "B. Increased force of contraction",
        "explanation": "Myocyte stretch by EDV optimizes actin-myosin overlap, increasing stroke volume."
    },
    {
        "id": 101,
        "question": "A positive inotropic agent acts primarily to:",
        "options": [
            "A. Reduce heart rate",
            "B. Increase heart rate",
            "C. Increase myocardial contractility",
            "D. Decrease contractility",
            "E. Enhance venous return"
        ],
        "answer": "C. Increase myocardial contractility",
        "explanation": "Inotropic agents alter myocardial contractility (force of contraction)."
    },
    {
        "id": 102,
        "question": "On the ventricular pressure-volume loop, the First Heart Sound (S1) occurs at:",
        "options": [
            "A. Point B (Mitral valve closure)",
            "B. Between A and B",
            "C. Between B and C",
            "D. Between C and D",
            "E. Between D and A"
        ],
        "answer": "A. Point B (Mitral valve closure)",
        "explanation": "Point B marks AV valve closure at the end of diastole, generating S1."
    },
    {
        "id": 103,
        "question": "What mechanical event marks the completion of Isovolumic Relaxation?",
        "options": [
            "A. AV valve closure",
            "B. Aortic valve opening",
            "C. Aortic valve closure",
            "D. Mitral valve opening",
            "E. Pulmonary valve closure"
        ],
        "answer": "D. Mitral valve opening",
        "explanation": "Isovolumic relaxation ends when ventricular pressure drops below atrial pressure, opening the mitral valve."
    },
    {
        "id": 104,
        "question": "Which cardiac event generates the First Heart Sound (S1)?",
        "options": [
            "A. Closure of aortic valve",
            "B. Rapid ventricular filling",
            "C. Start of diastole",
            "D. Opening of AV valves",
            "E. Closure of AV valves"
        ],
        "answer": "E. Closure of AV valves",
        "explanation": "S1 is generated by closure of the mitral and tricuspid (AV) valves at the onset of systole."
    },
    {
        "id": 105,
        "question": "Which phase of the cardiac cycle immediately follows the onset of the QRS wave on ECG?",
        "options": [
            "A. Isovolumic relaxation",
            "B. Ventricular ejection",
            "C. Atrial systole",
            "D. Diastasis",
            "E. Isovolumic contraction"
        ],
        "answer": "E. Isovolumic contraction",
        "explanation": "QRS represents ventricular depolarization, triggering Isovolumic Contraction."
    },
    {
        "id": 106,
        "question": "Ventricular pressure exceeds atrial pressure throughout the cardiac cycle EXCEPT during:",
        "options": [
            "A. Isovolumic contraction",
            "B. Atrial systole",
            "C. Rapid ejection",
            "D. Slow ejection",
            "E. None"
        ],
        "answer": "B. Atrial systole",
        "explanation": "During atrial systole, atrial contraction transiently raises atrial pressure above ventricular pressure to top off filling."
    },
    {
        "id": 107,
        "question": "Atrioventricular (AV) valves are open during which phase of the cardiac cycle?",
        "options": [
            "A. Isovolumic contraction",
            "B. Isovolumic relaxation",
            "C. Rapid filling phase",
            "D. Ejection"
        ],
        "answer": "C. Rapid filling phase",
        "explanation": "AV valves are open throughout ventricular diastole (rapid filling, diastasis, atrial systole)."
    },
    {
        "id": 108,
        "question": "During which phase of the cardiac cycle are ALL four heart valves open simultaneously?",
        "options": [
            "A. Isovolumic relaxation",
            "B. Isovolumic contraction",
            "C. Rapid filling",
            "D. None of the above"
        ],
        "answer": "D. None of the above",
        "explanation": "All four valves are never open at the same time in a normal cardiac cycle."
    },
    {
        "id": 109,
        "question": "The Second Heart Sound (S2) is generated by the closure of which valves?",
        "options": [
            "A. AV valves",
            "B. Semilunar valves (Aortic and Pulmonary)",
            "C. All valves",
            "D. Opening of AV valves",
            "E. None"
        ],
        "answer": "B. Semilunar valves (Aortic and Pulmonary)",
        "explanation": "S2 is caused by closure of the aortic and pulmonary semilunar valves at the end of systole."
    },
    {
        "id": 110,
        "question": "The First Heart Sound (S1) occurs when the:",
        "options": [
            "A. Ventricle relaxes",
            "B. Semilunar valves close",
            "C. AV valves close",
            "D. Atria contract",
            "E. Aortic valve closes"
        ],
        "answer": "C. AV valves close",
        "explanation": "S1 is produced by closure of the AV valves."
    },
    {
        "id": 111,
        "question": "A patient has Ejection Fraction = 0.25 and End-Systolic Volume (ESV) = 150 mL. What is his End-Diastolic Volume (EDV)?",
        "options": [
            "A. 50 mL",
            "B. 100 mL",
            "C. 125 mL",
            "D. 200 mL",
            "E. 250 mL"
        ],
        "answer": "D. 200 mL",
        "explanation": "EF = (EDV - ESV) / EDV => 0.25 = (EDV - 150) / EDV => 0.75 EDV = 150 => EDV = 200 mL."
    },
    {
        "id": 112,
        "question": "What is the typical normal resting ventricular ejection fraction (EF) in a healthy adult?",
        "options": [
            "A. 20%",
            "B. 30%",
            "C. 40%",
            "D. 60%",
            "E. 80%"
        ],
        "answer": "D. 60%",
        "explanation": "Normal resting ejection fraction is ~55-70% (60% standard)."
    },
    {
        "id": 113,
        "question": "The volume of blood pumped by one ventricle in one minute is defined as:",
        "options": [
            "A. Stroke volume",
            "B. End-diastolic volume",
            "C. Ejection fraction",
            "D. Cardiac output",
            "E. Venous return"
        ],
        "answer": "D. Cardiac output",
        "explanation": "Cardiac Output = Heart Rate x Stroke Volume (L/min)."
    },
    {
        "id": 114,
        "question": "Stroke volume is directly regulated by all of the following EXCEPT:",
        "options": [
            "A. End-diastolic volume (Preload)",
            "B. Cardiac output",
            "C. Contractility",
            "D. Peripheral resistance (Afterload)",
            "E. Venous return"
        ],
        "answer": "B. Cardiac output",
        "explanation": "Cardiac output is the result of SV x HR, not a regulator of stroke volume."
    },
    {
        "id": 115,
        "question": "The preload acting on a cardiac ventricle is best quantified by:",
        "options": [
            "A. Contractility",
            "B. Stroke volume",
            "C. End-diastolic volume",
            "D. Ejection fraction",
            "E. Cardiac output"
        ],
        "answer": "C. End-diastolic volume",
        "explanation": "Preload is the myocyte stretch prior to contraction, represented by EDV."
    },
    {
        "id": 116,
        "question": "The afterload imposed on the left ventricle corresponds to:",
        "options": [
            "A. End-systolic volume",
            "B. Atrial kick volume",
            "C. Total peripheral resistance / Aortic pressure",
            "D. Ejection fraction",
            "E. None"
        ],
        "answer": "C. Total peripheral resistance / Aortic pressure",
        "explanation": "Afterload is the load against which the ventricle must contract to eject blood."
    },
    {
        "id": 117,
        "question": "The Frank-Starling law describes the relationship between:",
        "options": [
            "A. SV and CO",
            "B. Stroke volume and End-Diastolic Volume",
            "C. SV and TPR",
            "D. CO and HR"
        ],
        "answer": "B. Stroke volume and End-Diastolic Volume",
        "explanation": "Frank-Starling law states stroke volume increases in proportion to EDV."
    },
    {
        "id": 118,
        "question": "Which mechanism increases venous return to the heart?",
        "options": [
            "A. Venous dilation",
            "B. Valve loss",
            "C. Increased skeletal muscle activity",
            "D. Decreased RR",
            "E. Expiration"
        ],
        "answer": "C. Increased skeletal muscle activity",
        "explanation": "Skeletal muscle pump action compresses veins to increase venous return."
    },
    {
        "id": 119,
        "question": "According to Starling's Law, cardiac output is directly related to:",
        "options": [
            "A. Ventricle size",
            "B. Heart rate",
            "C. Amount of blood returning to heart (Venous return)",
            "D. ESV",
            "E. Reserve"
        ],
        "answer": "C. Amount of blood returning to heart (Venous return)",
        "explanation": "Cardiac output matches venous return via Starling mechanism."
    },
    {
        "id": 120,
        "question": "How does a passive leg raise test affect venous return?",
        "options": [
            "A. Unchanged",
            "B. Decreases",
            "C. Increases",
            "D. Normalizes"
        ],
        "answer": "C. Increases",
        "explanation": "Passive leg raise transfers blood from lower limbs to central circulation, increasing venous return."
    },
    {
        "id": 121,
        "question": "What is the impact of a reduced respiratory rate on venous return and cardiac output?",
        "options": [
            "A. Both increase",
            "B. Both decrease",
            "C. Venous return decreases; Cardiac output remains constant",
            "D. VR decreases; CO increases"
        ],
        "answer": "C. Venous return decreases; Cardiac output remains constant",
        "explanation": "Reduced respiratory pump lowers VR, but autonomic compensations maintain near-constant CO."
    },
    {
        "id": 122,
        "question": "If a patient's BP is 110/70 mmHg, what is their Pulse Pressure?",
        "options": [
            "A. Pulse pressure is 40 mmHg",
            "B. Diastolic pressure is 40 mmHg",
            "C. Systolic pressure is 70 mmHg",
            "D. MAP is 120 mmHg",
            "E. All"
        ],
        "answer": "A. Pulse pressure is 40 mmHg",
        "explanation": "Pulse Pressure = SBP - DBP = 110 - 70 = 40 mmHg."
    },
    {
        "id": 123,
        "question": "Pulse pressure is calculated by:",
        "options": [
            "A. Adding SBP and DBP",
            "B. Subtracting DBP from SBP",
            "C. (SBP + DBP)/2",
            "D. DBP + 1/3(SBP-DBP)",
            "E. None"
        ],
        "answer": "B. Subtracting DBP from SBP",
        "explanation": "Pulse pressure = Systolic BP minus Diastolic BP."
    },
    {
        "id": 124,
        "question": "Friction between flowing blood and vessel walls is the physiological origin of:",
        "options": [
            "A. Decreased BP",
            "B. Increased flow",
            "C. Viscosity decrease",
            "D. Peripheral resistance",
            "E. No effect"
        ],
        "answer": "D. Peripheral resistance",
        "explanation": "Vascular resistance arises from friction between blood and endothelial walls."
    },
    {
        "id": 125,
        "question": "Which of the following factors causes an increase in peripheral vascular resistance?",
        "options": [
            "A. Increased blood viscosity",
            "B. Decreased hematocrit",
            "C. Increased vessel radius",
            "D. Decreased volume",
            "E. None"
        ],
        "answer": "A. Increased blood viscosity",
        "explanation": "Resistance is directly proportional to blood viscosity (Poiseuille's law)."
    },
    {
        "id": 126,
        "question": "The maximum peak pressure measured in a systemic artery during a cardiac cycle is:",
        "options": [
            "A. Systolic pressure",
            "B. Diastolic pressure",
            "C. Pulse pressure",
            "D. Mean pressure",
            "E. Osmotic pressure"
        ],
        "answer": "A. Systolic pressure",
        "explanation": "Systolic pressure is peak arterial pressure during ventricular contraction."
    },
    {
        "id": 127,
        "question": "Which natriuretic hormone is synthesized and released primarily by ventricular cardiac myocytes?",
        "options": [
            "A. Aldosterone",
            "B. Myoglobin",
            "C. ANP",
            "D. BNP"
        ],
        "answer": "D. BNP",
        "explanation": "B-type Natriuretic Peptide (BNP) is released by ventricles in response to wall stretch."
    },
    {
        "id": 128,
        "question": "Which regional vascular bed does NOT exhibit robust intrinsic blood flow autoregulation?",
        "options": [
            "A. Renal",
            "B. Splanchnic",
            "C. Coronary",
            "D. Cerebral"
        ],
        "answer": "B. Splanchnic",
        "explanation": "Renal, cerebral, and coronary beds strongly autoregulate; splanchnic bed autoregulation is weak."
    },
    {
        "id": 129,
        "question": "In which phase of the ventricular action potential is membrane sodium permeability highest?",
        "options": [
            "A. Phase 0",
            "B. Phase 1",
            "C. Phase 2",
            "D. Phase 3",
            "E. Phase 4"
        ],
        "answer": "A. Phase 0",
        "explanation": "Phase 0 upstroke is caused by rapid opening of voltage-gated Na+ channels."
    },
    {
        "id": 130,
        "question": "The SA node acts as the dominant pacemaker because:",
        "options": [
            "A. It has the fastest intrinsic discharge rate",
            "B. Rich nerve supply",
            "C. Atrial location",
            "D. Unaffected by ANS",
            "E. None"
        ],
        "answer": "A. It has the fastest intrinsic discharge rate",
        "explanation": "SA node fires at ~60-100 bpm, overriding slower latent pacemakers."
    },
    {
        "id": 131,
        "question": "The P wave on a surface ECG corresponds to:",
        "options": [
            "A. Beginning of atrial contraction",
            "B. End of atrial contraction",
            "C. Start of ventricular contraction",
            "D. End of ventricular contraction",
            "E. None"
        ],
        "answer": "A. Beginning of atrial contraction",
        "explanation": "P wave represents atrial depolarization, triggering atrial contraction."
    },
    {
        "id": 132,
        "question": "The P wave is characteristically absent prior to which ECG abnormality?",
        "options": [
            "A. Atrial hypertrophy",
            "B. Ventricular extrasystole (PVC)",
            "C. Heart failure",
            "D. SVT",
            "E. None"
        ],
        "answer": "B. Ventricular extrasystole (PVC)",
        "explanation": "Ectopic ventricular impulses do not originate from SA node / atrial depolarization."
    },
    {
        "id": 133,
        "question": "The R wave of the QRS complex is primarily caused by:",
        "options": [
            "A. Diastole",
            "B. Low amplitude",
            "C. Inversion",
            "D. Short duration",
            "E. Depolarization of main ventricular myocardium"
        ],
        "answer": "E. Depolarization of main ventricular myocardium",
        "explanation": "R wave reflects electrical depolarization of the large main ventricular muscle mass."
    },
    {
        "id": 134,
        "question": "The time required for an impulse to travel from SA node through the AV node is represented by:",
        "options": [
            "A. QRS complex",
            "B. ST interval",
            "C. P-Q (PR) interval",
            "D. QRS-T interval",
            "E. PS complex"
        ],
        "answer": "C. P-Q (PR) interval",
        "explanation": "PR (PQ) interval measures SA-to-ventricle conduction time."
    },
    {
        "id": 135,
        "question": "Which cardiac tissue possesses the SLOWEST intrinsic pacemaker rhythmicity?",
        "options": [
            "A. SA node",
            "B. Sympathetic SA node",
            "C. AV node",
            "D. Purkinje fibers",
            "E. None"
        ],
        "answer": "D. Purkinje fibers",
        "explanation": "Purkinje fibers have the slowest intrinsic rate (~15-40 bpm)."
    },
    {
        "id": 136,
        "question": "Electrical action potential conduction velocity is FASTEST in which cardiac tissue?",
        "options": [
            "A. SA node",
            "B. Atrial muscle",
            "C. AV node",
            "D. Purkinje fibers",
            "E. Ventricular muscle"
        ],
        "answer": "D. Purkinje fibers",
        "explanation": "Purkinje fibers conduct action potentials at up to 4 m/s."
    },
    {
        "id": 137,
        "question": "The QRS complex on an ECG represents:",
        "options": [
            "A. Ventricular repolarization",
            "B. Ventricular depolarization",
            "C. Atrial depolarization",
            "D. Atrial repolarization",
            "E. Systole"
        ],
        "answer": "B. Ventricular depolarization",
        "explanation": "QRS complex reflects ventricular myocardial depolarization."
    },
    {
        "id": 138,
        "question": "Which vascular layer is present in ALL parts of the blood vascular system?",
        "options": [
            "A. Tunica media",
            "B. Tunica adventitia",
            "C. Endothelial cell layer",
            "D. Vasa vasorum",
            "E. Internal elastic lamina"
        ],
        "answer": "C. Endothelial cell layer",
        "explanation": "Endothelium lines every vessel from heart to capillaries."
    },
    {
        "id": 139,
        "question": "In atherosclerosis, which vessel layer undergoes maximum pathological thickening?",
        "options": [
            "A. Tunica intima",
            "B. Tunica media",
            "C. Adventitia",
            "D. Externa",
            "E. Subserosa"
        ],
        "answer": "A. Tunica intima",
        "explanation": "Atherosclerotic plaques thicken the tunica intima."
    },
    {
        "id": 140,
        "question": "Vascular smooth muscle cells in the tunica media are arranged predominantly:",
        "options": [
            "A. Longitudinally",
            "B. Circularly",
            "C. Obliquely",
            "D. Radially",
            "E. Irregularly"
        ],
        "answer": "B. Circularly",
        "explanation": "Tunica media smooth muscle is circularly arranged."
    },
    {
        "id": 141,
        "question": "Lymphatic vessels function primarily to:",
        "options": [
            "A. Perform immune surveillance",
            "B. Filter lymph",
            "C. Transport leaked fluids/proteins to CV system",
            "D. Gas exchange",
            "E. Block proteins"
        ],
        "answer": "C. Transport leaked fluids/proteins to CV system",
        "explanation": "Lymphatics return leaked interstitial fluid and proteins to blood."
    }
]

RENAL_QS = [
    {
        "id": 142,
        "question": "In a healthy adult at rest, what is the normal value for total Renal Blood Flow (RBF)?",
        "options": [
            "A. 500 mL/min",
            "B. 500 to 1000 mL/min",
            "C. 1000 mL/min",
            "D. 1000 to 1500 mL/min"
        ],
        "answer": "D. 1000 to 1500 mL/min",
        "explanation": "Normal renal blood flow is ~1000-1200 mL/min (~20-25% of cardiac output)."
    },
    {
        "id": 143,
        "question": "If mean arterial pressure (MAP) increases from 140 mmHg to 190 mmHg (exceeding the upper limit of autoregulation at 180 mmHg), Renal Blood Flow will:",
        "options": [
            "A. Decrease",
            "B. Increase",
            "C. Remain constant",
            "D. Increase then decrease"
        ],
        "answer": "B. Increase",
        "explanation": "Above the 180 mmHg autoregulatory ceiling, renal blood flow increases passively with pressure."
    },
    {
        "id": 144,
        "question": "If mean arterial pressure (MAP) drops from 130 mmHg to 65 mmHg (falling below the lower limit of autoregulation at 80 mmHg), Renal Blood Flow will:",
        "options": [
            "A. Decrease",
            "B. Increase",
            "C. Remain constant",
            "D. Increase then decrease"
        ],
        "answer": "A. Decrease",
        "explanation": "Below 80 mmHg, autoregulation fails and renal blood flow falls passively."
    }
]


# ------------------------------------------------------------------------------
# 6. MAIN QUIZ INTERFACE & CATEGORY RENDERER
# ------------------------------------------------------------------------------
student = st.session_state.verified_user

st.sidebar.markdown(f"👤 **Logged-in Student:**\n- **Name:** {student['name']}\n- **ID:** `{student['id']}`")

if st.sidebar.button("Log Out / Switch Student"):
    st.session_state.verified_user = None
    st.rerun()

st.title("🫁 MSPC 237: Respiratory & Cardiovascular Systems Question Bank")
st.caption("Comprehensive 144-Question Exam Bank grounded in Past Exam Questions & Assessment Trends.")

tab1, tab2, tab3 = st.tabs([
    "🫁 Respiratory System (75 Qs)", 
    "🫀 Cardiovascular System (66 Qs)", 
    "🧪 Renal & Hemodynamics (3 Qs)"
])

def render_question_list(questions, category_name, prefix):
    for idx, q in enumerate(questions):
        st.subheader(f"Q{q['id']}. {q['question']}")
        key = f"{prefix}_{q['id']}"
        
        user_choice = st.radio("Select your answer:", q["options"], key=key, index=None)
        
        if user_choice is not None:
            is_correct = (user_choice == q["answer"])
            
            if is_correct:
                st.success(f"Correct! 🎉\n\n**Explanation:** {q['explanation']}")
            else:
                st.error(f"Incorrect. Correct Answer: **{q['answer']}**\n\n**Explanation:** {q['explanation']}")
            
            if f"logged_{key}" not in st.session_state:
                log_response(
                    module_name="MSPC237",
                    category=category_name,
                    question_text=q["question"],
                    selected_option=user_choice,
                    correct_answer=q["answer"],
                    is_correct=is_correct
                )
                st.session_state[f"logged_{key}"] = True
        st.divider()

with tab1:
    st.header("🫁 Respiratory Physiology, Anatomy & Development (Qs 1–75)")
    render_question_list(RESP_QS, "Respiratory System", "resp")

with tab2:
    st.header("🫀 Cardiovascular Physiology, Histology & ECG (Qs 76–141)")
    render_question_list(CV_QS, "Cardiovascular System", "cv")

with tab3:
    st.header("🧪 Renal Blood Flow Autoregulation & Hemodynamics (Qs 142–144)")
    render_question_list(RENAL_QS, "Renal & Hemodynamics", "renal")

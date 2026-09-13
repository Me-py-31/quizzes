import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# ------------------------------------------------------------------------------
# 1. STREAMLIT CONFIG & GOOGLE SHEETS INITIALIZATION
# ------------------------------------------------------------------------------
st.set_page_config(page_title="MSPC236 Interactive Quiz & Tracker", layout="wide")

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
        # Reads from the tab named after the module (e.g. "MSPC236")
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

st.title("🎓 MSPC236: Gastrointestinal, Renal & Reproductive Systems")
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
                    module_name="MSPC236",
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
        "question": "A surgeon approaches the lesser sac (omental bursa) through the epiploic foramen (Foramen of Winslow). Which structure forms the ANTERIOR boundary of this foramen?",
        "options": ["A. Hepatoduodenal ligament (containing portal triad)", "B. Inferior Vena Cava", "C. Caudate lobe of liver", "D. First part of duodenum"],
        "answer": "A",
        "explanation": "The epiploic foramen is bounded anteriorly by the free edge of the lesser omentum (hepatoduodenal ligament) enclosing the portal vein, proper hepatic artery, and bile duct."
    },
    {
        "type": "Direct Question",
        "question": "Which histological mucosal feature distinguishes the Duodenum from all other segments of the small and large intestine?",
        "options": ["A. Submucosal Brunner's glands", "B. Peyer's patches", "C. Crypts of Lieberkühn", "D. Plicae circulares"],
        "answer": "A",
        "explanation": "Brunner's glands are alkaline-secreting compound tubular glands located uniquely within the DUODENAL submucosa."
    },
    {
        "type": "Exception Question",
        "question": "All of the following anatomical structures are classified as SECONDARILY RETROPERITONEAL EXCEPT:",
        "options": ["A. Head and body of pancreas", "B. Descending and ascending colon", "C. Duodenum (2nd, 3rd, 4th parts)", "D. Jejunum and Ileum"],
        "answer": "D",
        "explanation": "The jejunum and ileum are intraperitoneal organs suspended by a mobile mesentery."
    },
    {
        "type": "True or False",
        "question": "Statement: The cremasteric muscle and fascia are derived directly from the aponeurosis of the internal oblique abdominal muscle.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "As the spermatic cord pierces the internal oblique, it receives the cremasteric layer."
    },
    {
        "type": "Case Scenario",
        "question": "A 68-year-old male with chronic urinary hesitancy undergoes digital rectal examination. A hard, nodular mass is palpated in the POSTERIOR aspect of the prostate. Which anatomical zone is affected?",
        "options": ["A. Peripheral zone", "B. Transitional zone", "C. Central zone", "D. Anterior fibromuscular stroma"],
        "answer": "A",
        "explanation": "Prostatic adenocarcinoma arises predominantly in the Peripheral zone (~70%), accessible via digital rectal examination. Benign Prostatic Hyperplasia (BPH) arises in the Transitional zone."
    },
    {
        "type": "Direct Question",
        "question": "Which pelvic diaphragm muscle provides primary anatomical support for the pelvic organs, preventing uterine prolapse?",
        "options": ["A. Levator ani muscle", "B. Obturator internus", "C. Piriformis", "D. Transverse perineal muscle"],
        "answer": "A",
        "explanation": "The levator ani (puborectalis, pubococcygeus, iliococcygeus) forms the muscular pelvic floor supporting pelvic viscera."
    },
    {
        "type": "Exception Question",
        "question": "Contents of the spermatic cord include all of the following structures EXCEPT:",
        "options": ["A. Vas deferens", "B. Testicular artery", "C. Pampiniform venous plexus", "D. Body and tail of Epididymis"],
        "answer": "D",
        "explanation": "The epididymis lies attached directly to the posterior border of the testis inside the scrotum; it is not inside the spermatic cord."
    },
    {
        "type": "True or False",
        "question": "Statement: The Perisinusoidal Space of Disse separates sinusoidal endothelial cells from hepatocyte microvilli and contains vitamin A-storing Ito (stellate) cells.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "The Space of Disse is the primary site of metabolic exchange between hepatocytes and blood plasma, housing hepatic stellate cells."
    },
    {
        "type": "Case Scenario",
        "question": "A 2-year-old child presents with painless lower GI bleeding. Technetium-99m scan reveals ectopic gastric mucosa in a true diverticulum on the antimesenteric border of the ileum. What is the embryological origin of this lesion?",
        "options": ["A. Remnant of the Vitelline duct (Omphalomesenteric duct)", "B. Remnant of the Urachus", "C. Failure of midgut rotation", "D. Defective urorectal septum"],
        "answer": "A",
        "explanation": "Meckel's diverticulum is a congenital remnant of the vitelline duct located ~2 feet proximal to the ileocecal valve."
    },
    {
        "type": "Direct Question",
        "question": "Which specialized epithelial cells located at the base of crypts of Lieberkühn secrete antimicrobial lysozyme and alpha-defensins?",
        "options": ["A. Paneth cells", "B. Goblet cells", "C. Enterochromaffin cells", "D. Chief cells"],
        "answer": "A",
        "explanation": "Paneth cells contain eosinophilic apical granules packed with lysozyme and defensins for mucosal innate defense."
    },
    {
        "type": "Exception Question",
        "question": "All of the following renal structures derive from the Ureteric Bud EXCEPT:",
        "options": ["A. Ureter and Renal pelvis", "B. Major and Minor Calyces", "C. Collecting ducts", "D. Glomeruli and Proximal Convoluted Tubules"],
        "answer": "D",
        "explanation": "Glomeruli, Bowman's capsule, PCT, Loop of Henle, and DCT derive from the Metanephric Blastema (Metanephric cap)."
    },
    {
        "type": "True or False",
        "question": "Statement: Normal fetal kidneys present a lobulated external surface that gradually smooths out during childhood as nephrons mature.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Fetal kidneys consist of 12-14 distinct renal lobules; lobulation usually disappears during infancy."
    },
    {
        "type": "Case Scenario",
        "question": "An ultrasound on a 25-year-old female reveals fluid collection in the most inferior peritoneal recess of the female pelvis while standing. Name this peritoneal space.",
        "options": ["A. Rectouterine Pouch (Pouch of Douglas)", "B. Vesicouterine pouch", "C. Retropubic space of Retzius", "D. Paravesical fossa"],
        "answer": "A",
        "explanation": "The rectouterine pouch is the lowest peritoneal space in females, situated between the posterior rectum and anterior uterine wall."
    },
    {
        "type": "Direct Question",
        "question": "Which tooth tissue is synthesized continuously throughout life by odontoblasts lining the pulp cavity?",
        "options": ["A. Dentin", "B. Enamel", "C. Cementum", "D. Periodontal ligament"],
        "answer": "A",
        "explanation": "Odontoblasts derived from neural crest lay down primary, secondary, and tertiary dentin. Ameloblasts (enamel) are lost at eruption."
    },
    {
        "type": "Exception Question",
        "question": "All of the following statements regarding the histology of the liver parenchyma are TRUE EXCEPT:",
        "options": ["A. Classical lobule is centered around a Central Vein", "B. Portal lobule is centered around a Portal Triad", "C. Hepatic acinus zone 3 is closest to the hepatic artery and best oxygenated", "D. Kupffer cells are resident tissue macrophages in sinusoids"],
        "answer": "C",
        "explanation": "Acinar Zone 1 is closest to the portal triad and best oxygenated; Zone 3 surrounds the central vein and is most susceptible to ischemic injury."
    },
    {
        "type": "True or False",
        "question": "Statement: The periodontal ligament attaches tooth cementum directly to the surrounding alveolar bone.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "The periodontal ligament consists of dense collagenous Sharpey's fibers connecting cementum to alveolar bone."
    },
    {
        "type": "Case Scenario",
        "question": "A newborn infant presents with a herniated sac at the umbilicus covered by amnion and peritoneum. The umbilical cord inserts directly into the apex of the sac. What is the diagnosis?",
        "options": ["A. Omphalocele", "B. Gastroschisis", "C. Umbilical hernia", "D. Meckel's diverticulum"],
        "answer": "A",
        "explanation": "Omphalocele is failure of midgut abdominal return at week 10; organs are enclosed within a peritoneal/amniotic sac."
    },
    {
        "type": "Direct Question",
        "question": "Which vein lies within the main lobar fissure (Cantlie's line) dividing the liver into functional right and left lobes?",
        "options": ["A. Middle hepatic vein", "B. Right hepatic vein", "C. Portal vein main branch", "D. Left hepatic vein"],
        "answer": "A",
        "explanation": "Cantlie's line runs from the IVC to the gallbladder fossa; the middle hepatic vein travels in this plane."
    },
    {
        "type": "Exception Question",
        "question": "All of the following congenital anomalies result from abnormal urorectal septum partitioning of the cloaca EXCEPT:",
        "options": ["A. Rectovaginal fistula", "B. Imperforate anus", "C. Rectourethral fistula", "D. Congenital megacolon (Hirschsprung disease)"],
        "answer": "D",
        "explanation": "Hirschsprung disease is caused by failure of neural crest cell migration into the myenteric plexus, not cloacal septation."
    },
    {
        "type": "True or False",
        "question": "Statement: Anteversion refers to the forward angling of the uterine body relative to the vagina at the external os.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Anteversion is the anterior angle between cervix and vagina (~90°); anteflexion is the forward bend between uterine body and cervix (~170°)."
    },
    {
        "type": "Case Scenario",
        "question": "A 70-year-old male with chronic urinary retention due to BPH presents with urine leaking from his umbilicus. What patent embryological remnant is present?",
        "options": ["A. Urachal fistula", "B. Vitelline fistula", "C. Omphalocele", "D. Patent processus vaginalis"],
        "answer": "A",
        "explanation": "Complete failure of allantois/urachus lumen obliteration results in a urachal fistula connecting the bladder dome to the umbilicus."
    },
    {
        "type": "Direct Question",
        "question": "Which salivary gland is a pure serous acinar gland possessing numerous centroacinar-like intercalated ducts?",
        "options": ["A. Parotid gland", "B. Submandibular gland", "C. Sublingual gland", "D. Von Ebner's minor glands"],
        "answer": "A",
        "explanation": "The parotid is entirely serous, producing watery amylase-rich saliva; submandibular is mixed; sublingual is predominantly mucous."
    },
    {
        "type": "Exception Question",
        "question": "All of the following features distinguish the Large Intestine from the Small Intestine EXCEPT:",
        "options": ["A. Taeniae coli", "B. Haustra (sacculations)", "C. Appendices epiploicae", "D. Continuous layer of villi across mucosa"],
        "answer": "D",
        "explanation": "Mucosal villi are present ONLY in the small intestine to maximize absorption; the colon lacks villi."
    },
    {
        "type": "True or False",
        "question": "Statement: The Blood-Testis Barrier is established by tight junctions (zonula occludentes) between adjacent Sertoli cells near the basal lamina.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Sertoli cell tight junctions divide the seminiferous epithelium into basal and adluminal compartments, preventing autoimmune destruction of haploid germ cells."
    },
    {
        "type": "Direct Question",
        "question": "Which embryonic germ layer gives rise to the ureters, kidneys, and internal reproductive ducts?",
        "options": ["A. Intermediate mesoderm", "B. Paraxial mesoderm", "C. Lateral plate mesoderm", "D. Endoderm"],
        "answer": "A",
        "explanation": "Intermediate mesoderm forms the urogenital ridge, generating pronephros, mesonephros, metanephros, and gonads."
    }
]

# Tab 2 Questions (25 MCQs)
q_tab2 = [
    {
        "type": "Case Scenario",
        "question": "A 70-kg healthy adult male has an estimated Total Body Water (TBW) of 42 L. What is his expected Extracellular Fluid (ECF) volume?",
        "options": ["A. 14 L", "B. 28 L", "C. 7 L", "D. 21 L"],
        "answer": "A",
        "explanation": "Rule of 60-40-20: TBW is 60% of body weight (42L), ICF is 40% (28L), and ECF is 20% (14L)."
    },
    {
        "type": "Direct Question",
        "question": "Which marker dye is used to measure Total Body Water (TBW) using the dilution principle?",
        "options": ["A. Heavy water (Deuterium oxide D2O or Tritiated water)", "B. Inulin", "C. Mannitol", "D. Evans Blue dye"],
        "answer": "A",
        "explanation": "D2O distributes freely across all fluid compartments. Inulin/Mannitol measure ECF; Evans Blue / Radioiodinated albumin measure Plasma Volume."
    },
    {
        "type": "Exception Question",
        "question": "Antidiuretic Hormone (ADH / Vasopressin) release from the posterior pituitary is stimulated by all of the following EXCEPT:",
        "options": ["A. Increased plasma osmolality sensed by hypothalamic osmoreceptors", "B. Hypovolemia / decreased effective circulating arterial volume", "C. Angiotensin II", "D. Increased Atrial Natriuretic Peptide (ANP) release"],
        "answer": "D",
        "explanation": "ANP signals hypervolemia and INHIBITS ADH release, promoting renal water and sodium excretion."
    },
    {
        "type": "True or False",
        "question": "Statement: ADH increases renal water reabsorption by inducing exocytosis and apical insertion of Aquaporin-2 channels in collecting duct principal cells via V2 receptors.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "V2 receptors act via cAMP/PKA to insert Aquaporin-2 water channels into the apical membrane of principal cells."
    },
    {
        "type": "Case Scenario",
        "question": "A patient with chronic essential hypertension undergoes renal function testing. His renal blood flow remains constant (~1000 mL/min) over mean arterial pressures between 90 and 180 mmHg. What effect does chronic hypertension have on the autoregulatory curve?",
        "options": ["A. Shifts the autoregulatory curve to the RIGHT", "B. Shifts the autoregulatory curve to the LEFT", "C. Shifts the curve DOWNWARD", "D. Causes complete loss of autoregulation"],
        "answer": "A",
        "explanation": "Arterial hypertrophic remodeling in chronic hypertension shifts the autoregulatory pressure plateau to higher pressure ranges (rightward shift)."
    },
    {
        "type": "Direct Question",
        "question": "Which luminal tubular structure acts as the sensor for sodium chloride (NaCl) concentration in Tubuloglomerular Feedback (TGF)?",
        "options": ["A. Macula densa of the juxtaglomerular apparatus", "B. Podocyte foot processes", "C. Granular juxtaglomerular cells", "D. Principal cells"],
        "answer": "A",
        "explanation": "Macula densa cells in the thick ascending limb sense increased NKCC2 NaCl load, releasing adenosine to constrict afferent arterioles."
    },
    {
        "type": "Exception Question",
        "question": "All of the following endocrine functions are performed directly by kidney tissue EXCEPT:",
        "options": ["A. Renin synthesis by juxtaglomerular granular cells", "B. Erythropoietin synthesis by cortical interstitial cells", "C. Final 1-alpha-hydroxylation of Vitamin D to Calcitriol in PCT", "D. Aldosterone synthesis"],
        "answer": "D",
        "explanation": "Aldosterone is synthesized and secreted by the Zona Glomerulosa of the adrenal cortex."
    },
    {
        "type": "True or False",
        "question": "Statement: Selective dilation of the renal afferent arteriole increases Glomerular Filtration Rate (GFR) and Glomerular Hydrostatic Pressure.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Afferent dilation increases hydraulic pressure inside glomerular capillaries, driving ultrafiltration."
    },
    {
        "type": "Case Scenario",
        "question": "A patient presenting with severe polyuria undergoes a 12-hour water deprivation test. Plasma osmolality rises, but urine remains dilute (100 mOsm/kg). Administering desmopressin (synthetic ADH) increases urine osmolality to 600 mOsm/kg. What is the diagnosis?",
        "options": ["A. Central (Neurogenic) Diabetes Insipidus", "B. Nephrogenic Diabetes Insipidus", "C. Psychogenic Polydipsia", "D. Primary Hyperaldosteronism"],
        "answer": "A",
        "explanation": "Central DI is caused by pituitary ADH deficiency; kidneys respond normally when exogenous desmopressin is supplied."
    },
    {
        "type": "Direct Question",
        "question": "Which GI gastrointestinal hormone is secreted by S-cells in the duodenal mucosa in response to luminal H+ (acid) to stimulate pancreatic bicarbonate release?",
        "options": ["A. Secretin", "B. Cholecystokinin (CCK)", "C. Gastrin", "D. Motilin"],
        "answer": "A",
        "explanation": "Secretin is nature's antacid; acid in the duodenum triggers secretin, activating ductal cAMP to secrete HCO3-."
    },
    {
        "type": "Exception Question",
        "question": "All of the following actions are triggered by Cholecystokinin (CCK) EXCEPT:",
        "options": ["A. Gallbladder smooth muscle contraction", "B. Relaxation of the Sphincter of Oddi", "C. Pancreatic acinar enzyme secretion", "D. Stimulation of gastric emptying"],
        "answer": "D",
        "explanation": "CCK INHIBITS gastric emptying (delays emptying) to allow adequate time for intestinal fat and protein digestion."
    },
    {
        "type": "True or False",
        "question": "Statement: Motilin is secreted by enteroendocrine M-cells during fasting to initiate the Migrating Motor Complex (MMC) every 90-120 minutes.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "The MMC ('interdigestive housekeeper') clears undigested residue from stomach and small gut during fasting under motilin control."
    },
    {
        "type": "Case Scenario",
        "question": "A 35-year-old patient with a gastrinoma (Zollinger-Ellison syndrome) develops multiple recalcitrant peptic ulcers. Excess gastrin acts on Enterochromaffin-like (ECL) cells to stimulate release of which potent acid secretagogue?",
        "options": ["A. Histamine", "B. Acetylcholine", "C. Somatostatin", "D. Prostaglandin E2"],
        "answer": "A",
        "explanation": "Gastrin binds CCK-B receptors on ECL cells, releasing histamine which acts on parietal H2 receptors to activate H+/K+ ATPase."
    },
    {
        "type": "Direct Question",
        "question": "Which intrinsic gastric secretory protein bound to vitamin B12 in the duodenum enables its receptor-mediated endocytosis in the terminal ileum?",
        "options": ["A. Intrinsic Factor (IF)", "B. Haptocorrin (R-binder)", "C. Transcobalamin II", "D. Pepsinogen"],
        "answer": "A",
        "explanation": "Intrinsic factor is secreted by parietal cells; the IF-B12 complex binds cubam receptors in the distal ileum."
    },
    {
        "type": "Exception Question",
        "question": "All of the following hormones inhibit gastric parietal cell H+ acid secretion EXCEPT:",
        "options": ["A. Somatostatin", "B. Prostaglandin E2", "C. Secretin", "D. Gastrin"],
        "answer": "D",
        "explanation": "Gastrin is a primary secretagogue that STIMULATES gastric acid secretion."
    },
    {
        "type": "True or False",
        "question": "Statement: The preovulatory Luteinizing Hormone (LH) surge triggers completion of Meiosis I in the primary oocyte, converting it to a secondary oocyte arrested in Metaphase II.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "The LH surge breaks meiotic arrest in prophase I; the secondary oocyte arrests in metaphase II until fertilization."
    },
    {
        "type": "Case Scenario",
        "question": "In the two-cell two-gonadotropin model of ovarian steroidogenesis, which pituitary gonadotropin acts on THICA cells to drive androgen synthesis?",
        "options": ["A. Luteinizing Hormone (LH)", "B. Follicle-Stimulating Hormone (FSH)", "C. Prolactin", "D. Human Chorionic Gonadotropin (hCG)"],
        "answer": "A",
        "explanation": "LH stimulates theca internal cells to produce androstenedione/testosterone; FSH stimulates granulosa cell aromatase to convert them to estrogens."
    },
    {
        "type": "Direct Question",
        "question": "Which hormone produced by syncytiotrophoblasts maintains the maternal corpus luteum during the first 8-10 weeks of pregnancy?",
        "options": ["A. Human Chorionic Gonadotropin (hCG)", "B. Human Placental Lactogen (hPL)", "C. Progesterone", "D. Prolactin"],
        "answer": "A",
        "explanation": "hCG rescues the corpus luteum from regression, maintaining progesterone production until the placenta takes over."
    },
    {
        "type": "Exception Question",
        "question": "Sertoli cells perform all of the following physiological functions in the testes EXCEPT:",
        "options": ["A. Establish the Blood-Testis Barrier", "B. Synthesize Androgen-Binding Protein (ABP) and Inhibin-B under FSH stimulation", "C. Phagocytize residual bodies during spermiation", "D. Synthesize and secrete testosterone"],
        "answer": "D",
        "explanation": "Leydig cells (interstitial cells) synthesize and secrete testosterone under LH stimulation, NOT Sertoli cells."
    },
    {
        "type": "True or False",
        "question": "Statement: Primary hyperaldosteronism (Conn syndrome) leads to ECF volume expansion, hypertension, hypokalemia, and metabolic alkalosis with LOW plasma renin.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Excess aldosterone increases distal Na+ reabsorption and H+/K+ secretion; ECF expansion suppresses renal renin release."
    },
    {
        "type": "Case Scenario",
        "question": "A 55-year-old male with chronic liver cirrhosis exhibits marked peripheral edema, ascites, and low urinary sodium. Why are his kidneys avidly reabsorbing sodium despite fluid overload?",
        "options": ["A. Splanchnic vasodilation reduces effective arterial blood volume, activating RAAS", "B. Primary renal tubular injury", "C. Excessive ANP secretion", "D. Hypoaldosteronism"],
        "answer": "A",
        "explanation": "Cirrhosis causes portal hypertension and splanchnic arterial vasodilation, dropping effective circulating volume and triggering maximal RAAS."
    },
    {
        "type": "Direct Question",
        "question": "What is the physiological function of the Gastrocolic Reflex?",
        "options": ["A. Increase colonic mass movements following food entry into the stomach", "B. Inhibit gastric motility when food enters the duodenum", "C. Contract the lower esophageal sphincter", "D. Inhibit defecation during sleep"],
        "answer": "A",
        "explanation": "Gastric distension triggers parasympathetic and hormonal signals that stimulate colonic motility and urge to defecate."
    },
    {
        "type": "Exception Question",
        "question": "Primary driving Starling forces that favor Glomerular Ultrafiltration include:",
        "options": ["A. Glomerular capillary hydrostatic pressure (Pgc)", "B. Bowman's space oncotic pressure (usually near 0)", "C. Bowman's space hydrostatic pressure (Pbs - opposes filtration)", "D. Glomerular capillary oncotic pressure (Pgc - opposes filtration)"],
        "answer": "A",
        "explanation": "Glomerular capillary hydrostatic pressure (~45-50 mmHg) is the dominant force FAVORING filtration."
    },
    {
        "type": "True or False",
        "question": "Statement: Type A Intercalated cells in the collecting duct secrete H+ ions via an apical H+-ATPase and reabsorb HCO3- via a basolateral Cl-/HCO3- exchanger.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Type A intercalated cells remediate metabolic acidosis by extruding H+ into urine and returning new HCO3- to blood."
    },
    {
        "type": "Direct Question",
        "question": "Which enzyme synthesized by ductal epithelial cells of the pancreas converts inactive Trypsinogen to active Trypsin in the intestinal lumen?",
        "options": ["A. Enteropeptidase (Enterokinase)", "B. Pepsin", "C. Carboxypeptidase", "D. Chymotrypsin"],
        "answer": "A",
        "explanation": "Enteropeptidase bound to duodenal brush border cleaves trypsinogen; trypsin then autocatalytically activates all zymogens."
    }
]

# Tab 3 Questions (25 MCQs)
q_tab3 = [
    {
        "type": "Case Scenario",
        "question": "An oral rehydration solution (ORS) containing glucose and NaCl is administered to a child with severe cholera diarrhea. What is the biochemical basis for using glucose in ORS?",
        "options": ["A. Intestinal Na+/Glucose cotransporter (SGLT-1) remains intact, driving Na+ and water absorption", "B. Glucose directly kills Vibrio cholerae bacteria", "C. Glucose inhibits cAMP production in enterocytes", "D. SGLT-1 is an active proton pump"],
        "answer": "A",
        "explanation": "Cholera toxin elevates intracellular cAMP, opening CFTR chloride channels. SGLT-1 is uninhibited by cAMP; luminal Na+ and glucose co-transport pulls water back into blood."
    },
    {
        "type": "Direct Question",
        "question": "Which apical membrane transporter mediates the sodium-independent, facilitated diffusion of Fructose into enterocytes?",
        "options": ["A. GLUT-5", "B. SGLT-1", "C. GLUT-2", "D. GLUT-4"],
        "answer": "A",
        "explanation": "Fructose is absorbed across the apical enterocyte membrane exclusively via GLUT-5 facilitated diffusion."
    },
    {
        "type": "Exception Question",
        "question": "Digestion and absorption of dietary triacylglycerols require all of the following biochemical components EXCEPT:",
        "options": ["A. Conjugated bile salts for micellar solubilization", "B. Pancreatic lipase and Colipase", "C. Re-esterification to TAG inside enterocytes and Chylomicron packaging", "D. Direct absorption of long-chain fatty acids into portal vein blood"],
        "answer": "D",
        "explanation": "Long-chain fatty acids are re-esterified into TAGs inside enterocytes and exported via lymphatics as Chylomicrons (only short/medium chain fatty acids enter portal blood)."
    },
    {
        "type": "True or False",
        "question": "Statement: Gastric Parietal cell proton pumps (H+/K+ ATPase) exchange intracellular H+ for luminal K+ against a million-fold concentration gradient.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "The apical H+/K+ ATPase is a primary active transport pump powered by ATP hydrolysis."
    },
    {
        "type": "Case Scenario",
        "question": "A patient with severe acute pancreatitis develops hypocalcemia, severe abdominal pain, and elevated serum amylase/lipase. What biochemical process causes local tissue necrosis and saponification?",
        "options": ["A. Premature intra-pancreatic activation of zymogens (trypsinogen) causing autodigestion", "B. Excessive secretin secretion", "C. Inhibition of pancreatic lipase", "D. Bacterial infection of pancreatic acini"],
        "answer": "A",
        "explanation": "Disrupted acinar packaging allows cathepsin B to activate trypsinogen inside acini, initiating a destructive cascade of autodigestion."
    },
    {
        "type": "Direct Question",
        "question": "Which enzyme converts indirect (unconjugated) hydrophobic bilirubin into water-soluble direct (conjugated) bilirubin inside hepatocytes?",
        "options": ["A. UDP-Glucuronosyltransferase (UGT1A1)", "B. Biliverdin reductase", "C. Heme oxygenase", "D. Beta-glucuronidase"],
        "answer": "A",
        "explanation": "UGT1A1 attaches two glucuronic acid molecules to bilirubin, forming bilirubin diglucuronide (conjugated bilirubin)."
    },
    {
        "type": "Exception Question",
        "question": "All of the following factors stimulate gastric parietal cell proton pumps EXCEPT:",
        "options": ["A. Gastrin binding to CCK-B receptors", "B. Histamine binding to H2 receptors (cAMP pathway)", "C. Acetylcholine binding to M3 receptors (IP3/Ca2+ pathway)", "D. Somatostatin binding to SST2 receptors"],
        "answer": "D",
        "explanation": "Somatostatin inhibits parietal cells directly and indirectly by blocking ECL histamine and G-cell gastrin release."
    },
    {
        "type": "True or False",
        "question": "Statement: Long-term NSAID use inhibits mucosal Cyclooxygenase-1 (COX-1), decreasing PGE2 and PGI2 synthesis and compromising gastric bicarbonate/mucus protection.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Prostaglandins stimulate gastric surface mucous cells to secrete protective mucus and bicarbonate; COX-1 blockade causes gastric ulceration."
    },
    {
        "type": "Case Scenario",
        "question": "A patient presents with bulky, foul-smelling, pale stools that float (steatorrhea). Laboratory evaluation shows fat malabsorption. Which enzyme deficiency or ductal obstruction is responsible?",
        "options": ["A. Pancreatic lipase / Bile duct obstruction", "B. Salivary amylase deficiency", "C. Pepsin deficiency", "D. Lactase deficiency"],
        "answer": "A",
        "explanation": "Pancreatic lipase and bile salts are essential for lipid hydrolysis and micellar solubilization; their lack produces steatorrhea."
    },
    {
        "type": "Direct Question",
        "question": "Which enterocyte basolateral membrane transporter transports Glucose, Galactose, and Fructose into interstitial blood capillaries?",
        "options": ["A. GLUT-2", "B. GLUT-1", "C. SGLT-1", "D. GLUT-4"],
        "answer": "A",
        "explanation": "GLUT-2 is a high-capacity, low-affinity facilitated transporter located on the basolateral membrane of enterocytes and hepatocytes."
    },
    {
        "type": "Exception Question",
        "question": "Primary constituents of normal hepatic bile include all of the following EXCEPT:",
        "options": ["A. Bile salts (cholic and chenodeoxycholic acids)", "B. Phospholipids (Lecithin)", "C. Cholesterol and Bilirubin", "D. High concentrations of active trypsin"],
        "answer": "D",
        "explanation": "Trypsin is a pancreatic protease, NOT a component of hepatic bile."
    },
    {
        "type": "True or False",
        "question": "Statement: Bacterial enzymes in the colon convert conjugated bilirubin into urobilinogen, portion of which is reabsorbed via the enterohepatic circulation.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Colonic bacteria deconjugate bilirubin to urobilinogen; ~20% is reabsorbed and recirculated to liver/kidneys, and the rest forms stercobilin."
    },
    {
        "type": "Case Scenario",
        "question": "A patient with chronic renal failure exhibits severe metabolic acidosis with a low serum bicarbonate. What is the primary biochemical defect in renal acid-base management?",
        "options": ["A. Impaired renal tubular ammoniagenesis and H+ excretion", "B. Excessive renal HCO3- secretion", "C. Accelerated carbonic anhydrase activity", "D. Hyperaldosteronism"],
        "answer": "A",
        "explanation": "Diseased nephrons cannot perform glutamine catabolism (ammoniagenesis) or extrude H+ ions, failing to regenerate HCO3-."
    },
    {
        "type": "Direct Question",
        "question": "Which amino acid is extracted from circulation by proximal convoluted tubule cells as the primary substrate for renal ammoniagenesis (NH4+ production)?",
        "options": ["A. Glutamine", "B. Alanine", "C. Glycine", "D. Aspartate"],
        "answer": "A",
        "explanation": "Renal glutaminase converts glutamine -> glutamate + NH4+; glutamate dehydrogenase then yields alpha-ketoglutarate + NH4+, generating 2 new HCO3- ions."
    },
    {
        "type": "Exception Question",
        "question": "All of the following brush border disaccharidases hydrolyze dietary disaccharides at the enterocyte surface EXCEPT:",
        "options": ["A. Lactase", "B. Sucrase", "C. Maltase", "D. Alpha-amylase"],
        "answer": "D",
        "explanation": "Alpha-amylase is a luminal endosaccharidase secreted by salivary and pancreatic glands, NOT an enterocyte brush border enzyme."
    },
    {
        "type": "True or False",
        "question": "Statement: Omeprazole inhibits gastric acid secretion by irreversibly binding to and inactivating the parietal cell H+/K+ ATPase (proton pump).",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "PPIs are prodrugs converted in acidic parietal canaliculi to active sulfenamides that form covalent disulfide bonds with the proton pump."
    },
    {
        "type": "Case Scenario",
        "question": "An adult experiences abdominal pain, bloating, and explosive diarrhea after consuming ice cream. Hydrogen breath test is positive. What enzyme activity is deficient?",
        "options": ["A. Brush border Lactase (Lactase-phlorizin hydrolase)", "B. Pancreatic lipase", "C. Sucrase-isomaltase", "D. Intestinal enteropeptidase"],
        "answer": "A",
        "explanation": "Lactase deficiency prevents lactose breakdown; unabsorbed lactose causes osmotic diarrhea and bacterial fermentation to H2 gas."
    },
    {
        "type": "Direct Question",
        "question": "Which intracellular secondary messenger cascade is activated when Histamine binds to H2 receptors on parietal cells?",
        "options": ["A. Adenylate cyclase activation -> elevated cAMP -> PKA activation", "B. Phospholipase C activation -> elevated IP3/DAG -> PKC activation", "C. Inhibition of cGMP", "D. Direct opening of ligand-gated chloride channels"],
        "answer": "A",
        "explanation": "H2 receptors are Gs-coupled, stimulating adenylate cyclase to increase cAMP, which translocationally inserts H+/K+ ATPases."
    },
    {
        "type": "Exception Question",
        "question": "All of the following components are present in chylomicrons exported into mesenteric lymphatics EXCEPT:",
        "options": ["A. Apolipoprotein B-48", "B. Re-synthesized Triacylglycerols", "C. Cholesteryl esters and fat-soluble vitamins", "D. Apolipoprotein B-100"],
        "answer": "D",
        "explanation": "ApoB-100 is synthesized exclusively by the LIVER on VLDL; enterocytes synthesize the truncated ApoB-48 for chylomicrons."
    },
    {
        "type": "True or False",
        "question": "Statement: Salivary mucous secretions contain high concentrations of mucin glycoproteins that lubricate food boluses for deglutition.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Mucins are heavily O-glycosylated proteins that trap water, providing high viscosity and lubrication."
    },
    {
        "type": "Case Scenario",
        "question": "A patient presents with acute intestinal colic, severe diarrhea, and flushing. Diagnosis confirms a carcinoid tumor of the ileum. Which vasoactive amine metabolite is elevated in urine?",
        "options": ["A. 5-HIAA (5-hydroxyindoleacetic acid)", "B. VMA (Vanillylmandelic acid)", "C. Homovanillic acid", "D. Histamine"],
        "answer": "A",
        "explanation": "Carcinoid tumors hypersecrete serotonin (5-HT), which is oxidized by MAO into 5-HIAA and excreted in urine."
    },
    {
        "type": "Direct Question",
        "question": "Which enzyme converts trypsinogen into active trypsin within the pancreatic duct to cause hereditary pancreatitis when mutated?",
        "options": ["A. Mutated Trypsin (loss of autolytic cleavage site)", "B. Enteropeptidase", "C. Chymotrypsin", "D. Elastase"],
        "answer": "A",
        "explanation": "PRSS1 mutations impair trypsin autolysis (self-destruction), allowing resistant trypsin to prematurely activate pancreatic digestive zymogens."
    },
    {
        "type": "Exception Question",
        "question": "Which of the following electrolyte transport mechanisms occurs in the Thick Ascending Limb (TAL) of Henle's Loop?",
        "options": ["A. Apical NKCC2 cotransporter (Na+/K+/2Cl-)", "B. Apical ROMK potassium channel back-leak", "C. Paracellular reabsorption of Ca2+ and Mg2+ driven by lumen-positive potential", "D. Apical SGLT-2 sodium-glucose cotransporter"],
        "answer": "D",
        "explanation": "SGLT-2 is located in the Early Proximal Convoluted Tubule, NOT in the Loop of Henle."
    },
    {
        "type": "True or False",
        "question": "Statement: Aldosterone stimulates luminal ENaC sodium channel insertion and apical K+ secretion in Principal cells of the late DCT and collecting duct.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Aldosterone binds intracellular mineralocorticoid receptors, upregulating ENaC channels and apical ROMK potassium channels."
    },
    {
        "type": "Direct Question",
        "question": "Which bile acid is a primary bile acid synthesized directly from cholesterol in hepatocytes?",
        "options": ["A. Cholic acid (and Chenodeoxycholic acid)", "B. Deoxycholic acid", "C. Lithocholic acid", "D. Ursodeoxycholic acid"],
        "answer": "A",
        "explanation": "Cholic acid and Chenodeoxycholic acid are primary bile acids synthesized by hepatocytes; intestinal bacteria dehydroxylate them into secondary bile acids (Deoxycholic/Lithocholic)."
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

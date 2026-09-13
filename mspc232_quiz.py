import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# ------------------------------------------------------------------------------
# 1. STREAMLIT CONFIG & GOOGLE SHEETS INITIALIZATION
# ------------------------------------------------------------------------------
st.set_page_config(page_title="MSPC232 Interactive Quiz & Tracker", layout="wide")

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
        # Reads from the tab named after the module (e.g. "MSPC232")
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

st.title("🎓 MSPC232: Medical Biochemistry & Bioenergetics")
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
                    module_name="MSPC232",
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
        "question": "A 34-year-old woman presents with multiple stress fractures. Investigations reveal a long-standing history of a severely low-calcium diet. Which structural component of bone tissue is primarily compromised?",
        "options": ["A. Osteoid (collagen matrix)", "B. Hydroxyapatite crystals", "C. Osteocytes", "D. Bone marrow"],
        "answer": "B",
        "explanation": "Hydroxyapatite crystals provide the inorganic mineral strength of bone. Chronic calcium deficiency impairs hydroxyapatite crystallization, leaving osteoid unmineralized."
    },
    {
        "type": "Case Scenario",
        "question": "A 5-year-old boy in a rural clinic weighs 11 kg (predicted 20 kg) with severe skeletal muscle wasting, loss of subcutaneous fat, and 'matchstick' limbs, but NO edema or abdominal distension. What is the diagnosis?",
        "options": ["A. Kwashiorkor", "B. Marasmus", "C. Scurvy", "D. Pellagra"],
        "answer": "B",
        "explanation": "Marasmus results from severe calorie and protein deficiency leading to loss of subcutaneous fat and severe muscle wasting without hepatic fatty change or edema."
    },
    {
        "type": "Exception Question",
        "question": "Characteristics of Kwashiorkor include all of the following EXCEPT:",
        "options": ["A. Generalized edema", "B. Fatty liver infiltration", "C. Complete loss of subcutaneous fat", "D. Subcutaneous fat retention with growth impairment"],
        "answer": "C",
        "explanation": "Kwashiorkor patients retain some subcutaneous fat but develop marked edema (hypoalbuminemia) and fatty liver due to impaired VLDL synthesis."
    },
    {
        "type": "Direct Question",
        "question": "Which amino acid hydroxyl residues form O-glycosidic linkages with carbohydrate moieties during glycoprotein synthesis?",
        "options": ["A. Serine and Threonine", "B. Glutamine and Asparagine", "C. Lysine and Arginine", "D. Alanine and Valine"],
        "answer": "A",
        "explanation": "Serine and Threonine contain side-chain hydroxyl groups (-OH) that form O-glycosidic linkages, whereas Asparagine forms N-glycosidic bonds."
    },
    {
        "type": "Direct Question",
        "question": "In rod photoreceptor cells, visual phototransduction involves which conversion during light exposure?",
        "options": ["A. All-trans-retinal to 11-cis-retinal", "B. 11-cis-retinal to all-trans-retinal", "C. Retinol to retinoic acid", "D. Opsin to rhodopsin synthesis"],
        "answer": "B",
        "explanation": "Absorption of a photon by rhodopsin isomerizes 11-cis-retinal to all-trans-retinal, activating transducin."
    },
    {
        "type": "True or False",
        "question": "Statement: Saturated fatty acids dominate cell membranes of organisms adapted to high environmental temperatures to prevent excessive membrane fluidity.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Saturated fatty acids lack double bonds, allowing tight packing which stabilizes the cell membrane against thermal hyper-fluidity."
    },
    {
        "type": "Direct Question",
        "question": "Which four-carbon monosaccharide is classified as a tetraketose?",
        "options": ["A. Erythrulose", "B. Erythrose", "C. Fructose", "D. Ribulose"],
        "answer": "A",
        "explanation": "Erythrulose is a 4-carbon ketose (tetraketose). Erythrose is an aldotetrose."
    },
    {
        "type": "Case Scenario",
        "question": "A premature infant delivered at 28 weeks gestation exhibits severe respiratory distress syndrome (RDS). Which phospholipid component of pulmonary surfactant is deficient?",
        "options": ["A. Dipalmitoylphosphatidylcholine (Lecithin)", "B. Sphingomyelin", "C. Phosphatidylglycerol", "D. Phosphatidylinositol"],
        "answer": "A",
        "explanation": "Dipalmitoylphosphatidylcholine reduces alveolar surface tension; its lack causes alveolar collapse in premature infants."
    },
    {
        "type": "Exception Question",
        "question": "All of the following lipid classes contain fatty acid components EXCEPT:",
        "options": ["A. Cholesteryl esters", "B. Sphingolipids", "C. Phospholipids", "D. None of the above (All contain fatty acids)"],
        "answer": "D",
        "explanation": "Cholesteryl esters, sphingolipids, and phospholipids all possess fatty acid chains esterified or amidated to their backbones."
    },
    {
        "type": "Direct Question",
        "question": "Which liver-derived lipoprotein contains the highest proportion of triacylglycerols and possesses ApoB-100?",
        "options": ["A. VLDL", "B. Chylomicron", "C. LDL", "D. HDL"],
        "answer": "A",
        "explanation": "VLDL is synthesized in hepatocytes with ApoB-100 and carries endogenous triacylglycerols."
    },
    {
        "type": "True or False",
        "question": "Statement: Cis-unsaturated fatty acids introduce rigid bends in hydrocarbon chains, lowering the melting point of plant oils compared to animal fats.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Cis double bonds introduce kinks that prevent tight packing, keeping unsaturated oils liquid at room temperature."
    },
    {
        "type": "Case Scenario",
        "question": "A newborn infant presents with severe chylomicronemia and lipemic serum. Genetic testing confirms Lipoprotein Lipase (LPL) deficiency. Which apolipoprotein cofactor is required for LPL activity?",
        "options": ["A. Apo C-II", "B. Apo B-48", "C. Apo E", "D. Apo A-I"],
        "answer": "A",
        "explanation": "Apo C-II is the essential obligate cofactor present on chylomicrons and VLDL that activates capillary endothelial LPL."
    },
    {
        "type": "Exception Question",
        "question": "All of the following metabolites are directly derived from Tryptophan EXCEPT:",
        "options": ["A. Serotonin", "B. Melatonin", "C. Niacin (Nicotinic acid)", "D. Alpha-ketoglutarate"],
        "answer": "D",
        "explanation": "Tryptophan degrades to alanine, acetoacetyl-CoA, formate, niacin, and serotonin. Alpha-ketoglutarate is derived from glutamate, arginine, proline, and histidine."
    },
    {
        "type": "Direct Question",
        "question": "Which central intermediate serves as the common precursor for the synthesis of both triacylglycerols and glycerophospholipids?",
        "options": ["A. Phosphatidic acid", "B. Diacylglycerol", "C. CDP-choline", "D. Glycerol-3-phosphate dehydrogenase"],
        "answer": "A",
        "explanation": "Phosphatidic acid is dephosphorylated to DAG (for TAGs) or converted to CDP-DAG (for phospholipids)."
    },
    {
        "type": "True or False",
        "question": "Statement: Serum ferritin is the most sensitive laboratory index for assessing early depletion of total body iron stores.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Serum ferritin correlates directly with reticuloendothelial storage iron; low levels indicate depleted iron stores."
    },
    {
        "type": "Case Scenario",
        "question": "A 52-year-old asthmatic patient takes an over-the-counter NSAID for knee arthritis and suffers severe bronchospasm. Which inflammatory mediators are elevated due to cyclooxygenase inhibition?",
        "options": ["A. Leukotrienes (LTC4, LTD4, LTE4)", "B. Thromboxane A2", "C. Prostaglandin E2", "D. Prostacyclin PGI2"],
        "answer": "A",
        "explanation": "NSAIDs block COX, shunting arachidonic acid into the 5-lipoxygenase pathway and elevating bronchoconstrictive leukotrienes."
    },
    {
        "type": "Direct Question",
        "question": "Which enzyme converts free cholesterol and fatty acyl-CoA into cholesteryl esters within hepatocytes?",
        "options": ["A. ACAT (Acyl-CoA:cholesterol acyltransferase)", "B. LCAT", "C. HMG-CoA reductase", "D. Cholesterol esterase"],
        "answer": "A",
        "explanation": "ACAT acts intracellularly inside tissue cells/hepatocytes, whereas LCAT acts extracellularly in HDL particles."
    },
    {
        "type": "Exception Question",
        "question": "All of the following amino acids possess hydrophobic, nonpolar side chains EXCEPT:",
        "options": ["A. Leucine", "B. Isoleucine", "C. Valine", "D. Aspartate"],
        "answer": "D",
        "explanation": "Aspartate is a negatively charged, polar, hydrophilic amino acid. Leucine, isoleucine, and valine are branched nonpolar amino acids."
    },
    {
        "type": "Direct Question",
        "question": "What is the function of brown adipose tissue Uncoupling Protein-1 (UCP-1 / Thermogenin)?",
        "options": ["A. Dissipate the inner mitochondrial proton gradient to generate heat", "B. Synthesize ATP rapidly during shivering", "C. Transport fatty acids across the outer mitochondrial membrane", "D. Inhibit Complex IV electron transfer"],
        "answer": "A",
        "explanation": "Thermogenin creates a proton leak across the inner mitochondrial membrane, uncoupling respiration from ATP synthesis to generate heat."
    },
    {
        "type": "True or False",
        "question": "Statement: Vitamin E (alpha-tocopherol) functions primarily as a lipid-soluble antioxidant that prevents lipid peroxidation of cell membrane polyunsaturated fatty acids.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Vitamin E scavenges free radicals in lipid bilayers, protecting cell membranes from oxidative destruction."
    },
    {
        "type": "Case Scenario",
        "question": "A 15-year-old adolescent female presents with clitoromegaly and primary amenorrhea. Serum steroid profile shows elevated 17-hydroxyprogesterone and urinary 17-ketosteroids. Which adrenal enzyme is deficient?",
        "options": ["A. 21-alpha-hydroxylase", "B. 11-beta-hydroxylase", "C. 17-alpha-hydroxylase", "D. 3-beta-hydroxysteroid dehydrogenase"],
        "answer": "A",
        "explanation": "21-hydroxylase deficiency impairs cortisol/aldosterone synthesis, diverting precursors to adrenal androgens and causing virilization."
    },
    {
        "type": "Direct Question",
        "question": "Which fatty acid is an essential polyunsaturated fatty acid that must be supplied in human diets?",
        "options": ["A. Linoleic acid (18:2 n-6)", "B. Oleic acid (18:1 n-9)", "C. Palmitic acid (16:0)", "D. Stearic acid (18:0)"],
        "answer": "A",
        "explanation": "Humans lack desaturase enzymes to insert double bonds beyond C-9; linoleic and alpha-linolenic acids are strictly essential."
    },
    {
        "type": "Exception Question",
        "question": "All of the following statements regarding collagen matrix architecture are TRUE EXCEPT:",
        "options": ["A. Glycine occurs at every third residue (Gly-X-Y)", "B. Hydroxyproline and hydroxylysine stabilization requires Vitamin C", "C. Collagen contains a left-handed triple helix of three alpha chains", "D. Collagen synthesis is unaffected by scurvy"],
        "answer": "D",
        "explanation": "Vitamin C is a mandatory cofactor for prolyl and lysyl hydroxylases; deficiency causes scurvy and weak collagen triple helices."
    },
    {
        "type": "True or False",
        "question": "Statement: Eicosapentaenoic acid (EPA, 20:5 n-3) yields series-3 thromboxanes (TXA3) which promote weaker platelet aggregation than arachidonic acid-derived TXA2.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "TXA3 has significantly reduced pro-aggregatory potency compared to TXA2, explaining the cardiovascular benefits of omega-3 fish oils."
    },
    {
        "type": "Direct Question",
        "question": "Which intracellular compartment contains the rate-limiting enzyme for de novo cholesterol biosynthesis (HMG-CoA Reductase)?",
        "options": ["A. Endoplasmic reticulum membrane", "B. Mitochondrial matrix", "C. Cytosol", "D. Peroxisome"],
        "answer": "A",
        "explanation": "HMG-CoA Reductase is an integral membrane protein of the smooth endoplasmic reticulum with its catalytic domain facing the cytosol."
    }
]

# Tab 2 Questions (25 MCQs)
q_tab2 = [
    {
        "type": "Direct Question",
        "question": "What is the general flow of phosphoryl group transfer potential in cellular bioenergetics?",
        "options": ["A. High-energy phosphate compounds -> ATP -> Low-energy phosphate compounds", "B. ATP -> High-energy phosphate compounds -> Low-energy phosphate compounds", "C. Low-energy phosphate compounds -> ATP -> High-energy phosphate compounds", "D. ATP -> Low-energy phosphate compounds only"],
        "answer": "A",
        "explanation": "Compounds with higher transfer potential (1,3-BPG, Phosphoenolpyruvate, Creatine phosphate) transfer phosphate to ADP to make ATP, which then phosphorylates low-energy acceptors."
    },
    {
        "type": "Case Scenario",
        "question": "An untrained individual runs a 400m sprint. Two minutes in, he experiences severe muscle fatigue and cramping due to lactic acidosis. What is the metabolic purpose of converting pyruvate to lactate during anaerobic exercise?",
        "options": ["A. Regenerate cytosolic NAD+ for continued glycolysis", "B. Generate GTP directly", "C. Produce acetyl-CoA for the TCA cycle", "D. Lower cytosolic ATP levels"],
        "answer": "A",
        "explanation": "Lactate dehydrogenase reduces pyruvate to lactate while oxidizing NADH back to NAD+, allowing glyceraldehyde-3-phosphate dehydrogenase to continue glycolysis."
    },
    {
        "type": "Exception Question",
        "question": "All of the following electron transport chain inhibitors block specific complexes EXCEPT:",
        "options": ["A. Rotenone - Complex I", "B. Antimycin A - Complex III", "C. Cyanide - Complex IV", "D. 2,4-Dinitrophenol (DNP) - Complex II"],
        "answer": "D",
        "explanation": "DNP is a synthetic protonophore (uncoupler) that dissipates the proton gradient across the inner mitochondrial membrane, not an electron transport complex inhibitor."
    },
    {
        "type": "Direct Question",
        "question": "Which enzyme of the Tricarboxylic Acid (TCA) cycle is embedded directly in the inner mitochondrial membrane and participates in the Electron Transport Chain as Complex II?",
        "options": ["A. Succinate dehydrogenase", "B. Isocitrate dehydrogenase", "C. Malate dehydrogenase", "D. Alpha-ketoglutarate dehydrogenase"],
        "answer": "A",
        "explanation": "Succinate dehydrogenase catalyzes the oxidation of succinate to fumarate while reducing FAD to FADH2 within Complex II."
    },
    {
        "type": "True or False",
        "question": "Statement: Mature human red blood cells rely exclusively on anaerobic glycolysis for ATP generation because they lack mitochondria.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Erythrocytes lose all organelles during maturation; they convert glucose to lactate to generate 2 ATP per glucose."
    },
    {
        "type": "Case Scenario",
        "question": "A patient with severe Glucose-6-Phosphate Dehydrogenase (G6PD) deficiency develops acute hemolytic anemia after starting primaquine. Which pathway is impaired, preventing glutathione reduction?",
        "options": ["A. Pentose Phosphate Pathway", "B. Glycolysis", "C. TCA Cycle", "D. Gluconeogenesis"],
        "answer": "A",
        "explanation": "G6PD is the rate-limiting enzyme of the Hexose Monophosphate Shunt (PPP), producing NADPH needed by glutathione reductase to neutralize reactive oxygen species."
    },
    {
        "type": "Direct Question",
        "question": "What effect does a high mitochondrial energy charge (high ATP/ADP and NADH/NAD+ ratios) have on metabolic enzymes?",
        "options": ["A. Inhibits Isocitrate Dehydrogenase, Pyruvate Dehydrogenase, and PFK-1", "B. Stimulates Pyruvate Dehydrogenase and Citrate Synthase", "C. Activates Glycolysis and glycogen breakdown", "D. Stimulates Complex I and Complex III"],
        "answer": "A",
        "explanation": "Abundant ATP and NADH signal energy sufficiency, allosterically inhibiting key regulatory enzymes in oxidative pathways."
    },
    {
        "type": "Exception Question",
        "question": "The Pyruvate Dehydrogenase (PDH) complex requires all of the following coenzymes EXCEPT:",
        "options": ["A. Thiamine pyrophosphate (TPP)", "B. Lipoic acid and Coenzyme A", "C. FAD and NAD+", "D. Biotin"],
        "answer": "D",
        "explanation": "PDH requires 5 coenzymes: TPP, Lipoamide, CoA, FAD, and NAD+. Biotin is required by carboxylases (e.g., Pyruvate Carboxylase)."
    },
    {
        "type": "True or False",
        "question": "Statement: In mitochondrial oxidative phosphorylation, molecular oxygen (O2) serves as the final terminal electron acceptor.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Complex IV (Cytochrome c oxidase) transfers electrons to O2, reducing it to H2O."
    },
    {
        "type": "Case Scenario",
        "question": "An industrial worker accidentally ingests sodium cyanide. Cyanide binds tightly to the ferric (Fe3+) iron in Cytochrome a3 of Complex IV. What is the immediate biochemical consequence?",
        "options": ["A. Complete arrest of electron transport and collapse of the proton gradient", "B. Uncoupling of ATP synthesis with hyperthermia", "C. Accelerated NADH oxidation", "D. Increased mitochondrial O2 consumption"],
        "answer": "A",
        "explanation": "Blocking Complex IV halts all upstream electron transfer, preventing proton pumping and terminating oxidative phosphorylation."
    },
    {
        "type": "Direct Question",
        "question": "Why is the hydrolysis of inorganic pyrophosphate (PPi -> 2 Pi) by pyrophosphatase crucial in synthetic biosynthetic pathways?",
        "options": ["A. It drives endergonic activation reactions forward by eliminating product", "B. It generates extra ATP directly", "C. It reduces NAD+ to NADH", "D. It inhibits uncoupling proteins"],
        "answer": "A",
        "explanation": "Pyrophosphate hydrolysis has a large negative Delta G (~ -7 kcal/mol), pulling reactions like fatty acid activation and nucleic acid synthesis to completion."
    },
    {
        "type": "Exception Question",
        "question": "All of the following statements about the TCA cycle are TRUE EXCEPT:",
        "options": ["A. It operates strictly under aerobic conditions", "B. It produces 3 NADH, 1 FADH2, and 1 GTP per acetyl-CoA", "C. It provides net synthesis of glucose directly from acetyl-CoA", "D. It provides intermediates for amino acid and heme synthesis"],
        "answer": "C",
        "explanation": "Acetyl-CoA enters the TCA cycle as 2 carbons and is lost as 2 CO2 molecules; humans cannot achieve net gluconeogenesis from acetyl-CoA."
    },
    {
        "type": "True or False",
        "question": "Statement: The actual intracellular free energy change (Delta G) of ATP hydrolysis in living cells is identical to the standard free energy change (Delta G°').",
        "options": ["A. True", "B. False"],
        "answer": "B",
        "explanation": "Delta G°' is measured at 1M standard concentrations. In vivo concentrations of ATP, ADP, and Pi differ markedly, making actual Delta G much more negative (~ -12 kcal/mol)."
    },
    {
        "type": "Case Scenario",
        "question": "A teenager ingests 2,4-Dinitrophenol (DNP) to lose weight. She is rushed to the ER with extreme hyperthermia, tachypnea, and metabolic acidosis. What is the mechanism of DNP toxicity?",
        "options": ["A. Proton gradient dissipation leading to energy release as heat instead of ATP", "B. Inhibition of ATP synthase catalytic subunit", "C. Irreversible blockade of Complex I", "D. Inhibition of carnitine palmitoyltransferase-1"],
        "answer": "A",
        "explanation": "DNP shuttles protons across the inner mitochondrial membrane into the matrix, bypassing ATP synthase. Respiration runs at maximum rate, releasing metabolic energy as heat."
    },
    {
        "type": "Direct Question",
        "question": "Which enzyme converts pyruvate to oxaloacetate in the mitochondrion, initiating gluconeogenesis?",
        "options": ["A. Pyruvate carboxylase", "B. Pyruvate kinase", "C. Malate dehydrogenase", "D. PEP carboxykinase"],
        "answer": "A",
        "explanation": "Pyruvate carboxylase is a biotin-dependent mitochondrial enzyme that converts pyruvate + CO2 + ATP into oxaloacetate."
    },
    {
        "type": "Exception Question",
        "question": "During prolonged starvation (3+ weeks), which tissue or organ CANNOT use ketone bodies (acetoacetate, beta-hydroxybutyrate) as fuel?",
        "options": ["A. Brain", "B. Skeletal muscle", "C. Red blood cells", "D. Myocardium"],
        "answer": "C",
        "explanation": "Red blood cells lack mitochondria and therefore lack thiophorase (beta-ketoacyl-CoA transferase), preventing ketone body oxidation."
    },
    {
        "type": "True or False",
        "question": "Statement: Arsenic poisoning causes toxic inhibition of lipoic acid-dependent enzyme complexes, including Pyruvate Dehydrogenase and Alpha-Ketoglutarate Dehydrogenase.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Arsenite binds vicinal sulfhydryl groups of lipoamide, inactivating PDH and alpha-KGDH, causing pyruvate/lactate accumulation."
    },
    {
        "type": "Case Scenario",
        "question": "A marathon runner 'hits the wall' at mile 20. Which endogenous fuel reserve has been depleted, forcing reliance on slower fatty acid oxidation?",
        "options": ["A. Liver and muscle glycogen", "B. Subcutaneous triacylglycerols", "C. Circulating ketone bodies", "D. Muscle protein"],
        "answer": "A",
        "explanation": "Glycogen depletion limits rapid ATP generation via glycolysis, causing sudden physical fatigue."
    },
    {
        "type": "Direct Question",
        "question": "How does insulin regulate key rate-limiting enzymes of fed-state metabolic pathways (e.g., Glycogen Synthase, Acetyl-CoA Carboxylase)?",
        "options": ["A. Promotes enzyme dephosphorylation via Protein Phosphatase-1", "B. Promotes cAMP-dependent phosphorylation", "C. Allosterically inhibits gene transcription", "D. Degrades intracellular phosphatases"],
        "answer": "A",
        "explanation": "Insulin signaling activates protein phosphatases that dephosphorylate glycogen synthase and acetyl-CoA carboxylase, converting them into active forms."
    },
    {
        "type": "Exception Question",
        "question": "All of the following conditions shift the hemoglobin oxygen dissociation curve to the RIGHT (promoting O2 unloading) EXCEPT:",
        "options": ["A. Increased 2,3-BPG", "B. Increased H+ (decreased pH)", "C. Increased temperature", "D. Decreased pCO2"],
        "answer": "D",
        "explanation": "Decreased pCO2 (or alkalosis) shifts the O2 dissociation curve to the LEFT, increasing hemoglobin affinity for oxygen."
    },
    {
        "type": "True or False",
        "question": "Statement: Glucagon signaling via GPCRs activates Protein Kinase A, causing phosphorylation and inactivation of Glycogen Synthase and Pyruvate Kinase in hepatocytes.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Glucagon elevates cAMP, activating PKA which phosphorylates rate-limiting glycolytic/glycogenic enzymes, turning off glucose consumption."
    },
    {
        "type": "Direct Question",
        "question": "Which shuttle mechanism transfers cytosolic NADH electrons into the mitochondrial matrix yielding ~2.5 ATP per pair in heart and liver?",
        "options": ["A. Malate-Aspartate Shuttle", "B. Glycerol-3-Phosphate Shuttle", "C. Citrate-Malate Shuttle", "D. Carnitine Shuttle"],
        "answer": "A",
        "explanation": "The Malate-Aspartate shuttle transfers electrons to mitochondrial NAD+, yielding ~2.5 ATP via Complex I."
    },
    {
        "type": "Case Scenario",
        "question": "An infant develops hypoglycemia, lethargy, and hypoketosis during an episode of viral gastroenteritis with poor feeding. Urinalysis shows dicarboxylic aciduria. What metabolic defect is present?",
        "options": ["A. Medium-Chain Acyl-CoA Dehydrogenase (MCAD) deficiency", "B. Pyruvate kinase deficiency", "C. Glucose-6-phosphatase deficiency", "D. Carnitine palmitoyltransferase II deficiency"],
        "answer": "A",
        "explanation": "MCAD deficiency impairs beta-oxidation of 6- to 12-carbon fatty acids, preventing ketone body formation and causing fasting hypoglycemia."
    },
    {
        "type": "Direct Question",
        "question": "Which metabolite allosterically activates Acetyl-CoA Carboxylase (ACC) to promote de novo fatty acid synthesis in the fed state?",
        "options": ["A. Citrate", "B. Palmitoyl-CoA", "C. AMP", "D. Glucagon"],
        "answer": "A",
        "explanation": "Citrate signals abundant mitochondrial acetyl-CoA and energy, polymerizing and activating ACC in the cytosol."
    },
    {
        "type": "Exception Question",
        "question": "All of the following statements concerning Myoglobin vs Hemoglobin oxygen binding are TRUE EXCEPT:",
        "options": ["A. Myoglobin displays a hyperbolic oxygen saturation curve", "B. Hemoglobin displays a sigmoidal oxygen saturation curve due to cooperativity", "C. Myoglobin has a higher affinity for oxygen than hemoglobin", "D. Myoglobin exhibits allosteric regulation by 2,3-BPG"],
        "answer": "D",
        "explanation": "Myoglobin is a monomeric protein with a single oxygen-binding heme site; it lacks quaternary structure and is NOT regulated by 2,3-BPG."
    }
]

# Tab 3 Questions (25 MCQs)
q_tab3 = [
    {
        "type": "Case Scenario",
        "question": "A 2-week-old infant suffers from vomiting, diarrhea, jaundice, and cataracts after milk feeds. Laboratory screening reveals galactosaemia. Which enzyme is most commonly deficient in classic galactosemia?",
        "options": ["A. Galactose-1-phosphate uridyltransferase (GALT)", "B. Galactokinase", "C. UDP-galactose epimerase", "D. Phosphoglucomutase"],
        "answer": "A",
        "explanation": "Classic galactosemia (Type I) is caused by GALT deficiency, leading to accumulation of toxic galactose-1-phosphate and galactitol."
    },
    {
        "type": "Case Scenario",
        "question": "A 1-year-old child presents with musty-smelling urine, severe developmental delay, and hypopigmentation (pale skin, blue eyes). Ferric chloride test on urine yields a green color. What is the diagnosis?",
        "options": ["A. Phenylketonuria (PKU)", "B. Alkaptonuria", "C. Maple Syrup Urine Disease", "D. Homocystinuria"],
        "answer": "A",
        "explanation": "PKU is caused by Phenylalanine Hydroxylase deficiency. Elevated phenylalanine converts to phenylpyruvate (green with ferric chloride) and causes hypopigmentation due to reduced tyrosine/melanin."
    },
    {
        "type": "Exception Question",
        "question": "Inborn errors of branched-chain amino acid metabolism include all of the following EXCEPT:",
        "options": ["A. Maple Syrup Urine Disease (MSUD)", "B. Isovaleric Acidemia", "C. Methylmalonic Acidemia", "D. Alkaptonuria"],
        "answer": "D",
        "explanation": "Alkaptonuria is an inborn error of aromatic amino acid (tyrosine/phenylalanine) degradation caused by homogentisate oxidase deficiency."
    },
    {
        "type": "Direct Question",
        "question": "Which enzyme deficiency causes dark pigmentation of sclera and cartilage (ochronosis) and urine that turns black upon standing?",
        "options": ["A. Homogentisate oxidase", "B. Tyrosinase", "C. Phenylalanine hydroxylase", "D. Fumarylacetoacetate hydrolase"],
        "answer": "A",
        "explanation": "Homogentisate oxidase deficiency (Alkaptonuria) leads to accumulation of homogentisic acid, which oxidizes to dark polymers."
    },
    {
        "type": "True or False",
        "question": "Statement: Pyridoxal Phosphate (PLP, Vitamin B6) is an essential coenzyme for all enzymatic transamination reactions.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "PLP acts as an intermediate amino-group carrier bound to aminotransferases during transamination."
    },
    {
        "type": "Case Scenario",
        "question": "A 66-year-old malnourished man presents with macrocytic anemia and peripheral neuropathy. Blood tests show elevated levels of BOTH serum homocysteine AND methylmalonic acid (MMA). Which vitamin is deficient?",
        "options": ["A. Vitamin B12 (Cobalamin)", "B. Vitamin B9 (Folate)", "C. Vitamin B6 (Pyridoxine)", "D. Vitamin B3 (Niacin)"],
        "answer": "A",
        "explanation": "Vitamin B12 is required by Methylmalonyl-CoA mutase; elevated MMA distinguishes B12 deficiency from pure Folate deficiency (where MMA is normal)."
    },
    {
        "type": "Direct Question",
        "question": "What is the primary neurotoxic mechanism of elevated blood ammonia (hyperammonemia) in the central nervous system?",
        "options": ["A. Depletion of alpha-ketoglutarate and glutamate in astrocytes", "B. Inhibition of glycolysis", "C. Direct destruction of myelin sheaths", "D. Inhibition of GABA synthesis"],
        "answer": "A",
        "explanation": "Excess NH4+ drives glutamate dehydrogenase and glutamine synthetase reactions, depleting alpha-ketoglutarate and disrupting TCA cycle bioenergetics in the brain."
    },
    {
        "type": "Exception Question",
        "question": "Lead poisoning inhibits heme biosynthesis by directly inactivating which two enzymes?",
        "options": ["A. ALA dehydratase and Ferrochelatase", "B. ALA synthase and Uroporphyrinogen decarboxylase", "C. Porphobilinogen deaminase and Heme oxygenase", "D. Biliverdin reductase and Ferrochelatase"],
        "answer": "A",
        "explanation": "Lead binds sulfhydryl groups of ALA dehydratase and displaces iron in Ferrochelatase, causing anemia and protoporphyrin accumulation."
    },
    {
        "type": "True or False",
        "question": "Statement: Acute Intermittent Porphyria (AIP) characteristically presents with severe abdominal pain and neuropsychiatric symptoms WITHOUT skin photosensitivity.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "AIP is caused by Hydroxymethylbilane synthase (PBG deaminase) deficiency; non-photosensitive porphyrin precursors (PBG, ALA) accumulate."
    },
    {
        "type": "Case Scenario",
        "question": "A 3-year-old child presents with severe photosensitivity, blistering lesions on sun-exposed skin, red urine, and anemia. Diagnosis confirms Congenital Erythropoietic Porphyria (CEP). Which enzyme is deficient?",
        "options": ["A. Uroporphyrinogen III cosynthase", "B. ALA synthase", "C. Ferrochelatase", "D. Biliverdin reductase"],
        "answer": "A",
        "explanation": "CEP (Gunther disease) results from Uroporphyrinogen III cosynthase deficiency, leading to accumulation of isomer I porphyrins which cause extreme photosensitivity."
    },
    {
        "type": "Direct Question",
        "question": "Which enzyme converts Arginine into Urea and Ornithine in the final step of the Urea Cycle?",
        "options": ["A. Arginase", "B. Argininosuccinate lyase", "C. Carbamoyl phosphate synthetase I", "D. Ornithine transcarbamoylase"],
        "answer": "A",
        "explanation": "Arginase cleaves arginine to produce urea (disposed via kidneys) and regenerates ornithine (re-enters mitochondria)."
    },
    {
        "type": "Exception Question",
        "question": "In obstructive jaundice (biliary tree obstruction), typical diagnostic laboratory findings include all of the following EXCEPT:",
        "options": ["A. Markedly elevated serum conjugated (direct) bilirubin", "B. Markedly elevated serum alkaline phosphatase (ALP)", "C. Pale, clay-colored (stercobilin-deficient) stools", "D. Markedly elevated urinary urobilinogen"],
        "answer": "D",
        "explanation": "Because bile flow into the duodenum is blocked, intestinal urobilinogen formation ceases; thus urinary urobilinogen is LOW or absent."
    },
    {
        "type": "True or False",
        "question": "Statement: Cysteine becomes an essential amino acid in patients suffering from Homocystinuria.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Cystathionine beta-synthase deficiency blocks transsulfuration of methionine to cysteine, making cysteine conditionally essential."
    },
    {
        "type": "Case Scenario",
        "question": "A newborn exhibits severe lethargy, sweet maple syrup odor in the diaper, ketoacidosis, and seizures. Diagnosis confirms Maple Syrup Urine Disease. Which enzyme complex is defective?",
        "options": ["A. Branched-Chain Alpha-Ketoacid Dehydrogenase (BCKD)", "B. Isovaleryl-CoA dehydrogenase", "C. Propionyl-CoA carboxylase", "D. Homogentisate oxidase"],
        "answer": "A",
        "explanation": "MSKD is caused by BCKD complex deficiency, preventing oxidative decarboxylation of leucine, isoleucine, and valine ketoacids."
    },
    {
        "type": "Direct Question",
        "question": "Which molecule acts as the obligate allosteric activator of Carbamoyl Phosphate Synthetase I (CPS-1) in the urea cycle?",
        "options": ["A. N-Acetylglutamate (NAG)", "B. Citrulline", "C. Acetyl-CoA", "D. Fumarate"],
        "answer": "A",
        "explanation": "NAG is synthesized by NAG synthase (stimulated by arginine) and is strictly required to activate CPS-1."
    },
    {
        "type": "Exception Question",
        "question": "Dietary management of classic Phenylketonuria (PKU) requires all of the following EXCEPT:",
        "options": ["A. Strict limitation of dietary Phenylalanine", "B. Dietary supplementation of Tyrosine", "C. Complete, 100% elimination of all dietary Phenylalanine forever", "D. Early initiation in neonatal period to prevent irreversible intellectual disability"],
        "answer": "C",
        "explanation": "Phenylalanine is an essential amino acid; complete elimination causes protein starvation and death. It must be restricted to minimal growth requirements."
    },
    {
        "type": "True or False",
        "question": "Statement: Unconjugated (indirect) bilirubin is lipid-soluble, bound to albumin in plasma, and cannot pass into urine.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Unconjugated bilirubin is nonpolar; it requires hepatic glucuronidation (via UDP-glucuronosyltransferase) to become water-soluble conjugated bilirubin."
    },
    {
        "type": "Case Scenario",
        "question": "An alcoholic patient presents with severe hypoglycemia. What is the metabolic mechanism by which excessive ethanol oxidation inhibits hepatic gluconeogenesis?",
        "options": ["A. High NADH/NAD+ ratio forces pyruvate -> lactate and OAA -> malate", "B. Direct competitive inhibition of Pyruvate Carboxylase", "C. Depletion of ATP in hepatocytes", "D. Inhibition of glycogen phosphorylase"],
        "answer": "A",
        "explanation": "Alcohol and aldehyde dehydrogenases generate massive cytosolic NADH, consuming pyruvate and oxaloacetate and halting gluconeogenesis."
    },
    {
        "type": "Direct Question",
        "question": "Which enzyme converts Glucose to Sorbitol in the Polyol Pathway, contributing to diabetic microvascular complications (cataracts, neuropathy)?",
        "options": ["A. Aldose reductase", "B. Sorbitol dehydrogenase", "C. Hexokinase", "D. Fructokinase"],
        "answer": "A",
        "explanation": "Aldose reductase reduces unphosphorylated glucose to sorbitol using NADPH. Sorbitol accumulation causes osmotic swelling."
    },
    {
        "type": "Exception Question",
        "question": "All of the following statements regarding the Ubiquitin-Proteasome System are TRUE EXCEPT:",
        "options": ["A. It degrades misfolded and short-lived regulatory proteins", "B. Polyubiquitin tagging requires ATP", "C. Degradation occurs within the 26S proteasome core", "D. It operates exclusively inside lysosomes"],
        "answer": "D",
        "explanation": "The ubiquitin-proteasome system operates in the cytosol and nucleus at neutral pH. Lysosomal degradation is a separate autophagic pathway."
    },
    {
        "type": "True or False",
        "question": "Statement: Steroidal anti-inflammatory drugs (e.g., Prednisolone) inhibit Phospholipase A2, blocking release of arachidonic acid from membrane phospholipids.",
        "options": ["A. True", "B. False"],
        "answer": "A",
        "explanation": "Glucocorticoids induce lipocortin (annexin A1), which inhibits Phospholipase A2 and prevents eicosanoid cascade initiation."
    },
    {
        "type": "Direct Question",
        "question": "Which cofactor is required by Propionyl-CoA Carboxylase during the catabolism of odd-chain fatty acids and branched-chain amino acids?",
        "options": ["A. Biotin (Vitamin B7)", "B. Thiamine (Vitamin B1)", "C. Cobalamin (Vitamin B12)", "D. Pyridoxine (Vitamin B6)"],
        "answer": "A",
        "explanation": "Propionyl-CoA Carboxylase is a biotin-dependent enzyme that converts propionyl-CoA + CO2 + ATP into D-methylmalonyl-CoA."
    },
    {
        "type": "Case Scenario",
        "question": "A patient with severe hemolytic anemia exhibits dark urine and yellow sclera. Blood tests show elevated UNCONJUGATED bilirubin and elevated urine urobilinogen, with NO urinary bilirubin. What type of jaundice is present?",
        "options": ["A. Hemolytic (Pre-hepatic) jaundice", "B. Obstructive (Post-hepatic) jaundice", "C. Hepatocellular jaundice", "D. Gilbert syndrome"],
        "answer": "A",
        "explanation": "Hemolysis overwhelms hepatic glucuronidation; unconjugated bilirubin increases in blood (bound to albumin, no urine bilirubin) and high urobilinogen is formed."
    },
    {
        "type": "Direct Question",
        "question": "Which amino acid is the primary carrier of amino groups from extrahepatic tissues (especially muscle) to the liver via blood?",
        "options": ["A. Glutamine", "B. Alanine", "C. Aspartate", "D. Glycine"],
        "answer": "A",
        "explanation": "Glutamine synthetase converts glutamate + NH4+ into non-toxic glutamine for safe transport to liver and kidneys."
    },
    {
        "type": "Exception Question",
        "question": "All of the following enzymes are localized within the mitochondrial matrix EXCEPT:",
        "options": ["A. Pyruvate Dehydrogenase", "B. Citrate Synthase", "C. Carbamoyl Phosphate Synthetase I", "D. Hexokinase"],
        "answer": "D",
        "explanation": "Hexokinase is a cytosolic enzyme (or bound to the outer mitochondrial membrane), participating in glycolytic phosphorylation."
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

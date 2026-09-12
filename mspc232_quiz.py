import streamlit as st

st.set_page_config(page_title="MSPC232 Comprehensive Quiz (72 MCQs)", layout="wide", page_icon="🧪")

st.title("🧪 MSPC232: Medical Biochemistry & Metabolism Interactive Quiz")
st.caption("Compiled from Exam 2030, IA 2030, and Past Exam Documents • Includes Case Scenarios, Direct MCQs, True/False & Exceptions")

if 'answers' not in st.session_state:
    st.session_state.answers = {}

tabs = st.tabs(["🧪 Biochemistry & Enzymology (30 Qs)", "⚡ Physiology & Clinical Bioenergetics (22 Qs)", "🫀 Anatomy & Nutrition (20 Qs)"])

# QUESTION BANK: BIOCHEMISTRY (30 Questions)
q_biochem = [
    {
        "id": "b1", "type": "Direct MCQs",
        "q": "What is the direction of phosphoryl group transfer in metabolism?",
        "options": ["A. ATP -> high-energy phosphate -> low-energy phosphate", "B. Low-energy phosphate -> high-energy phosphate -> ATP", "C. High-energy phosphate compounds -> ATP -> low-energy phosphate compounds", "D. ATP -> low-energy phosphate -> high-energy phosphate"],
        "answer": "C. High-energy phosphate compounds -> ATP -> low-energy phosphate compounds",
        "exp": "Phosphoryl groups flow from high-energy donors (e.g., PEP, 1,3-BPG) to ATP, which then donates phosphate to low-energy acceptors (e.g., glucose, glycerol)."
    },
    {
        "id": "b2", "type": "Case Scenarios",
        "q": "A research scientist adds avidin (a egg-white biotin-binding protein) to a hepatocyte culture. Which metabolic pathway conversion will be directly blocked?",
        "options": ["A. Glucose to pyruvate", "B. Pyruvate to glucose", "C. Oxaloacetate to glucose", "D. Glucose to ribose-5-phosphate"],
        "answer": "B. Pyruvate to glucose",
        "exp": "Pyruvate carboxylase requires biotin to convert pyruvate to oxaloacetate in gluconeogenesis. Avidin inhibits biotin, halting gluconeogenesis from pyruvate."
    },
    {
        "id": "b3", "type": "Exceptions",
        "q": "An infant presents with lethargy, vomiting, diarrhea, and failure to thrive after milk feeding, and is diagnosed with galactosemia. Which of the following enzymes is NOT typically compromised in galactosemia?",
        "options": ["A. Galactokinase", "B. Galactose-1-phosphate uridyl transferase (GALT)", "C. UDP-galactose 4-epimerase", "D. Phosphoglucomutase"],
        "answer": "D. Phosphoglucomutase",
        "exp": "Galactosemia results from deficiencies in Galactokinase, GALT, or Epimerase. Phosphoglucomutase converts G1P to G6P in glycogen pathways."
    },
    {
        "id": "b4", "type": "Direct MCQs",
        "q": "Why is olive oil liquid at room temperature while butter is solid?",
        "options": ["A. Olive oil contains predominantly cis-unsaturated fatty acids", "B. Olive oil contains trans-unsaturated fatty acids", "C. Olive oil contains saturated long-chain fatty acids", "D. Butter lacks saturated fatty acids"],
        "answer": "A. Olive oil contains predominantly cis-unsaturated fatty acids",
        "exp": "Cis double bonds introduce kinks in acyl chains, preventing tight intermolecular packing and lowering melting point."
    },
    {
        "id": "b5", "type": "Direct MCQs",
        "q": "Excessive ingestion of ethanol inhibits gluconeogenesis primarily through which mechanism?",
        "options": ["A. Increased NAD+/NADH ratio", "B. Decreased NAD+/NADH ratio (elevated NADH/NAD+)", "C. Direct allosteric inhibition of fructose-1,6-bisphosphatase", "D. Depletion of acetyl-CoA"],
        "answer": "B. Decreased NAD+/NADH ratio (elevated NADH/NAD+)",
        "exp": "Ethanol oxidation by alcohol dehydrogenase generates abundant cytosolic NADH, consuming pyruvate and oxaloacetate and causing hypoglycemia."
    },
    {
        "id": "b6", "type": "Direct MCQs",
        "q": "Which pair of amino acids contain hydroxyl groups capable of forming O-glycosidic linkages in glycoproteins?",
        "options": ["A. Glutamine and Asparagine", "B. Serine and Threonine", "C. Lysine and Arginine", "D. Aspartate and Glutamate"],
        "answer": "B. Serine and Threonine",
        "exp": "Serine and threonine possess side-chain hydroxyl (-OH) groups that undergo O-linked glycosylation."
    },
    {
        "id": "b7", "type": "Direct MCQs",
        "q": "Erythrulose is classified biochemically as a:",
        "options": ["A. Aldotetrose", "B. Tetraketose", "C. Aldopentose", "D. Ketohexose"],
        "answer": "B. Tetraketose",
        "exp": "Erythrulose is a four-carbon ketose sugar (tetraketose)."
    },
    {
        "id": "b8", "type": "Exceptions",
        "q": "Which of the following carbohydrates is NOT a substrate for aldose reductase in the polyol pathway?",
        "options": ["A. Glucose", "B. Galactose", "C. Sucrose", "D. Sorbitol precursor aldoses"],
        "answer": "C. Sucrose",
        "exp": "Aldose reductase acts on aldose monosaccharides (glucose, galactose). Disaccharides like sucrose do not fit the active site."
    },
    {
        "id": "b9", "type": "True or False",
        "q": "Select the TRUE statement regarding inorganic pyrophosphate (PPi) hydrolysis during amino acid activation:",
        "options": ["A. PPi hydrolysis absorbs heat and inhibits synthetic reactions", "B. Hydrolysis of PPi by pyrophosphatase yields a large negative Delta G, driving endergonic synthesis to completion", "C. PPi is directly recycled into ADP without loss of energy", "D. PPi hydrolysis reduces the yield of cellular ATP"],
        "answer": "B. Hydrolysis of PPi by pyrophosphatase yields a large negative Delta G, driving endergonic synthesis to completion",
        "exp": "Pyrophosphatase hydrolyzes PPi to 2 Pi (Delta G = -19 kJ/mol), making synthetic activation steps irreversible."
    },
    {
        "id": "b10", "type": "Exceptions",
        "q": "Which of the following lipid classes does NOT contain a fatty acid component?",
        "options": ["A. Cholesteryl esters", "B. Plasmalogens", "C. Free Cholesterol", "D. Sphingomyelin"],
        "answer": "C. Free Cholesterol",
        "exp": "Free cholesterol is a sterol lacking fatty acyl chains until esterified by ACAT/LCAT into cholesteryl esters."
    },
    {
        "id": "b11", "type": "Direct MCQs",
        "q": "To ensure maximum enzymatic activity of the Pyruvate Dehydrogenase (PDH) complex, which intramitochondrial metabolite level should be kept VERY LOW?",
        "options": ["A. NAD+", "B. Coenzyme A", "C. NADH", "D. Pyruvate"],
        "answer": "C. NADH",
        "exp": "NADH and Acetyl-CoA directly inhibit PDH and activate PDH kinase, inactivating the complex."
    },
    {
        "id": "b12", "type": "Case Scenarios",
        "q": "A 56-year-old man undergoing surgery is found to have dark brown cartilage in his hip joint (ochronosis). His urine turns dark black upon standing. Which enzyme is deficient?",
        "options": ["A. Tyrosinase", "B. Homogentisate oxidase", "C. Phenylalanine hydroxylase", "D. Fumarylacetoacetate hydrolase"],
        "answer": "B. Homogentisate oxidase",
        "exp": "Alkaptonuria is caused by homogentisate oxidase deficiency, leading to homogentisic acid accumulation, dark urine, and tissue ochronosis."
    },
    {
        "id": "b13", "type": "Exceptions",
        "q": "All of the following dietary/therapeutic interventions help ameliorate hyperammonemia EXCEPT:",
        "options": ["A. Citrulline", "B. Arginine", "C. Sodium benzoate", "D. High protein intake"],
        "answer": "D. High protein intake",
        "exp": "High dietary protein increases nitrogen load, worsening hyperammonemia."
    },
    {
        "id": "b14", "type": "Direct MCQs",
        "q": "Which combination of enzymes provides the primary pathway for converting amino acid nitrogen into free ammonia in humans?",
        "options": ["A. Aminotransferases and Glutamate Dehydrogenase", "B. Glutaminase and Arginase", "C. Alanine aminotransferase and Glutamine Synthetase", "D. Amino acid oxidase and Uricase"],
        "answer": "A. Aminotransferases and Glutamate Dehydrogenase",
        "exp": "Transdeamination pairs cytosolic aminotransferases with mitochondrial glutamate dehydrogenase to funnel nitrogen into free NH4+."
    },
    {
        "id": "b15", "type": "Exceptions",
        "q": "Inborn errors of branched-chain amino acid metabolism include all of the following EXCEPT:",
        "options": ["A. Maple Syrup Urine Disease (MSUD)", "B. Isovaleric acidemia", "C. Methylmalonic acidemia", "D. Alkaptonuria"],
        "answer": "D. Alkaptonuria",
        "exp": "Alkaptonuria affects tyrosine/phenylalanine degradation, not branched-chain amino acids."
    },
    {
        "id": "b16", "type": "Case Scenarios",
        "q": "A 66-year-old malnourished man presents with macrocytic anemia. Laboratory analysis reveals elevated blood levels of BOTH homocysteine and methylmalonic acid (MMA). What is the specific deficiency?",
        "options": ["A. Folate (Vitamin B9)", "B. Vitamin B12 (Cobalamin)", "C. Vitamin B6 (Pyridoxine)", "D. Iron"],
        "answer": "B. Vitamin B12 (Cobalamin)",
        "exp": "Vitamin B12 is required for methylmalonyl-CoA mutase and methionine synthase. Folate deficiency elevates homocysteine alone."
    },
    {
        "id": "b17", "type": "Direct MCQs",
        "q": "Propionyl-CoA carboxylase requires which essential cofactor, deficiency of which leads to propionic acidemia?",
        "options": ["A. Thiamine (B1)", "B. Biotin (B7)", "C. Niacin (B3)", "D. Pyridoxine (B6)"],
        "answer": "B. Biotin (B7)",
        "exp": "Propionyl-CoA carboxylase is a biotin-dependent enzyme."
    },
    {
        "id": "b18", "type": "Exceptions",
        "q": "Which of the following is NOT a feature of the Ubiquitin-Proteasome system of proteolysis?",
        "options": ["A. Requires ATP hydrolysis", "B. Targets proteins tagged with polyubiquitin chains", "C. Operates inside acidic lysosomal compartments", "D. Uses isopeptide bonds between ubiquitin and lysine residues"],
        "answer": "C. Operates inside acidic lysosomal compartments",
        "exp": "Ubiquitin-proteasome degradation occurs in the neutral cytosol and nucleus, not in acidic lysosomes."
    },
    {
        "id": "b19", "type": "Case Scenarios",
        "q": "A 2-year-old child presents with severe abdominal pain, dark urine containing uroporphyrin, and extreme skin photosensitivity. Diagnosis reveals Congenital Erythropoietic Porphyria (CEP). Which enzyme is deficient?",
        "options": ["A. ALA dehydratase", "B. Uroporphyrinogen III synthase (cosynthase)", "C. Ferrochelatase", "D. PBG deaminase"],
        "answer": "B. Uroporphyrinogen III synthase (cosynthase)",
        "exp": "CEP (Gunther disease) results from uroporphyrinogen III synthase deficiency, causing accumulation of photosensitizing type I porphyrins."
    },
    {
        "id": "b20", "type": "Case Scenarios",
        "q": "A 25-year-old patient presents with recurrent acute abdominal pain and confusion without skin photosensitivity. Urine assay shows elevated porphobilinogen (PBG). What is the diagnosis?",
        "options": ["A. Porphyria Cutanea Tarda", "B. Acute Intermittent Porphyria (AIP)", "C. Congenital Erythropoietic Porphyria", "D. Erythropoietic Protoporphyria"],
        "answer": "B. Acute Intermittent Porphyria (AIP)",
        "exp": "AIP is caused by PBG deaminase deficiency, presenting with neurovisceral symptoms without photosensitivity."
    },
    {
        "id": "b21", "type": "True or False",
        "q": "Select the TRUE statement regarding lead poisoning and heme biosynthesis:",
        "options": ["A. Lead specifically activates ALA synthase", "B. Lead inhibits ALA dehydratase and Ferrochelatase", "C. Lead enhances iron incorporation into protoporphyrin IX", "D. Lead causes uroporphyrin decarboxylase hyperfunction"],
        "answer": "B. Lead inhibits ALA dehydratase and Ferrochelatase",
        "exp": "Lead inactivates zinc-dependent ALA dehydratase and ferrochelatase, causing microcytic anemia and elevated zinc protoporphyrin."
    },
    {
        "id": "b22", "type": "Case Scenarios",
        "q": "A patient with gallstone obstruction of the common bile duct presents with yellow sclera and pale, clay-colored stools. The pale stool is due to the absence of:",
        "options": ["A. Biliverdin", "B. Stercobilin", "C. Conjugated bilirubin in urine", "D. Urobilinogen in bile"],
        "answer": "B. Stercobilin",
        "exp": "Stercobilin provides stool its brown color. Biliary obstruction prevents bilirubin from entering the intestine to form stercobilin."
    },
    {
        "id": "b23", "type": "Direct MCQs",
        "q": "What is the primary mechanism by which 2,4-dinitrophenol (DNP) uncouples oxidative phosphorylation?",
        "options": ["A. Directly inhibits ATP synthase F1 subunit", "B. Dissipates the inner mitochondrial proton gradient as heat", "C. Blocks electron transport at Complex III", "D. Inhibits the adenine nucleotide translocase"],
        "answer": "B. Dissipates the inner mitochondrial proton gradient as heat",
        "exp": "DNP transports protons across the inner mitochondrial membrane into the matrix, bypassing ATP synthase and dissipating energy as heat."
    },
    {
        "id": "b24", "type": "Direct MCQs",
        "q": "Which apolipoprotein is essential for the hepatic assembly and secretion of Very Low-Density Lipoproteins (VLDL)?",
        "options": ["A. ApoB-48", "B. ApoB-100", "C. ApoA-1", "D. ApoE"],
        "answer": "B. ApoB-100",
        "exp": "ApoB-100 is synthesized in hepatocytes for VLDL/LDL assembly; ApoB-48 is made in enterocytes for chylomicrons."
    },
    {
        "id": "b25", "type": "Case Scenarios",
        "q": "A 15-year-old girl with primary amenorrhea and clitoromegaly is diagnosed with Congenital Adrenal Hyperplasia (CAH). Which enzyme deficiency is most common?",
        "options": ["A. 17-alpha-hydroxylase", "B. 21-alpha-hydroxylase", "C. 11-beta-hydroxylase", "D. 3-beta-hydroxysteroid dehydrogenase"],
        "answer": "B. 21-alpha-hydroxylase",
        "exp": "21-hydroxylase deficiency impairs cortisol/aldosterone synthesis, shifting steroid precursors into adrenal androgens."
    },
    {
        "id": "b26", "type": "Direct MCQs",
        "q": "Acetyl-CoA produced in mitochondria exits into the cytosol for fatty acid synthesis in the form of:",
        "options": ["A. Pyruvate", "B. Citrate", "C. Oxaloacetate", "D. Malate"],
        "answer": "B. Citrate",
        "exp": "Citrate carries acetyl units across the inner mitochondrial membrane to the cytosol, where ATP citrate lyase cleaves it back into acetyl-CoA and OAA."
    },
    {
        "id": "b27", "type": "Case Scenarios",
        "q": "A patient taking NSAIDs develops gastric mucosal erosions due to inhibition of cyclooxygenase, decreasing synthesis of protective:",
        "options": ["A. Leukotrienes B4", "B. Prostaglandins E2 and I2", "C. Thromboxane A2", "D. Histamine"],
        "answer": "B. Prostaglandins E2 and I2",
        "exp": "PGE2 and PGI2 maintain gastric mucosal mucus, bicarbonate secretion, and blood flow."
    },
    {
        "id": "b28", "type": "Case Scenarios",
        "q": "An asthmatic patient takes aspirin for a headache and experiences acute bronchospasm. This occurs due to increased synthesis of:",
        "options": ["A. Thromboxanes", "B. Cysteinyl leukotrienes (LTC4, LTD4, LTE4)", "C. Prostacyclin", "D. Nitric oxide"],
        "answer": "B. Cysteinyl leukotrienes (LTC4, LTD4, LTE4)",
        "exp": "COX-1 inhibition shunts unesterified arachidonic acid into the 5-lipoxygenase pathway, generating bronchoconstrictor leukotrienes."
    },
    {
        "id": "b29", "type": "Case Scenarios",
        "q": "A 4-month-old infant presents with fasting hypoglycemia, hypoketosis, and dicarboxylic aciduria following a viral illness. What is the defect?",
        "options": ["A. G6PD deficiency", "B. Medium-Chain Acyl-CoA Dehydrogenase (MCAD) deficiency", "C. CPT-I deficiency", "D. Pyruvate kinase deficiency"],
        "answer": "B. Medium-Chain Acyl-CoA Dehydrogenase (MCAD) deficiency",
        "exp": "MCAD deficiency impairs medium-chain fatty acid beta-oxidation during fasting, leading to hypoketotic hypoglycemia."
    },
    {
        "id": "b30", "type": "Direct MCQs",
        "q": "Which intermediate is common to the synthesis of BOTH triacylglycerols and glycerophospholipids?",
        "options": ["A. CDP-choline", "B. Phosphatidic acid", "C. Diacylglycerol kinase", "D. Mevalonate"],
        "answer": "B. Phosphatidic acid",
        "exp": "Phosphatidic acid is the central branch-point intermediate for both TAG and phospholipid biosynthesis."
    }
]

# QUESTION BANK: PHYSIOLOGY (22 Questions)
q_physio = [
    {
        "id": "p1", "type": "Direct MCQs",
        "q": "During high-intensity anaerobic exercise, why is pyruvate reduced to lactate by Lactate Dehydrogenase?",
        "options": ["A. To lower cytosolic pH", "B. To regenerate NAD+ required for continued glycolysis", "C. To prevent ATP accumulation", "D. To stimulate glycogen phosphorylase"],
        "answer": "B. To regenerate NAD+ required for continued glycolysis",
        "exp": "Anaerobic LDH activity oxidizes NADH to NAD+, allowing GAPDH to sustain glycolytic ATP synthesis."
    },
    {
        "id": "p2", "type": "Case Scenarios",
        "q": "A male patient treated with primaquine for malaria develops sudden fatigue, dark urine, and jaundice. Heinz bodies are seen on blood smear. Which enzyme is deficient?",
        "options": ["A. Pyruvate kinase", "B. Glucose-6-Phosphate Dehydrogenase (G6PD)", "C. Glutathione reductase", "D. Transketolase"],
        "answer": "B. Glucose-6-Phosphate Dehydrogenase (G6PD)",
        "exp": "G6PD deficiency reduces NADPH production in RBCs, impairing glutathione reduction and leaving RBCs vulnerable to oxidative hemolysis."
    },
    {
        "id": "p3", "type": "Exceptions",
        "q": "Mature erythrocytes depend entirely on anaerobic glycolysis for ATP generation because they lack all of the following EXCEPT:",
        "options": ["A. Mitochondria", "B. Nucleus", "C. Cytosolic enzymes for glycolysis", "D. Electron transport chain complexes"],
        "answer": "C. Cytosolic enzymes for glycolysis",
        "exp": "RBCs lack mitochondria/nuclei but contain all cytosolic glycolytic enzymes."
    },
    {
        "id": "p4", "type": "Direct MCQs",
        "q": "Which hormone activates glycogen synthase in hepatocytes following a high-carbohydrate meal?",
        "options": ["A. Glucagon", "B. Epinephrine", "C. Insulin", "D. Cortisol"],
        "answer": "C. Insulin",
        "exp": "Insulin activates protein phosphatase-1, dephosphorylating and activating glycogen synthase."
    },
    {
        "id": "p5", "type": "Direct MCQs",
        "q": "During starvation, what becomes the predominant fuel used by the brain to spare muscle protein?",
        "options": ["A. Free fatty acids", "B. Ketone bodies (beta-hydroxybutyrate and acetoacetate)", "C. Branched-chain amino acids", "D. Lactate"],
        "answer": "B. Ketone bodies (beta-hydroxybutyrate and acetoacetate)",
        "exp": "Ketone bodies cross the BBB and supply up to 70% of brain energy during prolonged starvation."
    },
    {
        "id": "p6", "type": "True or False",
        "q": "Select the TRUE statement regarding erythrocyte metabolism during Pantothenate (Vitamin B5) deficiency:",
        "options": ["A. Erythrocyte glycolysis is completely halted", "B. Glycolysis in red blood cells proceeds normally because it does not require Coenzyme A", "C. Pentose phosphate pathway is blocked", "D. Lactic acid synthesis is completely inhibited"],
        "answer": "B. Glycolysis in red blood cells proceeds normally because it does not require Coenzyme A",
        "exp": "RBC glycolysis requires no Coenzyme A, so B5 deficiency does not impair RBC ATP production."
    },
    {
        "id": "p7", "type": "Exceptions",
        "q": "All of the following TCA cycle enzymes are located in the mitochondrial matrix EXCEPT:",
        "options": ["A. Citrate synthase", "B. Isocitrate dehydrogenase", "C. Succinate dehydrogenase", "D. Malate dehydrogenase"],
        "answer": "C. Succinate dehydrogenase",
        "exp": "Succinate dehydrogenase is embedded in the inner mitochondrial membrane as Complex II."
    },
    {
        "id": "p8", "type": "Direct MCQs",
        "q": "In Complex III of the electron transport chain, electrons are transferred from ubiquinol (QH2) to:",
        "options": ["A. Cytochrome a3", "B. Cytochrome c", "C. Oxygen", "D. FMN"],
        "answer": "B. Cytochrome c",
        "exp": "Complex III transfers electrons from ubiquinol to cytochrome c."
    },
    {
        "id": "p9", "type": "Direct MCQs",
        "q": "Cyanide inhibits cellular respiration by binding tightly to which electron transport chain component?",
        "options": ["A. Complex I", "B. Complex II", "C. Complex III", "D. Complex IV (Cytochrome c oxidase)"],
        "answer": "D. Complex IV (Cytochrome c oxidase)",
        "exp": "Cyanide binds Fe3+ in Complex IV, halting electron transfer to oxygen."
    },
    {
        "id": "p10", "type": "Direct MCQs",
        "q": "Malonyl-CoA inhibits which enzyme to prevent simultaneous fatty acid synthesis and beta-oxidation?",
        "options": ["A. Carnitine palmitoyltransferase I (CPT-I)", "B. Acyl-CoA dehydrogenase", "C. Hormone-sensitive lipase", "D. Fatty acid synthase"],
        "answer": "A. Carnitine palmitoyltransferase I (CPT-I)",
        "exp": "Malonyl-CoA inhibits CPT-I, blocking fatty acyl-CoA entry into mitochondria."
    },
    {
        "id": "p11", "type": "Case Scenarios",
        "q": "A sprinter completes a 100m race. What is the primary source of ATP during the first 5-10 seconds?",
        "options": ["A. Muscle glycogenolysis", "B. Creatine phosphate (phosphagen system)", "C. Fatty acid oxidation", "D. Liver gluconeogenesis"],
        "answer": "B. Creatine phosphate (phosphagen system)",
        "exp": "Creatine kinase transfers phosphate from phosphocreatine to ADP for immediate ATP during intense bursts."
    },
    {
        "id": "p12", "type": "Exceptions",
        "q": "Functions of the TCA cycle include all of the following EXCEPT:",
        "options": ["A. Generation of NADH and FADH2", "B. Direct net synthesis of glucose from Acetyl-CoA in humans", "C. Generation of GTP by substrate-level phosphorylation", "D. Oxidation of acetyl groups to CO2 and H2O"],
        "answer": "B. Direct net synthesis of glucose from Acetyl-CoA in humans",
        "exp": "Humans cannot convert Acetyl-CoA into net glucose because 2 carbons enter as acetyl-CoA and 2 exit as CO2."
    },
    {
        "id": "p13", "type": "Direct MCQs",
        "q": "What is the rate-limiting enzyme of cholesterol biosynthesis, targeted by statin drugs?",
        "options": ["A. HMG-CoA lyase", "B. HMG-CoA reductase", "C. Squalene synthase", "D. Mevalonate kinase"],
        "answer": "B. HMG-CoA reductase",
        "exp": "HMG-CoA reductase converts HMG-CoA to mevalonate and is inhibited by statins."
    },
    {
        "id": "p14", "type": "Case Scenarios",
        "q": "How do statins lower blood LDL cholesterol levels?",
        "options": ["A. Decreases intestinal fat absorption", "B. Up-regulates hepatic LDL receptor expression", "C. Degrades apolipoprotein B-100", "D. Increases cholesterol secretion in bile"],
        "answer": "B. Up-regulates hepatic LDL receptor expression",
        "exp": "Reduced intracellular hepatic cholesterol increases LDL receptor transcription, accelerating clearance of circulating LDL."
    },
    {
        "id": "p15", "type": "Direct MCQs",
        "q": "What is the rate-limiting enzyme of the Urea Cycle?",
        "options": ["A. Carbamoyl Phosphate Synthetase II (CPS II)", "B. Carbamoyl Phosphate Synthetase I (CPS I)", "C. Ornithine Transcarbamoylase (OTC)", "D. Argininosuccinate Synthetase"],
        "answer": "B. Carbamoyl Phosphate Synthetase I (CPS I)",
        "exp": "CPS I in mitochondria is rate-limiting and requires N-acetylglutamate (NAG) for activity."
    },
    {
        "id": "p16", "type": "Direct MCQs",
        "q": "Arginase catalyzes which step in the Urea Cycle?",
        "options": ["A. Cleavage of Argininosuccinate to Arginine and Fumarate", "B. Hydrolysis of Arginine to Ornithine and Urea", "C. Condensation of Citrulline and Aspartate", "D. Formation of Carbamoyl Phosphate"],
        "answer": "B. Hydrolysis of Arginine to Ornithine and Urea",
        "exp": "Arginase hydrolyzes arginine to release free urea and regenerate ornithine."
    },
    {
        "id": "p17", "type": "Exceptions",
        "q": "All of the following amino acids are both glucogenic and ketogenic EXCEPT:",
        "options": ["A. Phenylalanine", "B. Isoleucine", "C. Tyrosine", "D. Leucine"],
        "answer": "D. Leucine",
        "exp": "Leucine and Lysine are purely ketogenic."
    },
    {
        "id": "p18", "type": "Direct MCQs",
        "q": "Which major organ is the primary site of ammonia detoxification via urea synthesis?",
        "options": ["A. Kidney", "B. Brain", "C. Liver", "D. Skeletal muscle"],
        "answer": "C. Liver",
        "exp": "The liver is the sole organ containing all urea cycle enzymes."
    },
    {
        "id": "p19", "type": "Case Scenarios",
        "q": "An athlete experiences muscle cramps and myoglobinuria after intense exercise. Biopsy shows lipid vacuoles and impaired long-chain fatty acid oxidation. What is the defect?",
        "options": ["A. Carnitine Palmitoyltransferase II / Carnitine deficiency", "B. MCAD deficiency", "C. G6Pase deficiency", "D. Myophosphorylase deficiency"],
        "answer": "A. Carnitine Palmitoyltransferase II / Carnitine deficiency",
        "exp": "CPT II / carnitine deficiency impairs mitochondrial long-chain fatty acid entry, causing rhabdomyolysis and muscle lipid accumulation."
    },
    {
        "id": "p20", "type": "True or False",
        "q": "Select the TRUE statement regarding high cellular energy charge ([ATP]/[ADP] ratio):",
        "options": ["A. High energy charge stimulates PFK-1 and Isocitrate Dehydrogenase", "B. High energy charge inhibits catabolic glycolysis/TCA cycle and promotes anabolic pathways", "C. High energy charge activates PDH phosphatase", "D. High energy charge promotes AMPK"],
        "answer": "B. High energy charge inhibits catabolic glycolysis/TCA cycle and promotes anabolic pathways",
        "exp": "High ATP/NADH allosterically inhibits catabolic pathways."
    },
    {
        "id": "p21", "type": "Direct MCQs",
        "q": "Which enzyme enables extrahepatic tissues to utilize ketone bodies?",
        "options": ["A. HMG-CoA synthase", "B. Thiophorase (Beta-ketoacyl-CoA transferase)", "C. Acetoacetyl-CoA synthetase", "D. Acetyl-CoA carboxylase"],
        "answer": "B. Thiophorase (Beta-ketoacyl-CoA transferase)",
        "exp": "Thiophorase activates acetoacetate to acetoacetyl-CoA in extrahepatic cells; liver lacks this enzyme."
    },
    {
        "id": "p22", "type": "Exceptions",
        "q": "Which of the following compounds is NOT derived from Tryptophan metabolism?",
        "options": ["A. Niacin", "B. Serotonin", "C. Melatonin", "D. Epinephrine"],
        "answer": "D. Epinephrine",
        "exp": "Epinephrine is synthesized from Tyrosine; Tryptophan yields Serotonin, Melatonin, and Niacin."
    }
]

# QUESTION BANK: ANATOMY & NUTRITION (20 Questions)
q_anatomy = [
    {
        "id": "a1", "type": "Direct MCQs",
        "q": "Visual phototransduction in rod photoreceptors involves conversion of 11-cis-retinal into:",
        "options": ["A. 9-cis-retinal", "B. All-trans-retinal", "C. beta-carotene", "D. Retinoic acid"],
        "answer": "B. All-trans-retinal",
        "exp": "Light absorption isomerizes 11-cis-retinal to all-trans-retinal, activating rhodopsin."
    },
    {
        "id": "a2", "type": "Case Scenarios",
        "q": "A 34-year-old woman with chronic low calcium intake presents with bone fractures. Which bone component is primarily compromised?",
        "options": ["A. Osteoid (collagen matrix)", "B. Hydroxyapatite crystals [Ca10(PO4)6(OH)2]", "C. Sharpey fibers", "D. Osteoclast lysosomes"],
        "answer": "B. Hydroxyapatite crystals [Ca10(PO4)6(OH)2]",
        "exp": "Calcium deficiency impairs osteoid mineralization into hydroxyapatite crystals."
    },
    {
        "id": "a3", "type": "Case Scenarios",
        "q": "A 2-year-old child presents with 'matchstick' thin limbs, total wasting of subcutaneous fat, but NO edema or fatty liver. What is the diagnosis?",
        "options": ["A. Kwashiorkor", "B. Marasmus", "C. Scurvy", "D. Rickets"],
        "answer": "B. Marasmus",
        "exp": "Marasmus is severe calorie deficiency leading to muscle and fat wasting without edema."
    },
    {
        "id": "a4", "type": "Case Scenarios",
        "q": "A 3-year-old child presents with generalized pitting edema, distended abdomen ('pot belly'), and fatty liver hepatomegaly. What is the diagnosis?",
        "options": ["A. Marasmus", "B. Kwashiorkor", "C. Pellagra", "D. Beriberi"],
        "answer": "B. Kwashiorkor",
        "exp": "Kwashiorkor is severe protein deficiency causing hypoalbuminemic edema and hepatomegaly due to failed apolipoprotein synthesis."
    },
    {
        "id": "a5", "type": "Direct MCQs",
        "q": "Membranes of thermophilic organisms adapted to high environmental temperatures are enriched in:",
        "options": ["A. Polyunsaturated fatty acids", "B. Saturated fatty acids", "C. Short-chain cis-unsaturated fatty acids", "D. Free glycerol"],
        "answer": "B. Saturated fatty acids",
        "exp": "Saturated fatty acids pack tightly, preventing fluidization at high temperatures."
    },
    {
        "id": "a6", "type": "Direct MCQs",
        "q": "Vitamin E (alpha-tocopherol) functions in cell membranes primarily as a:",
        "options": ["A. Coenzyme for carboxylation", "B. Lipophilic antioxidant preventing lipid peroxidation", "C. Transcription factor for collagen", "D. Visual pigment precursor"],
        "answer": "B. Lipophilic antioxidant preventing lipid peroxidation",
        "exp": "Vitamin E protects cell membrane polyunsaturated lipids against free radical damage."
    },
    {
        "id": "a7", "type": "Exceptions",
        "q": "Symptoms of Vitamin B6 (Pyridoxine) deficiency include all of the following EXCEPT:",
        "options": ["A. Sideroblastic anemia", "B. Peripheral neuropathy", "C. Impaired transamination", "D. Macrocytic megaloblastic anemia"],
        "answer": "D. Macrocytic megaloblastic anemia",
        "exp": "Vitamin B6 deficiency causes microcytic sideroblastic anemia (ALA synthase requires PLP); macrocytic anemia is B12/Folate deficiency."
    },
    {
        "id": "a8", "type": "Direct MCQs",
        "q": "Primary structural surfactant component lacking in infant Respiratory Distress Syndrome (RDS) is:",
        "options": ["A. Sphingomyelin", "B. Dipalmitoylphosphatidylcholine", "C. Phosphatidylinositol", "D. Albumin"],
        "answer": "B. Dipalmitoylphosphatidylcholine",
        "exp": "Dipalmitoylphosphatidylcholine (lecithin) is the major surface-active component of lung surfactant."
    },
    {
        "id": "a9", "type": "Case Scenarios",
        "q": "Arsenic toxicity inhibits lipoic acid-dependent enzyme complexes. Which metabolites accumulate in blood?",
        "options": ["A. Glucose and Oxaloacetate", "B. Pyruvate and Lactate", "C. Acetyl-CoA and Citrate", "D. Succinate and Malate"],
        "answer": "B. Pyruvate and Lactate",
        "exp": "Arsenite inhibits PDH and alpha-ketoglutarate dehydrogenase, backing up pyruvate into lactate."
    },
    {
        "id": "a10", "type": "Direct MCQs",
        "q": "Serum ferritin level serves as the most sensitive clinical marker for:",
        "options": ["A. Transferrin saturation", "B. Total body iron stores", "C. Intestinal iron absorption rate", "D. Hemoglobin concentration"],
        "answer": "B. Total body iron stores",
        "exp": "Serum ferritin correlates directly with intracellular body iron reserves."
    },
    {
        "id": "a11", "type": "Direct MCQs",
        "q": "Fat-soluble vitamins (A, D, E, K) enter intestinal enterocytes via incorporation into:",
        "options": ["A. Free fatty acid transporters", "B. Mixed bile salt micelles", "C. Lipoprotein lipase complexes", "D. Chylomicron remnants"],
        "answer": "B. Mixed bile salt micelles",
        "exp": "Bile salts and lipids form amphipathic mixed micelles to transport fat-soluble vitamins across enterocyte brush borders."
    },
    {
        "id": "a12", "type": "True or False",
        "q": "Select the TRUE statement regarding essential fatty acids:",
        "options": ["A. Oleic acid is an essential fatty acid", "B. Linoleic acid (omega-6) and Alpha-linolenic acid (omega-3) cannot be synthesized de novo by humans", "C. Palmitic acid is an essential fatty acid", "D. Stearic acid is the precursor for leukotrienes"],
        "answer": "B. Linoleic acid (omega-6) and Alpha-linolenic acid (omega-3) cannot be synthesized de novo by humans",
        "exp": "Humans lack desaturases to insert double bonds beyond C9, making linoleic and alpha-linolenic acids essential."
    },
    {
        "id": "a13", "type": "Direct MCQs",
        "q": "Which tissue stores the majority of triacylglycerol reserves in the human body?",
        "options": ["A. Skeletal muscle", "B. Liver", "C. White adipose tissue", "D. Brown adipose tissue"],
        "answer": "C. White adipose tissue",
        "exp": "White adipocytes store unilocular TAG droplets for systemic energy."
    },
    {
        "id": "a14", "type": "Exceptions",
        "q": "All of the following are water-soluble vitamins that act as enzyme cofactors EXCEPT:",
        "options": ["A. Thiamine (B1)", "B. Riboflavin (B2)", "C. Ascorbic acid (Vitamin C)", "D. Tocopherol (Vitamin E)"],
        "answer": "D. Tocopherol (Vitamin E)",
        "exp": "Vitamin E is lipid-soluble."
    },
    {
        "id": "a15", "type": "Case Scenarios",
        "q": "A patient with bleeding gums, petechiae, and poor wound healing has a deficiency of:",
        "options": ["A. Ascorbic acid (Vitamin C)", "B. Niacin (Vitamin B3)", "C. Thiamine (Vitamin B1)", "D. Vitamin D"],
        "answer": "A. Ascorbic acid (Vitamin C)",
        "exp": "Scurvy results from Vitamin C deficiency, impairing prolyl/lysyl hydroxylase in collagen synthesis."
    },
    {
        "id": "a16", "type": "Direct MCQs",
        "q": "Pellagra (Dermatitis, Diarrhea, Dementia) is caused by deficiency of:",
        "options": ["A. Thiamine", "B. Niacin (B3) or Tryptophan", "C. Folate", "D. Riboflavin"],
        "answer": "B. Niacin (B3) or Tryptophan",
        "exp": "Pellagra results from Niacin or precursor Tryptophan deficiency."
    },
    {
        "id": "a17", "type": "Exceptions",
        "q": "Which condition is NOT associated with Vitamin D deficiency?",
        "options": ["A. Rickets in children", "B. Osteomalacia in adults", "C. Hypocalcemia", "D. Sideroblastic anemia"],
        "answer": "D. Sideroblastic anemia",
        "exp": "Sideroblastic anemia is associated with Vitamin B6 deficiency or lead toxicity."
    },
    {
        "id": "a18", "type": "Direct MCQs",
        "q": "Wernicke-Korsakoff syndrome in chronic alcoholism results from deficiency of:",
        "options": ["A. Thiamine (B1)", "B. Pyridoxine (B6)", "C. Cobalamin (B12)", "D. Folate"],
        "answer": "A. Thiamine (B1)",
        "exp": "Thiamine deficiency impairs TPP-dependent enzymes (PDH, alpha-KGDH, transketolase)."
    },
    {
        "id": "a19", "type": "Direct MCQs",
        "q": "Which apolipoprotein activates Lipoprotein Lipase (LPL) on capillary endothelium?",
        "options": ["A. ApoA-1", "B. ApoC-II", "C. ApoE", "D. ApoB-100"],
        "answer": "B. ApoC-II",
        "exp": "ApoC-II on chylomicrons and VLDL activates LPL to release free fatty acids."
    },
    {
        "id": "a20", "type": "Direct MCQs",
        "q": "Deficiency of ApoB-48 and ApoB-100 causes which hereditary lipid disorder?",
        "options": ["A. Familial Hypercholesterolemia", "B. Abetalipoproteinemia", "C. Tangier Disease", "D. Type I Hyperchylomicronemia"],
        "answer": "B. Abetalipoproteinemia",
        "exp": "MTP gene mutations prevent ApoB assembly, resulting in Abetalipoproteinemia (absence of chylomicrons, VLDL, and LDL)."
    }
]

def render_quiz(q_list, tab_key):
    st.write(f"**Total Questions: {len(q_list)}**")
    filter_type = st.selectbox(f"Filter Question Type ({tab_key}):", ["All", "Case Scenarios", "Direct MCQs", "True or False", "Exceptions"], key=f"f_{tab_key}")
    filtered = q_list if filter_type == "All" else [q for q in q_list if q['type'] == filter_type]
    
    score = 0
    submitted_count = 0
    
    for idx, item in enumerate(filtered):
        st.markdown("---")
        st.markdown(f"**Q{idx+1} [{item['type']}]: {item['q']}**")
        ans_key = f"key_{tab_key}_{item['id']}"
        choice = st.radio("Select option:", item['options'], key=ans_key)
        
        if st.button(f"Submit Q{idx+1}", key=f"btn_{ans_key}"):
            st.session_state.answers[ans_key] = choice
            
        if ans_key in st.session_state.answers:
            submitted_count += 1
            user_ans = st.session_state.answers[ans_key]
            if user_ans == item['answer']:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Incorrect. Correct Answer: **{item['answer']}**")
            with st.expander("💡 High-Yield Explanation"):
                st.info(item['exp'])

with tabs[0]:
    render_quiz(q_biochem, "biochem")

with tabs[1]:
    render_quiz(q_physio, "physio")

with tabs[2]:
    render_quiz(q_anatomy, "anatomy")

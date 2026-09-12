import streamlit as st

st.set_page_config(page_title="MSPC236 Comprehensive Quiz (74 MCQs)", layout="wide", page_icon="🫁")

st.title("🫁 MSPC236: Gastrointestinal, Renal & Reproductive Systems Quiz")
st.caption("Compiled from Exam 2030, IA 2030, and Past Papers • Includes Case Scenarios, Direct MCQs, True/False & Exceptions")

if 'answers' not in st.session_state:
    st.session_state.answers = {}

tabs = st.tabs(["🫀 Gross Anatomy, Histology & Embryology (28 Qs)", "⚡ GI, Renal & Reproductive Physiology (28 Qs)", "🧪 GI & Renal Biochemistry (18 Qs)"])

# QUESTION BANK: ANATOMY & HISTOLOGY & EMBRYOLOGY (28 Qs)
q_anatomy = [
    {
        "id": "a1", "type": "Direct MCQs",
        "q": "The epiploic foramen of Winslow provides communication between the greater and lesser peritoneal sacs. What structure forms its anterior boundary?",
        "options": ["A. Inferior vena cava", "B. Free margin of hepatoduodenal ligament (containing portal triad)", "C. Caudate lobe of liver", "D. First part of duodenum"],
        "answer": "B. Free margin of hepatoduodenal ligament (containing portal triad)",
        "exp": "Epiploic foramen boundaries: Anterior = Hepatoduodenal ligament (hepatic artery, portal vein, bile duct); Posterior = IVC; Superior = Caudate lobe; Inferior = 1st part of duodenum."
    },
    {
        "id": "a2", "type": "Direct MCQs",
        "q": "Prominent submucosal mucous glands (Brunner's glands) are characteristic histological features of which gastrointestinal tract region?",
        "options": ["A. Stomach antrum", "B. Duodenum", "C. Jejunum", "D. Ileum"],
        "answer": "B. Duodenum",
        "exp": "Brunner's glands reside in the duodenal submucosa and secrete alkaline bicarbonate-rich mucus to neutralize incoming gastric chyme."
    },
    {
        "id": "a3", "type": "Direct MCQs",
        "q": "Paneth cells, located at the base of the crypts of Lieberkühn, function in mucosal defense by secreting:",
        "options": ["A. Gastrin", "B. Lysozyme and alpha-defensins", "C. Mucin", "D. Hydrochloric acid"],
        "answer": "B. Lysozyme and alpha-defensins",
        "exp": "Paneth cells in intestinal crypt bases contain eosinophilic secretory granules filled with antimicrobial lysozyme and defensins."
    },
    {
        "id": "a4", "type": "Case Scenarios",
        "q": "A multiparous woman presents with uterine prolapse. Weakness or tearing of which pelvic floor structure is most directly responsible?",
        "options": ["A. Broad ligament", "B. Levator ani muscle (pelvic diaphragm)", "C. Round ligament of uterus", "D. Ovarian ligament"],
        "answer": "B. Levator ani muscle (pelvic diaphragm)",
        "exp": "The levator ani muscle complex (pubococcygeus, iliococcygeus) forms the main muscular pelvic floor supporting pelvic viscera."
    },
    {
        "id": "a5", "type": "Case Scenarios",
        "q": "A 28-year-old woman with a positive pregnancy test presents with severe right lower quadrant pain. Ultrasound confirms an ectopic pregnancy. What is the most common anatomical site?",
        "options": ["A. Ovary", "B. Ampulla of uterine tube", "C. Uterine cervix", "D. Pouch of Douglas"],
        "answer": "B. Ampulla of uterine tube",
        "exp": "Over 90% of ectopic pregnancies implant in the uterine tube, with the ampulla being the single most common site (~70%)."
    },
    {
        "id": "a6", "type": "Case Scenarios",
        "q": "A 65-year-old man undergoes a digital rectal examination. A hard nodule is palpated in the posterior aspect of the prostate. Which prostatic zone is affected?",
        "options": ["A. Transitional zone", "B. Central zone", "C. Peripheral zone", "D. Anterior fibromuscular stroma"],
        "answer": "C. Peripheral zone",
        "exp": "Prostatic adenocarcinoma arises predominantly in the posterior peripheral zone (palpable via DRE). Benign Prostatic Hyperplasia (BPH) arises in the transitional zone."
    },
    {
        "id": "a7", "type": "Direct MCQs",
        "q": "During vasectomy, which spermatic cord structure is surgically isolated and transected?",
        "options": ["A. Pampiniform plexus", "B. Testicular artery", "C. Vas (ductus) deferens", "D. Cremasteric artery"],
        "answer": "C. Vas (ductus) deferens",
        "exp": "Vasectomy involves bilateral transection and ligation of the vas deferens to prevent sperm entry into the ejaculate."
    },
    {
        "id": "a8", "type": "Exceptions",
        "q": "The contents of the spermatic cord include all of the following structures EXCEPT:",
        "options": ["A. Testicular artery", "B. Pampiniform venous plexus", "C. Body and head of Epididymis", "D. Genital branch of genitofemoral nerve"],
        "answer": "C. Body and head of Epididymis",
        "exp": "The epididymis lies posterolateral to the testis inside the scrotum, not within the spermatic cord."
    },
    {
        "id": "a9", "type": "Direct MCQs",
        "q": "Anatomically, normal 'anteversion' of the uterus describes the angle between the:",
        "options": ["A. Uterine body and cervix", "B. Long axis of cervix and long axis of vagina", "C. Uterus and broad ligament", "D. Cervix and rectum"],
        "answer": "B. Long axis of cervix and long axis of vagina",
        "exp": "Anteversion is the forward tipping of the cervix relative to the vagina (~90 deg). Anteflexion is the forward bending of the uterine body on the cervix (~170 deg)."
    },
    {
        "id": "a10", "type": "Case Scenarios",
        "q": "A 70-year-old man with prostatic hypertrophy and urethral obstruction presents with watery urine discharge from his umbilicus. What is the developmental cause?",
        "options": ["A. Patent vitelline duct (Omphalomesenteric duct)", "B. Urachal fistula (persistent allantois lumen)", "C. Meckel's diverticulum perforation", "D. Inguinal hernia"],
        "answer": "B. Urachal fistula (persistent allantois lumen)",
        "exp": "Failure of the urachus (allantois lumen) to obliterate leaves a patent urachal fistula connecting the bladder dome directly to the umbilicus."
    },
    {
        "id": "a11", "type": "Direct MCQs",
        "q": "Meckel's diverticulum represents a persistent remnant of which embryonic structure?",
        "options": ["A. Allantois", "B. Vitelline duct (Omphalomesenteric duct)", "C. Mesonephric duct", "D. Paramesonephric duct"],
        "answer": "B. Vitelline duct (Omphalomesenteric duct)",
        "exp": "Meckel's diverticulum is a congenital ileal outpouching resulting from incomplete obliteration of the vitelline duct."
    },
    {
        "id": "a12", "type": "Direct MCQs",
        "q": "The permanent metanephric kidney develops from which two embryonic mesodermal tissues?",
        "options": ["A. Paraxial mesoderm and Neural crest", "B. Ureteric bud and Metanephric blastema (condensed intermediate mesoderm)", "C. Lateral plate mesoderm and Endoderm", "D. Pronephros and Mesonephric duct"],
        "answer": "B. Ureteric bud and Metanephric blastema (condensed intermediate mesoderm)",
        "exp": "The ureteric bud gives rise to collecting ducts, calyces, pelvis, and ureter. The metanephric blastema forms nephrons (glomerulus to DCT)."
    },
    {
        "id": "a13", "type": "Exceptions",
        "q": "All of the following renal structures derive from the embryonic Ureteric Bud EXCEPT:",
        "options": ["A. Ureter", "B. Renal pelvis and Calyces", "C. Collecting ducts", "D. Bowman's capsule and Proximal Convoluted Tubule"],
        "answer": "D. Bowman's capsule and Proximal Convoluted Tubule",
        "exp": "Bowman's capsule, PCT, Loop of Henle, and DCT derive from the metanephric blastema."
    },
    {
        "id": "a14", "type": "Direct MCQs",
        "q": "In newborns, lobulated surface appearance of the kidneys is a normal anatomical finding resulting from:",
        "options": ["A. Polycystic kidney disease", "B. Cascade development of nephron clusters from metanephric caps over ureteric bud branches", "C. Vascular compromise", "D. Hydronephrosis"],
        "answer": "B. Cascade development of nephron clusters from metanephric caps over ureteric bud branches",
        "exp": "Fetal renal lobulation reflects underlying pyramids and renal lobes, which fuse during childhood."
    },
    {
        "id": "a15", "type": "Exceptions",
        "q": "Which of the following congenital renal anomalies is NOT compatible with life?",
        "options": ["A. Unilateral renal agenesis", "B. Horseshoe kidney", "C. Bilateral renal agenesis (Potter sequence)", "D. Ectopic pelvic kidney"],
        "answer": "C. Bilateral renal agenesis (Potter sequence)",
        "exp": "Bilateral renal agenesis leads to anhydramnios, pulmonary hypoplasia, facial anomalies, and neonatal death."
    },
    {
        "id": "a16", "type": "Direct MCQs",
        "q": "The cremasteric muscle and cremasteric fascia are derived from which anterior abdominal wall layer?",
        "options": ["A. External oblique aponeurosis", "B. Internal oblique muscle/aponeurosis", "C. Transversus abdominis", "D. Transversalis fascia"],
        "answer": "B. Internal oblique muscle/aponeurosis",
        "exp": "Spermatic cord coverings: External spermatic fascia = External oblique; Cremasteric fascia = Internal oblique; Internal spermatic fascia = Transversalis fascia."
    },
    {
        "id": "a17", "type": "Direct MCQs",
        "q": "The rectouterine pouch (Pouch of Douglas) represents the lowest peritoneal space in females between the:",
        "options": ["A. Bladder and uterus", "B. Posterior uterine wall and anterior rectum", "C. Ovary and broad ligament", "D. Pubic bone and bladder"],
        "answer": "B. Posterior uterine wall and anterior rectum",
        "exp": "The rectouterine pouch is the dependent peritoneal pouch where pelvic fluid, blood, or pus accumulates."
    },
    {
        "id": "a18", "type": "Direct MCQs",
        "q": "Primordial germ cells origin in early embryonic development is located in the:",
        "options": ["A. Gonadal ridge mesoderm", "B. Endodermal wall of the yolk sac near the allantois", "C. Mesonephric duct", "D. Neural crest"],
        "answer": "B. Endodermal wall of the yolk sac near the allantois",
        "exp": "PGCs arise in the umbilical yolk sac endoderm during week 3 and migrate along the dorsal mesentery into the genital ridges by week 5-6."
    },
    {
        "id": "a19", "type": "Direct MCQs",
        "q": "In the male fetus, anti-Müllerian hormone (AMH) secreted by Sertoli cells causes regression of which duct system?",
        "options": ["A. Mesonephric (Wolffian) ducts", "B. Paramesonephric (Müllerian) ducts", "C. Metanephric duct", "D. Vitelline duct"],
        "answer": "B. Paramesonephric (Müllerian) ducts",
        "exp": "Sertoli cell AMH causes regression of Müllerian ducts (which otherwise form uterus/fallopian tubes). Leydig cell testosterone stabilizes Wolffian ducts."
    },
    {
        "id": "a20", "type": "Exceptions",
        "q": "Derivatives of the embryonic Hindgut include all of the following EXCEPT:",
        "options": ["A. Distal one-third of transverse colon", "B. Descending and Sigmoid colon", "C. Rectum and upper anal canal", "D. Appendix and Cecum"],
        "answer": "D. Appendix and Cecum",
        "exp": "Cecum and appendix develop from the midgut loop (supplied by SMA). Hindgut is supplied by IMA."
    },
    {
        "id": "a21", "type": "Direct MCQs",
        "q": "The main pancreatic duct of Wirsung fuses with the common bile duct to form the hepatopancreatic ampulla of Vater, opening into the duodenum at the:",
        "options": ["A. Minor duodenal papilla", "B. Major duodenal papilla", "C. Pyloric sphincter", "D. Duodenojejunal flexure"],
        "answer": "B. Major duodenal papilla",
        "exp": "The ampulla of Vater opens into the 2nd part of the duodenum at the major duodenal papilla, controlled by the sphincter of Oddi."
    },
    {
        "id": "a22", "type": "Direct MCQs",
        "q": "The Blood-Testis Barrier is formed by specialized intercellular tight junctions between adjacent:",
        "options": ["A. Leydig cells", "B. Sertoli cells", "C. Spermatogonia", "D. Myoid cells"],
        "answer": "B. Sertoli cells",
        "exp": "Sertoli cell tight junctions divide the seminiferous epithelium into basal and adluminal compartments, shielding haploid germ cells from immune attack."
    },
    {
        "id": "a23", "type": "Case Scenarios",
        "q": "A neonate presents with failure to pass meconium within 48 hours of birth, abdominal distension, and bilious vomiting. Rectal biopsy shows absence of autonomic ganglion cells in the myenteric plexus. What is the diagnosis?",
        "options": ["A. Pyloric stenosis", "B. Hirschsprung disease (Congenital megacolon)", "C. Imperforate anus", "D. Meckel's diverticulum"],
        "answer": "B. Hirschsprung disease (Congenital megacolon)",
        "exp": "Hirschsprung disease results from failed neural crest migration to the distal bowel, leaving distal colon aganglionic (lacking Meissner and Auerbach plexuses)."
    },
    {
        "id": "a24", "type": "Direct MCQs",
        "q": "Which artery supplies derivatives of the embryonic Foregut (stomach, liver, spleen, upper duodenum)?",
        "options": ["A. Celiac trunk", "B. Superior mesenteric artery", "C. Inferior mesenteric artery", "D. Internal iliac artery"],
        "answer": "A. Celiac trunk",
        "exp": "Foregut = Celiac trunk; Midgut = Superior Mesenteric Artery (SMA); Hindgut = Inferior Mesenteric Artery (IMA)."
    },
    {
        "id": "a25", "type": "Direct MCQs",
        "q": "In the liver, microscopic Spaces of Disse represent perisinusoidal spaces located between hepatocytes and:",
        "options": ["A. Central veins", "B. Fenestrated sinusoidal endothelial cells", "C. Bile canaliculi", "D. Glisson's capsule"],
        "answer": "B. Fenestrated sinusoidal endothelial cells",
        "exp": "The Space of Disse lies between hepatocyte microvilli and sinusoidal endothelia, housing stellate Ito cells (storing Vitamin A)."
    },
    {
        "id": "a26", "type": "Direct MCQs",
        "q": "The Glomerular Filtration Barrier consists of fenestrated capillary endothelium, glomerular basement membrane, and filtration slits formed by:",
        "options": ["A. Parietal epithelial cells", "B. Podocyte pedicels (foot processes)", "C. Mesangial cells", "D. Macula densa cells"],
        "answer": "B. Podocyte pedicels (foot processes)",
        "exp": "Visceral epithelial podocytes interdigitate over capillaries, forming filtration slits bridged by nephrin diaphragms."
    },
    {
        "id": "a27", "type": "Direct MCQs",
        "q": "The female urethra is lined proximally by transitional epithelium and distally by:",
        "options": ["A. Simple columnar epithelium", "B. Non-keratinized stratified squamous epithelium", "C. Pseudostratified columnar epithelium", "D. Simple cuboidal epithelium"],
        "answer": "B. Non-keratinized stratified squamous epithelium",
        "exp": "The short female urethra transitions from transitional near the bladder neck to non-keratinized stratified squamous near the external meatus."
    },
    {
        "id": "a28", "type": "Exceptions",
        "q": "Anatomical characteristics distinguishing the female pelvis from the male pelvis include all EXCEPT:",
        "options": ["A. Wider subpubic angle (>80-90 deg)", "B. Broad, oval pelvic inlet", "C. Narrow, heart-shaped pelvic inlet", "D. Less prominent ischial spines"],
        "answer": "C. Narrow, heart-shaped pelvic inlet",
        "exp": "A narrow, heart-shaped pelvic inlet and acute subpubic angle (<70 deg) are typical android (male) pelvic features."
    }
]

# QUESTION BANK: PHYSIOLOGY (28 Qs)
q_physio = [
    {
        "id": "p1", "type": "Direct MCQs",
        "q": "A 70-kg healthy male has a Total Body Water (TBW) of 42 L. What is his estimated Extracellular Fluid (ECF) volume?",
        "options": ["A. 7 L", "B. 14 L", "C. 21 L", "D. 28 L"],
        "answer": "B. 14 L",
        "exp": "TBW (60% body weight) is 42 L. ICF is 2/3 of TBW (28 L); ECF is 1/3 of TBW (14 L)."
    },
    {
        "id": "p2", "type": "Direct MCQs",
        "q": "In a 70-kg male with a plasma volume of 3.0 L and a Hematocrit (PCV) of 40%, what is the total blood volume?",
        "options": ["A. 4.0 L", "B. 5.0 L", "C. 6.0 L", "D. 7.0 L"],
        "answer": "B. 5.0 L",
        "exp": "Blood Volume = Plasma Volume / (1 - Hct) = 3.0 L / (1 - 0.40) = 3.0 / 0.60 = 5.0 L."
    },
    {
        "id": "p3", "type": "Direct MCQs",
        "q": "Which indicator substance is used to measure Total Body Water using the indicator dilution principle?",
        "options": ["A. Inulin / Mannitol", "B. Deuterium oxide (D2O) / Tritiated water", "C. Evans blue dye / Radioiodinated albumin", "D. Radio-chromium RBCs"],
        "answer": "B. Deuterium oxide (D2O) / Tritiated water",
        "exp": "Heavy water (D2O) distributes freely across all cell membranes throughout total body water."
    },
    {
        "id": "p4", "type": "Direct MCQs",
        "q": "Extracellular Fluid (ECF) compartment volume can be measured specifically using:",
        "options": ["A. D2O", "B. Inulin / Mannitol", "C. Evans blue", "D. Antipyrine"],
        "answer": "B. Inulin / Mannitol",
        "exp": "Inulin and mannitol cross capillary walls into interstitial fluid but cannot penetrate cell membranes, measuring ECF."
    },
    {
        "id": "p5", "type": "Direct MCQs",
        "q": "Antidiuretic Hormone (ADH / Vasopressin) increases principal cell water reabsorption in collecting ducts by inserting:",
        "options": ["A. Aquaporin-1", "B. Aquaporin-2 into apical membranes", "C. Aquaporin-3 / 4 into basolateral membranes", "D. ENaC channels"],
        "answer": "B. Aquaporin-2 into apical membranes",
        "exp": "V2 receptor activation increases cAMP, triggering exocytosis of Aquaporin-2 storage vesicles to the apical membrane."
    },
    {
        "id": "p6", "type": "Direct MCQs",
        "q": "What is the most potent physiological stimulus for hypothalamic ADH secretion?",
        "options": ["A. Decreased blood pressure", "B. Increased plasma osmolality (detected by osmoreceptors)", "C. Hyponatremia", "D. Atrial natriuretic peptide"],
        "answer": "B. Increased plasma osmolality (detected by osmoreceptors)",
        "exp": "A 1% increase in plasma osmolality stimulates ADH release via organum vasculosum osmoreceptors; hypovolemia requires a 10% drop."
    },
    {
        "id": "p7", "type": "Direct MCQs",
        "q": "In tubuloglomerular feedback (TGF), which specialized tubular cell structure senses luminal NaCl delivery?",
        "options": ["A. Podocytes", "B. Macula densa of early distal tubule", "C. Granular juxtaglomerular cells", "D. Principal cells"],
        "answer": "B. Macula densa of early distal tubule",
        "exp": "Macula densa cells sense luminal NaCl via NKCC2 cotransporters and release adenosine/ATP to constrict afferent arterioles when NaCl is elevated."
    },
    {
        "id": "p8", "type": "Direct MCQs",
        "q": "Renin is synthesized, stored, and secreted by which kidney cells?",
        "options": ["A. Macula densa cells", "B. Granular juxtaglomerular (JG) cells of afferent arteriole", "C. Podocytes", "D. Mesangial cells"],
        "answer": "B. Granular juxtaglomerular (JG) cells of afferent arteriole",
        "exp": "JG vascular smooth muscle cells in afferent arterioles synthesize and release renin in response to low renal perfusion or low NaCl."
    },
    {
        "id": "p9", "type": "Direct MCQs",
        "q": "Final 1-alpha-hydroxylation converting 25-hydroxyvitamin D into active 1,25-dihydroxyvitamin D3 (Calcitriol) occurs in:",
        "options": ["A. Liver hepatocytes", "B. Skin keratinocytes", "C. Renal proximal convoluted tubule cells", "D. Distal tubule cells"],
        "answer": "C. Renal proximal convoluted tubule cells",
        "exp": "Mitochondrial 1-alpha-hydroxylase in proximal tubule cells converts 25(OH)D3 into active calcitriol under PTH stimulation."
    },
    {
        "id": "p10", "type": "Direct MCQs",
        "q": "Primary Starling force driving ultrafiltration across glomerular capillaries into Bowman's space is:",
        "options": ["A. Bowman's space hydrostatic pressure", "B. Glomerular capillary hydrostatic pressure (Pgc ~45-50 mmHg)", "C. Glomerular capillary oncotic pressure", "D. Interstitial pressure"],
        "answer": "B. Glomerular capillary hydrostatic pressure (Pgc ~45-50 mmHg)",
        "exp": "High Pgc maintained by afferent/efferent arteriolar resistance tone provides the main driving force favoring filtration."
    },
    {
        "id": "p11", "type": "Direct MCQs",
        "q": "Selective dilation of the renal afferent arteriole produces which hemodynamic changes?",
        "options": ["A. Decreased GFR and decreased RBF", "B. Increased Glomerular Hydrostatic Pressure, Increased GFR, and Increased RBF", "C. Decreased Pgc and increased GFR", "D. No change"],
        "answer": "B. Increased Glomerular Hydrostatic Pressure, Increased GFR, and Increased RBF",
        "exp": "Dilating the afferent arteriole reduces upstream resistance, increasing blood flow and hydrostatic pressure inside glomerular capillaries."
    },
    {
        "id": "p12", "type": "Case Scenarios",
        "q": "A patient with primary hyperaldosteronism (Conn syndrome) will typically display which acid-base and electrolyte pattern?",
        "options": ["A. Hyperkalemic metabolic acidosis", "B. Hypokalemic metabolic alkalosis with hypertension", "C. Hyponatremic metabolic acidosis", "D. Hypercalcemic alkalosis"],
        "answer": "B. Hypokalemic metabolic alkalosis with hypertension",
        "exp": "Aldosterone stimulates principal cell Na+ reabsorption and K+ secretion, and alpha-intercalated cell H+ secretion, causing hypokalemia and metabolic alkalosis."
    },
    {
        "id": "p13", "type": "Case Scenarios",
        "q": "A 55-year-old patient with adrenal destruction (Addison disease / aldosterone deficiency) presents with hypotension. What electrolyte abnormality is expected?",
        "options": ["A. Hypokalemia and hypernatremia", "B. Hyponatremia, hyperkalemia, and metabolic acidosis", "C. Hypercalcemia and hypokalemia", "D. Normal potassium"],
        "answer": "B. Hyponatremia, hyperkalemia, and metabolic acidosis",
        "exp": "Loss of aldosterone impairs renal Na+ reabsorption and K+/H+ excretion, causing renal salt wasting, hyperkalemia, and acidosis."
    },
    {
        "id": "p14", "type": "Case Scenarios",
        "q": "A patient with polyuria is subjected to water deprivation. Urine osmolality remains low. Following synthetic desmopressin (ADH) injection, urine osmolality increases by 300%. What is the diagnosis?",
        "options": ["A. Nephrogenic diabetes insipidus", "B. Central diabetes insipidus", "C. Primary polydipsia", "D. SIADH"],
        "answer": "B. Central diabetes insipidus",
        "exp": "Central DI lacks pituitary ADH release, so kidneys respond normally to exogenous desmopressin. Nephrogenic DI fails to respond to desmopressin."
    },
    {
        "id": "p15", "type": "Direct MCQs",
        "q": "Cholecystokinin (CCK) is secreted by I-cells in the duodenum in response to fatty acids and amino acids. CCK stimulates:",
        "options": ["A. Gastric acid secretion", "B. Gallbladder contraction and pancreatic acinar enzyme secretion", "C. Pancreatic duct bicarbonate release", "D. Intestinal motility inhibition"],
        "answer": "B. Gallbladder contraction and pancreatic acinar enzyme secretion",
        "exp": "CCK causes gallbladder smooth muscle contraction, sphincter of Oddi relaxation, and pancreatic acinar zymogen secretion."
    },
    {
        "id": "p16", "type": "Direct MCQs",
        "q": "Secretin is released by S-cells in the duodenal mucosa in response to low luminal pH (<4.5). Secretin acts on pancreatic duct cells to stimulate:",
        "options": ["A. Pancreatic digestive enzyme secretion", "B. Bicarbonate-rich fluid secretion via cAMP elevation", "C. Gastric emptying", "D. Bile acid synthesis"],
        "answer": "B. Bicarbonate-rich fluid secretion via cAMP elevation",
        "exp": "Secretin opens CFTR Cl- channels and Cl-/HCO3- exchangers in pancreatic duct cells, producing alkaline bicarbonate fluid to neutralize gastric acid."
    },
    {
        "id": "p17", "type": "Direct MCQs",
        "q": "Which gastrointestinal hormone initiates the interdigestive Migrating Motor Complex (MMC) every 90-120 minutes during fasting?",
        "options": ["A. Gastrin", "B. Secretin", "C. Motilin", "D. VIP"],
        "answer": "C. Motilin",
        "exp": "Motilin, secreted by M-cells during fasting, triggers cyclical Phase III MMC contractions to sweep food remnants toward the colon."
    },
    {
        "id": "p18", "type": "Case Scenarios",
        "q": "A patient with Zollinger-Ellison syndrome has a gastrin-secreting neuroendocrine tumor. Gastrin stimulates parietal cell H+ secretion directly and indirectly via releasing:",
        "options": ["A. Somatostatin from D cells", "B. Histamine from Enterochromaffin-like (ECL) cells", "C. Acetylcholine from vagal fibers", "D. Secretin"],
        "answer": "B. Histamine from Enterochromaffin-like (ECL) cells",
        "exp": "Gastrin binds CCK-B receptors on ECL cells, stimulating powerful paracrine histamine release that drives parietal cell proton pumps."
    },
    {
        "id": "p19", "type": "Direct MCQs",
        "q": "In parietal cells, proton secretion into the gastric lumen by H+/K+ ATPase is directly inhibited by which drug class?",
        "options": ["A. H2 receptor antagonists", "B. Proton Pump Inhibitors (PPIs like Omeprazole)", "C. Antacids", "D. Muscarinic antagonists"],
        "answer": "B. Proton Pump Inhibitors (PPIs like Omeprazole)",
        "exp": "PPIs covalently bind and irreversibly inhibit the apical H+/K+ ATPase pump."
    },
    {
        "id": "p20", "type": "Direct MCQs",
        "q": "Primary peristaltic waves in the esophagus and gastric motility are initiated during deglutition by autonomic impulses carried in the:",
        "options": ["A. Sympathetic splanchnic nerves", "B. Vagus nerve (CN X)", "C. Pelvic splanchnic nerves", "D. Phrenic nerve"],
        "answer": "B. Vagus nerve (CN X)",
        "exp": "Vagal efferents mediate swallowing peristalsis and receptive relaxation of the gastric fundus."
    },
    {
        "id": "p21", "type": "Direct MCQs",
        "q": "Primary active transport of sodium across the basolateral membrane of renal tubular cells is executed by:",
        "options": ["A. SGLT-2 transporters", "B. Na+/K+ ATPase pumps", "C. NKCC2 cotransporters", "D. Na+/H+ exchangers"],
        "answer": "B. Na+/K+ ATPase pumps",
        "exp": "Basolateral Na+/K+ ATPase pumps 3 Na+ out and 2 K+ in, maintaining low intracellular Na+ that drives secondary active luminal transport."
    },
    {
        "id": "p22", "type": "Case Scenarios",
        "q": "A woman experiences immediate urge to defecate shortly after consuming a large breakfast. This reflex is known as the:",
        "options": ["A. Enterogastric reflex", "B. Gastrocolic reflex", "C. Intestino-intestinal reflex", "D. Defecation spinal reflex"],
        "answer": "B. Gastrocolic reflex",
        "exp": "Gastric distension and food entry stimulate parasympathetic/motilin signals that increase colonic mass movements (gastrocolic reflex)."
    },
    {
        "id": "p23", "type": "Direct MCQs",
        "q": "In the two-cell, two-gonadotropin model of ovarian steroidogenesis, LH acts on Theca cells to stimulate production of:",
        "options": ["A. Estrogens directly", "B. Androstenedione and testosterone", "C. Progesterone alone", "D. Inhibin B"],
        "answer": "B. Androstenedione and testosterone",
        "exp": "LH stimulates theca cells to synthesize androgens. Androgens diffuse into granulosa cells, where FSH stimulates aromatase to convert them into estrogens."
    },
    {
        "id": "p24", "type": "Direct MCQs",
        "q": "Ovulation and luteinization of granulosa cells are directly triggered by the mid-cycle surge of:",
        "options": ["A. Progesterone", "B. Luteinizing Hormone (LH)", "C. Follicle-Stimulating Hormone (FSH)", "D. Human Chorionic Gonadotropin (hCG)"],
        "answer": "B. Luteinizing Hormone (LH)",
        "exp": "High sustained preovulatory estrogen levels exert positive feedback on the pituitary, triggering the massive LH surge that induces follicular rupture."
    },
    {
        "id": "p25", "type": "Direct MCQs",
        "q": "Spermatozoa ejaculated into the female genital tract undergo essential glycoprotein coat removal and membrane fluidization called:",
        "options": ["A. Acrosome reaction", "B. Capacitation", "C. Spermiogenesis", "D. Cortical reaction"],
        "answer": "B. Capacitation",
        "exp": "Capacitation in the female tract removes inhibitory seminal plasma proteins, increases Ca2+ influx, and hyperactivates flagellar motility."
    },
    {
        "id": "p26", "type": "Direct MCQs",
        "q": "During fertilization, sperm binding to ZP3 triggers the acrosome reaction. Polyspermy is subsequently prevented by the:",
        "options": ["A. Capacitation phase", "B. Cortical reaction (exocytosis of cortical granules altering ZP3)", "C. Luteal phase", "D. Cumulative pressure"],
        "answer": "B. Cortical reaction (exocytosis of cortical granules altering ZP3)",
        "exp": "Ca2+ wave upon sperm fusion causes cortical granule exocytosis, cleaving ZP3 and hardening the zona pellucida (slow block to polyspermy)."
    },
    {
        "id": "p27", "type": "Direct MCQs",
        "q": "In early pregnancy, syncytiotrophoblast cells secrete which hormone to maintain the corpus luteum and progesterone production?",
        "options": ["A. Human Chorionic Gonadotropin (hCG)", "B. Human Placental Lactogen", "C. Prolactin", "D. Estriol"],
        "answer": "A. Human Chorionic Gonadotropin (hCG)",
        "exp": "hCG mimics LH to rescue the corpus luteum, sustaining progesterone production through the first trimester until placental shift."
    },
    {
        "id": "p28", "type": "Direct MCQs",
        "q": "Atrial Natriuretic Peptide (ANP), released in response to atrial stretch, promotes natriuresis and diuresis by:",
        "options": ["A. Constricting afferent arterioles", "B. Dilating afferent arterioles, constricting efferent arterioles, and inhibiting Na+ reabsorption in medullary collecting ducts", "C. Stimulating aldosterone release", "D. Stimulating renin secretion"],
        "answer": "B. Dilating afferent arterioles, constricting efferent arterioles, and inhibiting Na+ reabsorption in medullary collecting ducts",
        "exp": "ANP increases GFR (afferent dilation/efferent constriction) and directly inhibits principal cell ENaC channels and renin/aldosterone."
    }
]

# QUESTION BANK: BIOCHEMISTRY (18 Qs)
q_biochem = [
    {
        "id": "b1", "type": "Direct MCQs",
        "q": "Glucose and galactose are absorbed across the apical lumen of enterocytes via which sodium-dependent active transporter?",
        "options": ["A. GLUT-2", "B. SGLT-1 (Sodium-Glucose Cotransporter 1)", "C. GLUT-5", "D. GLUT-4"],
        "answer": "B. SGLT-1 (Sodium-Glucose Cotransporter 1)",
        "exp": "SGLT-1 utilizes the Na+ electrochemical gradient to secondary-actively transport glucose/galactose into enterocytes. GLUT-5 transports fructose; GLUT-2 exits basolaterally."
    },
    {
        "id": "b2", "type": "Direct MCQs",
        "q": "Fructose is absorbed across the apical membrane of intestinal enterocytes via facilitated diffusion by:",
        "options": ["A. SGLT-1", "B. GLUT-5", "C. GLUT-2", "D. SGLT-2"],
        "answer": "B. GLUT-5", "exp": "GLUT-5 is a specific facilitated diffusion hexose transporter for fructose on the apical luminal enterocyte membrane."
    },
    {
        "id": "b3", "type": "Case Scenarios",
        "q": "A patient following total gastrectomy lacks intrinsic factor. This causes pernicious anemia because intrinsic factor is required for receptor-mediated absorption of Vitamin B12 in the:",
        "options": ["A. Duodenum", "B. Jejunum", "C. Terminal ileum", "D. Colon"],
        "answer": "C. Terminal ileum",
        "exp": "Intrinsic factor-B12 complexes bind cubam receptors on enterocytes in the terminal ileum for receptor-mediated endocytosis."
    },
    {
        "id": "b4", "type": "Direct MCQs",
        "q": "Pancreatic zymogens (trypsinogen, chymotrypsinogen) are activated in the duodenal lumen. What intestinal brush-border enzyme initiates this cascade by cleaving trypsinogen?",
        "options": ["A. Pepsin", "B. Enteropeptidase (Enterokinase)", "C. Carboxypeptidase", "D. Elastase"],
        "answer": "B. Enteropeptidase (Enterokinase)",
        "exp": "Duodenal mucosa enteropeptidase cleaves trypsinogen to active trypsin, which then auto-activates all other pancreatic zymogens."
    },
    {
        "id": "b5", "type": "Direct MCQs",
        "q": "Dietary long-chain triacylglycerols are hydrolyzed in the small intestine primary by pancreatic lipase, requiring which helper protein for lipid interface anchoring?",
        "options": ["A. Apolipoprotein C-II", "B. Colipase", "C. Bile salt exporter", "D. Phospholipase A2"],
        "answer": "B. Colipase",
        "exp": "Pancreatic colipase binds bile-salt-coated lipid droplets and anchors pancreatic lipase to hydrolyze TAGs into 2-monoacylglycerol and free fatty acids."
    },
    {
        "id": "b6", "type": "Direct MCQs",
        "q": "Absorbed dietary lipids are re-esterified inside enterocytes and packaged into which lipoprotein for lymphatic transport via the thoracic duct?",
        "options": ["A. VLDL", "B. Chylomicrons", "C. HDL", "D. LDL"],
        "answer": "B. Chylomicrons",
        "exp": "Enterocytes synthesize ApoB-48 and assemble triacylglycerols, cholesterol esters, and fat-soluble vitamins into chylomicrons, which enter lacteals."
    },
    {
        "id": "b7", "type": "Direct MCQs",
        "q": "In hepatocytes, unconjugated bilirubin is rendered water-soluble for biliary excretion by conjugation with glucuronic acid by which enzyme?",
        "options": ["A. Biliverdin reductase", "B. UDP-glucuronosyltransferase (UGT1A1)", "C. Heme oxygenase", "D. Beta-glucuronidase"],
        "answer": "B. UDP-glucuronosyltransferase (UGT1A1)",
        "exp": "UGT1A1 transfers two glucuronic acid molecules from UDP-glucuronic acid to bilirubin, forming water-soluble bilirubin diglucuronide."
    },
    {
        "id": "b8", "type": "Direct MCQs",
        "q": "Primary bile acids synthesized from cholesterol in human hepatocytes are:",
        "options": ["A. Deoxycholic acid and Lithocholic acid", "B. Cholic acid and Chenodeoxycholic acid", "C. Ursodeoxycholic acid and Taurocholate", "D. Bilirubin and Biliverdin"],
        "answer": "B. Cholic acid and Chenodeoxycholic acid",
        "exp": "Cholesterol 7-alpha-hydroxylase initiates synthesis of primary bile acids: cholic acid and chenodeoxycholic acid. Intestinal bacteria convert them to secondary bile acids (deoxycholic and lithocholic)."
    },
    {
        "id": "b9", "type": "Direct MCQs",
        "q": "Rate-limiting step in bile acid biosynthesis from cholesterol is catalyzed by:",
        "options": ["A. HMG-CoA reductase", "B. Cholesterol 7-alpha-hydroxylase (CYP7A1)", "C. Acyl-CoA cholesterol acyltransferase", "D. 27-hydroxylase"],
        "answer": "B. Cholesterol 7-alpha-hydroxylase (CYP7A1)",
        "exp": "CYP7A1 is the rate-limiting enzyme in hepatic bile acid synthesis and is feedback-inhibited by bile salts returning via enterohepatic circulation."
    },
    {
        "id": "b10", "type": "Direct MCQs",
        "q": "Glucose reabsorption in the proximal convoluted tubule S1/S2 segments across the apical membrane occurs via:",
        "options": ["A. SGLT-2 (Sodium-Glucose Cotransporter 2)", "B. SGLT-1", "C. GLUT-1", "D. GLUT-4"],
        "answer": "A. SGLT-2 (Sodium-Glucose Cotransporter 2)",
        "exp": "SGLT-2 reabsorbs ~90% of filtered glucose in the early PCT (targeted by gliflozin drugs). SGLT-1 reabsorbs remaining 10% in S3."
    },
    {
        "id": "b11", "type": "Direct MCQs",
        "q": "The Thick Ascending Limb (TAL) of Henle's loop reabsorbs Na+, K+, and Cl- via which luminal cotransporter, inhibited by loop diuretics like Furosemide?",
        "options": ["A. NCC (Na+/Cl- cotransporter)", "B. NKCC2 (Na+/K+/2Cl- cotransporter)", "C. ENaC channels", "D. SGLT-2"],
        "answer": "B. NKCC2 (Na+/K+/2Cl- cotransporter)",
        "exp": "Apical NKCC2 in the TAL reabsorbs 1 Na+, 1 K+, and 2 Cl-. Furosemide blocks NKCC2, dissipating the corticomedullary osmotic gradient."
    },
    {
        "id": "b12", "type": "Direct MCQs",
        "q": "Thiazide diuretics (e.g. Hydrochlorothiazide) inhibit sodium and chloride reabsorption in the Distal Convoluted Tubule by blocking:",
        "options": ["A. NKCC2 cotransporters", "B. NCC (Electroneutral Na+/Cl- cotransporter)", "C. ENaC channels", "D. Carbonic anhydrase"],
        "answer": "B. NCC (Electroneutral Na+/Cl- cotransporter)",
        "exp": "Thiazides specifically block the apical NCC cotransporter in the DCT."
    },
    {
        "id": "b13", "type": "Direct MCQs",
        "q": "In proximal tubule cells, Carbonic Anhydrase II and IV are essential for reabsorbing 80-85% of filtered:",
        "options": ["A. Glucose", "B. Bicarbonate (HCO3-)", "C. Urea", "D. Calcium"],
        "answer": "B. Bicarbonate (HCO3-)",
        "exp": "Luminal CA IV converts filtered HCO3- + H+ to CO2 and H2O, allowing CO2 diffusion into PCT cells, where cytosolic CA II regenerates HCO3- for basolateral transport."
    },
    {
        "id": "b14", "type": "Direct MCQs",
        "q": "Primary renal mechanism for generating NEW bicarbonate ions during chronic metabolic acidosis is:",
        "options": ["A. Increased SGLT-2 transport", "B. Proximal tubule Ammoniagenesis (glutamine metabolism to 2 NH4+ and 2 HCO3-)", "C. Distal urea reabsorption", "D. Phosphate filtration reduction"],
        "answer": "B. Proximal tubule Ammoniagenesis (glutamine metabolism to 2 NH4+ and 2 HCO3-)",
        "exp": "PCT deamination of glutamine produces 2 NH4+ (excreted in urine) and 2 new HCO3- ions (reabsorbed into blood)."
    },
    {
        "id": "b15", "type": "Direct MCQs",
        "q": "Which enzyme converts testosterone to the more potent androgen Dihydrotestosterone (DHT) in male external genitalia and prostate stroma?",
        "options": ["A. Aromatase", "B. 5-alpha-reductase", "C. 17-beta-hydroxysteroid dehydrogenase", "D. 21-hydroxylase"],
        "answer": "B. 5-alpha-reductase",
        "exp": "5-alpha-reductase converts testosterone to DHT, which mediates virilization of male external genitalia and prostate growth."
    },
    {
        "id": "b16", "type": "Direct MCQs",
        "q": "Aromatase (CYP19A1) catalyzes the conversion of testosterone and androstenedione into:",
        "options": ["A. Dihydrotestosterone", "B. Estradiol and Estrone", "C. Progesterone", "D. Cortisol"],
        "answer": "B. Estradiol and Estrone",
        "exp": "Aromatase in ovarian granulosa cells, adipose tissue, and placenta converts C19 androgens into C18 estrogens."
    },
    {
        "id": "b17", "type": "Exceptions",
        "q": "Which of the following compounds is NOT a constituent of normal seminal vesicle secretions?",
        "options": ["A. Fructose (nutrient for sperm motility)", "B. Prostaglandins", "C. Semenogelin (coagulating protein)", "D. Prostate-Specific Antigen (PSA)"],
        "answer": "D. Prostate-Specific Antigen (PSA)",
        "exp": "PSA is a serine protease secreted by prostatic glandular epithelium, which liquefies the seminal coagulum."
    },
    {
        "id": "b18", "type": "Direct MCQs",
        "q": "Prostate-Specific Antigen (PSA) functions biochemically in semen as a:",
        "options": ["A. Transglutaminase", "B. Serine protease that cleaves semenogelin to liquefy ejaculated semen", "C. Glycolytic enzyme", "D. Lipid esterase"],
        "answer": "B. Serine protease that cleaves semenogelin to liquefy ejaculated semen",
        "exp": "PSA hydrolyzes semenogelin proteins formed by seminal vesicles, liquefying the seminal clot 15-20 minutes post-ejaculation."
    }
]

def render_quiz(q_list, tab_key):
    st.write(f"**Total Questions: {len(q_list)}**")
    filter_type = st.selectbox(f"Filter Question Type ({tab_key}):", ["All", "Case Scenarios", "Direct MCQs", "True or False", "Exceptions"], key=f"f_{tab_key}")
    filtered = q_list if filter_type == "All" else [q for q in q_list if q['type'] == filter_type]
    
    for idx, item in enumerate(filtered):
        st.markdown("---")
        st.markdown(f"**Q{idx+1} [{item['type']}]: {item['q']}**")
        ans_key = f"key_{tab_key}_{item['id']}"
        choice = st.radio("Select option:", item['options'], key=ans_key)
        
        if st.button(f"Submit Q{idx+1}", key=f"btn_{ans_key}"):
            st.session_state.answers[ans_key] = choice
            
        if ans_key in st.session_state.answers:
            user_ans = st.session_state.answers[ans_key]
            if user_ans == item['answer']:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. Correct Answer: **{item['answer']}**")
            with st.expander("💡 High-Yield Explanation"):
                st.info(item['exp'])

with tabs[0]:
    render_quiz(q_anatomy, "anatomy")

with tabs[1]:
    render_quiz(q_physio, "physio")

with tabs[2]:
    render_quiz(q_biochem, "biochem")

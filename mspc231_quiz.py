import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# ------------------------------------------------------------------------------
# 1. STREAMLIT CONFIG & GOOGLE SHEETS INITIALIZATION
# ------------------------------------------------------------------------------
st.set_page_config(page_title="MSPC 231 Interactive Quiz & Tracker", layout="wide")

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
                st.rerun()
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

st.sidebar.markdown(f"👤 **Logged-in Student:**\n- **Name:** {student['name']}\n- **ID:** `{student['id']}`")

if st.sidebar.button("Log Out / Switch Student"):
    st.session_state.verified_user = None
    st.rerun()

st.title("🎓 MSPC 231: Cell Biology, Histology & Physiology (120 Questions)")
st.caption("Interactive Comprehensive Question Bank grounded in Compiled Past Exam Questions.")

tab1, tab2, tab3 = st.tabs(["🫀 Anatomy & Histology (40 Qs)", "⚡ Physiology (40 Qs)", "🧪 Biochemistry & Bioenergetics (40 Qs)"])

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
                    module_name="MSPC231",
                    category=category_name,
                    question_text=q["question"],
                    selected_option=user_choice,
                    correct_answer=q["answer"],
                    is_correct=is_correct
                )
                st.session_state[f"logged_{key}"] = True
        st.divider()


ANAT_QS = [
    {
        "id": 1,
        "question": "Which of the following cellular structures best distinguishes eukaryotic cells from prokaryotic cells?",
        "options": [
            "Ability to reproduce",
            "Ability to undergo metabolism",
            "Presence of a plasma membrane",
            "Presence of membrane-bound organelles",
            "Presence of ribosomes"
        ],
        "answer": "Presence of membrane-bound organelles",
        "explanation": "Eukaryotic cells are defined by the presence of a membrane-enclosed nucleus and membrane-bound organelles such as mitochondria and lysosomes, whereas prokaryotes lack these structures."
    },
    {
        "id": 2,
        "question": "In cells with a well-defined nucleus, which organelle is primarily responsible for modifying, sorting, and packaging proteins and lipids received from the endoplasmic reticulum?",
        "options": [
            "Centrioles",
            "Golgi Apparatus",
            "Lysosomes",
            "Peroxisome",
            "Ribosome"
        ],
        "answer": "Golgi Apparatus",
        "explanation": "The Golgi apparatus modifies proteins (e.g., glycosylation) and packages them into vesicles for transport to lysosomes, the plasma membrane, or secretion."
    },
    {
        "id": 3,
        "question": "Gaucher disease primarily results from a hereditary enzyme deficiency leading to the abnormal accumulation of glucosylceramide within which cell organelle?",
        "options": [
            "Endoplasmic Reticulum",
            "Golgi apparatus",
            "Lysosomes",
            "Mitochondria",
            "Peroxisomes"
        ],
        "answer": "Lysosomes",
        "explanation": "Gaucher disease is a lysosomal storage disorder caused by glucocerebrosidase deficiency, causing glucosylceramide buildup in lysosomal macrophages."
    },
    {
        "id": 4,
        "question": "A 22-year-old athlete presenting with exercise intolerance, muscle weakness, and elevated blood lactate is diagnosed with a metabolic myopathy. Dysfunctional activity of which organelle is responsible, and what is its mode of inheritance?",
        "options": [
            "Endoplasmic Reticulum; X-linked",
            "Golgi apparatus; Autosomal dominant",
            "Lysosome; Autosomal recessive",
            "Mitochondria; Maternal inheritance",
            "Nucleus; Paternal inheritance"
        ],
        "answer": "Mitochondria; Maternal inheritance",
        "explanation": "Mitochondrial myopathies are caused by defects in mitochondrial oxidative phosphorylation, inherited maternally because mitochondria are derived from the ovum."
    },
    {
        "id": 5,
        "question": "Which cellular organelle consists of a pair of micro-tubular structures arranged perpendicularly and plays a key role in organizing the mitotic spindle during cell division?",
        "options": [
            "Centrosome / Centrioles",
            "Lysosome",
            "Peroxisome",
            "Nucleolus",
            "Ribosome"
        ],
        "answer": "Centrosome / Centrioles",
        "explanation": "The centrosome contains two centrioles that migrate to opposite poles during prophase to organize the mitotic spindle apparatus."
    },
    {
        "id": 6,
        "question": "Under the electron microscope, Nissl bodies in neuronal cell bodies correspond to which cellular organelles?",
        "options": [
            "Smooth endoplasmic reticulum",
            "Rough endoplasmic reticulum and free ribosomes",
            "Golgi complex cisternae",
            "Mitochondrial cristae",
            "Lysosomes"
        ],
        "answer": "Rough endoplasmic reticulum and free ribosomes",
        "explanation": "Nissl bodies are basophilic clumps in neurons formed by extensive stacks of rough endoplasmic reticulum (RER) and polyribosomes dedicated to neurotransmitter protein synthesis."
    },
    {
        "id": 7,
        "question": "Which of the following pioneer scientists is credited with adding the third tenet of cell theory, stating that all living cells arise only from pre-existing cells ('Omnis cellula e cellula')?",
        "options": [
            "Antonie van Leeuwenhoek",
            "Mathias Schleiden",
            "Robert Hooke",
            "Rudolf Virchow",
            "Theodor Schwann"
        ],
        "answer": "Rudolf Virchow",
        "explanation": "Rudolf Virchow popularized the third tenet of cell theory in 1855, establishing that cells originate only through division of pre-existing cells."
    },
    {
        "id": 8,
        "question": "How many major physiological organ systems are classically described in the human body?",
        "options": [
            "10",
            "11",
            "12",
            "13",
            "9"
        ],
        "answer": "11",
        "explanation": "The human body consists of 11 physiological organ systems: integumentary, skeletal, muscular, nervous, endocrine, cardiovascular, lymphatic, respiratory, digestive, urinary, and reproductive."
    },
    {
        "id": 9,
        "question": "The physiological system responsible for protecting internal tissues against the external environment, preventing desiccation, and regulating body temperature is the:",
        "options": [
            "Skeletal system",
            "Lymphatic system",
            "Integumentary system",
            "Endocrine system",
            "Nervous system"
        ],
        "answer": "Integumentary system",
        "explanation": "The integumentary system (skin, hair, nails, sweat glands) provides physical protection, thermoregulation, and cutaneous sensation."
    },
    {
        "id": 10,
        "question": "Which basic component of connective tissue is primarily responsible for resisting tensile stress and providing structural strength?",
        "options": [
            "Ground substance",
            "Elastic fibers",
            "Collagen bundles",
            "Reticular fibers",
            "Proteoglycan aggregates"
        ],
        "answer": "Collagen bundles",
        "explanation": "Collagen fibers (especially Type I) have immense tensile strength and resist mechanical tearing across connective tissues."
    },
    {
        "id": 11,
        "question": "Marfan syndrome results from a genetic mutation in the FBN1 gene encoding the extracellular matrix protein fibrillin-1. Which connective tissue fiber component is directly impaired?",
        "options": [
            "Collagen fibers",
            "Elastic fibers",
            "Reticular fibers",
            "Ground substance proteoglycans",
            "Basement membrane laminin"
        ],
        "answer": "Elastic fibers",
        "explanation": "Fibrillin-1 provides a microfibrillar scaffold for elastin deposition; mutations disrupt elastic fiber assembly, leading to aortic root dilation and lens dislocation."
    },
    {
        "id": 12,
        "question": "A 7-year-old girl presents with hypermobile joints, skin hyperextensibility, and frequent joint dislocations. Inherited defect in which protein family accounts for these findings?",
        "options": [
            "Actin",
            "Collagen",
            "Elastin",
            "Fibrillin",
            "Keratin"
        ],
        "answer": "Collagen",
        "explanation": "Hypermobility and joint laxity characteristic of Ehlers-Danlos syndrome result from genetic defects in Type I, III, or V collagen synthesis and processing."
    },
    {
        "id": 13,
        "question": "Which connective tissue cell type releases histamine, heparin, and leukotrienes during type I hypersensitivity reactions (allergic rhinitis / hay fever)?",
        "options": [
            "Adipocytes",
            "Fibroblasts",
            "Macrophages",
            "Mast cells",
            "Plasma cells"
        ],
        "answer": "Mast cells",
        "explanation": "IgE cross-linking on mast cell surfaces triggers degranulation, releasing preformed histamine and synthesizing inflammatory mediators."
    },
    {
        "id": 14,
        "question": "Arranging the layers of a long bone from outer surface to inner marrow space, through which order of structures does a bone marrow biopsy needle pass?",
        "options": [
            "Skeletal muscle -> Endosteum -> Osteons -> Periosteum -> Marrow",
            "Skeletal muscle -> Periosteum -> Outer circumferential lamellae -> Osteons -> Inner circumferential lamellae -> Endosteum -> Marrow",
            "Periosteum -> Skeletal muscle -> Endosteum -> Osteons -> Marrow",
            "Skeletal muscle -> Endosteum -> Periosteum -> Marrow",
            "Periosteum -> Endosteum -> Osteons -> Marrow"
        ],
        "answer": "Skeletal muscle -> Periosteum -> Outer circumferential lamellae -> Osteons -> Inner circumferential lamellae -> Endosteum -> Marrow",
        "explanation": "The needle penetrates overlying muscle, periosteum, outer cortical bone, osteon layer, inner circumferential lamellae, endosteum, and finally enters the medullary marrow cavity."
    },
    {
        "id": 15,
        "question": "Which microscopic channels directly connect the Haversian canal of one osteon to Haversian canals of adjacent osteons or to the periosteum?",
        "options": [
            "Canaliculi",
            "Caveoli",
            "Howship's lacunae",
            "Trabeculae",
            "Volkmann's canals"
        ],
        "answer": "Volkmann's canals",
        "explanation": "Volkmann's (perforating) canals run perpendicular/transversely to Haversian canals, carrying neurovascular structures between adjacent osteons and the periosteum/endosteum."
    },
    {
        "id": 16,
        "question": "Sulphated glycosaminoglycans (such as chondroitin sulfate and keratan sulfate) covalently attach to core proteins to form which major extracellular macromolecule?",
        "options": [
            "Hyaluronan",
            "Elastic fibers",
            "Type I collagen",
            "Proteoglycans",
            "Multiadhesive glycoproteins"
        ],
        "answer": "Proteoglycans",
        "explanation": "Proteoglycans consist of a core protein with covalently attached GAG chains; their negative charges attract water, providing turgor and shock absorption."
    },
    {
        "id": 17,
        "question": "Which type of cartilage is avascular, lacks a perichondrium, and contains abundant Type I collagen fibers arranged in parallel bundles?",
        "options": [
            "Hyaline cartilage",
            "Elastic cartilage",
            "Fibrocartilage",
            "Articular cartilage",
            "Epiphyseal cartilage"
        ],
        "answer": "Fibrocartilage",
        "explanation": "Fibrocartilage (found in intervertebral discs and pubic symphysis) contains dense Type I collagen and lacks a perichondrium, undergoing only interstitial growth."
    },
    {
        "id": 18,
        "question": "Which statement regarding cell junctions in epithelial tissue is correct?",
        "options": [
            "Desmosomes prevent paracellular diffusion of solutes",
            "Tight junctions (zonula occludens) create a primary barrier to paracellular transport",
            "Gap junctions anchor cells directly to the basement membrane",
            "Hemidesmosomes allow direct movement of ions between adjacent cells",
            "Adherens junctions form a complete seal around the apical membrane"
        ],
        "answer": "Tight junctions (zonula occludens) create a primary barrier to paracellular transport",
        "explanation": "Zonula occludens (tight junctions) ring the apical boundary of epithelial cells, regulating paracellular permeability and maintaining cell polarity."
    },
    {
        "id": 19,
        "question": "Pseudostratified columnar epithelium with stereocilia is characteristically found lining which part of the male reproductive tract?",
        "options": [
            "Ductus deferens and epididymis",
            "Prostatic urethra",
            "Seminal vesicles",
            "Testicular efferent ductules",
            "Rete testis"
        ],
        "answer": "Ductus deferens and epididymis",
        "explanation": "The epididymis and ductus deferens are lined by pseudostratified columnar epithelium with long, non-motile microvilli (stereocilia) that absorb fluid."
    },
    {
        "id": 20,
        "question": "Exocrine glands whose secretory mechanism involves the total destruction and shedding of the entire secretory cell are classified as:",
        "options": [
            "Holocrine glands",
            "Merocrine glands",
            "Apocrine glands",
            "Paracrine glands",
            "Endocrine glands"
        ],
        "answer": "Holocrine glands",
        "explanation": "In holocrine secretion (e.g., sebaceous glands), the cell accumulates secretory product in cytoplasm and undergoes apoptosis/lysis to release it."
    },
    {
        "id": 21,
        "question": "Which cell type in the connective tissue proper is derived from blood monocytes and functions as a professional antigen-presenting phagocyte (histiocyte)?",
        "options": [
            "Fibroblast",
            "Plasma cell",
            "Tissue macrophage",
            "Mast cell",
            "Adipocyte"
        ],
        "answer": "Tissue macrophage",
        "explanation": "Tissue macrophages (histiocytes) differentiate from circulating monocytes, phagocytosing debris and pathogens."
    },
    {
        "id": 22,
        "question": "Which of the following is true regarding brown adipose tissue compared to white adipose tissue?",
        "options": [
            "Brown adipocytes contain a single large lipid droplet (unilocular)",
            "Brown adipose tissue is rich in mitochondria expressing uncoupling protein-1 (UCP-1 / thermogenin)",
            "Brown fat is more abundant in human adults than in newborns",
            "Brown fat stores energy more efficiently than yellow fat",
            "Brown fat adipocytes lack sympathetic nerve supply"
        ],
        "answer": "Brown adipose tissue is rich in mitochondria expressing uncoupling protein-1 (UCP-1 / thermogenin)",
        "explanation": "Brown fat contains multilocular lipid droplets and dense mitochondria with UCP-1, uncoupling oxidative phosphorylation to generate heat (non-shivering thermogenesis)."
    },
    {
        "id": 23,
        "question": "Tendons and ligaments are composed of which type of connective tissue?",
        "options": [
            "Loose irregular connective tissue",
            "Dense regular connective tissue",
            "Dense irregular connective tissue",
            "Reticular connective tissue",
            "Elastic cartilage"
        ],
        "answer": "Dense regular connective tissue",
        "explanation": "Dense regular connective tissue consists of densely packed collagen bundles arranged parallel to the direction of linear tension."
    },
    {
        "id": 24,
        "question": "What is the specialized embryonic connective tissue derived from mesoderm that serves as the precursor for all adult connective tissues and skeleton?",
        "options": [
            "Mucous connective tissue (Wharton's jelly)",
            "Mesenchyme",
            "Areolar tissue",
            "Adipose tissue",
            "Reticular tissue"
        ],
        "answer": "Mesenchyme",
        "explanation": "Mesenchyme is embryonic connective tissue comprising star-shaped mesenchymal cells in a gel-like ground substance that differentiates into all connective tissues."
    },
    {
        "id": 25,
        "question": "During bone development, osteoblasts differentiate directly from mesenchymal stem cell condensations without a cartilage intermediate in which process?",
        "options": [
            "Endochondral ossification",
            "Intramembranous ossification",
            "Interstitial cartilage growth",
            "Appositional cartilage growth",
            "Haversian remodeling"
        ],
        "answer": "Intramembranous ossification",
        "explanation": "Flat bones of the skull and clavicle form via intramembranous ossification, where mesenchymal cells differentiate directly into osteoblasts."
    },
    {
        "id": 26,
        "question": "In the histology of skeletal muscle fibers, which band represents the central region of the A-band containing only thick (myosin) filaments?",
        "options": [
            "I-band",
            "H-band",
            "Z-disc",
            "M-line",
            "A-band"
        ],
        "answer": "H-band",
        "explanation": "The H-band (H-zone) is the light region in the center of the A-band where thick myosin filaments do not overlap with thin actin filaments."
    },
    {
        "id": 27,
        "question": "In a cardiac muscle cell histology slide, which unique structural feature connects adjacent muscle cells end-to-end, housing desmosomes and gap junctions?",
        "options": [
            "T-tubules",
            "Intercalated discs",
            "Triads",
            "Caveolae",
            "Nissl bodies"
        ],
        "answer": "Intercalated discs",
        "explanation": "Intercalated discs join cardiac myocytes end-to-end; transverse components contain fascia adherens/desmosomes for mechanical adhesion, while longitudinal components contain gap junctions for electrical coupling."
    },
    {
        "id": 28,
        "question": "Morphologically, the multipolar motor neurons situated in the anterior (ventral) horn of the spinal cord are classified as:",
        "options": [
            "Unipolar neurons",
            "Multipolar neurons",
            "Pseudounipolar neurons",
            "Bipolar neurons",
            "Anaxonic neurons"
        ],
        "answer": "Multipolar neurons",
        "explanation": "Ventral horn alpha motor neurons possess multiple dendrites and a single axon, making them classic multipolar neurons."
    },
    {
        "id": 29,
        "question": "Which connective tissue sheath surrounds an individual nerve axon and its associated myelin sheath within a peripheral nerve fascicle?",
        "options": [
            "Epineurium",
            "Perineurium",
            "Endoneurium",
            "Neurilemma",
            "Perimysium"
        ],
        "answer": "Endoneurium",
        "explanation": "Endoneurium is delicate loose connective tissue surrounding individual nerve fibers; perineurium surrounds fascicles, and epineurium surrounds the entire nerve."
    },
    {
        "id": 30,
        "question": "In routine histological tissue preparation, Hematoxylin is classified as a basic dye that preferentially stains acidic cellular components purple. Which structure is basophilic?",
        "options": [
            "Cytoplasm",
            "Cell nucleus / DNA",
            "Mitochondria",
            "Collagen fibers",
            "Red blood cells"
        ],
        "answer": "Cell nucleus / DNA",
        "explanation": "Hematoxylin is basic and binds acidic nucleic acids (DNA/RNA) in the nucleus and RER, imparting a dark purple/blue color."
    },
    {
        "id": 31,
        "question": "Which reagent is commonly used as a clearing agent in histological tissue processing to remove alcohol and make tissue miscible with paraffin wax?",
        "options": [
            "Formalin",
            "Absolute ethanol",
            "Xylene",
            "Glutaraldehyde",
            "Picric acid"
        ],
        "answer": "Xylene",
        "explanation": "Xylene is an organic solvent used during clearing to displace dehydrating ethanol so molten paraffin wax can infiltrate the tissue."
    },
    {
        "id": 32,
        "question": "What is the spatial organization of Spermatogonia, Spermatocytes, and Spermatids within the seminiferous tubule wall?",
        "options": [
            "Spermatids at basal lamina, Spermatogonia in lumen",
            "Spermatogonia at basal compartment, Primary spermatocytes in adluminal compartment, Spermatids near lumen",
            "Spermatocytes at basal lamina, Spermatogonia in lumen",
            "Leydig cells inside seminiferous tubule lumen",
            "Sertoli cells located outside the basement membrane"
        ],
        "answer": "Spermatogonia at basal compartment, Primary spermatocytes in adluminal compartment, Spermatids near lumen",
        "explanation": "Spermatogenesis proceeds centripetally: diploid spermatogonia reside on the basal lamina, meiotic spermatocytes move into the adluminal compartment, and haploid spermatids mature near the lumen."
    },
    {
        "id": 33,
        "question": "The blood-testis barrier that isolates immunologically foreign haploid germ cells from blood circulation is formed by tight junctions between adjacent:",
        "options": [
            "Leydig cells",
            "Sertoli cells",
            "Spermatogonia Type A",
            "Myoid cells",
            "Primary spermatocytes"
        ],
        "answer": "Sertoli cells",
        "explanation": "Zonula occludens (tight junctions) between adjacent Sertoli cells establish the blood-testis barrier, creating basal and adluminal compartments."
    },
    {
        "id": 34,
        "question": "Spermatids undergo morphological transformation into mature spermatozoa (spermiogenesis). Which organelle forms the acrosome cap containing hydrolytic enzymes?",
        "options": [
            "Lysosome",
            "Golgi apparatus",
            "Centriole",
            "Mitochondrion",
            "Smooth ER"
        ],
        "answer": "Golgi apparatus",
        "explanation": "During spermiogenesis, the Golgi apparatus produces acrosomal vesicles that fuse over the anterior nuclear surface to form the acrosome."
    },
    {
        "id": 35,
        "question": "In human embryonic development, what is the correct chronological sequence of early developmental stages?",
        "options": [
            "Blastocyst -> Zygote -> Morula -> Implantation",
            "Zygote -> Morula -> Blastocyst -> Implantation",
            "Morula -> Blastocyst -> Implantation -> Zygote",
            "Zygote -> Blastocyst -> Morula -> Implantation",
            "Blastocyst -> Morula -> Zygote -> Implantation"
        ],
        "answer": "Zygote -> Morula -> Blastocyst -> Implantation",
        "explanation": "Fertilization produces a single-celled Zygote, cleavage forms a solid ball of cells (Morula ~day 3-4), fluid accumulation creates a Blastocyst (~day 5), which undergoes Implantation (~day 6-7)."
    },
    {
        "id": 36,
        "question": "Stem cells capable of generating all 220 cell types of the adult body AS WELL AS extraembryonic placental tissues are defined as:",
        "options": [
            "Pluripotent",
            "Multipotent",
            "Totipotent",
            "Unipotent",
            "Oligopotent"
        ],
        "answer": "Totipotent",
        "explanation": "Totipotent cells (zygote and early blastomeres up to 4-8 cell stage) can form both the embryo proper and extraembryonic tissues (placenta)."
    },
    {
        "id": 37,
        "question": "The inner cell mass (embryoblast) of the blastocyst consists of cells that can differentiate into all tissues of the body but NOT extraembryonic membranes. These cells are:",
        "options": [
            "Totipotent",
            "Pluripotent",
            "Multipotent",
            "Unipotent",
            "Differentiated"
        ],
        "answer": "Pluripotent",
        "explanation": "Pluripotent stem cells (embryonic stem cells derived from the inner cell mass) can form all three germ layers (endoderm, mesoderm, ectoderm) but not placental tissues."
    },
    {
        "id": 38,
        "question": "Undifferentiated Type A dark spermatogonia in the basal compartment of the seminiferous tubule serve as self-renewing stem cells. In terms of potency, they are:",
        "options": [
            "Totipotent",
            "Pluripotent",
            "Multipotent",
            "Unipotent",
            "Nullipotent"
        ],
        "answer": "Unipotent",
        "explanation": "Unipotent stem cells produce cells along a single lineage (e.g., spermatogonia giving rise strictly to germline cells/spermatozoa)."
    },
    {
        "id": 39,
        "question": "Hematopoietic stem cells (HSCs) residing in adult bone marrow can differentiate into erythrocytes, leukocytes, and platelets. Their developmental potency is:",
        "options": [
            "Totipotent",
            "Pluripotent",
            "Multipotent",
            "Unipotent",
            "Reprogrammed"
        ],
        "answer": "Multipotent",
        "explanation": "Multipotent stem cells give rise to multiple cell types within a specific tissue lineage (e.g., HSCs generating all blood cell lines)."
    },
    {
        "id": 40,
        "question": "Reprogramming adult somatic cells into induced pluripotent stem cells (iPSCs) using retroviral vectors carries which primary safety concern for clinical therapy?",
        "options": [
            "Vectors dilute out after one cell division",
            "Integrative viral vectors can insert into host DNA and reactivate oncogenes, causing tumors",
            "iPS cells immediately undergo senescence",
            "Retroviruses cannot infect human cells",
            "Cells lose all genomic DNA"
        ],
        "answer": "Integrative viral vectors can insert into host DNA and reactivate oncogenes, causing tumors",
        "explanation": "Genomic integration of retroviral vectors carries a risk of insertional mutagenesis and re-activation of pluripotency transgene oncogenes (e.g., c-Myc), causing tumorigenesis."
    }
]
PHYS_QS = [
    {
        "id": 41,
        "question": "A patient with uncontrolled Type 1 Diabetes Mellitus presents with severe hyperglycemia (blood glucose = 450 mg/dL). What is the immediate effect on extracellular fluid (ECF) osmolality?",
        "options": [
            "Increased osmolality",
            "Decreased osmolality",
            "No change in osmolality",
            "Decreased oncotic pressure",
            "Increased intracellular hydration"
        ],
        "answer": "Increased osmolality",
        "explanation": "Glucose is an effective osmole; severe hyperglycemia increases ECF osmolality, drawing water out of intracellular compartments into the ECF."
    },
    {
        "id": 42,
        "question": "A patient with acute severe cholera diarrhea loses 4 liters of fluid containing equal proportions of water and electrolytes. How do body fluid parameters change?",
        "options": [
            "ECF volume decreases with isotonic osmolality",
            "ECF volume increases with hypo-osmolality",
            "ICF volume expands dramatically",
            "Osmolality drops below 200 mOsm/kg",
            "Plasma oncotic pressure decreases"
        ],
        "answer": "ECF volume decreases with isotonic osmolality",
        "explanation": "Isotonic fluid loss (severe diarrhea) leads to ECF volume contraction without changing initial ECF osmolality."
    },
    {
        "id": 43,
        "question": "Consumption of a high-sodium diet increases plasma sodium levels. What is the physiological response of central osmoreceptors in the anterior hypothalamus?",
        "options": [
            "Inhibition of osmoreceptors -> decreased ADH release",
            "Stimulation of osmoreceptors -> increased Antidiuretic Hormone (ADH) release from posterior pituitary",
            "No change in osmoreceptor firing",
            "Suppression of thirst center",
            "Increased renal free water clearance"
        ],
        "answer": "Stimulation of osmoreceptors -> increased Antidiuretic Hormone (ADH) release from posterior pituitary",
        "explanation": "Hyperosmolality shrinks hypothalamic osmoreceptors, triggering thirst and stimulating ADH (vasopressin) release to promote renal water reabsorption."
    },
    {
        "id": 44,
        "question": "Why are rapid, high-velocity changes in neuronal membrane potential mediated by ion channel proteins rather than ATP-driven protein pumps?",
        "options": [
            "Channel proteins move ions against concentration gradients",
            "Channel proteins allow passive ion flux down electrochemical gradients at far faster rates (~10^7 ions/sec) without requiring ATP hydrolysis per ion",
            "Protein pumps are less specific than channel proteins",
            "Channel proteins require GTP hydrolysis",
            "Protein pumps cannot bind Na+ ions"
        ],
        "answer": "Channel proteins allow passive ion flux down electrochemical gradients at far faster rates (~10^7 ions/sec) without requiring ATP hydrolysis per ion",
        "explanation": "Ion channels open to allow passive diffusion of up to 10^7-10^8 ions per second down electrochemical gradients, whereas pumps undergo conformational cycles moving ~10^2-10^3 ions/sec."
    },
    {
        "id": 45,
        "question": "Opening of selective ion channels in the neuronal cell membrane affects electrical properties by:",
        "options": [
            "Increasing membrane resistance",
            "Decreasing membrane resistance (increasing conductance)",
            "Increasing membrane capacitance",
            "Abolishing membrane capacitance",
            "Preventing ion flow"
        ],
        "answer": "Decreasing membrane resistance (increasing conductance)",
        "explanation": "Opening ion channels increases membrane permeability/conductance ($g$), which is inversely related to membrane electrical resistance ($R = 1/g$)."
    },
    {
        "id": 46,
        "question": "On a neuronal cell membrane, which region possesses the highest density of voltage-gated Na+ channels, making it the site of action potential initiation (spike trigger zone)?",
        "options": [
            "Distal dendrite",
            "Somatic sub-membrane zone",
            "Axon hillock / initial segment",
            "Axon terminal button",
            "Node of Ranvier central core"
        ],
        "answer": "Axon hillock / initial segment",
        "explanation": "The axon hillock and initial segment have a high concentration of voltage-gated Na+ channels, giving it the lowest threshold for action potential generation."
    },
    {
        "id": 47,
        "question": "Which sensory receptor cells rely on mechanically-gated ion channels to detect sensory stimuli?",
        "options": [
            "Retinal rod and cone photoreceptors",
            "Olfactory receptor neurons",
            "Auditory hair cells in the Organ of Corti",
            "Gustatory taste bud cells",
            "Hypothalamic osmoreceptors"
        ],
        "answer": "Auditory hair cells in the Organ of Corti",
        "explanation": "Bending of hair cell stereocilia in the inner ear pulls tip links, mechanically opening K+/Ca2+ channels to initiate auditory transduction."
    },
    {
        "id": 48,
        "question": "Calculated by the Nernst equation at body temperature ($37^\\circ\\text{C}$), what is the typical equilibrium potential ($E_K$) for Potassium ions ($K^+$) across a resting neuron membrane?",
        "options": [
            "+60 mV",
            "+30 mV",
            "0 mV",
            "-70 mV",
            "-90 mV"
        ],
        "answer": "-90 mV",
        "explanation": "Using typical intracellular ($140\\text{ mM}$) and extracellular ($4\\text{ mM}$) $K^+$ concentrations, $E_K = 61.5 \\log(4/140) \\approx -90\\text{ mV}$."
    },
    {
        "id": 49,
        "question": "Which statement regarding the Sodium equilibrium potential ($E_{Na}$) is TRUE?",
        "options": [
            "It is more negative than the resting membrane potential",
            "It is independent of temperature",
            "It is positive (approximately +60 mV) and depends on intracellular vs extracellular Na+ concentrations",
            "Increasing intracellular Na+ makes E_Na more positive",
            "It equals the threshold potential (-55 mV)"
        ],
        "answer": "It is positive (approximately +60 mV) and depends on intracellular vs extracellular Na+ concentrations",
        "explanation": "With high extracellular ($145\\text{ mM}$) relative to intracellular ($15\\text{ mM}$) $Na^+$, $E_{Na} = +61.5 \\log(145/15) \\approx +60\\text{ mV}$."
    },
    {
        "id": 50,
        "question": "Under what condition can a single sub-threshold Excitatory Post-Synaptic Potential (EPSP) trigger an action potential at the axon hillock?",
        "options": [
            "When it occurs at the distal tip of a long dendrite",
            "When it undergoes summation with another sub-threshold EPSP arriving synchronously (spatial) or in rapid succession (temporal)",
            "When preceded by a strong Inhibitory Post-Synaptic Potential (IPSP)",
            "When leak K+ channels are hyper-activated",
            "When extracellular Na+ concentration is reduced by half"
        ],
        "answer": "When it undergoes summation with another sub-threshold EPSP arriving synchronously (spatial) or in rapid succession (temporal)",
        "explanation": "Subthreshold EPSPs do not reach threshold alone; spatial or temporal summation combines depolarizations to reach the threshold voltage (-55 mV)."
    },
    {
        "id": 51,
        "question": "Assuming all other axon characteristics are equal, which nerve fiber will exhibit the fastest action potential conduction velocity?",
        "options": [
            "Unmyelinated fiber, 2 \u00b5m diameter",
            "Myelinated fiber, 10 \u00b5m diameter",
            "Myelinated fiber, 25 \u00b5m diameter",
            "Unmyelinated fiber, 25 \u00b5m diameter",
            "Myelinated fiber, 5 \u00b5m diameter"
        ],
        "answer": "Myelinated fiber, 25 \u00b5m diameter",
        "explanation": "Conduction velocity increases with axon diameter (reduced internal longitudinal resistance) and myelination (saltatory conduction)."
    },
    {
        "id": 52,
        "question": "The Na+/K+ ATPase pump maintains resting ion gradients by moving ions across the plasma membrane. What type of transporter is it?",
        "options": [
            "Uniporter",
            "Symporter (Co-transporter)",
            "Antiporter (Exchanger) driven by primary active ATP hydrolysis",
            "Facilitated diffusion channel",
            "Passive leak channel"
        ],
        "answer": "Antiporter (Exchanger) driven by primary active ATP hydrolysis",
        "explanation": "The Na+/K+ pump hydrolyzes 1 ATP to pump 3 Na+ out of the cell and 2 K+ into the cell, operating as a primary active antiporter."
    },
    {
        "id": 53,
        "question": "The distance a electrotonic graded potential can travel along a dendrite before decaying (length constant $\\lambda$) can be INCREASED by:",
        "options": [
            "Decreasing membrane transverse resistance (rm)",
            "Increasing internal longitudinal axon resistance (ri)",
            "Increasing membrane transverse resistance (rm) and decreasing internal axial resistance (ri)",
            "Increasing the density of potassium leak channels",
            "Decreasing myelin sheath thickness"
        ],
        "answer": "Increasing membrane transverse resistance (rm) and decreasing internal axial resistance (ri)",
        "explanation": "Length constant $\\lambda = \\sqrt{r_m / r_i}$. High transverse membrane resistance ($r_m$) prevents current leakage, increasing signal propagation distance."
    },
    {
        "id": 54,
        "question": "Under normal physiological conditions, how does increasing extracellular sodium concentration ([Na+]o) affect the resting membrane potential of a neuron?",
        "options": [
            "The resting membrane potential becomes markedly hyperpolarized",
            "The resting membrane potential remains largely unchanged because resting Na+ permeability is very low compared to K+ permeability",
            "The resting potential immediately shifts to +60 mV",
            "The resting potential becomes -120 mV",
            "Na+ channels permanently close"
        ],
        "answer": "The resting membrane potential remains largely unchanged because resting Na+ permeability is very low compared to K+ permeability",
        "explanation": "At rest, membrane permeability to K+ is ~20-100 times greater than to Na+; thus $RMP$ is close to $E_K$ and insensitive to modest changes in $[Na^+]_o$."
    },
    {
        "id": 55,
        "question": "According to Fick's Law of Diffusion, the net rate of simple diffusion ($J$) across a cell membrane is directly proportional to:",
        "options": [
            "Membrane surface area, concentration gradient, and lipid solubility",
            "Membrane thickness and molecular weight",
            "ATP concentration inside the cytoplasm",
            "Number of Na+/K+ pumps",
            "Degree of myelin insulation"
        ],
        "answer": "Membrane surface area, concentration gradient, and lipid solubility",
        "explanation": "Fick's Law: $J = \\frac{A \\cdot D \\cdot \\Delta C}{\\Delta x}$. Diffusion rate increases with surface area ($A$), diffusion coefficient/solubility ($D$), and concentration gradient ($\\Delta C$)."
    },
    {
        "id": 56,
        "question": "What prevents an action potential from propagating backward toward the soma during its travel down an axon?",
        "options": [
            "Inactivation of voltage-gated Na+ channels (Absolute Refractory Period) in the wake of the impulse",
            "Hyper-activation of ligand-gated channels",
            "Retrograde ATP hydrolysis",
            "Depletion of intracellular K+",
            "Myelin sheath mechanical resistance"
        ],
        "answer": "Inactivation of voltage-gated Na+ channels (Absolute Refractory Period) in the wake of the impulse",
        "explanation": "Voltage-gated Na+ channels enter an inactivated state during repolarization; the refractory period ensures unidirectional propagation."
    },
    {
        "id": 57,
        "question": "In saltatory conduction along a myelinated axon, action potentials regenerate exclusively at which sites?",
        "options": [
            "Somatic plasma membrane",
            "Internodal axonal segments",
            "Nodes of Ranvier",
            "Schwann cell cytoplasm",
            "Dendritic spines"
        ],
        "answer": "Nodes of Ranvier",
        "explanation": "Myelin insulates internodes, forcing ionic current to jump between Nodes of Ranvier where voltage-gated Na+ channels are concentrated."
    },
    {
        "id": 58,
        "question": "A cell cycle phase during which non-dividing differentiated cells (e.g., mature neurons, cardiac myocytes) exist in a reversible or permanent quiescent state is:",
        "options": [
            "G1 phase",
            "S phase",
            "G2 phase",
            "M phase",
            "G0 phase"
        ],
        "answer": "G0 phase",
        "explanation": "G0 is the resting/quiescent phase outside the active cell cycle; mature post-mitotic cells reside in G0."
    },
    {
        "id": 59,
        "question": "During which cell cycle phase does nuclear DNA replication occur, resulting in a doubling of genetic material (from 2n to 4n DNA content)?",
        "options": [
            "G1 phase",
            "S phase",
            "G2 phase",
            "Prophase",
            "Telophase"
        ],
        "answer": "S phase",
        "explanation": "DNA synthesis/replication occurs during S (Synthesis) phase of interphase."
    },
    {
        "id": 60,
        "question": "Cancer chemotherapy drugs targeting the mitotic spindle (such as paclitaxel and vincristine) act by arresting dividing cells at which phase of mitosis?",
        "options": [
            "Prophase",
            "Metaphase / Anaphase transition",
            "Interphase G1",
            "S phase",
            "Telophase"
        ],
        "answer": "Metaphase / Anaphase transition",
        "explanation": "Microtubule inhibitors disrupt mitotic spindle assembly, triggering the spindle assembly checkpoint to arrest cells at metaphase."
    },
    {
        "id": 61,
        "question": "Human primary oocytes are formed in fetal life and remain arrested in which meiotic stage until ovulation at puberty?",
        "options": [
            "Leptotene of Prophase I",
            "Dictyotene (Diplotene) stage of Prophase I",
            "Metaphase I",
            "Anaphase II",
            "Prophase II"
        ],
        "answer": "Dictyotene (Diplotene) stage of Prophase I",
        "explanation": "Primary oocytes enter Meiosis I during fetal development and remain arrested in the dictyotene stage of Prophase I until LH surges prior to ovulation."
    },
    {
        "id": 62,
        "question": "When does a secondary oocyte complete Meiosis II during female gametogenesis?",
        "options": [
            "At birth",
            "During monthly LH surge",
            "Immediately after fertilization by a spermatozoon",
            "At menopause",
            "During blastocyst implantation"
        ],
        "answer": "Immediately after fertilization by a spermatozoon",
        "explanation": "Ovulated secondary oocytes are arrested in Metaphase II; completion of Meiosis II is triggered by sperm entry during fertilization."
    },
    {
        "id": 63,
        "question": "Why does advanced maternal age (>35 years) significantly increase the incidence of chromosomal nondisjunction (e.g., Down syndrome)?",
        "options": [
            "Decreased estrogen levels",
            "Primary oocytes remain arrested in Prophase I for decades, leading to degradation of meiotic cohesin proteins",
            "Increased frequency of mitotic divisions",
            "Rapid uterine lining atrophy",
            "Hyper-activation of follicular development"
        ],
        "answer": "Primary oocytes remain arrested in Prophase I for decades, leading to degradation of meiotic cohesin proteins",
        "explanation": "Decades-long arrest in Prophase I leads to age-dependent decay of meiotic chromosome cohesins and spindle apparatus components, causing nondisjunction."
    },
    {
        "id": 64,
        "question": "A 28-year-old man presenting with male factor infertility is found to have a left-sided varicocele. What is the pathogenetic mechanism of defective spermatogenesis?",
        "options": [
            "Autoimmune destruction of Leydig cells",
            "Elevated testicular temperature due to venous stasis in the pampiniform plexus",
            "Chromosomal non-disjunction",
            "Decreased pituitary LH secretion",
            "Azoospermia from vas deferens occlusion"
        ],
        "answer": "Elevated testicular temperature due to venous stasis in the pampiniform plexus",
        "explanation": "Varicoceles impair pampiniform plexus heat exchange, raising testicular temperature above the optimal $34-35^\\circ\\text{C}$ required for normal spermatogenesis."
    },
    {
        "id": 65,
        "question": "A newborn male infant is diagnosed with bilateral cryptorchidism (undescended testes). If untreated, what fertility impairment will manifest in adulthood?",
        "options": [
            "Aspermia",
            "Asthenozoospermia",
            "Azoospermia due to heat-induced germ cell degeneration",
            "Teratozoospermia",
            "Polyspermia"
        ],
        "answer": "Azoospermia due to heat-induced germ cell degeneration",
        "explanation": "Bilateral abdominal position exposes testes to normal body temperature ($37^\\circ\\text{C}$), causing degeneration of spermatogonia and adult azoospermia."
    },
    {
        "id": 66,
        "question": "In premature ovarian insufficiency (POI), female patients experience amenorrhea and infertility before what age?",
        "options": [
            "30 years",
            "40 years",
            "50 years",
            "60 years",
            "25 years"
        ],
        "answer": "40 years",
        "explanation": "Premature ovarian insufficiency (POI) is defined as hypergonadotropic hypogonadism and cessation of ovarian function before age 40."
    },
    {
        "id": 67,
        "question": "What is the key clinical diagnostic benefit of Preimplantation Genetic Diagnosis (PGD) performed during In Vitro Fertilization (IVF)?",
        "options": [
            "Elimination of polyspermy risk",
            "Identification and selection of single embryos free of specific single-gene or chromosomal mutations prior to transfer",
            "Elimination of blastocyst culture",
            "Guaranteed 100% pregnancy rate",
            "Prevention of ectopic implantation"
        ],
        "answer": "Identification and selection of single embryos free of specific single-gene or chromosomal mutations prior to transfer",
        "explanation": "PGD biopsies a blastomere/trophectoderm cell to screen for monogenic disorders or aneuploidies, ensuring unaffected embryos are selected for transfer."
    },
    {
        "id": 68,
        "question": "Excitation-contraction coupling in smooth muscle differs from skeletal muscle because cross-bridge activation in smooth muscle requires Ca2+ binding to:",
        "options": [
            "Troponin C",
            "Calmodulin, which activates Myosin Light Chain Kinase (MLCK)",
            "Tropomyosin",
            "Dihydropyridine receptor",
            "Calsequestrin"
        ],
        "answer": "Calmodulin, which activates Myosin Light Chain Kinase (MLCK)",
        "explanation": "Smooth muscle lacks troponin; elevated $Ca^{2+}$ binds Calmodulin, forming a complex that activates MLCK to phosphorylate myosin light chains."
    },
    {
        "id": 69,
        "question": "Skeletal muscle fibers undergo tetanic contraction upon high-frequency electrical stimulation because of:",
        "options": [
            "Sustained elevation of intracellular Ca2+ in the sarcoplasm preventing muscle relaxation",
            "Depletion of intracellular ATP",
            "Accumulation of intracellular Na+",
            "Inhibition of acetylcholinesterase",
            "Closure of ryanodine receptors"
        ],
        "answer": "Sustained elevation of intracellular Ca2+ in the sarcoplasm preventing muscle relaxation",
        "explanation": "High-frequency action potentials release $Ca^{2+}$ faster than SERCA pumps can re-sequester it into the SR, maintaining cross-bridge activity and continuous force."
    },
    {
        "id": 70,
        "question": "In a laboratory cell fractionation experiment, organelles in a tissue homogenate are separated by differential centrifugation. Which principle governs pelleting order?",
        "options": [
            "Larger, denser organelles pellet at lower centrifugal forces (speeds), whereas smaller, less dense organelles require higher speeds",
            "All organelles pellet simultaneously regardless of mass",
            "Lighter organelles pellet first at low speeds",
            "Soluble cytosolic proteins pellet before nuclei",
            "Centrifugal force does not separate organelles"
        ],
        "answer": "Larger, denser organelles pellet at lower centrifugal forces (speeds), whereas smaller, less dense organelles require higher speeds",
        "explanation": "Differential centrifugation pellets heavy/large components (nuclei) at low speed ($1000g$), mitochondria at medium speed ($10,000g$), and small vesicles/microsomes at high speed ($100,000g$)."
    },
    {
        "id": 71,
        "question": "Plasma membrane fluidity enables cells to alter shape and function. How do cells adapt membrane fluidity in response to cold environmental temperatures?",
        "options": [
            "Increase saturation of fatty acid chains (remove double bonds)",
            "Increase the proportion of cis-unsaturated fatty acids in phospholipids",
            "Remove all cholesterol molecules",
            "Degrade integral membrane proteins",
            "Increase chain length of fatty acids to 30 carbons"
        ],
        "answer": "Increase the proportion of cis-unsaturated fatty acids in phospholipids",
        "explanation": "Cis-double bonds create kinks in acyl chains, preventing tight packing and maintaining membrane fluidity in cold conditions."
    },
    {
        "id": 72,
        "question": "Glucose transport across the apical membrane of intestinal epithelial cells occurs against its concentration gradient via Na+/glucose co-transporter 1 (SGLT-1). What mechanism is this?",
        "options": [
            "Simple diffusion",
            "Primary active transport",
            "Secondary active transport (symport)",
            "Facilitated diffusion",
            "Pinocytosis"
        ],
        "answer": "Secondary active transport (symport)",
        "explanation": "SGLT-1 uses the Na+ electrochemical gradient (established by the primary active Na+/K+ pump) to co-transport glucose into enterocytes."
    },
    {
        "id": 73,
        "question": "Glucose exit across the basolateral membrane of enterocytes into blood down its concentration gradient is mediated by GLUT-2 via:",
        "options": [
            "Primary active transport",
            "Facilitated diffusion",
            "Secondary active antiport",
            "Simple diffusion",
            "Endocytosis"
        ],
        "answer": "Facilitated diffusion",
        "explanation": "GLUT-2 is a uniporter protein carrier that transports glucose passively down its concentration gradient without energy expenditure."
    },
    {
        "id": 74,
        "question": "Movement of water across a semipermeable membrane from a region of low solute concentration to high solute concentration is:",
        "options": [
            "Primary active transport",
            "Osmosis",
            "Secondary active transport",
            "Filtration",
            "Bulk flow"
        ],
        "answer": "Osmosis",
        "explanation": "Osmosis is passive water movement across a selective membrane driven by an osmotic pressure gradient."
    },
    {
        "id": 75,
        "question": "Which cell cycle checkpoint ensures that all chromosomes are properly aligned at the equatorial plate and attached to spindle fibers before sister chromatid segregation?",
        "options": [
            "G1/S checkpoint",
            "G2/M checkpoint",
            "Metaphase (Spindle Assembly) checkpoint",
            "G0 checkpoint",
            "S phase checkpoint"
        ],
        "answer": "Metaphase (Spindle Assembly) checkpoint",
        "explanation": "The spindle assembly checkpoint (SAC) delays anaphase onset until all kinetochores are bi-oriented and attached to spindle microtubules."
    },
    {
        "id": 76,
        "question": "Sister chromatids are split apart and pulled toward opposite spindle poles during which mitotic phase?",
        "options": [
            "Prophase",
            "Metaphase",
            "Anaphase",
            "Telophase",
            "Cytokinesis"
        ],
        "answer": "Anaphase",
        "explanation": "During Anaphase, separase cleaves cohesin complexes holding sister chromatids together, allowing them to segregate."
    },
    {
        "id": 77,
        "question": "Which phase of Meiosis I is the longest in duration, involving synapsis, tetrad formation, and homologous recombination (crossing over)?",
        "options": [
            "Metaphase I",
            "Prophase I",
            "Anaphase I",
            "Telophase I",
            "Prophase II"
        ],
        "answer": "Prophase I",
        "explanation": "Prophase I is extended (subdivided into leptotene, zygotene, pachytene, diplotene, and diakinesis) to accommodate homologous pairing and genetic recombination."
    },
    {
        "id": 78,
        "question": "Tay-Sachs disease is a fatal genetic disorder caused by deficiency of hexosaminidase A, leading to GM2 ganglioside accumulation in neurons. Which organelle is impaired?",
        "options": [
            "Peroxisome",
            "Lysosome",
            "Mitochondrion",
            "Golgi apparatus",
            "Endoplasmic reticulum"
        ],
        "answer": "Lysosome",
        "explanation": "Tay-Sachs is a lysosomal storage disease resulting from defective lysosomal degradation of sphingolipids."
    },
    {
        "id": 79,
        "question": "Which organelle contains catalase and oxidase enzymes responsible for detoxifying hydrogen peroxide (H2O2) and beta-oxidizing very long chain fatty acids (VLCFAs)?",
        "options": [
            "Lysosome",
            "Peroxisome",
            "Mitochondrion",
            "Golgi complex",
            "Proteasome"
        ],
        "answer": "Peroxisome",
        "explanation": "Peroxisomes carry out oxidative reactions producing H2O2, which catalase converts to H2O and O2, and oxidize VLCFAs."
    },
    {
        "id": 80,
        "question": "The resting membrane potential ($RMP$) of a human skeletal muscle cell (typically -90 mV) is primarily established by leak conductance of which ion?",
        "options": [
            "Na+",
            "K+",
            "Ca2+",
            "Cl-",
            "HCO3-"
        ],
        "answer": "K+",
        "explanation": "High resting membrane permeability to K+ via inward rectifier K+ leak channels makes the RMP close to $E_K$ (-90 mV)."
    }
]
BIOCHEM_QS = [
    {
        "id": 81,
        "question": "Which standard amino acid possesses a side chain (R-group) containing an aromatic ring with a hydroxyl group, giving it amphipathic properties?",
        "options": [
            "Alanine",
            "Phenylalanine",
            "Tyrosine",
            "Glycine",
            "Leucine"
        ],
        "answer": "Tyrosine",
        "explanation": "Tyrosine contains a phenolic hydroxyl group attached to a phenyl ring, making it polar aromatic."
    },
    {
        "id": 82,
        "question": "Which amino acid lacks an enantiomeric L- or D- configuration because its alpha-carbon is bonded to two hydrogen atoms (achiral)?",
        "options": [
            "Alanine",
            "Glycine",
            "Proline",
            "Valine",
            "Isoleucine"
        ],
        "answer": "Glycine",
        "explanation": "Glycine's R-group is a single hydrogen atom; thus its alpha-carbon is not chiral."
    },
    {
        "id": 83,
        "question": "Ranking the standard amino acids Alanine (Ala), Tyrosine (Tyr), Glycine (Gly), and Aspartate (Asp) in order of INCREASING polarity at pH 7.0 yields:",
        "options": [
            "Ala < Gly < Tyr < Asp",
            "Asp < Tyr < Gly < Ala",
            "Gly < Ala < Tyr < Asp",
            "Ala < Tyr < Gly < Asp",
            "Tyr < Ala < Gly < Asp"
        ],
        "answer": "Ala < Gly < Tyr < Asp",
        "explanation": "Ala (nonpolar aliphatic) < Gly (achiral small nonpolar) < Tyr (polar aromatic) < Asp (charged acidic R-group)."
    },
    {
        "id": 84,
        "question": "The transmembrane domain of an integral membrane receptor (such as the Amyloid Precursor Protein) passes through the hydrophobic lipid bilayer. Which peptide sequence is most likely found in this domain?",
        "options": [
            "Glu-Glu-Ser-Tyr",
            "Thr-Ile-Glu-Asn",
            "Phe-Leu-Ile-Val",
            "Asp-Lys-Lys-Lys",
            "Arg-Glu-Asp-His"
        ],
        "answer": "Phe-Leu-Ile-Val",
        "explanation": "Transmembrane domains consist of nonpolar, hydrophobic amino acid residues (Phe, Leu, Ile, Val) that interact favorably with fatty acyl chains."
    },
    {
        "id": 85,
        "question": "At physiological pH (7.4), the tripeptide Asp-Pro-Lys carries a net charge of:",
        "options": [
            "+2",
            "+1",
            "0 (Isoelectric zwitterion)",
            "-1",
            "-2"
        ],
        "answer": "0 (Isoelectric zwitterion)",
        "explanation": "At pH 7.4: N-terminus (+1), Asp side chain (-1), Lys side chain (+1), C-terminus (-1). Net charge = +1 - 1 + 1 - 1 = 0."
    },
    {
        "id": 86,
        "question": "Patients with Scurvy present with bleeding gums and poor wound healing due to impaired collagen triple helix stabilization. Which post-translational modification is defective?",
        "options": [
            "Carboxylation of Glutamate",
            "Hydroxylation of Proline and Lysine residues by prolyl hydroxylase (requiring Vitamin C)",
            "Phosphorylation of Serine",
            "Glycosylation of Asparagine",
            "Methylation of Histidine"
        ],
        "answer": "Hydroxylation of Proline and Lysine residues by prolyl hydroxylase (requiring Vitamin C)",
        "explanation": "Prolyl and lysyl hydroxylase require Vitamin C (ascorbate) as a cofactor to form 4-hydroxyproline, essential for inter-chain hydrogen bonding in collagen."
    },
    {
        "id": 87,
        "question": "What primary chemical force stabilizes the alpha-helix and beta-pleated sheet secondary structures of proteins?",
        "options": [
            "Covalent disulfide bonds between Cysteine residues",
            "Hydrogen bonding between peptide backbone N-H and C=O groups",
            "Hydrophobic interactions between nonpolar side chains",
            "Ionic salt bridges between Lysine and Aspartate",
            "Van der Waals dispersion forces"
        ],
        "answer": "Hydrogen bonding between peptide backbone N-H and C=O groups",
        "explanation": "Protein secondary structures are formed by regular hydrogen bonds between peptide amide N-H and carbonyl C=O backbone atoms."
    },
    {
        "id": 88,
        "question": "The primary structure of a protein is defined exclusively by its:",
        "options": [
            "3D globular folding pattern",
            "Isoelectric point (pI)",
            "Linear amino acid sequence joined by peptide bonds",
            "Subunit quaternary arrangement",
            "Alpha-helical content"
        ],
        "answer": "Linear amino acid sequence joined by peptide bonds",
        "explanation": "Primary structure is the specific, genetically determined linear sequence of amino acids linked by covalent peptide bonds."
    },
    {
        "id": 89,
        "question": "Denaturation of a globular enzyme by heat or extreme pH disrupts its 3D native conformation and catalytic activity. Which structural level remains intact?",
        "options": [
            "Primary structure",
            "Secondary structure",
            "Tertiary structure",
            "Quaternary structure",
            "All structural levels are destroyed"
        ],
        "answer": "Primary structure",
        "explanation": "Denaturation breaks non-covalent secondary/tertiary interactions (hydrogen bonds, ionic bonds) but does NOT hydrolyze covalent peptide bonds of the primary structure."
    },
    {
        "id": 90,
        "question": "An infant presents with severe vomiting, metabolic acidosis, and elevated plasma levels of Leucine, Isoleucine, and Valine. What metabolic disorder is present?",
        "options": [
            "Phenylketonuria (PKU)",
            "Maple Syrup Urine Disease (MSUD)",
            "Alkaptonuria",
            "Homocystinuria",
            "Tyrosinemia Type 1"
        ],
        "answer": "Maple Syrup Urine Disease (MSUD)",
        "explanation": "MSUD results from deficiency of branched-chain alpha-keto acid dehydrogenase, leading to buildup of branched-chain amino acids (Leu, Ile, Val)."
    },
    {
        "id": 91,
        "question": "A 60-year-old institutionalized man with severe intellectual disability has urine that turns dark green upon addition of Ferric Chloride (FeCl3). Which metabolite is detected?",
        "options": [
            "Homogentisic acid",
            "Phenylpyruvate (from Phenylalanine)",
            "Methylmalonic acid",
            "Uroporphyrin",
            "Bilirubin diglucuronide"
        ],
        "answer": "Phenylpyruvate (from Phenylalanine)",
        "explanation": "In PKU (phenylalanine hydroxylase deficiency), excess phenylalanine transaminates to phenylpyruvate, which produces a characteristic green color with ferric chloride."
    },
    {
        "id": 92,
        "question": "Neurodegenerative Alzheimer's disease is pathologically characterized by extracellular senile plaques composed of misfolded aggregations of:",
        "options": [
            "Alpha-synuclein",
            "Beta-amyloid (A-beta) peptides rich in beta-pleated sheets",
            "Prion protein (PrPSc)",
            "Huntingtin protein",
            "Tau neurofibrillary tangles"
        ],
        "answer": "Beta-amyloid (A-beta) peptides rich in beta-pleated sheets",
        "explanation": "Abnormal cleavage of Amyloid Precursor Protein (APP) yields A-beta monomers that misfold into insoluble, cross-beta sheet amyloid fibrils."
    },
    {
        "id": 93,
        "question": "Comparing the oxygen binding curves of Hemoglobin (Hb) and Myoglobin (Mb):",
        "options": [
            "Mb curve is sigmoidal; Hb curve is hyperbolic",
            "Mb curve is hyperbolic (high affinity, no cooperativity); Hb curve is sigmoidal due to positive cooperativity among 4 subunits",
            "Both curves are identical",
            "Hb has higher O2 affinity than Mb at all pO2 values",
            "Mb binds 4 O2 molecules per monomer"
        ],
        "answer": "Mb curve is hyperbolic (high affinity, no cooperativity); Hb curve is sigmoidal due to positive cooperativity among 4 subunits",
        "explanation": "Monomeric Myoglobin binds O2 hyperbolically with high affinity ($P_{50} = 2.8\\text{ mmHg}$). Tetrameric Hemoglobin binds O2 cooperatively, yielding a sigmoidal curve ($P_{50} = 26\\text{ mmHg}$)."
    },
    {
        "id": 94,
        "question": "Carbon Monoxide (CO) poisoning causes severe tissue hypoxia because CO:",
        "options": [
            "Destroys red blood cells instantly",
            "Binds to iron in heme with ~200-fold higher affinity than O2, competing with O2 and locking remaining subunits in the high-affinity R-state",
            "Inhibits carbonic anhydrase",
            "Decreases 2,3-BPG synthesis",
            "Converts hemoglobin into methemoglobin"
        ],
        "answer": "Binds to iron in heme with ~200-fold higher affinity than O2, competing with O2 and locking remaining subunits in the high-affinity R-state",
        "explanation": "CO binds Hb with 200x affinity of O2, reducing O2 carrying capacity and shifting the O2 dissociation curve left, preventing oxygen release to tissues."
    },
    {
        "id": 95,
        "question": "What is the primary emergency clinical management for acute severe Carbon Monoxide poisoning?",
        "options": [
            "Intravenous sodium bicarbonate",
            "Administration of 100% normobaric or hyperbaric oxygen",
            "Immediate blood exchange transfusion",
            "Subcutaneous erythropoietin",
            "Dialysis"
        ],
        "answer": "Administration of 100% normobaric or hyperbaric oxygen",
        "explanation": "High pO2 displaces CO from hemoglobin by mass action, shortening the half-life of carboxyhemoglobin from ~320 minutes to ~80 minutes (or ~20 min hyperbaric)."
    },
    {
        "id": 96,
        "question": "The digestive protease Pepsin has an isoelectric point (pI) < 2.0, whereas Lysozyme has a pI of 11.0. Which amino acids predominate in each protein?",
        "options": [
            "Aspartate/Glutamate in Pepsin; Lysine/Arginine in Lysozyme",
            "Lysine in Pepsin; Aspartate in Lysozyme",
            "Histidine in Pepsin; Leucine in Lysozyme",
            "Glycine in Pepsin; Alanine in Lysozyme",
            "Cysteine in Pepsin; Proline in Lysozyme"
        ],
        "answer": "Aspartate/Glutamate in Pepsin; Lysine/Arginine in Lysozyme",
        "explanation": "Proteins with low pI are rich in acidic residues (Asp, Glu), while proteins with high pI are rich in basic residues (Lys, Arg)."
    },
    {
        "id": 97,
        "question": "Coenzymes essential for metabolic catalysis (such as NAD+, FAD, TPP, and Coenzyme A) are organic derivatives synthesized from dietary:",
        "options": [
            "Essential fatty acids",
            "Water-soluble B-complex vitamins",
            "Fat-soluble vitamins (A, D, E, K)",
            "Trace mineral elements",
            "Essential amino acids"
        ],
        "answer": "Water-soluble B-complex vitamins",
        "explanation": "B-vitamins serve as precursors for coenzymes: Niacin (NAD+), Riboflavin (FAD), Thiamine (TPP), Pantothenic acid (CoA), Pyridoxine (PLP)."
    },
    {
        "id": 98,
        "question": "Which amino acid substitution in a protein is LEAST likely to alter its tertiary structure and function?",
        "options": [
            "Glutamate (charged acidic) to Aspartate (charged acidic)",
            "Glutamate (charged) to Valine (nonpolar)",
            "Glycine to Proline",
            "Cysteine to Serine",
            "Lysine (basic) to Glutamate (acidic)"
        ],
        "answer": "Glutamate (charged acidic) to Aspartate (charged acidic)",
        "explanation": "Conservative amino acid substitutions replace a residue with one of similar size, charge, and polarity (Glu -> Asp), preserving structure."
    },
    {
        "id": 99,
        "question": "Sickle Cell Anemia results from a single point mutation in the beta-globin gene causing which amino acid substitution at position 6?",
        "options": [
            "Glutamate -> Valine",
            "Valine -> Glutamate",
            "Lysine -> Arginine",
            "Glycine -> Alanine",
            "Aspartate -> Serine"
        ],
        "answer": "Glutamate -> Valine",
        "explanation": "HbS mutation substitutes a polar surface Glutamate with nonpolar Valine at position 6 of the beta chain, causing hydrophobic polymer formation when deoxygenated."
    },
    {
        "id": 100,
        "question": "In the Bohr effect, an increase in blood CO2 concentration and decrease in pH shift the Hemoglobin-Oxygen dissociation curve:",
        "options": [
            "To the left (increasing O2 affinity)",
            "To the right (decreasing O2 affinity, promoting O2 unloading)",
            "Upward",
            "Downward without shifting P50",
            "No change"
        ],
        "answer": "To the right (decreasing O2 affinity, promoting O2 unloading)",
        "explanation": "Higher $H^+$ and $CO_2$ stabilize the T-state of Hb, shifting the dissociation curve right ($P_{50}$ increases), facilitating O2 release in metabolically active tissues."
    },
    {
        "id": 101,
        "question": "2,3-Bisphosphoglycerate (2,3-BPG) binds selectively to the central cavity of deoxygenated Hemoglobin. How does elevated 2,3-BPG affect oxygen delivery?",
        "options": [
            "Increases O2 affinity",
            "Decreases O2 affinity, shifting curve right and enhancing O2 unloading in peripheral tissues during high altitude adaptation",
            "Prevents CO2 transport",
            "Converts Hb into myoglobin",
            "Inhibits heme synthesis"
        ],
        "answer": "Decreases O2 affinity, shifting curve right and enhancing O2 unloading in peripheral tissues during high altitude adaptation",
        "explanation": "2,3-BPG stabilizes the T-state (deoxy-Hb), lowering O2 affinity and shifting the binding curve right to maximize tissue O2 unloading."
    },
    {
        "id": 102,
        "question": "Why does Fetal Hemoglobin (HbF, alpha2-gamma2) possess a higher affinity for oxygen than Adult Hemoglobin (HbA, alpha2-beta2)?",
        "options": [
            "HbF has 6 subunits",
            "The gamma-chains of HbF have lower affinity for 2,3-BPG due to substitution of Histidine-143 with Serine",
            "HbF contains ferric iron (Fe3+)",
            "HbF does not bind oxygen cooperatively",
            "HbA lacks alpha chains"
        ],
        "answer": "The gamma-chains of HbF have lower affinity for 2,3-BPG due to substitution of Histidine-143 with Serine",
        "explanation": "Fetal gamma chains lack positive His-143 residues required to bind 2,3-BPG tightly; lower 2,3-BPG binding allows HbF to bind O2 more tightly than HbA, facilitating transplacental O2 transfer."
    },
    {
        "id": 103,
        "question": "Methemoglobinemia occurs when the heme iron of hemoglobin is oxidized from the ferrous state (Fe2+) to the ferric state (Fe3+). What is the functional consequence?",
        "options": [
            "Ferric heme cannot bind O2, causing cyanosis and chocolate-brown blood",
            "Increases O2 transport capacity",
            "Causes immediate hemolysis",
            "Turns blood bright red",
            "Increases renal clearance of iron"
        ],
        "answer": "Ferric heme cannot bind O2, causing cyanosis and chocolate-brown blood",
        "explanation": "Fe3+ (ferric iron) cannot reversibly bind O2; methemoglobinemia impairs oxygen transport and presents with chocolate-brown blood and cyanosis."
    },
    {
        "id": 104,
        "question": "Which enzyme reduces methemoglobin back to functional ferrous hemoglobin (Fe2+) in erythrocytes using NADH generated by glycolysis?",
        "options": [
            "Methemoglobin reductase (Cytochrome b5 reductase)",
            "Glucose-6-Phosphate Dehydrogenase",
            "Glutathione peroxidase",
            "Superoxide dismutase",
            "Catalase"
        ],
        "answer": "Methemoglobin reductase (Cytochrome b5 reductase)",
        "explanation": "Erythrocyte Cytochrome b5 reductase (Methemoglobin reductase) uses glycolytic NADH to reduce Fe3+ back to Fe2+."
    },
    {
        "id": 105,
        "question": "Which amino acid residue in myoglobin and hemoglobin directly chelates the Fe2+ atom of the heme prosthetic group at the 5th coordination position?",
        "options": [
            "Proximal Histidine (F8)",
            "Distal Histidine (E7)",
            "Valine E11",
            "Phenylalanine CD1",
            "Lysine EF6"
        ],
        "answer": "Proximal Histidine (F8)",
        "explanation": "The Proximal Histidine (His F8) forms a direct coordination bond with the 5th coordination site of the heme Fe2+ atom."
    },
    {
        "id": 106,
        "question": "The Distal Histidine (His E7) in hemoglobin functions to:",
        "options": [
            "Bind directly to iron",
            "Sterically hinder linear carbon monoxide binding while stabilizing bound O2 via a hydrogen bond",
            "Hydrolyze ATP",
            "Phosphorylate heme",
            "Cleave peptide bonds"
        ],
        "answer": "Sterically hinder linear carbon monoxide binding while stabilizing bound O2 via a hydrogen bond",
        "explanation": "His E7 creates steric hindrance that forces CO to bind at an angle (reducing its binding affinity) while hydrogen bonding to bent bound O2."
    },
    {
        "id": 107,
        "question": "Enzymes increase the rate of chemical reactions by several orders of magnitude by:",
        "options": [
            "Increasing overall free energy change (Delta G)",
            "Lowering activation energy (Ea) of the transition state",
            "Shifting reaction equilibrium constant (Keq)",
            "Consuming ATP in all reactions",
            "Increasing temperature"
        ],
        "answer": "Lowering activation energy (Ea) of the transition state",
        "explanation": "Enzymes stabilize the transition state intermediate, lowering the activation energy barrier ($E_a$) without altering net $\\Delta G$ or $K_{eq}$."
    },
    {
        "id": 108,
        "question": "In Michaelis-Menten enzyme kinetics, the Michaelis constant (Km) represents:",
        "options": [
            "Maximal velocity (Vmax)",
            "Substrate concentration [S] at which reaction velocity is half Vmax (1/2 Vmax)",
            "Enzyme turnover number (kcat)",
            "Inhibitor dissociation constant",
            "Total enzyme concentration"
        ],
        "answer": "Substrate concentration [S] at which reaction velocity is half Vmax (1/2 Vmax)",
        "explanation": "$K_m$ is the substrate concentration required to achieve $50\\%$ of $V_{max}$; a low $K_m$ indicates high enzyme-substrate affinity."
    },
    {
        "id": 109,
        "question": "How does a Competitive Enzyme Inhibitor affect Vmax and Km values on a Lineweaver-Burk plot?",
        "options": [
            "Km increases (affinity appears reduced); Vmax remains unchanged",
            "Vmax decreases; Km remains unchanged",
            "Both Km and Vmax decrease",
            "Both Km and Vmax increase",
            "Vmax increases; Km decreases"
        ],
        "answer": "Km increases (affinity appears reduced); Vmax remains unchanged",
        "explanation": "Competitive inhibitors bind to the active site, increasing apparent $K_m$ (requires more substrate to reach $1/2 V_{max}$), but $V_{max}$ is unchanged because high substrate concentration overcomes inhibition."
    },
    {
        "id": 110,
        "question": "A Noncompetitive Enzyme Inhibitor alters kinetic parameters by:",
        "options": [
            "Increasing Km; Vmax unchanged",
            "Decreasing Vmax; Km remains unchanged",
            "Decreasing Km; Vmax unchanged",
            "Increasing both Vmax and Km",
            "Abolishing all substrate binding"
        ],
        "answer": "Decreasing Vmax; Km remains unchanged",
        "explanation": "Noncompetitive inhibitors bind an allosteric site on both free enzyme and ES complex, reducing catalytic efficiency ($V_{max}$ decreases) without altering substrate binding affinity ($K_m$ unchanged)."
    },
    {
        "id": 111,
        "question": "Organophosphate nerve agents (such as sarin) irreversibly inhibit Acetylcholinesterase by forming a covalent bond with which active-site amino acid residue?",
        "options": [
            "Serine",
            "Histidine",
            "Aspartate",
            "Cysteine",
            "Lysine"
        ],
        "answer": "Serine",
        "explanation": "Organophosphates covalently phosphorylate the active-site Serine hydroxyl group of acetylcholinesterase, leading to cholinergic crisis."
    },
    {
        "id": 112,
        "question": "The catalytic triad present in serine proteases (such as trypsin, chymotrypsin, and elastase) consists of which three amino acid residues?",
        "options": [
            "Serine, Histidine, Aspartate",
            "Serine, Cysteine, Lysine",
            "Alanine, Glycine, Valine",
            "Proline, Hydroxyproline, Lysine",
            "Glutamate, Glutamine, Arginine"
        ],
        "answer": "Serine, Histidine, Aspartate",
        "explanation": "Serine proteases utilize a catalytic triad of Ser-195, His-57, and Asp-102 to generate a nucleophilic alkoxide ion on Serine."
    },
    {
        "id": 113,
        "question": "Trypsin cleaves peptide bonds on the carboxyl side of which specific amino acid residues?",
        "options": [
            "Aromatic residues (Phe, Tyr, Trp)",
            "Basic, positively charged residues (Lysine, Arginine)",
            "Small uncharged residues (Ala, Gly)",
            "Acidic residues (Asp, Glu)",
            "Proline"
        ],
        "answer": "Basic, positively charged residues (Lysine, Arginine)",
        "explanation": "Trypsin's specificity pocket contains a negatively charged Asp-189 at the bottom, attracting positively charged Lysine and Arginine side chains."
    },
    {
        "id": 114,
        "question": "Chymotrypsin selectively hydrolyzes peptide bonds adjacent to bulky nonpolar residues because its active site specificity pocket is lined with:",
        "options": [
            "Hydrophobic amino acids suited for aromatic side chains (Phe, Tyr, Trp)",
            "Positively charged Lysine residues",
            "Negatively charged Aspartate residues",
            "Zinc ions",
            "Carbohydrate chains"
        ],
        "answer": "Hydrophobic amino acids suited for aromatic side chains (Phe, Tyr, Trp)",
        "explanation": "Chymotrypsin has a deep, hydrophobic binding pocket that accommodates large aromatic rings (Phe, Tyr, Trp)."
    },
    {
        "id": 115,
        "question": "What is the primary function of Zymogens (proenzymes) synthesized by digestive glands?",
        "options": [
            "Inactive precursor forms that prevent premature autodigestion of pancreatic and gastric cellular tissues",
            "Active enzymes that digest dietary lipids",
            "Storage forms of amino acids",
            "Hormones regulating blood glucose",
            "Coenzymes for vitamins"
        ],
        "answer": "Inactive precursor forms that prevent premature autodigestion of pancreatic and gastric cellular tissues",
        "explanation": "Zymogens (e.g., trypsinogen, pepsinogen) are inactive precursors secreted into digestive lumens where specific proteolytic cleavages activate them safely."
    },
    {
        "id": 116,
        "question": "Enteropeptidase (enterokinase) secreted by duodenal mucosal cells activates the pancreatic digestive enzyme cascade by cleaving:",
        "options": [
            "Trypsinogen to active Trypsin",
            "Chymotrypsinogen to Chymotrypsin",
            "Procarboxypeptidase to Carboxypeptidase",
            "Pepsinogen to Pepsin",
            "Proelastase to Elastase"
        ],
        "answer": "Trypsinogen to active Trypsin",
        "explanation": "Enteropeptidase cleaves hexapeptide from trypsinogen to produce active Trypsin, which then autocatalytically activates all other pancreatic zymogens."
    },
    {
        "id": 117,
        "question": "Which enzyme converts inactive Pepsinogen into active Pepsin in the gastric lumen?",
        "options": [
            "Hydrochloric acid (HCl) and active Pepsin (autocatalysis)",
            "Enteropeptidase",
            "Trypsin",
            "Gastrin",
            "Bicarbonate"
        ],
        "answer": "Hydrochloric acid (HCl) and active Pepsin (autocatalysis)",
        "explanation": "Low gastric pH ($< 2.0$) induced by HCl causes pepsinogen to undergo conformational change and self-cleavage into active Pepsin."
    },
    {
        "id": 118,
        "question": "Allosteric enzymes display sigmoidal kinetics rather than hyperbolic Michaelis-Menten kinetics because of:",
        "options": [
            "Cooperativity among multiple active sites upon effector binding at allosteric sites",
            "Irreversible inhibition",
            "Denaturation at high substrate concentration",
            "Lack of quaternary structure",
            "Covalent modification"
        ],
        "answer": "Cooperativity among multiple active sites upon effector binding at allosteric sites",
        "explanation": "Allosteric enzymes are multi-subunit complexes; binding of substrates or effectors induces conformational shifts between T (low affinity) and R (high affinity) states."
    },
    {
        "id": 119,
        "question": "In the regulation of Glycolysis, Phosphofructokinase-1 (PFK-1) is allosterically ACTIVATED by:",
        "options": [
            "AMP and Fructose-2,6-bisphosphate",
            "ATP and Citrate",
            "NADH and Acetyl-CoA",
            "Glucagon",
            "Long-chain fatty acids"
        ],
        "answer": "AMP and Fructose-2,6-bisphosphate",
        "explanation": "PFK-1 is the key rate-limiting glycolytic enzyme; low cellular energy (high AMP) and high insulin signaling (Fructose-2,6-bisphosphate) potently activate PFK-1."
    },
    {
        "id": 120,
        "question": "Isoenzymes (isozymes) are defined as:",
        "options": [
            "Enzymes that catalyze the same chemical reaction but differ in amino acid sequence, tissue distribution, and kinetic properties (e.g., LDH1 vs LDH5)",
            "Identical enzymes found in different cell organelles",
            "Enzymes activated by proteolysis",
            "Inactive precursor proteins",
            "Enzymes that function without cofactors"
        ],
        "answer": "Enzymes that catalyze the same chemical reaction but differ in amino acid sequence, tissue distribution, and kinetic properties (e.g., LDH1 vs LDH5)",
        "explanation": "Isozymes are distinct proteins (encoded by different genes or splice variants) that catalyze the same reaction but possess different kinetic parameters and tissue distribution."
    }
]

def render_quiz_section(questions, prefix):
    if f"score_{prefix}" not in st.session_state:
        st.session_state[f"score_{prefix}"] = 0
    if f"submitted_{prefix}" not in st.session_state:
        st.session_state[f"submitted_{prefix}"] = {}

    user_answers = {}
    
    for q in questions:
        qid = q["id"]
        st.subheader(f"Q{qid}. {q['question']}")
        opts = q["options"]
        
        user_choice = st.radio(
            "Select your answer:",
            opts,
            key=f"{prefix}_q_{qid}",
            index=None
        )
        user_answers[qid] = user_choice
        
        if st.session_state[f"submitted_{prefix}"].get(qid):
            if user_choice == q["answer"]:
                st.success(f"✅ Correct! Answer: {q['answer']}")
            else:
                st.error(f"❌ Incorrect. Correct Answer: {q['answer']}")
            st.info(f"💡 **Explanation:** {q['explanation']}")
        st.markdown("---")

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button(f"Submit All Answers", key=f"btn_{prefix}"):
            correct_count = 0
            for q in questions:
                qid = q["id"]
                st.session_state[f"submitted_{prefix}"][qid] = True
                if user_answers.get(qid) == q["answer"]:
                    correct_count += 1
            st.session_state[f"score_{prefix}"] = correct_count
            st.rerun()

    if any(st.session_state[f"submitted_{prefix}"].values()):
        score = st.session_state[f"score_{prefix}"]
        total = len(questions)
        pct = (score / total) * 100
        st.metric(label=f"Module Score ({prefix.upper()})", value=f"{score} / {total}", delta=f"{pct:.1f}%")


with tab1:
    st.header("🫀 Anatomy & Histology (40 Questions)")
    render_question_list(ANAT_QS, "Anatomy & Histology", "anat")

with tab2:
    st.header("⚡ Physiology (40 Questions)")
    render_question_list(PHYS_QS, "Physiology", "phys")

with tab3:
    st.header("🧪 Biochemistry & Bioenergetics (40 Questions)")
    render_question_list(BIOCHEM_QS, "Biochemistry", "biochem")

import streamlit as st

st.set_page_config(page_title="MSPC235 Interactive Exam Quiz", layout="wide")

st.title("💪🏼 MSPC 235: Musculoskeletal & Locomotor Systems (MSPC235)")
st.markdown("### Interactive Comprehensive Question Bank (120 Questions)")
st.caption("Grounded in Compiled Past Exam Questions and Assessment Trends.")

# Define tabs
tab1, tab2, tab3 = st.tabs(["🫀 Anatomy & Histology (40 Qs)", "⚡ Physiology (40 Qs)", "🧪 Biochemistry & Bioenergetics (40 Qs)"])

ANAT_QS = [
    {
        "id": 1,
        "question": "A 25-year-old motorcyclist falls onto his right shoulder, markedly increasing the angle between his neck and shoulder. Physical examination reveals an arm hanging by his side, medially rotated, and pronated ('waiter's tip' stance). Which spinal nerve roots of the brachial plexus are damaged (Erb-Duchenne palsy)?",
        "options": [
            "C5 and C6 roots",
            "C8 and T1 roots",
            "C7 and C8 roots",
            "T1 and T2 roots",
            "C6 and C7 roots"
        ],
        "answer": "C5 and C6 roots",
        "explanation": "Traction injury separating neck and shoulder ruptures C5-C6 roots/upper trunk, paralyzing abductors (deltoid, supraspinatus), lateral rotators (infraspinatus, teres minor), and supinators (biceps brachii)."
    },
    {
        "id": 2,
        "question": "When examining a patient with Erb-Duchenne palsy (upper trunk brachial plexus injury), which of the following upper limb movements remains UNAFFECTED?",
        "options": [
            "Abduction of arm at shoulder",
            "Lateral rotation of arm",
            "Forearm supination",
            "Elbow flexion",
            "Adduction of arm at shoulder"
        ],
        "answer": "Adduction of arm at shoulder",
        "explanation": "Arm adduction is powered by Pectoralis major and Latissimus dorsi (innervated by pectoral, thoracodorsal, and subscapular nerves derived from C6-C8/T1), remaining functional."
    },
    {
        "id": 3,
        "question": "A female gymnast falls and grabs a high bar with one hand, excessively stretching her arm superiorly. She develops weakness of intrinsic hand muscles resulting in a 'claw hand' deformity. Injury to which part of the brachial plexus occurred (Klumpke's palsy)?",
        "options": [
            "Upper trunk (C5-C6)",
            "Middle trunk (C7)",
            "Lower trunk / C8-T1 roots",
            "Lateral cord",
            "Posterior cord"
        ],
        "answer": "Lower trunk / C8-T1 roots",
        "explanation": "Hyperabduction injuries rupture C8-T1 roots or the lower trunk, damaging ulnar and median nerve contributions to intrinsic hand muscles (lumbricals, interossei)."
    },
    {
        "id": 4,
        "question": "A 45-year-old woman undergoes chest tube placement in the 5th intercostal space. On day 2, she displays winging of the scapula when pushing her right hand against a wall. Which nerve was injured?",
        "options": [
            "Axillary nerve",
            "Thoracodorsal nerve",
            "Long thoracic nerve",
            "Median nerve",
            "Accessory nerve"
        ],
        "answer": "Long thoracic nerve",
        "explanation": "The long thoracic nerve (roots C5-C7) runs along the outer surface of Serratus anterior on the thoracic wall; injury paralyzes Serratus anterior, causing scapular winging."
    },
    {
        "id": 5,
        "question": "Approximately 75% of the lymphatic drainage from the mammary gland drains into which group of axillary lymph nodes?",
        "options": [
            "Pectoral (Anterior) group",
            "Central axillary group",
            "Apical group",
            "Lateral group",
            "Subscapular group"
        ],
        "answer": "Central axillary group",
        "explanation": "Lymph from anterior/pectoral nodes drains into the Central axillary lymph nodes before passing to apical nodes."
    },
    {
        "id": 6,
        "question": "The axillary tail of Spence of the breast extends superolaterally into the axilla through an opening in the deep fascia called the:",
        "options": [
            "Foramen of Winslow",
            "Foramen of Langer",
            "Costocoracoid membrane",
            "Clavipectoral fascia",
            "Suspensory ligament of Cooper"
        ],
        "answer": "Foramen of Langer",
        "explanation": "The axillary tail of Spence projects into the axilla through Langer's foramen in the deep axillary fascia."
    },
    {
        "id": 7,
        "question": "In a nulliparous woman in the anatomical position, the breast nipple is clinically located over which intercostal space?",
        "options": [
            "2nd intercostal space",
            "3rd intercostal space",
            "4th intercostal space",
            "5th intercostal space",
            "6th intercostal space"
        ],
        "answer": "4th intercostal space",
        "explanation": "In nulliparous females, the nipple is located at the 4th intercostal space in the midclavicular line."
    },
    {
        "id": 8,
        "question": "Which structure pierces the costocoracoid membrane portion of the clavipectoral fascia?",
        "options": [
            "Basilic vein",
            "Cephalic vein",
            "Radial nerve",
            "Musculocutaneous nerve",
            "Brachial artery"
        ],
        "answer": "Cephalic vein",
        "explanation": "Structures piercing the costocoracoid membrane: Cephalic vein, Thoracoacromial artery, Lateral pectoral nerve, and lymphatic vessels."
    },
    {
        "id": 9,
        "question": "A stab wound to the left axilla severs the posterior cord of the brachial plexus. Which muscle will be paralyzed?",
        "options": [
            "Flexor digitorum profundus",
            "Brachialis",
            "Latissimus dorsi",
            "Biceps brachii",
            "Flexor carpi ulnaris"
        ],
        "answer": "Latissimus dorsi",
        "explanation": "The posterior cord gives off upper subscapular, thoracodorsal (supplying Latissimus dorsi), lower subscapular, axillary, and radial nerves."
    },
    {
        "id": 10,
        "question": "Which muscle forms the medial boundary of the axilla?",
        "options": [
            "Pectoralis major",
            "Latissimus dorsi",
            "Serratus anterior",
            "Subscapularis",
            "Teres major"
        ],
        "answer": "Serratus anterior",
        "explanation": "The medial wall of the axilla is formed by the upper 4-5 ribs, intercostal muscles, and the overlying Serratus anterior muscle."
    },
    {
        "id": 11,
        "question": "Which muscle of the rotator cuff is responsible for initiating the first 0 to 15 degrees of arm abduction at the glenohumeral joint?",
        "options": [
            "Deltoid",
            "Supraspinatus",
            "Infraspinatus",
            "Teres minor",
            "Subscapularis"
        ],
        "answer": "Supraspinatus",
        "explanation": "Supraspinatus initiates abduction (0-15\u00b0); Deltoid takes over for 15-90\u00b0, and Serratus anterior/Trapezius rotate the scapula beyond 90\u00b0."
    },
    {
        "id": 12,
        "question": "A 55-year-old tennis player experiences severe shoulder pain. She cannot initiate abduction, but if her arm is elevated past 15 degrees passively, she can fully abduct it. Which muscle tendon is ruptured?",
        "options": [
            "Deltoid",
            "Infraspinatus",
            "Supraspinatus",
            "Teres major",
            "Subscapularis"
        ],
        "answer": "Supraspinatus",
        "explanation": "Inability to initiate 0-15\u00b0 abduction indicates supraspinatus tear or suprascapular nerve damage; deltoid remains functional for >15\u00b0."
    },
    {
        "id": 13,
        "question": "Which rotator cuff muscle acts as the primary, strongest medial rotator of the humerus at the shoulder joint?",
        "options": [
            "Supraspinatus",
            "Infraspinatus",
            "Teres minor",
            "Subscapularis",
            "Teres major"
        ],
        "answer": "Subscapularis",
        "explanation": "Subscapularis inserts into the lesser tubercle of the humerus and is the sole rotator cuff muscle that medially rotates the arm."
    },
    {
        "id": 14,
        "question": "Which muscle is NOT part of the rotator cuff (SITS) functional group?",
        "options": [
            "Supraspinatus",
            "Infraspinatus",
            "Teres minor",
            "Subscapularis",
            "Teres major"
        ],
        "answer": "Teres major",
        "explanation": "The rotator cuff consists of Supraspinatus, Infraspinatus, Teres minor, and Subscapularis (SITS). Teres major is NOT part of the cuff."
    },
    {
        "id": 15,
        "question": "A patient fractures the mid-shaft of the humerus. Which nerve traveling in the radial groove is injured, causing wrist drop?",
        "options": [
            "Axillary nerve",
            "Median nerve",
            "Ulnar nerve",
            "Radial nerve",
            "Musculocutaneous nerve"
        ],
        "answer": "Radial nerve",
        "explanation": "Mid-shaft humerus fractures endanger the radial nerve in the radial (spiral) groove, paralyzing wrist extensors (wrist drop)."
    },
    {
        "id": 16,
        "question": "Fracture of the surgical neck of the humerus endangers which nerve and companion artery passing through the quadrangular space?",
        "options": [
            "Radial nerve and deep brachial artery",
            "Axillary nerve and posterior circumflex humeral artery",
            "Suprascapular nerve and artery",
            "Median nerve and brachial artery",
            "Ulnar nerve and superior ulnar collateral artery"
        ],
        "answer": "Axillary nerve and posterior circumflex humeral artery",
        "explanation": "The axillary nerve and posterior circumflex humeral artery wrap around the surgical neck of the humerus through the quadrangular space."
    },
    {
        "id": 17,
        "question": "A patient falls on an outstretched hand and radiological examination shows anterior dislocation of a proximal carpal bone into the carpal tunnel. Which carpal bone is dislocated?",
        "options": [
            "Scaphoid",
            "Lunate",
            "Capitate",
            "Pisiform",
            "Trapezium"
        ],
        "answer": "Lunate",
        "explanation": "The lunate is the most frequently dislocated carpal bone; anterior dislocation compresses the median nerve in the carpal tunnel."
    },
    {
        "id": 18,
        "question": "What is the most frequently fractured carpal bone following a fall on an outstretched hand, presenting with point tenderness in the anatomical snuffbox?",
        "options": [
            "Lunate",
            "Scaphoid",
            "Hamate",
            "Triquetrum",
            "Capitate"
        ],
        "answer": "Scaphoid",
        "explanation": "The scaphoid is the most commonly fractured carpal bone; retrograde blood supply puts the proximal pole at risk of avascular necrosis."
    },
    {
        "id": 19,
        "question": "Which tendon forms the medial (posterior) boundary of the anatomical snuffbox?",
        "options": [
            "Extensor pollicis brevis",
            "Abductor pollicis longus",
            "Extensor pollicis longus",
            "Abductor pollicis brevis",
            "Extensor indicis"
        ],
        "answer": "Extensor pollicis longus",
        "explanation": "Anatomical snuffbox boundaries: Medial/Posterior = Extensor pollicis longus tendon; Lateral/Anterior = Extensor pollicis brevis and Abductor pollicis longus tendons."
    },
    {
        "id": 20,
        "question": "Compression of the median nerve within the carpal tunnel results in all of the following signs EXCEPT:",
        "options": [
            "Loss of cutaneous sensation over the palmar aspect of the radial 3.5 digits",
            "Wasting of thenar eminence muscles",
            "Loss of thumb opposition",
            "Loss of cutaneous sensation over the hypothenar eminence",
            "Tinel's sign over the flexor retinaculum"
        ],
        "answer": "Loss of cutaneous sensation over the hypothenar eminence",
        "explanation": "Hypothenar sensation is supplied by the ulnar nerve; carpal tunnel syndrome affects median nerve distributions."
    },
    {
        "id": 21,
        "question": "Which nerve innervates the Brachioradialis muscle in the forearm?",
        "options": [
            "Median nerve",
            "Ulnar nerve",
            "Radial nerve",
            "Musculocutaneous nerve",
            "Axillary nerve"
        ],
        "answer": "Radial nerve",
        "explanation": "Brachioradialis is a flexor located in the anterior/lateral forearm, but it is uniquely innervated by the Radial nerve."
    },
    {
        "id": 22,
        "question": "Which nerve pierces and innervates the Coracobrachialis muscle before descending between Biceps brachii and Brachialis?",
        "options": [
            "Median nerve",
            "Axillary nerve",
            "Musculocutaneous nerve",
            "Radial nerve",
            "Ulnar nerve"
        ],
        "answer": "Musculocutaneous nerve",
        "explanation": "The musculocutaneous nerve (C5-C7) pierces Coracobrachialis and supplies all muscles of the anterior compartment of the arm."
    },
    {
        "id": 23,
        "question": "What structures form the superior articular surfaces of the humerus in the elbow joint?",
        "options": [
            "Coronoid process and olecranon",
            "Capitulum and Trochlea",
            "Head of radius and radial notch",
            "Medial and lateral epicondyles",
            "Trochlear notch"
        ],
        "answer": "Capitulum and Trochlea",
        "explanation": "The capitulum (articulates with radial head) and trochlea (articulates with trochlear notch of ulna) form the distal humerus articular surfaces."
    },
    {
        "id": 24,
        "question": "To avoid injuring the sciatic nerve during intramuscular injections in the gluteal region, the injection must be administered into which quadrant?",
        "options": [
            "Upper medial quadrant",
            "Upper lateral quadrant",
            "Lower medial quadrant",
            "Lower lateral quadrant",
            "Ischial tuberosity center"
        ],
        "answer": "Upper lateral quadrant",
        "explanation": "Intramuscular gluteal injections are placed in the upper lateral quadrant (gluteus medius) to avoid the sciatic nerve in lower quadrants."
    },
    {
        "id": 25,
        "question": "Weakness of the Gluteus medius and minimus muscles (paralysis of superior gluteal nerve) causes the pelvis to drop on the unsupported side during walking, known as:",
        "options": [
            "Waddling gait",
            "Trendelenburg sign",
            "Steppage gait",
            "Festinating gait",
            "Antalgic gait"
        ],
        "answer": "Trendelenburg sign",
        "explanation": "Trendelenburg sign occurs when superior gluteal nerve injury paralyzes pelvic abductors (gluteus medius/minimus), causing pelvic tilt toward the unweighted side."
    },
    {
        "id": 26,
        "question": "Which structure lies OUTSIDE the femoral sheath within the femoral triangle?",
        "options": [
            "Femoral artery",
            "Femoral vein",
            "Femoral canal",
            "Femoral nerve",
            "Deep inguinal lymph node of Cloquet"
        ],
        "answer": "Femoral nerve",
        "explanation": "The femoral sheath contains the femoral artery, femoral vein, and femoral canal, but the Femoral Nerve lies outside laterally."
    },
    {
        "id": 27,
        "question": "The popliteus muscle unlocks the fully extended knee joint at the initiation of flexion by executing which movement?",
        "options": [
            "Medially rotating the tibia (or laterally rotating the femur on fixed tibia)",
            "Laterally rotating the tibia on femur",
            "Extending the patella",
            "Anteriorly translating the tibia",
            "Adducting the knee"
        ],
        "answer": "Medially rotating the tibia (or laterally rotating the femur on fixed tibia)",
        "explanation": "Popliteus unlocks the 'screwed-home' knee by laterally rotating the femur on the fixed tibia (or medially rotating tibia on fixed femur)."
    },
    {
        "id": 28,
        "question": "Anterior compartment syndrome of the leg compresses which nerve, causing loss of skin sensation in the web space between the 1st and 2nd toes and foot drop?",
        "options": [
            "Superficial fibular nerve",
            "Deep fibular nerve",
            "Tibial nerve",
            "Saphenous nerve",
            "Sural nerve"
        ],
        "answer": "Deep fibular nerve",
        "explanation": "The deep fibular (peroneal) nerve supplies anterior compartment leg muscles (dorsiflexors) and skin between 1st and 2nd toes."
    },
    {
        "id": 29,
        "question": "Fracture of the neck of the fibula endangers which nerve as it winds around the lateral aspect of the fibular neck?",
        "options": [
            "Tibial nerve",
            "Common fibular (peroneal) nerve",
            "Deep fibular nerve",
            "Superficial fibular nerve",
            "Sciatic nerve"
        ],
        "answer": "Common fibular (peroneal) nerve",
        "explanation": "The common fibular nerve wraps superficially around the fibular neck; trauma causes foot drop (paralysis of dorsiflexors/everters)."
    },
    {
        "id": 30,
        "question": "Pulsations of the posterior tibial artery are best palpated at which anatomical landmark?",
        "options": [
            "Anterior to lateral malleolus",
            "Posterior to medial malleolus",
            "Popliteal fossa floor",
            "Dorsum of foot",
            "Head of fibula"
        ],
        "answer": "Posterior to medial malleolus",
        "explanation": "The posterior tibial artery passes behind the medial malleolus beneath the flexor retinaculum (Tom, Dick, And Nervous Harry)."
    },
    {
        "id": 31,
        "question": "Which intrinsic back muscle group forms the primary extensor of the vertebral column (Iliocostalis, Longissimus, Spinalis)?",
        "options": [
            "Transversospinalis",
            "Erector spinae",
            "Splenius capitis",
            "Interspinales",
            "Rhomboids"
        ],
        "answer": "Erector spinae",
        "explanation": "The erector spinae (iliocostalis, longissimus, spinalis) forms the main intermediate intrinsic muscle mass extending the spine."
    },
    {
        "id": 32,
        "question": "Paralysis of the Trapezius muscle resulting in inability to shrug the shoulder indicates damage to which cranial nerve?",
        "options": [
            "CN V (Trigeminal)",
            "CN VII (Facial)",
            "CN IX (Glossopharyngeal)",
            "CN XI (Spinal Accessory)",
            "CN XII (Hypoglossal)"
        ],
        "answer": "CN XI (Spinal Accessory)",
        "explanation": "CN XI (Spinal Accessory nerve) innervates Trapezius and Sternocleidomastoid; injury impairs shoulder elevation/shrugging."
    },
    {
        "id": 33,
        "question": "Testing the patency of the Thoracodorsal nerve involves evaluating functional contraction of which muscle during shoulder adduction and extension?",
        "options": [
            "Trapezius",
            "Latissimus dorsi",
            "Levator scapulae",
            "Rhomboid major",
            "Serratus anterior"
        ],
        "answer": "Latissimus dorsi",
        "explanation": "The thoracodorsal nerve (C6-C8) innervates Latissimus dorsi ('chin-up' muscle: extends, adducts, medially rotates humerus)."
    },
    {
        "id": 34,
        "question": "In adults, a lumbar puncture (spinal tap) is safely performed between which lumbar spinous processes to avoid spinal cord injury?",
        "options": [
            "L1 and L2",
            "L2 and L3",
            "L3 and L4 (or L4-L5)",
            "T12 and L1",
            "L5 and S1"
        ],
        "answer": "L3 and L4 (or L4-L5)",
        "explanation": "The spinal cord terminates at L1-L2 (conus medullaris) in adults; L3-L4 or L4-L5 needles enter the subarachnoid space safely below cord termination."
    },
    {
        "id": 35,
        "question": "Which curvature of the vertebral column is present at birth (primary curvature)?",
        "options": [
            "Cervical lordosis",
            "Thoracic kyphosis",
            "Lumbar lordosis",
            "Lateral scoliosis",
            "Cervical and lumbar lordosis"
        ],
        "answer": "Thoracic kyphosis",
        "explanation": "Primary curvatures (thoracic and sacral kyphosis) are concave anteriorly and present in fetal life; secondary curvatures (cervical and lumbar lordosis) develop after birth."
    },
    {
        "id": 36,
        "question": "Secondary spinal lordosis in the cervical region develops when an infant begins to:",
        "options": [
            "Sit up unsupported",
            "Hold up its head (~3-4 months)",
            "Walk upright (~12 months)",
            "Crawl on hands and knees",
            "Turn over"
        ],
        "answer": "Hold up its head (~3-4 months)",
        "explanation": "Cervical lordosis develops as the infant learns to hold its head erect; lumbar lordosis develops when the child begins walking upright."
    },
    {
        "id": 37,
        "question": "The great saphenous vein originates on the dorsum of the foot and ascends anterior to which bony landmark?",
        "options": [
            "Lateral malleolus",
            "Medial malleolus",
            "Tibial tuberosity",
            "Head of fibula",
            "Patella"
        ],
        "answer": "Medial malleolus",
        "explanation": "The great saphenous vein passes immediately anterior to the medial malleolus before ascending the medial leg and thigh to enter the saphenous opening."
    },
    {
        "id": 38,
        "question": "Which superficial vein of the leg pierces the deep popliteal fascia to terminate in the popliteal vein?",
        "options": [
            "Great saphenous vein",
            "Small (short) saphenous vein",
            "Anterior tibial vein",
            "Femoral vein",
            "Obturator vein"
        ],
        "answer": "Small (short) saphenous vein",
        "explanation": "The small saphenous vein ascends along the posterior calf behind the lateral malleolus and pierces popliteal fascia to drain into the popliteal vein."
    },
    {
        "id": 39,
        "question": "Which nerve innervates the muscles of the anterior compartment of the thigh (Rectus femoris, Vastus lateralis, Vastus medialis, Vastus intermedius, Sartorius)?",
        "options": [
            "Obturator nerve",
            "Femoral nerve",
            "Sciatic nerve",
            "Superior gluteal nerve",
            "Genitofemoral nerve"
        ],
        "answer": "Femoral nerve",
        "explanation": "The femoral nerve (L2-L4) innervates all anterior compartment thigh muscles (quadriceps femoris and sartorius)."
    },
    {
        "id": 40,
        "question": "The adductor magnus muscle receives dual innervation from which two nerves?",
        "options": [
            "Femoral and Obturator nerves",
            "Obturator nerve and Tibial part of Sciatic nerve",
            "Tibial and Common Fibular nerves",
            "Superior and Inferior gluteal nerves",
            "Femoral and Sciatic nerves"
        ],
        "answer": "Obturator nerve and Tibial part of Sciatic nerve",
        "explanation": "Adductor magnus is a hybrid muscle: adductor part is innervated by the Obturator nerve; hamstring part is innervated by the Tibial portion of the Sciatic nerve."
    }
]
PHYS_QS = [
    {
        "id": 41,
        "question": "Non-keratinized stratified squamous epithelium lines moist mucous surfaces exposed to mechanical abrasion. In which combination of organs is it found?",
        "options": [
            "Vagina, Esophagus, and Oral Cavity / Hard Palate",
            "Skin, Trachea, and Urinary Bladder",
            "Stomach, Colon, and Gallbladder",
            "Alveoli, Capillaries, and Glomerulus",
            "Ureter, Renal pelvis, and Urethra"
        ],
        "answer": "Vagina, Esophagus, and Oral Cavity / Hard Palate",
        "explanation": "Non-keratinized stratified squamous epithelium protects moist internal surfaces subject to friction: oral cavity, esophagus, vagina, and anal canal."
    },
    {
        "id": 42,
        "question": "What is the simple squamous epithelium lining the internal surface of blood vessels and lymphatic channels called?",
        "options": [
            "Mesothelium",
            "Endothelium",
            "Epithelioid tissue",
            "Transitional epithelium",
            "Urothelium"
        ],
        "answer": "Endothelium",
        "explanation": "Endothelium is specialized simple squamous epithelium lining the lumen of all blood and lymphatic vessels."
    },
    {
        "id": 43,
        "question": "Simple squamous epithelium lining serous body cavities (peritoneal, pleural, pericardial) is termed:",
        "options": [
            "Endothelium",
            "Mesothelium",
            "Epidermis",
            "Lamina propria",
            "Adventitia"
        ],
        "answer": "Mesothelium",
        "explanation": "Mesothelium is simple squamous epithelium covering serous membranes (pleura, pericardium, peritoneum)."
    },
    {
        "id": 44,
        "question": "Clostridium perfringens enterotoxin binds to Claudin transmembrane proteins, disrupting paracellular barriers in the intestinal epithelium and causing severe watery diarrhea. Which junction is disrupted?",
        "options": [
            "Zonula adherens",
            "Macula adherens (Desmosome)",
            "Gap junction",
            "Zonula occludens (Tight junction)",
            "Focal adhesion"
        ],
        "answer": "Zonula occludens (Tight junction)",
        "explanation": "Claudin and Occludin are core transmembrane proteins of Zonula occludens (tight junctions); their breakdown destroys paracellular barrier integrity."
    },
    {
        "id": 45,
        "question": "Transmembrane hexameric protein complexes called Connexons form central hydrophilic channels connecting adjacent cells in which junction type?",
        "options": [
            "Desmosome",
            "Zonula occludens",
            "Gap junction (Nexus)",
            "Hemidesmosome",
            "Adherens junction"
        ],
        "answer": "Gap junction (Nexus)",
        "explanation": "Gap junctions (nexuses) consist of connexons (6 connexin subunits) that align across intercellular space to permit direct diffusion of ions and small molecules."
    },
    {
        "id": 46,
        "question": "Which cell junction serves as the primary site of intracellular attachment for ACTIN microfilaments?",
        "options": [
            "Macula adherens (Desmosome)",
            "Zonula adherens (Intermediate junction)",
            "Gap junction",
            "Hemidesmosome",
            "Connexon"
        ],
        "answer": "Zonula adherens (Intermediate junction)",
        "explanation": "Zonula adherens anchors actin microfilament networks via E-cadherins and catenins; desmosomes anchor intermediate filaments."
    },
    {
        "id": 47,
        "question": "Desmosomes (macula adherens) connect adjacent cells mechanically by anchoring to which cytoskeletal filaments?",
        "options": [
            "Actin microfilaments",
            "Microtubules",
            "Intermediate filaments (keratin tonofilaments)",
            "Myosin filaments",
            "Spectrin"
        ],
        "answer": "Intermediate filaments (keratin tonofilaments)",
        "explanation": "Desmosomes insert into intracellular plaques linked to intermediate filaments (cytokeratins in epithelia), providing high mechanical shear resistance."
    },
    {
        "id": 48,
        "question": "Eccrine sweat glands of the skin and Brunner's glands of the duodenum release secretory products via membrane-bound exocytosis without loss of cell membrane or cytoplasm. This mode of secretion is:",
        "options": [
            "Holocrine",
            "Merocrine (Eccrine)",
            "Apocrine",
            "Paracrine",
            "Autocrine"
        ],
        "answer": "Merocrine (Eccrine)",
        "explanation": "Merocrine (eccrine) secretion involves exocytosis of membrane-bound vesicles with zero loss of cellular cytoplasm."
    },
    {
        "id": 49,
        "question": "Lactating mammary glands and apocrine ciliary glands release secretory product along with a thin apical rim of cytoplasm. This mode is:",
        "options": [
            "Merocrine",
            "Holocrine",
            "Apocrine",
            "Endocrine",
            "Cytocrine"
        ],
        "answer": "Apocrine",
        "explanation": "Apocrine secretion involves pinching off of the apical cytoplasm containing the secretory droplets."
    },
    {
        "id": 50,
        "question": "Sebaceous glands of the skin release sebum through which mode of secretion?",
        "options": [
            "Merocrine",
            "Apocrine",
            "Holocrine",
            "Paracrine",
            "Eccrine"
        ],
        "answer": "Holocrine",
        "explanation": "Sebaceous glands use holocrine secretion: disintegrating dead cells release accumulated lipid contents into the hair follicle."
    },
    {
        "id": 51,
        "question": "Histological classification of exocrine glands with a branching duct system draining multiple secretory acini is:",
        "options": [
            "Simple tubular gland",
            "Simple acinar gland",
            "Compound gland (e.g., compound acinar / tubuloacinar)",
            "Unicellular gland",
            "Apocrine gland"
        ],
        "answer": "Compound gland (e.g., compound acinar / tubuloacinar)",
        "explanation": "Glands with branched duct networks (pancreas, salivary glands) are classified as compound glands."
    },
    {
        "id": 52,
        "question": "Under H&E staining, mucous acinar cells of the sublingual salivary gland differ from serous acinar cells by displaying:",
        "options": [
            "Round central nucleus with intensely basophilic cytoplasm",
            "Flattened, basal nucleus with pale-staining, foamy-appearing cytoplasm",
            "Eosinophilic zymogen granules in apical cytoplasm",
            "Multinucleated architecture",
            "Absence of basement membrane"
        ],
        "answer": "Flattened, basal nucleus with pale-staining, foamy-appearing cytoplasm",
        "explanation": "Mucus washes out during H&E preparation, leaving mucous acini with pale/foamy cytoplasm and flattened nuclei compressed against the basal membrane."
    },
    {
        "id": 53,
        "question": "The most abundant, predominant cell type in connective tissue proper responsible for synthesizing collagen, elastin, and ground substance is the:",
        "options": [
            "Mast cell",
            "Macrophage",
            "Fibroblast",
            "Plasma cell",
            "Adipocyte"
        ],
        "answer": "Fibroblast",
        "explanation": "Fibroblasts are the primary structural cells of connective tissue proper, synthesizing ECM fibers and glycosaminoglycans."
    },
    {
        "id": 54,
        "question": "Which connective tissue cell displays metachromasia (changing dye color from blue to purple/red when stained with toluidine blue) due to high content of heparin sulfate granules?",
        "options": [
            "Fibroblast",
            "Mast cell",
            "Plasma cell",
            "Erythrocyte",
            "Histiocyte"
        ],
        "answer": "Mast cell",
        "explanation": "Mast cell secretory granules contain densely polyanionic heparin, causing metachromasia with basic thiazine dyes like toluidine blue."
    },
    {
        "id": 55,
        "question": "Differentiated B-lymphocytes dedicated to synthesizing and secreting circulating immunoglobulins (antibodies) are:",
        "options": [
            "Mast cells",
            "Fibroblasts",
            "Plasma cells",
            "Macrophages",
            "Eosinophils"
        ],
        "answer": "Plasma cells",
        "explanation": "Plasma cells are antibody-producing cells with a characteristic 'clock-face' nucleus and prominent perinuclear Golgi halo."
    },
    {
        "id": 56,
        "question": "Bacterial pathogens (such as Staphylococcus aureus and Clostridium) invade connective tissue rapidly by producing which ECM-degrading enzyme?",
        "options": [
            "Hyaluronidase",
            "Carboxypeptidase",
            "Lipase",
            "Ribonuclease",
            "Amylase"
        ],
        "answer": "Hyaluronidase",
        "explanation": "Hyaluronidase cleaves hyaluronan in the ground substance, reducing matrix viscosity and facilitating bacterial spread."
    },
    {
        "id": 57,
        "question": "Why is cartilage unable to grow very thick, relying strictly on perichondrial diffusion for nourishment?",
        "options": [
            "Cartilage is completely avascular; oxygen and nutrients must diffuse through hydrated matrix gel, which is inefficient over large distances",
            "Chondrocytes undergo rapid mitosis",
            "Cartilage contains dense blood capillary networks",
            "Cartilage matrix is impermeable to water",
            "Perichondrium inhibits growth"
        ],
        "answer": "Cartilage is completely avascular; oxygen and nutrients must diffuse through hydrated matrix gel, which is inefficient over large distances",
        "explanation": "Cartilage lacks blood vessels, lymphatics, and nerves; nutrients diffuse from perichondrial capillaries, limiting functional cartilage thickness."
    },
    {
        "id": 58,
        "question": "Which type of cartilage covers the articulating surface of bones in synovial joints, lacks a perichondrium, and is composed of Type II collagen?",
        "options": [
            "Elastic cartilage",
            "Fibrocartilage",
            "Articular (Hyaline) cartilage",
            "Fibroelastic cartilage",
            "Epiphyseal plate cartilage"
        ],
        "answer": "Articular (Hyaline) cartilage",
        "explanation": "Articular cartilage is specialized hyaline cartilage covering joint surfaces; it lacks a perichondrium to maintain a smooth low-friction surface."
    },
    {
        "id": 59,
        "question": "Which large, multinucleated cell derived from monocyte-macrophage lineage is responsible for bone resorption by secreting H+ and lysosomal enzymes into Howship's lacunae?",
        "options": [
            "Osteoblast",
            "Osteocyte",
            "Osteoclast",
            "Osteoprogenitor cell",
            "Chondroclast"
        ],
        "answer": "Osteclast",
        "explanation": "Osteoclasts are giant multinucleated cells that resorb bone matrix by creating a sealed sub-osteoclastic zone and pumping protons."
    },
    {
        "id": 60,
        "question": "Bone matrix synthesis is initiated by osteoblasts secreting unmineralized organic matrix composed primarily of Type I collagen and glycoproteins, termed:",
        "options": [
            "Osteoid",
            "Hydroxyapatite",
            "Chondroitin",
            "Cementum",
            "Perosteum"
        ],
        "answer": "Osteoid",
        "explanation": "Osteoblasts lay down uncalcified organic matrix (osteoid), which subsequently undergoes mineralization with calcium hydroxyapatite."
    },
    {
        "id": 61,
        "question": "In the healing of a bone fracture, what type of bone tissue is formed first within the callus before remodeling into mature lamellar bone?",
        "options": [
            "Compact bone",
            "Woven (non-lamellar) bone",
            "Cortical bone",
            "Osteonal bone",
            "Elastic bone"
        ],
        "answer": "Woven (non-lamellar) bone",
        "explanation": "Immature woven bone with irregular collagen arrangement is formed rapidly during initial fracture repair before being remodeled into lamellar bone."
    },
    {
        "id": 62,
        "question": "What primary fixative is used in routine histological tissue processing to cross-link proteins and prevent autolysis?",
        "options": [
            "10% Neutral Buffered Formalin",
            "70% Ethanol",
            "Xylene",
            "Paraffin wax",
            "Glutaraldehyde"
        ],
        "answer": "10% Neutral Buffered Formalin",
        "explanation": "Formalin (37% formaldehyde gas in water) cross-links lysine amino groups in proteins, preserving cell structure."
    },
    {
        "id": 63,
        "question": "What is the primary purpose of staining tissue sections with Hematoxylin and Eosin (H&E) during histological processing?",
        "options": [
            "To kill remaining bacteria",
            "To generate visual color contrast between acidic (nuclear) and basic (cytoplasmic/ECM) tissue components under light microscopy",
            "To dissolve paraffin wax",
            "To dehydrate the tissue section",
            "To prevent tissue shrinkage"
        ],
        "answer": "To generate visual color contrast between acidic (nuclear) and basic (cytoplasmic/ECM) tissue components under light microscopy",
        "explanation": "H&E staining provides structural contrast: Hematoxylin stains acidic structures (nuclei) purple/blue; Eosin stains basic structures (cytoplasm/collagen) pink."
    },
    {
        "id": 64,
        "question": "During limb development in week 4-8, which specialized ectodermal structure at the distal margin of the limb bud regulates proximo-distal outgrowth via FGF signaling?",
        "options": [
            "Zone of Polarizing Activity (ZPA)",
            "Apical Ectodermal Ridge (AER)",
            "Progress Zone",
            "Neural crest",
            "Somite myotome"
        ],
        "answer": "Apical Ectodermal Ridge (AER)",
        "explanation": "The AER is a thickened ectodermal structure at the distal tip of the limb bud that secretes FGFs to maintain distal mesenchyme proliferation and proximo-distal axis growth."
    },
    {
        "id": 65,
        "question": "Patterning of the antero-posterior (thumb-to-little finger) axis of the developing limb is controlled by Sonic Hedgehog (SHH) secreted from the:",
        "options": [
            "Apical Ectodermal Ridge (AER)",
            "Zone of Polarizing Activity (ZPA)",
            "Progress Zone",
            "Stylopod",
            "Ectoderm"
        ],
        "answer": "Zone of Polarizing Activity (ZPA)",
        "explanation": "The ZPA is a mesodermal block at the posterior border of the limb bud that secretes SHH to establish antero-posterior digit identity."
    },
    {
        "id": 66,
        "question": "Administration of Thalidomide during early pregnancy causes severe congenital limb reduction defects where proximal limb segments are absent (hands/feet attached to trunk). This condition is:",
        "options": [
            "Amelia",
            "Phocomelia",
            "Syndactyly",
            "Polydactyly",
            "Brachydactyly"
        ],
        "answer": "Phocomelia",
        "explanation": "Phocomelia ('seal limbs') is characterized by absence or severe shortening of long proximal bones (stylopod/zeugopod) with hands/feet attached directly to the shoulder/hip."
    },
    {
        "id": 67,
        "question": "Failure of programmed cell death (apoptosis) in the interdigital necrotic zones of the Apical Ectodermal Ridge during week 7 results in:",
        "options": [
            "Ectrodactyly",
            "Syndactyly (webbed digits)",
            "Polydactyly",
            "Phocomelia",
            "Amelia"
        ],
        "answer": "Syndactyly (webbed digits)",
        "explanation": "Apoptosis in interdigital tissue separates individual fingers and toes; failure of apoptosis leads to fused/webbed digits (syndactyly)."
    },
    {
        "id": 68,
        "question": "Positioning of the upper and lower limb buds along the craniocaudal axis of the embryo is regulated by expression of:",
        "options": [
            "Hox genes",
            "FGF-4",
            "BMP-2",
            "Wnt-7a",
            "Retinoic acid receptors"
        ],
        "answer": "Hox genes",
        "explanation": "HOX gene expression patterns along the craniocaudal body axis specify the exact vertebral levels where upper and lower limb buds originate."
    },
    {
        "id": 69,
        "question": "During week 7 of limb development, what crucial rotation occurs in the upper and lower limbs?",
        "options": [
            "Upper limbs rotate 90 degrees laterally; lower limbs rotate 90 degrees medially",
            "Upper limbs rotate medially; lower limbs rotate laterally",
            "Both upper and lower limbs rotate 180 degrees laterally",
            "No rotation occurs",
            "Limbs invert completely"
        ],
        "answer": "Upper limbs rotate 90 degrees laterally; lower limbs rotate 90 degrees medially",
        "explanation": "Upper limbs rotate 90\u00b0 laterally (extensors face posteriorly, thumb lateral); lower limbs rotate 90\u00b0 medially (extensors face anteriorly, big toe medial)."
    },
    {
        "id": 70,
        "question": "Paneth cells located at the base of intestinal crypts of Lieberk\u00fchn provide innate mucosal defense by secreting:",
        "options": [
            "Mucin",
            "Lysozyme and alpha-defensins",
            "Gastrin",
            "Secretin",
            "Histamine"
        ],
        "answer": "Lysozyme and alpha-defensins",
        "explanation": "Paneth cells contain prominent eosinophilic apical granules filled with lysozyme, phospholipase A2, and defensins to destroy enteric bacteria."
    },
    {
        "id": 71,
        "question": "Duodenal submucosa is histologically identified by the presence of rich branched tubuloacinar glands secreting alkaline mucus, known as:",
        "options": [
            "Crypts of Lieberk\u00fchn",
            "Brunner's glands",
            "Peyer's patches",
            "Islets of Langerhans",
            "Meissner's plexus"
        ],
        "answer": "Brunner's glands",
        "explanation": "Brunner's glands are confined to the duodenal submucosa, secreting HCO3- rich alkaline mucus to neutralize acidic gastric chyme."
    },
    {
        "id": 72,
        "question": "Congenital megacolon (Hirschsprung disease) results from developmental failure of neural crest cells to migrate and form which enteric nerve plexus?",
        "options": [
            "Celiac plexus",
            "Myenteric (Auerbach's) and Submucosal (Meissner's) plexuses",
            "Hypogastric plexus",
            "Sympathetic chain",
            "Pudendal plexus"
        ],
        "answer": "Myenteric (Auerbach's) and Submucosal (Meissner's) plexuses",
        "explanation": "Hirschsprung disease is caused by aganglionosis of the distal colon due to failure of neural crest cell migration into Auerbach's and Meissner's plexuses."
    },
    {
        "id": 73,
        "question": "The structural functional unit of the liver centered around a central vein and bounded by peripheral portal triads is the:",
        "options": [
            "Classical hepatic lobule",
            "Portal lobule",
            "Hepatic acinus of Rappaport",
            "Space of Disse",
            "Kupffer lobule"
        ],
        "answer": "Classical hepatic lobule",
        "explanation": "The classical hepatic lobule is hexagonal with central vein in the middle and portal triads at the corners, draining blood inward."
    },
    {
        "id": 74,
        "question": "In the microscopic liver, perisinusoidal Spaces of Disse house specialized Ito (hepatic stellate) cells whose primary physiological function is storing:",
        "options": [
            "Glycogen",
            "Vitamin A (retinoids) and producing collagen when activated",
            "Iron / Ferritin",
            "Bile salts",
            "Bilirubin"
        ],
        "answer": "Vitamin A (retinoids) and producing collagen when activated",
        "explanation": "Hepatic stellate (Ito) cells reside in the Space of Disse, storing lipid-soluble Vitamin A; during liver injury, they transform into myofibroblasts causing fibrosis."
    },
    {
        "id": 75,
        "question": "Resident macrophages lining the hepatic sinusoids responsible for phagocytosing particulate matter and aged erythrocytes are:",
        "options": [
            "Ito cells",
            "Kupffer cells",
            "Hepatocytes",
            "Endothelial cells",
            "Langerhans cells"
        ],
        "answer": "Kupffer cells",
        "explanation": "Kupffer cells are specialized tissue macrophages attached to the luminal endothelial lining of hepatic sinusoids."
    },
    {
        "id": 76,
        "question": "The filtration barrier of the renal glomerulus comprises three structural layers:",
        "options": [
            "Fenestrated capillary endothelium, Glomerular basement membrane (GBM), and Podocyte foot processes (pedicels) with slit diaphragms",
            "Simple cuboidal epithelium, macula densa, and mesangium",
            "Endothelium, parietal layer of Bowman's capsule, and loop of Henle",
            "Juxtaglomerular cells, macula densa, and extraglomerular mesangial cells",
            "Capillaries, distal tubule, and collecting duct"
        ],
        "answer": "Fenestrated capillary endothelium, Glomerular basement membrane (GBM), and Podocyte foot processes (pedicels) with slit diaphragms",
        "explanation": "The glomerular filtration barrier consists of fenestrated endothelium, thick fused GBM, and visceral podocytes with interdigitating filtration slits."
    },
    {
        "id": 77,
        "question": "In the male prostate gland, Benign Prostatic Hyperplasia (BPH) originates predominantly within which anatomical zone?",
        "options": [
            "Peripheral zone",
            "Transitional (Periurethral) zone",
            "Central zone",
            "Anterior fibromuscular stroma",
            "Preprostatic zone"
        ],
        "answer": "Transitional (Periurethral) zone",
        "explanation": "BPH arises in the Transitional zone surrounding the prostatic urethra, causing urinary obstruction; Prostate Carcinoma arises mainly in the Peripheral zone."
    },
    {
        "id": 78,
        "question": "Prostatic Adenocarcinoma develops most frequently in which zone of the prostate gland accessible to digital rectal examination?",
        "options": [
            "Transitional zone",
            "Peripheral zone",
            "Central zone",
            "Periurethral glands",
            "Ejaculatory duct wall"
        ],
        "answer": "Peripheral zone",
        "explanation": "70-80% of prostatic carcinomas originate in the posterior Peripheral zone, making them palpable via digital rectal examination."
    },
    {
        "id": 79,
        "question": "Remnant of the embryonic vitelline duct (omphalomesenteric duct) that persists as a true diverticulum on the ileum (~2 feet from ileocecal valve) is:",
        "options": [
            "Urachal cyst",
            "Meckel's diverticulum",
            "Omphalocele",
            "Gastroschisis",
            "Hirschsprung segment"
        ],
        "answer": "Meckel's diverticulum",
        "explanation": "Meckel's diverticulum results from incomplete obliteration of the vitelline duct, obeying the Rule of 2s (2% population, 2 inches long, 2 feet from ileocecal valve, 2 types of ectopic tissue)."
    },
    {
        "id": 80,
        "question": "Herniation of abdominal viscera through an unclosed umbilical ring into the base of the umbilical cord covered by a amnion/peritoneal sac is:",
        "options": [
            "Gastroschisis",
            "Omphalocele",
            "Congenital umbilical hernia",
            "Meckel's diverticulum",
            "Indirect inguinal hernia"
        ],
        "answer": "Omphalocele",
        "explanation": "Omphalocele is a midline defect covered by a protective peritoneal/amniotic membrane sac resulting from failure of physiological gut rotation to return into abdomen."
    }
]
BIOCHEM_QS = [
    {
        "id": 81,
        "question": "Elevated intracellular Calcium ions ($Ca^{2+}$) serve as the indispensable trigger for excitation-contraction coupling in which muscle types?",
        "options": [
            "Skeletal muscle only",
            "Smooth muscle only",
            "Cardiac muscle only",
            "All three muscle types (Skeletal, Smooth, and Cardiac)",
            "Skeletal and Smooth muscle only"
        ],
        "answer": "All three muscle types (Skeletal, Smooth, and Cardiac)",
        "explanation": "Intracellular $Ca^{2+}$ elevation is the universal intracellular signal initiating cross-bridge cycling in skeletal, smooth, and cardiac muscle."
    },
    {
        "id": 82,
        "question": "What is the correct temporal sequence of events during Excitation-Contraction Coupling in skeletal muscle?",
        "options": [
            "Action potential in sarcolemma -> T-tubule depolarization -> DHP receptor activation -> Ryanodine channel opening -> Ca2+ release from SR -> Ca2+ binding to Troponin C",
            "Ca2+ release from SR -> T-tubule depolarization -> Action potential",
            "ATP hydrolysis -> Ca2+ influx from ECF -> Action potential",
            "T-tubule depolarization -> Troponin binding -> Action potential",
            "Ryanodine opening -> Action potential -> Ca2+ uptake"
        ],
        "answer": "Action potential in sarcolemma -> T-tubule depolarization -> DHP receptor activation -> Ryanodine channel opening -> Ca2+ release from SR -> Ca2+ binding to Troponin C",
        "explanation": "Sarcolemma action potential travels down T-tubules, activating DHP receptors physically linked to RYR1 channels on terminal cisternae, releasing SR $Ca^{2+}$."
    },
    {
        "id": 83,
        "question": "In skeletal muscle, binding of Ca2+ to Troponin C causes a conformational shift in which protein to uncover myosin-binding sites on actin?",
        "options": [
            "Tropomyosin",
            "Titin",
            "Myosin heavy chain",
            "Actinin",
            "Dystrophin"
        ],
        "answer": "Tropomyosin",
        "explanation": "Ca2+ binding to Troponin C shifts Tropomyosin deep into the actin groove, exposing myosin-binding sites on G-actin monomers."
    },
    {
        "id": 84,
        "question": "During cross-bridge cycling in skeletal muscle, what step is specifically required to cause DETACHMENT of the myosin head from the actin filament?",
        "options": [
            "Hydrolysis of ATP into ADP and Pi",
            "Binding of a new ATP molecule to the myosin head",
            "Release of inorganic phosphate (Pi)",
            "Binding of Ca2+ to troponin",
            "Depolarization of T-tubules"
        ],
        "answer": "Binding of a new ATP molecule to the myosin head",
        "explanation": "ATP binding to the nucleotide pocket of the myosin head reduces its affinity for actin, causing immediate cross-bridge detachment."
    },
    {
        "id": 85,
        "question": "What causes Rigor Mortis (post-mortem muscle stiffness) after death?",
        "options": [
            "Massive influx of Na+ into cytoplasm",
            "Depletion of cellular ATP preventing detachment of myosin heads from actin filaments",
            "Hyper-activation of SERCA Ca2+ pumps",
            "Degradation of troponin",
            "Overproduction of lactic acid"
        ],
        "answer": "Depletion of cellular ATP preventing detachment of myosin heads from actin filaments",
        "explanation": "After death, ATP synthesis ceases; without ATP, myosin heads remain locked to actin in a rigid cross-bridge complex (rigor)."
    },
    {
        "id": 86,
        "question": "A patient diagnosed with Myasthenia Gravis presents with ptosis and muscle fatigability due to autoantibodies against nicotinic ACh receptors. Treatment with an Acetylcholinesterase Inhibitor (Pyridostigmine) improves strength by:",
        "options": [
            "Increasing ACh synthesis in motor neurons",
            "Preventing degradation of acetylcholine, increasing ACh concentration and duration in the synaptic cleft to activate remaining receptors",
            "Increasing the number of ACh receptors",
            "Directly releasing Ca2+ from SR",
            "Blocking voltage-gated K+ channels"
        ],
        "answer": "Preventing degradation of acetylcholine, increasing ACh concentration and duration in the synaptic cleft to activate remaining receptors",
        "explanation": "AChE inhibitors block synaptic ACh breakdown, preserving high ACh levels at the motor endplate to prolong EPP generation."
    },
    {
        "id": 87,
        "question": "The postsynaptic membrane of the Neuromuscular Junction (motor endplate) is predominantly composed of which ion channel type?",
        "options": [
            "Voltage-gated Na+ channels",
            "Ligand-gated nicotinic ACh receptor cation channels",
            "Voltage-gated Ca2+ channels",
            "Voltage-gated K+ channels",
            "Mechanically-gated channels"
        ],
        "answer": "Ligand-gated nicotinic ACh receptor cation channels",
        "explanation": "The motor endplate is densely packed with ionotropic nicotinic ACh receptors ($nAChRs$), which are ligand-gated Na+/K+ channels."
    },
    {
        "id": 88,
        "question": "A single motor neuron together with all the individual skeletal muscle fibers it innervates is defined as a:",
        "options": [
            "Sarcomere",
            "Motor unit",
            "Motor endplate",
            "Myofibril",
            "Reflex arc"
        ],
        "answer": "Motor unit",
        "explanation": "A motor unit consists of one alpha motor neuron and all the specific muscle fibers supplied by its axon terminals."
    },
    {
        "id": 89,
        "question": "Which statement correctly compares Slow-Oxidative (Type I) and Fast-Glycolytic (Type IIb) skeletal muscle fibers?",
        "options": [
            "Type I fibers have low myoglobin and fatigue rapidly",
            "Type I (Slow-Red) fibers have high myoglobin, dense mitochondria, high oxidative capacity, and resist fatigue",
            "Type IIb fibers generate low contraction tension",
            "Type IIb fibers are rich in capillaries",
            "Type I fibers rely strictly on anaerobic glycolysis"
        ],
        "answer": "Type I (Slow-Red) fibers have high myoglobin, dense mitochondria, high oxidative capacity, and resist fatigue",
        "explanation": "Type I (slow-twitch) fibers rely on aerobic metabolism, containing abundant myoglobin and mitochondria for sustained fatigue-resistant activity."
    },
    {
        "id": 90,
        "question": "Sensory receptors embedded in skeletal muscle tendons that respond to changes in muscle TENSION to prevent tendon avulsion (autogenic inhibition) are:",
        "options": [
            "Muscle spindles",
            "Golgi tendon organs",
            "Pacinian corpuscles",
            "Free nerve endings",
            "Meissner corpuscles"
        ],
        "answer": "Golgi tendon organs",
        "explanation": "Golgi tendon organs (GTOs) are arranged in series with tendon fibers, sensing muscle tension and mediating the inverse stretch reflex."
    },
    {
        "id": 91,
        "question": "Sensory receptors arranged in parallel with extrafusal muscle fibers that detect changes in muscle LENGTH and rate of stretch are:",
        "options": [
            "Golgi tendon organs",
            "Muscle spindles (intrafusal fibers)",
            "Pacinian corpuscles",
            "Ruffini endings",
            "Merkel discs"
        ],
        "answer": "Muscle spindles (intrafusal fibers)",
        "explanation": "Muscle spindles monitor muscle length/stretch, initiating the monosynaptic stretch reflex (e.g., knee-jerk reflex)."
    },
    {
        "id": 92,
        "question": "Which band of the skeletal muscle sarcomere maintains a CONSTANT length during isometric and isotonic muscle contraction?",
        "options": [
            "I-band",
            "H-zone",
            "A-band",
            "Distance between Z-discs",
            "Sarcomere total length"
        ],
        "answer": "A-band",
        "explanation": "The A-band corresponds to the full length of thick myosin filaments; during contraction, actin slides past myosin, shortening I-bands and H-zones while A-band width remains constant."
    },
    {
        "id": 93,
        "question": "During maximum muscle contraction, which zones of the sarcomere narrow or disappear completely?",
        "options": [
            "A-band and M-line",
            "I-band and H-zone",
            "Z-disc only",
            "A-band only",
            "No zones change width"
        ],
        "answer": "I-band and H-zone",
        "explanation": "As thin filaments are pulled toward the M-line, the I-band (actin only) and H-zone (myosin only) narrow and can disappear."
    },
    {
        "id": 94,
        "question": "Duchenne Muscular Dystrophy (DMD) is a severe X-linked recessive disorder caused by complete absence of which sarcolemmal anchoring protein?",
        "options": [
            "Dystrophin",
            "Titin",
            "Nebulin",
            "Desmin",
            "Myomesin"
        ],
        "answer": "Dystrophin",
        "explanation": "Dystrophin links internal actin cytoskeleton to the extracellular matrix glycoprotein complex; absence causes sarcolemmal micro-tears during contraction, leading to muscle necrosis."
    },
    {
        "id": 95,
        "question": "Smooth muscle cells are capable of undergoing both cellular hypertrophy AND cell division (hyperplasia). An anatomical example is:",
        "options": [
            "Skeletal muscle of quadriceps",
            "Uterine smooth muscle during pregnancy",
            "Cardiac ventricular myocytes",
            "Neurons of cerebral cortex",
            "Lens fiber cells"
        ],
        "answer": "Uterine smooth muscle during pregnancy",
        "explanation": "Myometrial smooth muscle cells in the pregnant uterus undergo extensive hyperplasia (mitosis) and hypertrophy to accommodate fetal growth."
    },
    {
        "id": 96,
        "question": "What is the primary high-energy phosphagen system utilized by skeletal muscle to rapidly regenerate ATP during the first 10 seconds of intense sprinting?",
        "options": [
            "Anaerobic glycolysis",
            "Creatine Phosphate (Phosphocreatine) system",
            "Oxidative phosphorylation",
            "Beta-oxidation",
            "Glycogenolysis"
        ],
        "answer": "Creatine Phosphate (Phosphocreatine) system",
        "explanation": "Phosphocreatine donates its high-energy phosphate to ADP via Creatine Kinase, supplying instant ATP for the initial 5-10 seconds of maximal exertion."
    },
    {
        "id": 97,
        "question": "During intense short-term anaerobic exertion (e.g., 400m dash), lactic acid accumulates in muscle because Pyruvate is converted to Lactate to regenerate:",
        "options": [
            "ATP",
            "NAD+ required to sustain Glycolysis",
            "FAD",
            "Glucose",
            "Acetyl-CoA"
        ],
        "answer": "NAD+ required to sustain Glycolysis",
        "explanation": "Lactate Dehydrogenase reduces Pyruvate to Lactate while oxidizing NADH back to NAD+, allowing GAPDH to continue glycolysis anaerobically."
    },
    {
        "id": 98,
        "question": "In cardiac muscle, Excitation-Contraction coupling relies on 'Calcium-Induced Calcium Release' (CICR). What is the primary source of initial Ca2+ entry?",
        "options": [
            "Extracellular Ca2+ entry through L-type voltage-gated Ca2+ channels (Cav1.2) during action potential plateau",
            "Intracellular Ca2+ release from mitochondria",
            "Passive Na+/Ca2+ exchanger reverse mode only",
            "Nuclear membrane Ca2+ channels",
            "Direct mechanical pull on ryanodine receptors"
        ],
        "answer": "Extracellular Ca2+ entry through L-type voltage-gated Ca2+ channels (Cav1.2) during action potential plateau",
        "explanation": "In cardiac myocytes, influx of extracellular Ca2+ through L-type channels triggers opening of RYR2 channels on the sarcoplasmic reticulum (CICR)."
    },
    {
        "id": 99,
        "question": "Which fluid compartment volume is measured directly using Deuterium Oxide (D2O) or Tritiated Water via the indicator dilution principle?",
        "options": [
            "Extracellular Fluid (ECF)",
            "Total Body Water (TBW)",
            "Plasma Volume",
            "Intracellular Fluid (ICF)",
            "Interstitial Fluid"
        ],
        "answer": "Total Body Water (TBW)",
        "explanation": "Deuterium oxide ($D_2O$), tritiated water, or antipyrine distribute evenly throughout all body fluid compartments, measuring TBW."
    },
    {
        "id": 100,
        "question": "Extracellular Fluid (ECF) volume (~20% of body weight) can be specifically measured using which indicator solute that does NOT penetrate cell membranes?",
        "options": [
            "Deuterium oxide (D2O)",
            "Inulin (or Mannitol / Sulfate)",
            "Evans Blue dye",
            "Radio-iodinated Serum Albumin (RISA)",
            "Heavy water"
        ],
        "answer": "Inulin (or Mannitol / Sulfate)",
        "explanation": "Inulin, mannitol, and sucrose distribute throughout plasma and interstitial space but cannot cross plasma membranes, measuring total ECF volume."
    },
    {
        "id": 101,
        "question": "Plasma volume (~5% of body weight) is measured using an indicator solute that remains confined strictly within the vascular system, such as:",
        "options": [
            "Inulin",
            "Deuterium oxide",
            "Evans Blue dye (or I-125 labeled Albumin)",
            "Mannitol",
            "Urea"
        ],
        "answer": "Evans Blue dye (or I-125 labeled Albumin)",
        "explanation": "Evans Blue dye binds tightly to serum albumin, staying within blood vessels and measuring total Plasma Volume."
    },
    {
        "id": 102,
        "question": "Applying the 60-40-20 rule for a healthy 70 kg adult male, what are the normal volumes of Total Body Water (TBW), Intracellular Fluid (ICF), and Extracellular Fluid (ECF)?",
        "options": [
            "TBW = 42 L (60%), ICF = 28 L (40%), ECF = 14 L (20%)",
            "TBW = 50 L, ICF = 10 L, ECF = 40 L",
            "TBW = 30 L, ICF = 15 L, ECF = 15 L",
            "TBW = 42 L, ICF = 14 L, ECF = 28 L",
            "TBW = 60 L, ICF = 20 L, ECF = 40 L"
        ],
        "answer": "TBW = 42 L (60%), ICF = 28 L (40%), ECF = 14 L (20%)",
        "explanation": "TBW = 60% of 70kg = 42L; ICF = 2/3 of TBW (40% body weight) = 28L; ECF = 1/3 of TBW (20% body weight) = 14L."
    },
    {
        "id": 103,
        "question": "Tubuloglomerular Feedback (TGF) regulates renal blood flow and Glomerular Filtration Rate (GFR). Which specialized cells in the distal convoluted tubule sense luminal NaCl concentration?",
        "options": [
            "Juxtaglomerular granular cells",
            "Macula densa cells",
            "Podocytes",
            "Mesangial cells",
            "Principal cells"
        ],
        "answer": "Macula densa cells",
        "explanation": "Macula densa cells in the thick ascending limb/early DCT monitor luminal NaCl load via NKCC2 co-transporters, releasing adenosine to constrict afferent arterioles when GFR is high."
    },
    {
        "id": 104,
        "question": "Juxtaglomerular (JG) granular cells located in the walls of afferent arterioles synthesize and release which enzyme in response to renal hypoperfusion or sympathetic stimulation?",
        "options": [
            "Angiotensinogen",
            "Renin",
            "ACE",
            "Aldosterone",
            "Antidiuretic Hormone"
        ],
        "answer": "Renin",
        "explanation": "JG granular cells release Renin, which cleaves liver angiotensinogen to angiotensin I in the renin-angiotensin-aldosterone system (RAAS)."
    },
    {
        "id": 105,
        "question": "Antidiuretic Hormone (ADH / Vasopressin) increases water reabsorption in collecting duct principal cells by binding to V2 receptors and stimulating insertion of which water channels into the apical membrane?",
        "options": [
            "Aquaporin-1",
            "Aquaporin-2",
            "Aquaporin-3",
            "Aquaporin-4",
            "SGLT-2"
        ],
        "answer": "Aquaporin-2",
        "explanation": "V2 receptor activation increases intracellular cAMP, triggering exocytosis of Aquaporin-2 (AQP2) water channels into the apical plasma membrane of collecting duct principal cells."
    },
    {
        "id": 106,
        "question": "Atrial Natriuretic Peptide (ANP) released from cardiac atria in response to hypervolemia decreases blood pressure and ECF volume by:",
        "options": [
            "Dilating afferent arterioles and constricting efferent arterioles to increase GFR, while inhibiting Na+ reabsorption in medullary collecting ducts",
            "Stimulating renin secretion",
            "Increasing aldosterone synthesis",
            "Stimulating ADH release",
            "Constricting renal arteries"
        ],
        "answer": "Dilating afferent arterioles and constricting efferent arterioles to increase GFR, while inhibiting Na+ reabsorption in medullary collecting ducts",
        "explanation": "ANP causes natriuresis and diuresis by increasing GFR (afferent dilation/efferent constriction) and directly suppressing Na+ reabsorption in collecting ducts."
    },
    {
        "id": 107,
        "question": "Which gastrointestinal hormone released by duodenal I-cells in response to fatty acids and amino acids stimulates gallbladder contraction and pancreatic enzyme secretion?",
        "options": [
            "Gastrin",
            "Secretin",
            "Cholecystokinin (CCK)",
            "Motilin",
            "Glucose-dependent Insulinotropic Peptide (GIP)"
        ],
        "answer": "Cholecystokinin (CCK)",
        "explanation": "CCK stimulates gallbladder contraction, relaxes the Sphincter of Oddi, and stimulates pancreatic acinar cells to secrete digestive enzymes."
    },
    {
        "id": 108,
        "question": "Secretin is released by S-cells in the duodenal mucosa in response to acidic chyme (pH < 4.5). What is its primary physiological action?",
        "options": [
            "Stimulating gastric acid secretion",
            "Stimulating rich HCO3- (bicarbonate) and water secretion from pancreatic duct cells to neutralize duodenal acid",
            "Inhibiting gallbladder contraction",
            "Stimulating intestinal motility",
            "Promoting hunger"
        ],
        "answer": "Stimulating rich HCO3- (bicarbonate) and water secretion from pancreatic duct cells to neutralize duodenal acid",
        "explanation": "Secretin acts on pancreatic ductal cells via cAMP to stimulate HCO3- and H2O secretion, raising duodenal pH to optimal enzyme levels (~7-8)."
    },
    {
        "id": 109,
        "question": "Which GI hormone released during fasting conditions initiates the Migrating Motor Complex (MMC) to clear undigested residue from the stomach and small intestine?",
        "options": [
            "Gastrin",
            "CCK",
            "Secretin",
            "Motilin",
            "VIP"
        ],
        "answer": "Motilin",
        "explanation": "Motilin is secreted by M-cells during interdigestive fasting states (every 90-120 minutes), triggering Phase III waves of the Migrating Motor Complex."
    },
    {
        "id": 110,
        "question": "Gastric Parietal (oxyntic) cells secrete Hydrochloric Acid (HCl) into the gastric lumen using which primary active transport pump on their apical canalicular membrane?",
        "options": [
            "Na+/K+ ATPase",
            "H+/K+ ATPase (Proton pump)",
            "Ca2+ ATPase",
            "Na+/H+ exchanger",
            "Cl-/HCO3- exchanger"
        ],
        "answer": "H+/K+ ATPase (Proton pump)",
        "explanation": "Apical H+/K+ ATPase pumps H+ into the gastric lumen in exchange for K+; proton pump inhibitors (omeprazole) irreversibly block this enzyme."
    },
    {
        "id": 111,
        "question": "Which three secretagogues directly stimulate parietal cells to increase gastric acid secretion?",
        "options": [
            "Histamine (H2 receptor), Acetylcholine (M3 receptor), and Gastrin (CCK2 receptor)",
            "Somatostatin, Secretin, and GIP",
            "Prostaglandin E2, VIP, and Motilin",
            "Insulin, Glucagon, and Epinephrine",
            "CCK, Dopamine, and Serotonin"
        ],
        "answer": "Histamine (H2 receptor), Acetylcholine (M3 receptor), and Gastrin (CCK2 receptor)",
        "explanation": "Histamine (cAMP pathway), ACh, and Gastrin (Ca2+ pathway) act synergistically on parietal cell membrane receptors to stimulate HCl secretion."
    },
    {
        "id": 112,
        "question": "Enterochromaffin-like (ECL) cells in the gastric mucosa release which local paracrine agent that serves as the most potent activator of parietal cell acid secretion?",
        "options": [
            "Serotonin",
            "Histamine",
            "Somatostatin",
            "Acetylcholine",
            "Prostaglandin"
        ],
        "answer": "Histamine",
        "explanation": "ECL cells release Histamine upon stimulation by Gastrin and Vagus nerve ACh; Histamine acts locally on parietal cell H2 receptors."
    },
    {
        "id": 113,
        "question": "Intrinsically, parietal cells also secrete Intrinsic Factor (IF). Intrinsic factor is essential for the absorption of which vital nutrient in the terminal ileum?",
        "options": [
            "Folic acid",
            "Vitamin B12 (Cobalamin)",
            "Iron",
            "Vitamin D",
            "Calcium"
        ],
        "answer": "Vitamin B12 (Cobalamin)",
        "explanation": "Intrinsic factor binds Vitamin B12 in the duodenum, forming a complex that resists digestion and binds cubam receptors in the terminal ileum for receptor-mediated endocytosis."
    },
    {
        "id": 114,
        "question": "Surgical resection or disease of the terminal ileum (e.g., Crohn's disease) leads to malabsorption of Vitamin B12 and:",
        "options": [
            "Iron deficiency anemia",
            "Bile salts (causing fat malabsorption, steatorrhea, and gallstones)",
            "Glucose intolerance",
            "Scurvy",
            "Rickets"
        ],
        "answer": "Bile salts (causing fat malabsorption, steatorrhea, and gallstones)",
        "explanation": "The terminal ileum absorbs both Vitamin B12-IF complexes and conjugated bile salts (enterohepatic circulation); resection causes B12 deficiency megaloblastic anemia and bile acid diarrhea/steatorrhea."
    },
    {
        "id": 115,
        "question": "In the liver, unconjugated (indirect) hydrophobic bilirubin is rendered water-soluble for biliary excretion by conjugation with two molecules of glucuronic acid catalyzed by:",
        "options": [
            "Biliverdin reductase",
            "UDP-Glucuronosyltransferase (UGT1A1)",
            "Heme oxygenase",
            "Beta-glucuronidase",
            "Alcohol dehydrogenase"
        ],
        "answer": "UDP-Glucuronosyltransferase (UGT1A1)",
        "explanation": "Hepatocyte UGT1A1 conjugates bilirubin with glucuronic acid to form water-soluble bilirubin diglucuronide (direct conjugated bilirubin)."
    },
    {
        "id": 116,
        "question": "Jaundice characterized by high serum unconjugated (indirect) bilirubin, elevated urinary urobilinogen, and normal dark-colored stools is diagnostic of:",
        "options": [
            "Obstructive (Post-hepatic) jaundice",
            "Hemolytic (Pre-hepatic) jaundice",
            "Hepatic cholestasis",
            "Biliary stricture",
            "Gallstones"
        ],
        "answer": "Hemolytic (Pre-hepatic) jaundice",
        "explanation": "Excessive RBC breakdown overwhelms liver conjugation capacity, raising unconjugated bilirubin; increased bile entry into gut raises urobilinogen."
    },
    {
        "id": 117,
        "question": "Gallstone obstruction of the common bile duct (Post-hepatic obstructive jaundice) results in which characteristic laboratory and clinical findings?",
        "options": [
            "Elevated conjugated (direct) bilirubin, pale clay-colored stools (absence of stercobilin), dark tea-colored urine (conjugated bilirubinuria), and intense pruritus",
            "Elevated unconjugated bilirubin and dark brown stools",
            "Increased urinary urobilinogen",
            "Normal serum alkaline phosphatase",
            "Decreased plasma cholesterol"
        ],
        "answer": "Elevated conjugated (direct) bilirubin, pale clay-colored stools (absence of stercobilin), dark tea-colored urine (conjugated bilirubinuria), and intense pruritus",
        "explanation": "Biliary obstruction prevents conjugated bilirubin from reaching the gut (clay stools); conjugated bilirubin leaks into blood and urine (dark urine), while bile salts cause itching."
    },
    {
        "id": 118,
        "question": "In the ovarian follicle, the 'Two-Cell, Two-Gonadotropin' model of estrogen synthesis dictates that:",
        "options": [
            "Theca cells synthesize Androstenedione under LH stimulation; Granulosa cells convert Androstenedione to Estradiol via Aromatase under FSH stimulation",
            "Granulosa cells synthesize testosterone under LH",
            "Theca cells synthesize progesterone under FSH",
            "Granulosa cells lack aromatase",
            "LH acts exclusively on oocytes"
        ],
        "answer": "Theca cells synthesize Androstenedione under LH stimulation; Granulosa cells convert Androstenedione to Estradiol via Aromatase under FSH stimulation",
        "explanation": "LH stimulates Theca interna cells to produce androgens (androstenedione); FSH stimulates Granulosa cells to express Aromatase (CYP19A1), converting androgens to Estradiol."
    },
    {
        "id": 119,
        "question": "What mid-cycle hormonal event triggers rupture of the mature Graafian follicle and ovulation of the secondary oocyte?",
        "options": [
            "Progesterone drop",
            "Luteinizing Hormone (LH) surge triggered by positive feedback of high Estradiol",
            "FSH withdrawal",
            "Inhibin B peak",
            "Prolactin surge"
        ],
        "answer": "Luteinizing Hormone (LH) surge triggered by positive feedback of high Estradiol",
        "explanation": "Sustained high estradiol levels (>200 pg/mL for 36 hours) exert positive feedback on the hypothalamus/pituitary, triggering a massive LH surge that causes ovulation."
    },
    {
        "id": 120,
        "question": "In the male testicular interstitium, Leydig cells synthesize and secret Testosterone in response to stimulation by which anterior pituitary gonadotropin?",
        "options": [
            "Follicle-Stimulating Hormone (FSH)",
            "Luteinizing Hormone (LH)",
            "Prolactin",
            "ACTH",
            "Growth Hormone"
        ],
        "answer": "Luteinizing Hormone (LH)",
        "explanation": "LH binds LH receptors on Leydig cells to stimulate testosterone synthesis; FSH acts on Sertoli cells to support spermatogenesis and produce ABP/inhibin."
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
    render_quiz_section(ANAT_QS, "anat")

with tab2:
    render_quiz_section(PHYS_QS, "phys")

with tab3:
    render_quiz_section(BIOCHEM_QS, "biochem")

import streamlit as st

st.set_page_config(page_title="MSPC234 Comprehensive Quiz (74 MCQs)", layout="wide", page_icon="🧠")

st.title("🧠 MSPC234: Head & Neck Anatomy, Neuroanatomy & Neuropharmacology Quiz")
st.caption("Compiled from Exam 2030, IA 2030, and Past Papers • Includes Case Scenarios, Direct MCQs, True/False & Exceptions")

if 'answers' not in st.session_state:
    st.session_state.answers = {}

tabs = st.tabs(["🫀 Gross Anatomy & Neuroanatomy (30 Qs)", "⚡ Neurophysiology & Special Senses (24 Qs)", "💊 Neuropharmacology & Neurochemistry (20 Qs)"])

# QUESTION BANK: GROSS ANATOMY & NEUROANATOMY (30 Qs)
q_anatomy = [
    {
        "id": "a1", "type": "Direct MCQs",
        "q": "Which cranial nerve passes through the Foramen Ovale of the skull base?",
        "options": ["A. Ophthalmic nerve (V1)", "B. Maxillary nerve (V2)", "C. Mandibular nerve (V3)", "D. Glossopharyngeal nerve (IX)"],
        "answer": "C. Mandibular nerve (V3)",
        "exp": "The Mandibular nerve (V3) exits the skull base through Foramen Ovale (Mnemonic: OVALE - Otic ganglion, V3, Accessory meningeal artery, Lesser petrosal nerve, Emissary vein)."
    },
    {
        "id": "a2", "type": "Case Scenarios",
        "q": "A 28-year-old man undergoes extraction of an impacted lower 3rd molar. Post-surgery, he has loss of general sensation over the anterior two-thirds of the tongue. Which nerve was injured?",
        "options": ["A. Inferior alveolar nerve", "B. Lingual nerve", "C. Chorda tympani", "D. Glossopharyngeal nerve"],
        "answer": "B. Lingual nerve",
        "exp": "The lingual nerve lies directly medial to the periosteum of the alveolar socket of the mandibular third molar and carries somatic sensation from the anterior 2/3 of the tongue."
    },
    {
        "id": "a3", "type": "Direct MCQs",
        "q": "The giant pyramidal cells of Betz are located in which cortical layer of the primary motor cortex (Area 4)?",
        "options": ["A. Layer III (External pyramidal)", "B. Layer IV (Internal granular)", "C. Layer V (Internal pyramidal)", "D. Layer VI (Multiform)"],
        "answer": "C. Layer V (Internal pyramidal)",
        "exp": "Betz cells are large upper motor neurons residing in Layer V of the primary motor cortex that give rise to corticospinal fibers."
    },
    {
        "id": "a4", "type": "Exceptions",
        "q": "Neural crest cells contribute to the development of all the following structures EXCEPT:",
        "options": ["A. Melanocytes", "B. Odontoblasts", "C. Intrinsic muscles of the tongue", "D. Meninges (Pia and Arachnoid)"],
        "answer": "C. Intrinsic muscles of the tongue",
        "exp": "Intrinsic muscles of the tongue develop from occipital myotomes (somites), not neural crest."
    },
    {
        "id": "a5", "type": "Direct MCQs",
        "q": "The structure located in the floor of the inferior horn of the lateral ventricle is the:",
        "options": ["A. Tail of caudate nucleus", "B. Stria terminalis", "C. Hippocampus", "D. Thalamus"],
        "answer": "C. Hippocampus",
        "exp": "The hippocampus forms the floor and medial wall of the inferior (temporal) horn of the lateral ventricle."
    },
    {
        "id": "a6", "type": "Exceptions",
        "q": "All of the following deep cerebellar nuclei are paired correctly from lateral to medial EXCEPT:",
        "options": ["A. Dentate (most lateral)", "B. Emboliform", "C. Fastigial (most medial)", "D. Globose (most lateral)"],
        "answer": "D. Globose (most lateral)",
        "exp": "From lateral to medial, deep cerebellar nuclei are Dentate, Emboliform, Globose, Fastigial (Mnemonic: Don't Eat Greasy Foods)."
    },
    {
        "id": "a7", "type": "Case Scenarios",
        "q": "A 65-year-old woman presents with sudden right-sided face and arm weakness without lower limb involvement and without aphasia. Which artery is occluded?",
        "options": ["A. Anterior cerebral artery", "B. Middle cerebral artery (superior division/branches)", "C. Posterior cerebral artery", "D. Anterior inferior cerebellar artery"],
        "answer": "B. Middle cerebral artery (superior division/branches)",
        "exp": "MCA supplies the lateral precentral gyrus (face and upper limb motor cortex). ACA supplies the medial surface (lower limb)."
    },
    {
        "id": "a8", "type": "Direct MCQs",
        "q": "Preganglionic parasympathetic fibers in the greater petrosal nerve synapse in which peripheral ganglion?",
        "options": ["A. Otic ganglion", "B. Submandibular ganglion", "C. Pterygopalatine ganglion", "D. Ciliary ganglion"],
        "answer": "C. Pterygopalatine ganglion",
        "exp": "The greater petrosal nerve (branch of CN VII) carries preganglionic parasympathetic fibers to the pterygopalatine ganglion for lacrimal and nasal mucosal secretion."
    },
    {
        "id": "a9", "type": "Direct MCQs",
        "q": "Superficial temporal artery pulse can be palpated anterior to the tragus of the ear over which bone?",
        "options": ["A. Maxilla", "B. Zygomatic arch / Temporal bone", "C. Mandibular angle", "D. Parietal bone"],
        "answer": "B. Zygomatic arch / Temporal bone",
        "exp": "The superficial temporal artery pulse is easily felt as it crosses the root of the zygomatic arch anterior to the auricle."
    },
    {
        "id": "a10", "type": "Direct MCQs",
        "q": "In an adult, the spinal cord conus medullaris typically terminates at vertebral level:",
        "options": ["A. T10-T11", "B. L1-L2", "C. L3-L4", "D. S1-S2"],
        "answer": "B. L1-L2",
        "exp": "The adult spinal cord ends at L1-L2 vertebra; in newborns it terminates at L3."
    },
    {
        "id": "a11", "type": "Case Scenarios",
        "q": "A patient with an abducent nerve (CN VI) palsy and ipsilateral facial weakness has a brainstem lesion at the level of the facial colliculus in the:",
        "options": ["A. Midbrain tegmentum", "B. Dorsal pons", "C. Open medulla", "D. Subthalamus"],
        "answer": "B. Dorsal pons",
        "exp": "The facial colliculus in the floor of the 4th ventricle in the dorsal pons is formed by facial nerve motor fibers looping over the abducent nucleus."
    },
    {
        "id": "a12", "type": "Direct MCQs",
        "q": "Cerebrospinal fluid drains from the subarachnoid space into dural venous sinuses via:",
        "options": ["A. Choroid plexus capillaries", "B. Arachnoid granulations (villi)", "C. Virchow-Robin spaces", "D. Foramina of Luschka"],
        "answer": "B. Arachnoid granulations (villi)",
        "exp": "Arachnoid granulations project into the superior sagittal sinus and act as one-way valves for CSF reabsorption."
    },
    {
        "id": "a13", "type": "Direct MCQs",
        "q": "Which dural fold separates the cerebellar hemispheres from the overlying occipital lobes?",
        "options": ["A. Falx cerebri", "B. Tentorium cerebelli", "C. Falx cerebelli", "D. Diaphragma sellae"],
        "answer": "B. Tentorium cerebelli", "exp": "Tentorium cerebelli roofs the posterior cranial fossa."
    },
    {
        "id": "a14", "type": "Case Scenarios",
        "q": "A patient presents with bitemporal hemianopia ('tunnel vision'). Where is the lesion located?",
        "options": ["A. Left optic nerve", "B. Right optic tract", "C. Optic chiasm", "D. Geniculocalcarine tract"],
        "answer": "C. Optic chiasm",
        "exp": "A pituitary tumor compressing the center of the optic chiasm interrupts decussating nasal retinal fibers, causing loss of peripheral (temporal) vision in both eyes."
    },
    {
        "id": "a15", "type": "Direct MCQs",
        "q": "The medial lemniscus is formed by decussating second-order sensory axons originating from the:",
        "options": ["A. Substantia gelatinosa", "B. Nucleus gracilis and Nucleus cuneatus", "C. Ventral posterolateral thalamic nucleus", "D. Clarke's column"],
        "answer": "B. Nucleus gracilis and Nucleus cuneatus",
        "exp": "Second-order sensory neurons in gracile/cuneate nuclei cross in the lower medulla as internal arcuate fibers to form the medial lemniscus."
    },
    {
        "id": "a16", "type": "Exceptions",
        "q": "All of the following cranial nerve nuclei are located in the medulla oblongata EXCEPT:",
        "options": ["A. Hypoglossal nucleus (XII)", "B. Nucleus ambiguus (IX, X, XI)", "C. Solitary nucleus (VII, IX, X)", "D. Abducent nucleus (VI)"],
        "answer": "D. Abducent nucleus (VI)",
        "exp": "The abducent nucleus resides in the caudal pons."
    },
    {
        "id": "a17", "type": "Case Scenarios",
        "q": "An arterial occlusion of the posterior inferior cerebellar artery (PICA) produces Wallenberg lateral medullary syndrome. Which tract damage causes loss of pain and temperature on the contralateral body?",
        "options": ["A. Corticospinal tract", "B. Lateral spinothalamic tract", "C. Medial lemniscus", "D. Fasciculus gracilis"],
        "answer": "B. Lateral spinothalamic tract",
        "exp": "PICA supplies the anterolateral medulla; damaging the lateral spinothalamic tract causes contralateral body analgesia."
    },
    {
        "id": "a18", "type": "Exceptions",
        "q": "Features of Upper Motor Neuron (UMN) lesions include all of the following EXCEPT:",
        "options": ["A. Spastic paralysis", "B. Hyperreflexia and clonus", "C. Extensor plantar response (Babinski sign)", "D. Severe neurogenic muscle denervation atrophy"],
        "answer": "D. Severe neurogenic muscle denervation atrophy",
        "exp": "Severe neurogenic atrophy occurs in Lower Motor Neuron (LMN) lesions; UMN lesions cause mild disuse atrophy."
    },
    {
        "id": "a19", "type": "Direct MCQs",
        "q": "Broca's motor speech area corresponds to Brodmann areas 44 and 45 in the:",
        "options": ["A. Superior temporal gyrus", "B. Inferior frontal gyrus", "C. Postcentral gyrus", "D. Cingulate gyrus"],
        "answer": "B. Inferior frontal gyrus",
        "exp": "Broca's area resides in the pars opercularis and pars triangularis of the dominant inferior frontal gyrus."
    },
    {
        "id": "a20", "type": "Direct MCQs",
        "q": "Wernicke's receptive language area is located in the posterior part of the:",
        "options": ["A. Inferior frontal gyrus", "B. Superior temporal gyrus", "C. Precentral gyrus", "D. Angular gyrus"],
        "answer": "B. Superior temporal gyrus",
        "exp": "Wernicke's area (Brodmann 22) resides in the posterior superior temporal gyrus."
    },
    {
        "id": "a21", "type": "Case Scenarios",
        "q": "A newborn baby is born with a cystic sac on the lower back containing meninges and spinal cord elements covered by thin skin. What is the diagnosis?",
        "options": ["A. Anencephaly", "B. Myelomeningocele (Spina bifida cystica)", "C. Encephalocele", "D. Spina bifida occulta"],
        "answer": "B. Myelomeningocele (Spina bifida cystica)",
        "exp": "Failure of neural tube closure at the caudal neuropore leads to spina bifida cystica with herniation of cord and meninges."
    },
    {
        "id": "a22", "type": "Direct MCQs",
        "q": "What total volume of cerebrospinal fluid (CSF) is contained within the adult ventricles and subarachnoid space?",
        "options": ["A. 50 mL", "B. 150 mL", "C. 500 mL", "D. 1000 mL"],
        "answer": "B. 150 mL",
        "exp": "Total adult CSF volume is ~150 mL, produced at ~500 mL/day and turned over 3-4 times daily."
    },
    {
        "id": "a23", "type": "Exceptions",
        "q": "Which structure passes through the internal acoustic meatus alongside Cranial Nerve VIII?",
        "options": ["A. Facial nerve (CN VII)", "B. Glossopharyngeal nerve (CN IX)", "C. Labyrinthine artery", "D. Vestibulocochlear nerve (CN VIII)"],
        "answer": "B. Glossopharyngeal nerve (CN IX)",
        "exp": "The internal acoustic meatus transmits CN VII, CN VIII, and the labyrinthine artery. CN IX exits via the jugular foramen."
    },
    {
        "id": "a24", "type": "Direct MCQs",
        "q": "The optic radiation fibers carrying visual signals from the lateral geniculate nucleus to the primary visual cortex pass through which part of the internal capsule?",
        "options": ["A. Anterior limb", "B. Genu", "C. Retrolenticular part", "D. Anterior 2/3 of posterior limb"],
        "answer": "C. Retrolenticular part",
        "exp": "Optic radiation fibers travel in the retrolenticular and sublenticular parts of the posterior limb of the internal capsule."
    },
    {
        "id": "a25", "type": "Direct MCQs",
        "q": "Which brain vesicle gives rise to the adult cerebral hemispheres and lateral ventricles?",
        "options": ["A. Telencephalon", "B. Diencephalon", "C. Metencephalon", "D. Myelencephalon"],
        "answer": "A. Telencephalon",
        "exp": "Forebrain (prosencephalon) divides into telencephalon (cerebral cortex, striatum) and diencephalon (thalamus, hypothalamus)."
    },
    {
        "id": "a26", "type": "Exceptions",
        "q": "All of the following are components of the basal ganglia EXCEPT:",
        "options": ["A. Caudate nucleus", "B. Putamen", "C. Globus pallidus", "D. Dentate nucleus"],
        "answer": "D. Dentate nucleus",
        "exp": "The dentate nucleus is a deep cerebellar nucleus."
    },
    {
        "id": "a27", "type": "Case Scenarios",
        "q": "A 50-year-old man presents with resting tremor ('pill-rolling'), muscle rigidity ('lead-pipe'), and bradykinesia. What pathway is degenerated?",
        "options": ["A. Corticospinal tract", "B. Nigrostriatal dopaminergic pathway", "C. Cerebellothalamic tract", "D. Spinothalamic tract"],
        "answer": "B. Nigrostriatal dopaminergic pathway",
        "exp": "Parkinson's disease is caused by loss of dopaminergic neurons in the substantia nigra pars compacta projecting to the striatum."
    },
    {
        "id": "a28", "type": "Direct MCQs",
        "q": "Primary visual cortex (Brodmann area 17) surrounds which cortical sulcus on the medial surface of the occipital lobe?",
        "options": ["A. Central sulcus", "B. Calcarine sulcus", "C. Lateral sulcus", "D. Parieto-occipital sulcus"],
        "answer": "B. Calcarine sulcus",
        "exp": "Area 17 (striate cortex) lines the upper and lower banks of the calcarine sulcus."
    },
    {
        "id": "a29", "type": "Direct MCQs",
        "q": "The primary sensory nucleus of the thalamus receiving medial lemniscal and spinothalamic inputs from the body is the:",
        "options": ["A. Ventral posteromedial (VPM) nucleus", "B. Ventral posterolateral (VPL) nucleus", "C. Mediodorsal nucleus", "D. Lateral geniculate nucleus"],
        "answer": "B. Ventral posterolateral (VPL) nucleus",
        "exp": "VPL receives somatosensory signals from the body (VPM receives facial sensations from CN V)."
    },
    {
        "id": "a30", "type": "Direct MCQs",
        "q": "Histologically, myelin sheaths surrounding axons in the central nervous system (CNS) are formed by:",
        "options": ["A. Schwann cells", "B. Oligodendrocytes", "C. Astrocytes", "D. Microglia"],
        "answer": "B. Oligodendrocytes",
        "exp": "Oligodendrocytes myelinate multiple CNS axons; Schwann cells myelinate single PNS axons."
    }
]

# QUESTION BANK: NEUROPHYSIOLOGY & SPECIAL SENSES (24 Qs)
q_physio = [
    {
        "id": "p1", "type": "Direct MCQs",
        "q": "The resting membrane potential of a neuron (-70 mV) is closest to the equilibrium potential for which ion?",
        "options": ["A. Sodium (+60 mV)", "B. Potassium (-90 mV)", "C. Calcium (+120 mV)", "D. Chloride (-70 mV)"],
        "answer": "B. Potassium (-90 mV)",
        "exp": "Neuronal membranes at rest have high leak permeability for K+, bringing resting potential near the Nernst equilibrium potential for K+."
    },
    {
        "id": "p2", "type": "Direct MCQs",
        "q": "Which ion flux is primarily responsible for the rapid repolarization phase of an action potential?",
        "options": ["A. Influx of Na+", "B. Efflux of K+", "C. Influx of Ca2+", "D. Efflux of Cl-"],
        "answer": "B. Efflux of K+", "exp": "Inactivation of voltage-gated Na+ channels and opening of voltage-gated K+ channels drives outward K+ efflux, repolarizing the membrane."
    },
    {
        "id": "p3", "type": "Direct MCQs",
        "q": "Which inorganic ion acts as an endogenous voltage-dependent blocker of NMDA receptors at resting membrane potentials?",
        "options": ["A. Sodium", "B. Potassium", "C. Magnesium (Mg2+)", "D. Zinc"],
        "answer": "C. Magnesium (Mg2+)",
        "exp": "Extracellular Mg2+ plugs NMDA receptor channels at resting potential; membrane depolarization expels Mg2+, permitting Ca2+ influx."
    },
    {
        "id": "p4", "type": "Case Scenarios",
        "q": "Light striking retinal rod photoreceptors causes which intracellular physiological response?",
        "options": ["A. Activation of guanylyl cyclase and depolarization", "B. Activation of phosphodiesterase, decrease in cGMP, and hyperpolarization", "C. Influx of Na+ and action potential firing", "D. Release of glutamate"],
        "answer": "B. Activation of phosphodiesterase, decrease in cGMP, and hyperpolarization",
        "exp": "Rhodopsin absorption activates transducin, stimulating cGMP phosphodiesterase. Dropping cGMP closes CNG cation channels, hyperpolarizing rod cells."
    },
    {
        "id": "p5", "type": "Direct MCQs",
        "q": "The length constant (lambda) of an axon increases with:",
        "options": ["A. Increased internal axoplasmic resistance", "B. Increased membrane resistance (myelination) and increased axon diameter", "C. Demyelination", "D. Reduced membrane resistance"],
        "answer": "B. Increased membrane resistance (myelination) and increased axon diameter",
        "exp": "Lambda = sqrt(rm/ri). Myelination increases membrane resistance (rm) and larger diameter reduces internal resistance (ri), increasing signal conduction distance."
    },
    {
        "id": "p6", "type": "Direct MCQs",
        "q": "The afferent sensory limb of the corneal blink reflex is mediated by which nerve?",
        "options": ["A. Optic nerve (CN II)", "B. Ophthalmic nerve (CN V1)", "C. Facial nerve (CN VII)", "D. Oculomotor nerve (CN III)"],
        "answer": "B. Ophthalmic nerve (CN V1)",
        "exp": "CN V1 nasociliary branch provides sensory innervation to the cornea (afferent limb); CN VII motor branch closes orbicularis oculi (efferent limb)."
    },
    {
        "id": "p7", "type": "Direct MCQs",
        "q": "The Inverse Stretch Reflex is initiated by activation of which sensory receptor?",
        "options": ["A. Muscle spindle intrafusal fibers", "B. Golgi tendon organ (IB afferents)", "C. Pacinian corpuscle", "D. Free nerve endings"],
        "answer": "B. Golgi tendon organ (IB afferents)",
        "exp": "Golgi tendon organs sense muscle contraction tension and send IB sensory signals that inhibit alpha motor neurons, relaxing the muscle to prevent tendon tearing."
    },
    {
        "id": "p8", "type": "Exceptions",
        "q": "Which sensory modality is relayed directly to the cerebral cortex WITHOUT synapsing in the thalamus?",
        "options": ["A. Gustation (Taste)", "B. Vision", "C. Olfaction (Smell)", "D. Audition (Hearing)"],
        "answer": "C. Olfaction (Smell)",
        "exp": "Olfactory bulb tracts project directly to the primary olfactory cortex (pyriform cortex) without prior thalamic relay."
    },
    {
        "id": "p9", "type": "Direct MCQs",
        "q": "Sensory TRPV1 ion channels are activated by noxious heat (>43°C) and which chemical compound?",
        "options": ["A. Menthol", "B. Capsaicin", "C. Mustard oil", "D. Cold temperatures"],
        "answer": "B. Capsaicin",
        "exp": "TRPV1 (transient receptor potential vanilloid 1) non-selective cation channels are opened by capsaicin (chili peppers), heat, and protons."
    },
    {
        "id": "p10", "type": "Case Scenarios",
        "q": "A Weber tuning fork test lateralizes to the abnormal right ear, and Rinne test shows bone conduction > air conduction in the right ear. What type of hearing loss is present?",
        "options": ["A. Right sensorineural hearing loss", "B. Right conductive hearing loss", "C. Left conductive hearing loss", "D. Normal hearing"],
        "answer": "B. Right conductive hearing loss",
        "exp": "Conductive hearing loss blocks ambient environmental noise, causing Weber to lateralize to the affected ear and Rinne to show BC > AC (negative Rinne)."
    },
    {
        "id": "p11", "type": "Direct MCQs",
        "q": "Depolarization of inner ear hair cells in the Organ of Corti is driven by influx of which ion from the endolymph?",
        "options": ["A. Na+", "B. K+", "C. Ca2+", "D. Cl-"],
        "answer": "B. K+",
        "exp": "Endolymph in the scala media has a high K+ concentration (+80 mV potential). Opening apical mechanosensitive channels drives K+ influx into hair cells."
    },
    {
        "id": "p12", "type": "Direct MCQs",
        "q": "Fast, sharp, pricking pain sensation is transmitted to the spinal cord via which type of nerve fibers?",
        "options": ["A. Unmyelinated C fibers", "B. Small myelinated A-delta fibers", "C. Large myelinated A-alpha fibers", "D. A-beta fibers"],
        "answer": "B. Small myelinated A-delta fibers",
        "exp": "A-delta fibers carry fast, localized nociception; unmyelinated C fibers transmit slow, burning, dull pain."
    },
    {
        "id": "p13", "type": "Direct MCQs",
        "q": "Which protein component of the presynaptic SNARE complex is cleaved by Botulinum toxin A to block acetylcholine release?",
        "options": ["A. Synaptotagmin", "B. SNAP-25", "C. Syntaxin", "D. Synaptobrevin (VAMP)"],
        "answer": "B. SNAP-25",
        "exp": "Botulinum toxin A light chain cleaves SNAP-25, preventing presynaptic vesicle fusion and causing flaccid paralysis."
    },
    {
        "id": "p14", "type": "Exceptions",
        "q": "Features of electrotonic local potentials include all of the following EXCEPT:",
        "options": ["A. Graded amplitude proportional to stimulus strength", "B. Decremental spread with distance", "C. Non-refractory summation", "D. All-or-none regenerative propagation"],
        "answer": "D. All-or-none regenerative propagation",
        "exp": "All-or-none propagation is a feature of action potentials, whereas graded electrotonic potentials decay passively over distance."
    },
    {
        "id": "p15", "type": "Direct MCQs",
        "q": "In muscle spindles, gamma motor neurons innervate which contractile structures?",
        "options": ["A. Extrafusal muscle fibers", "B. Intrafusal muscle fiber contractile ends", "C. Golgi tendon organs", "D. Joint capsules"],
        "answer": "B. Intrafusal muscle fiber contractile ends",
        "exp": "Gamma motor neurons adjust spindle sensitivity by contracting the intrafusal fiber ends, maintaining spindle tension during voluntary muscle contraction."
    },
    {
        "id": "p16", "type": "True or False",
        "q": "Select the TRUE statement regarding the Blood-Brain Barrier (BBB):",
        "options": ["A. Endothelial cells of the BBB lack tight junctions", "B. Astrocytic end-feet and endothelial tight junctions (claudins/occludins) form a selective diffusion barrier", "C. Glucose crosses the BBB via simple passive lipid diffusion", "D. Area postrema possesses a highly impermeable BBB"],
        "answer": "B. Astrocytic end-feet and endothelial tight junctions (claudins/occludins) form a selective diffusion barrier",
        "exp": "BBB capillary endothelia have continuous tight junctions and astrocytic end-feet. Glucose requires GLUT-1 facilitated transport; area postrema lacks BBB."
    },
    {
        "id": "p17", "type": "Direct MCQs",
        "q": "Lateral inhibition in sensory nervous systems serves primarily to:",
        "options": ["A. Decrease receptor sensitivity", "B. Enhance spatial acuity and border contrast", "C. Prolong adaptation rate", "D. Inhibit motor neuron firing"],
        "answer": "B. Enhance spatial acuity and border contrast",
        "exp": "Inhibitory interneurons suppress signals from neighboring receptive fields, sharpening sensory perception contrast."
    },
    {
        "id": "p18", "type": "Case Scenarios",
        "q": "A patient exhibits muscle weakness that improves significantly following administration of Edrophonium (Tensilon test). What receptor is targeted by autoantibodies in this disease?",
        "options": ["A. Muscarinic M3 receptors", "B. Nicotinic acetylcholine receptors (Nm) at neuromuscular junctions", "C. D2 dopamine receptors", "D. Voltage-gated calcium channels"],
        "answer": "B. Nicotinic acetylcholine receptors (Nm) at neuromuscular junctions",
        "exp": "Myasthenia gravis involves autoantibodies against postsynaptic Nm receptors; acetylcholinesterase inhibitors like edrophonium temporarily boost ACh levels to improve strength."
    },
    {
        "id": "p19", "type": "Direct MCQs",
        "q": "Which major second messenger system is activated by Gs protein-coupled receptors?",
        "options": ["A. Phospholipase C -> IP3 / DAG", "B. Adenylyl cyclase -> cyclic AMP (cPMP)", "C. cGMP phosphodiesterase", "D. Tyrosine kinase"],
        "answer": "B. Adenylyl cyclase -> cyclic AMP (cPMP)",
        "exp": "Gs alpha subunit activates adenylyl cyclase, converting ATP to cAMP and activating Protein Kinase A."
    },
    {
        "id": "p20", "type": "Exceptions",
        "q": "All of the following taste modalities utilize G-protein coupled receptors (GPCRs) EXCEPT:",
        "options": ["A. Sweet", "B. Umami", "C. Bitter", "D. Salty"],
        "answer": "D. Salty",
        "exp": "Salty (ENaC channels) and Sour (H+ channels) use direct ion channels, whereas Sweet, Umami, and Bitter use GPCRs (T1R / T2R families)."
    },
    {
        "id": "p21", "type": "Direct MCQs",
        "q": "Long-Term Potentiation (LTP) in hippocampal synapses requires Ca2+ influx through which receptor type?",
        "options": ["A. AMPA receptors", "B. NMDA receptors", "C. Kainate receptors", "D. GABA-A receptors"],
        "answer": "B. NMDA receptors",
        "exp": "Postsynaptic depolarization removes Mg2+ block from NMDA receptors, allowing Ca2+ influx that triggers LTP synaptic plasticity."
    },
    {
        "id": "p22", "type": "Direct MCQs",
        "q": "The primary inhibitory neurotransmitter in the spinal cord and brainstem is:",
        "options": ["A. Glutamate", "B. Glycine", "C. Acetylcholine", "D. Substance P"],
        "answer": "B. Glycine",
        "exp": "Glycine opens strychnine-sensitive Cl- channels in spinal interneurons, producing IPSPs. GABA is the main inhibitory transmitter in the brain."
    },
    {
        "id": "p23", "type": "Direct MCQs",
        "q": "Dantrolene relaxes skeletal muscle by blocking which sarcoplasmic reticulum membrane channel?",
        "options": ["A. Dihydropyridine (DHP) receptors", "B. Ryanodine receptors (RyR1)", "C. SERCA pumps", "D. Na+/K+ ATPase"],
        "answer": "B. Ryanodine receptors (RyR1)",
        "exp": "Dantrolene inhibits RyR1 Ca2+ release channels in skeletal muscle SR, treating malignant hyperthermia."
    },
    {
        "id": "p24", "type": "Case Scenarios",
        "q": "Electromyography (EMG) showing high-amplitude long-duration motor unit action potentials with reduced recruitment during voluntary contraction indicates:",
        "options": ["A. Myopathy", "B. Neuropathy / Denervation with reinnervation", "C. Normal muscle", "D. Neuromuscular junction transmission defect"],
        "answer": "B. Neuropathy / Denervation with reinnervation",
        "exp": "Denervation followed by collateral sprouting increases motor unit territory, producing giant high-amplitude EMG potentials."
    }
]

# QUESTION BANK: NEUROPHARMACOLOGY & NEUROCHEMISTRY (20 Qs)
q_pharm = [
    {
        "id": "rx1", "type": "Direct MCQs",
        "q": "Formoterol is classified pharmacologically as a selective:",
        "options": ["A. Alpha-1 adrenergic agonist", "B. Alpha-2 adrenergic agonist", "C. Beta-1 adrenergic agonist", "D. Long-acting Beta-2 adrenergic agonist (LABA)"],
        "answer": "D. Long-acting Beta-2 adrenergic agonist (LABA)",
        "exp": "Formoterol is a LABA used for bronchodilation in asthma and COPD management."
    },
    {
        "id": "rx2", "type": "Direct MCQs",
        "q": "Which centrally-acting alpha-2 adrenergic agonist is used as a first-line antihypertensive in pregnancy?",
        "options": ["A. Clonidine", "B. Methyldopa", "C. Phenylephrine", "D. Propranolol"],
        "answer": "B. Methyldopa",
        "exp": "Methyldopa is metabolized to alpha-methylnorepinephrine in the CNS, stimulating alpha-2 receptors to decrease sympathetic outflow safely in pregnancy."
    },
    {
        "id": "rx3", "type": "Case Scenarios",
        "q": "A patient receiving general anesthesia for surgery develops severe adrenal steroidogenesis inhibition (inhibition of 11-beta-hydroxylase). Which agent was administered?",
        "options": ["A. Propofol", "B. Ketamine", "C. Etomidate", "D. Sevoflurane"],
        "answer": "C. Etomidate",
        "exp": "Etomidate inhibits 11-beta-hydroxylase, suppressing cortisol and aldosterone synthesis."
    },
    {
        "id": "rx4", "type": "Direct MCQs",
        "q": "Ketamine acts as a dissociative general anesthetic primarily by antagonizing which receptor?",
        "options": ["A. GABA-A receptors", "B. NMDA receptors", "C. Mu opioid receptors", "D. Muscarinic receptors"],
        "answer": "B. NMDA receptors",
        "exp": "Ketamine is a non-competitive antagonist of NMDA glutamate receptors, producing analgesia, amnesia, and catatonia (dissociative anesthesia)."
    },
    {
        "id": "rx5", "type": "Exceptions",
        "q": "Barbiturates exert all of the following pharmacological effects EXCEPT:",
        "options": ["A. Prolong GABA-A channel opening duration", "B. Cause central respiratory depression", "C. Induce hepatic cytochrome P450 enzymes", "D. Exert cardio-stimulatory positive inotropic effects"],
        "answer": "D. Exert cardio-stimulatory positive inotropic effects",
        "exp": "Barbiturates depress cardiovascular and respiratory centers, causing vasodilation and hypotension."
    },
    {
        "id": "rx6", "type": "Direct MCQs",
        "q": "Which intravenous general anesthetic exhibits intrinsic antiemetic properties, making post-operative nausea and vomiting unlikely?",
        "options": ["A. Ketamine", "B. Propofol", "C. Nitrous oxide", "D. Etomidate"],
        "answer": "B. Propofol",
        "exp": "Propofol possesses antiemetic effects at sub-anesthetic doses."
    },
    {
        "id": "rx7", "type": "Case Scenarios",
        "q": "Cocaine increases synaptic dopamine concentration and produces euphoria by inhibiting which presynaptic membrane transport protein?",
        "options": ["A. Vesicular monoamine transporter (VMAT)", "B. Dopamine active transporter (DAT)", "C. Monoamine oxidase (MAO)", "D. Choline acetyltransferase"],
        "answer": "B. Dopamine active transporter (DAT)",
        "exp": "Cocaine blocks DAT reuptake, prolonging synaptic dopamine accumulation in the nucleus accumbens reward pathway."
    },
    {
        "id": "rx8", "type": "Direct MCQs",
        "q": "Inhibition of acetylcholinesterase by Pyridostigmine leads to:",
        "options": ["A. Rapid breakdown of synaptic ACh", "B. Accumulation of ACh in the neuromuscular synaptic cleft", "C. Blockade of muscarinic receptors", "D. Inhibition of choline uptake"],
        "answer": "B. Accumulation of ACh in the neuromuscular synaptic cleft",
        "exp": "AChE inhibitors prevent ACh hydrolysis, boosting synaptic ACh concentration to overcome receptor block in myasthenia gravis."
    },
    {
        "id": "rx9", "type": "Exceptions",
        "q": "Side effects of atropine (muscarinic receptor antagonist) include all of the following EXCEPT:",
        "options": ["A. Mydriasis (pupillary dilation)", "B. Miosis (pupillary constriction)", "C. Anhidrosis (dry skin/fever)", "D. Urinary retention"],
        "answer": "B. Miosis (pupillary constriction)",
        "exp": "Atropine blocks M3 receptors on the sphincter pupillae, causing mydriasis and cycloplegia. Miosis is caused by cholinomimetics."
    },
    {
        "id": "rx10", "type": "Direct MCQs",
        "q": "Which direct-acting muscarinic agonist is used to treat non-obstructive post-operative urinary retention?",
        "options": ["A. Bethanechol", "B. Pilocarpine", "C. Atropine", "D. Scopolamine"],
        "answer": "A. Bethanechol",
        "exp": "Bethanechol selectively activates GI/bladder smooth muscle M3 receptors, stimulating detrusor contraction to treat urinary retention."
    },
    {
        "id": "rx11", "type": "Case Scenarios",
        "q": "A patient with organophosphate insecticide poisoning presents with salivation, lacrimation, urination, defecation, and muscle fasciculations. Which drug reactivates acetylcholinesterase?",
        "options": ["A. Atropine", "B. Pralidoxime (2-PAM)", "C. Physostigmine", "D. Neostigmine"],
        "answer": "B. Pralidoxime (2-PAM)",
        "exp": "Pralidoxime regenerates phosphorylated acetylcholinesterase if given before 'aging' occurs. Atropine blocks muscarinic signs but does not reactivate AChE."
    },
    {
        "id": "rx12", "type": "Direct MCQs",
        "q": "Which volatile inhaled anesthetic acts partly via two-pore domain potassium channels (TREK/TASK)?",
        "options": ["A. Isoflurane", "B. Ketamine", "C. Propofol", "D. Etomidate"],
        "answer": "A. Isoflurane",
        "exp": "Inhaled halogenated anesthetics (isoflurane, sevoflurane) activate background 2-pore K+ channels, hyperpolarizing CNS neurons."
    },
    {
        "id": "rx13", "type": "Case Scenarios",
        "q": "Glaucoma treatment with Pilocarpine lowers intraocular pressure by opening the trabecular meshwork via contraction of which muscle?",
        "options": ["A. Dilator pupillae muscle", "B. Ciliary muscle", "C. Superior rectus muscle", "D. Levator palpebrae"],
        "answer": "B. Ciliary muscle",
        "exp": "Pilocarpine contracts the M3-mediated ciliary muscle and sphincter pupillae, pulling the scleral spur to open trabecular meshwork drainage of aqueous humor."
    },
    {
        "id": "rx14", "type": "Direct MCQs",
        "q": "Administration of a Monoamine Oxidase B (MAO-B) inhibitor like Selegiline in Parkinson's disease results in:",
        "options": ["A. Decreased synaptic dopamine levels", "B. Reduced dopamine breakdown in the striatum", "C. Increased degradation of levodopa", "D. Blockade of D2 receptors"],
        "answer": "B. Reduced dopamine breakdown in the striatum",
        "exp": "MAO-B selectively metabolizes dopamine in the brain; inhibiting MAO-B prolongs striatal dopamine survival."
    },
    {
        "id": "rx15", "type": "Exceptions",
        "q": "Local anesthetics are less effective in infected tissues because of:",
        "options": ["A. Decreased extracellular pH causing ion trapping in the ionized protonated form", "B. Increased tissue vascularity clearing the drug", "C. Direct enzymatic inactivation by bacterial enzymes", "D. Hyperpolarization of nerve membranes"],
        "answer": "A. Decreased extracellular pH causing ion trapping in the ionized protonated form",
        "exp": "Infected tissue is acidic (low pH), converting weak base local anesthetics into their ionized BH+ form, which cannot penetrate lipophilic nerve sheaths."
    },
    {
        "id": "rx16", "type": "Direct MCQs",
        "q": "Co-administration of epinephrine with local anesthetics (e.g. Lidocaine) serves to:",
        "options": ["A. Cause local vasoconstriction via alpha-1 receptors, decreasing systemic absorption and prolonging anesthesia", "B. Increase systemic absorption rate", "C. Neutralize local tissue acid", "D. Directly block voltage-gated Na+ channels"],
        "answer": "A. Cause local vasoconstriction via alpha-1 receptors, decreasing systemic absorption and prolonging anesthesia",
        "exp": "Epinephrine vasoconstricts local arterioles, keeping the anesthetic localized, enhancing blockade, and reducing toxicity."
    },
    {
        "id": "rx17", "type": "Direct MCQs",
        "q": "Which atypical antipsychotic acts as a partial agonist at D2 and 5-HT1A receptors and antagonist at 5-HT2A receptors?",
        "options": ["A. Haloperidol", "B. Clozapine", "C. Aripiprazole", "D. Chlorpromazine"],
        "answer": "C. Aripiprazole",
        "exp": "Aripiprazole is a 'dopamine system stabilizer' acting as a D2 partial agonist."
    },
    {
        "id": "rx18", "type": "Case Scenarios",
        "q": "A transdermal patch of Scopolamine applied behind the ear prevents motion sickness primarily by antagonizing muscarinic receptors in the:",
        "options": ["A. Gastrointestinal tract", "B. Vestibular nuclei and vomiting center (area postrema)", "C. Cerebral cortex", "D. Carotid sinus"],
        "answer": "B. Vestibular nuclei and vomiting center (area postrema)",
        "exp": "Scopolamine blocks M1 muscarinic receptors in the vestibular apparatus and nucleus tractus solitarius, suppressing motion-induced nausea."
    },
    {
        "id": "rx19", "type": "Direct MCQs",
        "q": "Benzodiazepines (e.g., Diazepam) enhance GABAergic neurotransmission by increasing the:",
        "options": ["A. Channel opening duration of GABA-A Cl- channels", "B. Channel opening frequency of GABA-A Cl- channels", "C. Synthesis of GABA", "D. Reuptake of glutamate"],
        "answer": "B. Channel opening frequency of GABA-A Cl- channels",
        "exp": "Benzodiazepines increase GABA-A channel opening FREQUENCY (Barbiturates increase DURATION)."
    },
    {
        "id": "rx20", "type": "Direct MCQs",
        "q": "Which cholinesterase inhibitor crosses the blood-brain barrier and is used to improve cognitive function in Alzheimer's disease?",
        "options": ["A. Neostigmine", "B. Pyridostigmine", "C. Donepezil / Rivastigmine", "D. Edrophonium"],
        "answer": "C. Donepezil / Rivastigmine",
        "exp": "Donepezil, Rivastigmine, and Galantamine are lipophilic central acetylcholinesterase inhibitors used in Alzheimer's disease."
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
    render_quiz(q_pharm, "pharm")

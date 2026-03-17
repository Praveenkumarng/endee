"""
Cotton Disease Knowledge Base Loader
=====================================
Loads a comprehensive, built-in knowledge base about cotton leaf diseases
directly into the Endee Vector Database (no external PDFs required).

Run once before starting the backend:
    python rag/document_processor.py
"""

import os
from endee_client import EndeeClient
from sentence_transformers import SentenceTransformer

# ============================================================
# BUILT-IN COTTON DISEASE KNOWLEDGE BASE
# ============================================================

COTTON_KNOWLEDGE = [

    # ── BACTERIAL BLIGHT ──────────────────────────────────────
    {
        "id": "bb_overview",
        "text": (
            "Bacterial Blight of Cotton (Xanthomonas citri pv. malvacearum) is one of the most "
            "destructive bacterial diseases of cotton. Symptoms include water-soaked angular leaf spots "
            "that turn brown or black, blackarm on stems and branches, and boll rot. "
            "Disease spreads rapidly in warm, humid, rainy conditions (25–35°C)."
        )
    },
    {
        "id": "bb_chemical_treatment",
        "text": (
            "Chemical treatment for Bacterial Blight: Spray Streptomycin Sulphate 100 ppm "
            "(1g in 10 litres of water) or Copper Oxychloride 0.3% (3g per litre of water). "
            "Apply 2–3 sprays at 10-day intervals. Avoid overhead irrigation to reduce spread. "
            "Use Bacterinashak or Blitox-50 as alternatives. Start spraying at the first sign of infection."
        )
    },
    {
        "id": "bb_organic_treatment",
        "text": (
            "Organic control for Bacterial Blight: Use PGPR (Plant Growth Promoting Rhizobacteria) "
            "seed treatment. Spray neem seed kernel extract (NSKE) at 5%. Bordeaux mixture (1%) "
            "is effective as a protective spray. Remove and burn infected plant debris. "
            "Maintain field sanitation and avoid waterlogging."
        )
    },
    {
        "id": "bb_resistant_varieties",
        "text": (
            "Resistant cotton varieties for Bacterial Blight: LRA 5166, MCU 5, Suvin, NHH 44, "
            "DHH 11, Kiran, Savita, and LD 327 show good resistance. "
            "Seed treatment with Thiram 75% WP @ 3g/kg or Carbendazim 50% WP @ 2g/kg "
            "helps prevent seed-borne infection."
        )
    },
    {
        "id": "bb_prevention",
        "text": (
            "Prevention of Bacterial Blight: Use certified disease-free seeds. Adopt crop rotation "
            "with non-host crops. Avoid excessive nitrogen fertilization which promotes lush growth "
            "susceptible to disease. Ensure proper drainage in fields. "
            "Destroy all crop residues after harvest. Plough deep after harvest to bury infected debris."
        )
    },

    # ── FUSARIUM WILT ─────────────────────────────────────────
    {
        "id": "fw_overview",
        "text": (
            "Fusarium Wilt (Fusarium oxysporum f.sp. vasinfectum) is a serious soil-borne fungal disease "
            "of cotton. It causes yellowing of leaves starting from older leaves, wilting of the plant, "
            "vascular discoloration (brown streaks inside the stem), and plant death. "
            "The pathogen survives in soil for many years. Most damaging in sandy, acidic soils."
        )
    },
    {
        "id": "fw_chemical_treatment",
        "text": (
            "Chemical treatment for Fusarium Wilt: Seed treatment with Thiram 75% WP @ 2g/kg + "
            "Carbendazim 50% WP @ 1g/kg. Soil drench with Carbendazim 0.1% (1g per litre) "
            "around the root zone at first sign of wilt. Apply Trichoderma viride @ 4g/kg seed "
            "for biocontrol. Metalaxyl-based treatments are also effective."
        )
    },
    {
        "id": "fw_soil_management",
        "text": (
            "Soil management for Fusarium Wilt: Apply neem cake @ 250 kg/ha before sowing to suppress "
            "soil-borne pathogens. Lime the soil to maintain pH 6.5–7.0, as the fungus thrives in acidic soils. "
            "Avoid water stress and waterlogging. Practice deep tillage to reduce inoculum levels. "
            "Apply well-decomposed FYM (Farm Yard Manure) to improve soil health."
        )
    },
    {
        "id": "fw_biocontrol",
        "text": (
            "Biological control for Fusarium Wilt: Trichoderma viride or T. harzianum @ 4g/kg seed "
            "or soil application @ 2.5 kg/ha mixed with FYM. Pseudomonas fluorescens @ 10g/kg seed. "
            "These antagonistic fungi suppress Fusarium growth in the root zone. PGPR inoculants "
            "like Azospirillum also help build plant immunity."
        )
    },
    {
        "id": "fw_resistant_varieties",
        "text": (
            "Resistant cotton varieties for Fusarium Wilt: MCU 7, LRA 5166, Surya, LRK 516, "
            "Varalaxmi, Kanchana, and CA 100 show moderate to high resistance. "
            "Avoid continuous cotton cultivation in the same field. Crop rotation with jowar, "
            "groundnut, or maize for 2–3 years helps break the disease cycle."
        )
    },
    {
        "id": "fw_symptoms_diagnosis",
        "text": (
            "Diagnosing Fusarium Wilt: Cut the stem at the base — brown/dark vascular discoloration "
            "inside the stem (xylem) is a clear sign of Fusarium Wilt. Yellowing starts from "
            "lower/older leaves. Entire plant wilts even when soil moisture is adequate. "
            "Unlike Bacterial Blight, there are no leaf spots. Roots may appear rotten."
        )
    },

    # ── LEAF CURL VIRUS ───────────────────────────────────────
    {
        "id": "lcv_overview",
        "text": (
            "Cotton Leaf Curl Disease (CLCuD) is caused by Cotton Leaf Curl Virus (CLCuV), "
            "transmitted by the whitefly (Bemisia tabaci). Symptoms include upward/downward leaf "
            "curling, enation (leaf-like outgrowths on leaf undersides), thickening of veins, "
            "stunted plant growth, and reduced boll formation. It is the most devastating virus "
            "disease of cotton in South Asia. No chemical cure; management focuses on vector control."
        )
    },
    {
        "id": "lcv_whitefly_control",
        "text": (
            "Whitefly (vector) control for Leaf Curl Virus: Spray Imidacloprid 17.8 SL @ 0.5ml/litre "
            "or Thiamethoxam 25 WG @ 0.3g/litre. Alternate with Spiromesifen 22.9 SC @ 1ml/litre "
            "or Pyriproxyfen 10 EC @ 1ml/litre to prevent resistance. "
            "Apply yellow sticky traps @ 5/acre to monitor and reduce whitefly populations. "
            "Spray during evening to protect pollinators."
        )
    },
    {
        "id": "lcv_organic_control",
        "text": (
            "Organic and cultural control for Leaf Curl Virus: Spray NSKE (Neem Seed Kernel Extract) "
            "at 5% to deter whiteflies. Use silver/reflective mulch to repel whiteflies. "
            "Remove rogued (infected) plants early to prevent virus spread. "
            "Intercrops with cowpea or okra attract natural predators of whitefly. "
            "Avoid planting near virus-infected alternate host plants like tomato, brinjal, hibiscus."
        )
    },
    {
        "id": "lcv_resistant_varieties",
        "text": (
            "Resistant cotton varieties for Leaf Curl Virus: CIM-496, CIM-506, MNH-786, IUB-222, "
            "FH-142, Sitara-008 show tolerance. In India, varieties like HS6, F846, and some "
            "Bt hybrids with CLCuV resistance are available. Tolerant varieties significantly "
            "reduce yield losses even when disease is present."
        )
    },
    {
        "id": "lcv_prevention",
        "text": (
            "Prevention of Leaf Curl Virus: Seed treatment with Imidacloprid 70 WS @ 7g/kg seed "
            "protects seedlings from early whitefly attack. Maintain field hygiene — remove weeds "
            "that act as virus reservoirs. Avoid late sowing. Maintain optimum plant spacing "
            "(60x30 cm) to allow air circulation. Scout fields weekly for early detection."
        )
    },
    {
        "id": "lcv_diagnosis",
        "text": (
            "Diagnosing Leaf Curl Virus vs nutrient deficiency: Leaf curl with enations (raised "
            "outgrowths under the leaf) is a definitive sign of CLCuV — not seen in nutrient deficiency. "
            "Vein thickening and darkening, stunted growth, and small deformed bolls confirm the disease. "
            "Whiteflies visible on underside of leaves. No wilting or stem discoloration."
        )
    },

    # ── HEALTHY LEAF / GENERAL COTTON CARE ────────────────────
    {
        "id": "healthy_general",
        "text": (
            "A healthy cotton leaf is flat, bright green, and free of spots, curling, or discoloration. "
            "For optimal cotton health: apply balanced NPK fertilizer (N:P:K = 120:60:60 kg/ha). "
            "Irrigate at critical stages: germination, squaring, boll formation. "
            "Scout for pests weekly. Use integrated pest management (IPM) for sustainable production."
        )
    },
    {
        "id": "healthy_ipm",
        "text": (
            "Integrated Pest Management (IPM) for cotton: Use pheromone traps for bollworm monitoring "
            "(5 traps/ha). Release Trichogramma chilonis @ 1.5 lakh/ha for egg parasitization. "
            "Apply HaNPV (Helicoverpa Nuclear Polyhedrosis Virus) for bollworm. "
            "Avoid prophylactic insecticide sprays — spray only when pest reaches economic threshold."
        )
    },
    {
        "id": "healthy_soil",
        "text": (
            "Soil and nutrition for healthy cotton: Cotton grows best in deep, well-drained black cotton soil "
            "or sandy loam with pH 6.0–8.0. Apply 10–15 tonnes FYM/ha before sowing. "
            "Use micronutrient mixtures if Iron (Fe), Zinc (Zn) or Boron (B) deficiencies appear. "
            "Foliar spray of 2% DAP (di-ammonium phosphate) boosts boll development."
        )
    },

    # ── GENERAL TREATMENT TIPS ────────────────────────────────
    {
        "id": "general_spray_tips",
        "text": (
            "General spraying guidelines for cotton: Always spray in early morning or late evening "
            "to minimise evaporation and protect beneficial insects. Use 200–250 litres of water per acre. "
            "Shake the spray solution well before and during application. "
            "Wear protective gear (gloves, mask). Clean sprayers after use. "
            "Rotate chemicals with different modes of action to prevent resistance development."
        )
    },
    {
        "id": "general_harvesting",
        "text": (
            "Cotton harvesting and post-harvest: Harvest when 50–60% bolls are open (about 150–180 days "
            "after sowing). Pick early in the morning. Store in dry, clean jute bags. "
            "Remove and burn all crop residues after harvest to eliminate disease and pest sources "
            "for the next season. Deep plough the field after harvest."
        )
    },
]

# ============================================================
# ENDEE LOADER
# ============================================================

def get_or_create_collection(client, collection_name="cotton_knowledge_base"):
    try:
        col = client.get_collection(collection_name)
        print(f"✓ Collection '{collection_name}' already exists.")
        return col, False  # False = already existed
    except Exception:
        print(f"  Creating new collection '{collection_name}'...")
        col = client.create_collection(
            name=collection_name,
            dimension=384,  # all-MiniLM-L6-v2 outputs 384-dim vectors
        )
        return col, True   # True = freshly created


def load_builtin_knowledge(force_reload: bool = False):
    """
    Embeds the built-in COTTON_KNOWLEDGE list and inserts it into Endee.
    If the collection already exists and force_reload=False, skips loading.
    """
    print("=" * 60)
    print("  Cotton Disease Knowledge Base Loader")
    print("=" * 60)

    print("\n[1/3] Connecting to Endee at http://localhost:8080 ...")
    try:
        client = EndeeClient(url="http://localhost:8080")
    except Exception as e:
        print(f"❌ Could not connect to Endee: {e}")
        print("   Make sure Endee is running (e.g. via docker-compose up -d)")
        return

    collection, is_new = get_or_create_collection(client)

    if not is_new and not force_reload:
        print("  Knowledge base already populated. Use force_reload=True to reload.")
        print("=" * 60)
        return

    print("\n[2/3] Loading sentence-transformers model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print(f"✓ Model loaded. Embedding {len(COTTON_KNOWLEDGE)} knowledge chunks...")

    ids = []
    vectors = []
    metadata = []

    for entry in COTTON_KNOWLEDGE:
        embedding = model.encode(entry["text"]).tolist()
        ids.append(entry["id"])
        vectors.append(embedding)
        metadata.append({"text": entry["text"], "source": "builtin_cotton_knowledge"})

    print(f"\n[3/3] Inserting {len(ids)} vectors into Endee...")
    try:
        collection.insert(ids=ids, vectors=vectors, metadata=metadata)
        print(f"✓ Successfully loaded {len(ids)} knowledge entries into Endee!")
    except Exception as e:
        print(f"❌ Insert failed: {e}")
        return

    print("\n" + "=" * 60)
    print("  ✅ Knowledge base ready! Start the backend now.")
    print("=" * 60)


if __name__ == "__main__":
    # Set force_reload=True to overwrite an existing collection
    load_builtin_knowledge(force_reload=False)

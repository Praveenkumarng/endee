"""
Expert Chatter — RAG-powered Agricultural AI Assistant
=======================================================
Flow:
  1. Embed user question using sentence-transformers
  2. Search Endee Vector DB for relevant agricultural context  
  3. If Endee is unavailable → fallback to built-in knowledge base
  4. Inject context + call LLM (OpenAI or Gemini) for final answer
"""

import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# ─── Embedding Model ────────────────────────────────────────────────
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    embedding_model = None
    print(f"[ExpertChat] Warning: Could not load sentence-transformers: {e}")

# ─── Built-in Fallback Knowledge Base ───────────────────────────────
# Used when Endee Vector DB is offline (no Docker)

BUILTIN_KB = [
    # Bacterial Blight
    ("bacterial blight treatment spray chemical",
     "For Bacterial Blight: Spray Streptomycin Sulphate 100 ppm (1g per 10 litres water) "
     "or Copper Oxychloride 0.3% (3g/litre). Apply 2–3 sprays at 10-day intervals. "
     "Alternatives: Blitox-50, Bacterinashak."),
    ("bacterial blight organic neem prevention",
     "Organic control for Bacterial Blight: Spray NSKE (Neem Seed Kernel Extract) at 5%. "
     "Bordeaux mixture (1%) as protective spray. Remove and burn infected debris. Avoid waterlogging."),
    ("bacterial blight resistant variety seed",
     "Resistant varieties for Bacterial Blight: LRA 5166, MCU 5, Suvin, NHH 44, DHH 11, Kiran, Savita. "
     "Seed treatment: Thiram 75% WP @ 3g/kg or Carbendazim 50% WP @ 2g/kg."),
    ("bacterial blight symptoms identify",
     "Bacterial Blight symptoms: Angular water-soaked leaf spots turning brown/black, "
     "blackarm on stems, boll rot. Spreads in warm humid rainy weather (25–35°C)."),

    # Fusarium Wilt
    ("fusarium wilt treatment chemical seed",
     "Fusarium Wilt treatment: Seed treatment with Thiram 75% WP @ 2g/kg + Carbendazim @ 1g/kg. "
     "Soil drench with Carbendazim 0.1% around root zone at first sign of wilt. Metalaxyl also effective."),
    ("fusarium wilt biocontrol trichoderma organic",
     "Biocontrol for Fusarium Wilt: Trichoderma viride/harzianum @ 4g/kg seed or 2.5 kg/ha soil application. "
     "Pseudomonas fluorescens @ 10g/kg seed. Neem cake @ 250 kg/ha before sowing."),
    ("fusarium wilt soil management lime pH",
     "Soil management for Fusarium Wilt: Lime soil to maintain pH 6.5–7.0 (fungus thrives in acidic soil). "
     "Avoid waterlogging. Deep tillage to reduce inoculum. Apply FYM for soil health improvement."),
    ("fusarium wilt symptoms diagnosis stem",
     "Diagnosing Fusarium Wilt: Cut stem at base — brown vascular discoloration inside stem (xylem). "
     "Yellowing starts from lower older leaves. Plant wilts even with adequate soil moisture. "
     "Roots may appear rotten. No leaf spots (unlike Bacterial Blight)."),
    ("fusarium wilt resistant variety crop rotation",
     "Resistant varieties for Fusarium Wilt: MCU 7, LRA 5166, Surya, Varalaxmi, Kanchana, CA 100. "
     "Crop rotation with jowar, groundnut, or maize for 2–3 years breaks the disease cycle."),

    # Leaf Curl Virus
    ("leaf curl virus whitefly insecticide control",
     "Whitefly control for Leaf Curl Virus: Spray Imidacloprid 17.8 SL @ 0.5ml/litre or "
     "Thiamethoxam 25 WG @ 0.3g/litre. Alternate with Spiromesifen 22.9 SC @ 1ml/litre. "
     "Use yellow sticky traps @ 5/acre. Spray in evening to protect pollinators."),
    ("leaf curl virus organic cultural neem",
     "Organic control for Leaf Curl Virus: Spray NSKE at 5% to deter whiteflies. "
     "Use silver reflective mulch. Remove infected plants early. "
     "Intercrops cowpea/okra to attract whitefly predators."),
    ("leaf curl virus resistant variety seed treatment",
     "Resistant varieties for Leaf Curl Virus: CIM-496, CIM-506, MNH-786, FH-142, IUB-222. "
     "India: HS6, F846, and some Bt hybrids. Seed treatment: Imidacloprid 70 WS @ 7g/kg seed."),
    ("leaf curl virus symptoms diagnosis enation",
     "Leaf Curl Virus symptoms: Upward/downward leaf curling with enations (raised outgrowths under leaf). "
     "Vein thickening, darkening, stunted growth, deformed small bolls. "
     "Whiteflies visible on leaf undersides. No wilt or stem discoloration."),

    # General
    ("cotton healthy care fertilizer water",
     "Healthy cotton care: Apply NPK @ 120:60:60 kg/ha. Irrigate at germination, squaring, boll formation. "
     "Scout weekly for pests. Use IPM approach for sustainable production."),
    ("cotton spray tips pesticide application",
     "Spraying tips: Spray early morning or late evening. Use 200–250 litres water/acre. "
     "Rotate chemicals to prevent resistance. Wear protective gear. Clean sprayers after use."),
    ("cotton harvest post harvest residue",
     "Harvesting: Harvest when 50–60% bolls are open (150–180 days after sowing). "
     "Pick in morning. Store in dry jute bags. Burn crop residue to eliminate pathogens and pests."),
]


def _cosine_similarity(v1, v2):
    """Simple cosine similarity between two lists."""
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = sum(a * a for a in v1) ** 0.5
    mag2 = sum(b * b for b in v2) ** 0.5
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def _search_builtin_kb(query: str, disease_name: str, top_k: int = 3) -> str:
    """Search the built-in knowledge base using embedding similarity."""
    if embedding_model is None:
        # Last resort: keyword match
        results = []
        query_lower = query.lower()
        disease_lower = disease_name.lower().replace(" ", "")
        for keywords, text in BUILTIN_KB:
            if disease_lower in keywords or any(w in query_lower for w in keywords.split()):
                results.append(text)
        return "\n---\n".join(results[:top_k]) if results else ""

    query_vec = embedding_model.encode(f"{disease_name}. {query}").tolist()
    scored = []
    for keywords, text in BUILTIN_KB:
        kb_vec = embedding_model.encode(f"{keywords}. {text}").tolist()
        score = _cosine_similarity(query_vec, kb_vec)
        scored.append((score, text))
    scored.sort(reverse=True)
    top = [text for _, text in scored[:top_k]]
    return "\n---\n".join(top)


def get_endee_context(query: str, disease_name: str, collection_name: str = "cotton_knowledge_base", top_k: int = 3) -> tuple[str, str]:
    """
    Try Endee first; if unavailable, fall back to built-in knowledge base.
    Returns: (context_text, source_label)
    """
    try:
        from endee_client import EndeeClient
        client = EndeeClient(url="http://localhost:8080")
        query_vector = embedding_model.encode(f"{disease_name}. {query}").tolist()
        collection = client.get_collection(collection_name)
        results = collection.search(query_vectors=[query_vector], limit=top_k)

        context_chunks = []
        if results and len(results) > 0:
            for match in results[0]:
                metadata = getattr(match, 'metadata', {})
                if 'text' in metadata:
                    context_chunks.append(metadata['text'])

        if context_chunks:
            return "\n---\n".join(context_chunks), "Endee Vector DB"
        else:
            print("[ExpertChat] Endee returned no results, using built-in KB.")
            return _search_builtin_kb(query, disease_name, top_k), "Built-in Knowledge Base"

    except Exception as e:
        print(f"[ExpertChat] Endee unavailable ({type(e).__name__}), using built-in KB.")
        return _search_builtin_kb(query, disease_name, top_k), "Built-in Knowledge Base"


def _call_llm(system_prompt: str, user_question: str) -> str:
    """Try OpenAI first, then fall back to Gemini if configured."""

    # ── Try OpenAI ───────────────────────────────────────────
    openai_key = os.getenv("OPENAI_API_KEY", "")
    if openai_key and not openai_key.startswith("your_"):
        try:
            import openai
            openai.api_key = openai_key
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.7,
                max_tokens=350
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[ExpertChat] OpenAI failed: {e}")

    # ── Try Gemini ───────────────────────────────────────────
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    if gemini_key and not gemini_key.startswith("your_"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            full_prompt = f"{system_prompt}\n\nUser question: {user_question}"
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"[ExpertChat] Gemini failed: {e}")

    return None


def generate_expert_response(disease_name: str, user_question: str, language: str = 'en') -> str:
    """
    RAG Pipeline:
      1. Retrieve context from Endee (or built-in KB if offline)
      2. Build prompt with context
      3. Call LLM (OpenAI → Gemini fallback)
      4. If no LLM configured, return context directly as answer
    """
    # Map language codes to names
    lan_map = {
        'en': 'English',
        'hi': 'Hindi',
        'te': 'Telugu',
        'kn': 'Kannada'
    }
    target_language = lan_map.get(language, 'English')

    # 1. Retrieve context
    context, source = get_endee_context(user_question, disease_name)

    # 2. Build system prompt
    system_prompt = f"""You are an expert agricultural AI assistant specializing in Cotton crops.
The user has uploaded an image and the AI has detected: {disease_name}.

CRITICAL: You MUST provide your entire response in {target_language}. 
Even if the retrieved context is in English, translate the important points into {target_language}.

Use the following retrieved context (sourced from: {source}) to answer the user's question.
If the context doesn't fully answer, supplement with general agricultural knowledge.
Keep your answer concise, practical, and farmer-friendly.

Retrieved Context:
{context}
"""

    # 3. Call LLM
    llm_answer = _call_llm(system_prompt, user_question)

    if llm_answer:
        return llm_answer

    # 4. Fallback: return raw context if no LLM is configured
    if context:
        header = {
            'en': f"**Based on our knowledge base for {disease_name}:**",
            'hi': f"**{disease_name} के लिए हमारे ज्ञान आधार के आधार पर:**",
            'te': f"**{disease_name} కోసం మా నాలెడ్జ్ బేస్ ఆధారంగా:**",
            'kn': f"**{disease_name} ಗಾಗಿ ನಮ್ಮ ಜ್ಞಾನದ ಆಧಾರದ ಮೇಲೆ:**"
        }.get(language, f"**Based on our knowledge base for {disease_name}:**")
        
        footer = {
            'en': "\n\n*(Note: For more personalized advice, configure an OpenAI or Gemini API key)*",
            'hi': "\n\n*(नोट: अधिक व्यक्तिगत सलाह के लिए, OpenAI या Gemini API कुंजी कॉन्फ़िगर करें)*",
            'te': "\n\n*(గమనిక: మరింత వ్యక్తిగత సలహా కోసం, OpenAI లేదా Gemini API కీని కాన్ఫిగర్ చేయండి)*",
            'kn': "\n\n*(ಸೂಚನೆ: ಹೆಚ್ಚಿನ ವೈಯಕ್ತಿಕ ಸಲಹೆಗಾಗಿ, OpenAI ಅಥವಾ Gemini API ಕೀಲಿಯನ್ನು ಕಾನ್ಫಿಗರ್ ಮಾಡಿ)*"
        }.get(language, "\n\n*(Note: For more personalized advice, configure an OpenAI or Gemini API key)*")

        return (
            header + "\n\n"
            + context.replace("---", "\n")
            + footer
        )

    fallback_msg = {
        'en': f"I don't have specific data for that query about {disease_name} in our knowledge base.",
        'hi': f"मेरे पास हमारे ज्ञान आधार में {disease_name} के बारे में उस प्रश्न के लिए विशिष्ट डेटा नहीं है।",
        'te': f"మా నాలెడ్జ్ బేస్‌లో {disease_name} గురించి ఆ ప్రశ్న కోసం నా దగ్గర నిర్దిష్ట డేటా లేదు.",
        'kn': f"ನಮ್ಮ ಜ್ಞಾನದ ಮೂಲದಲ್ಲಿ {disease_name} ಕುರಿತಾದ ಆ ಪ್ರಶ್ನೆಗೆ ನನ್ನ ಬಳಿ ನಿರ್ದಿಷ್ಟ ಡೇಟಾ ಇಲ್ಲ."
    }.get(language, f"I don't have specific data for that query about {disease_name}.")
    
    return fallback_msg

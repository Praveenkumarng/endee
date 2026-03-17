import os
from endee_client import EndeeClient
from sentence_transformers import SentenceTransformer
import openai
from dotenv import load_dotenv

load_dotenv()

# Initialize Local Embedding Model
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading sentence transformer: {e}")

# Initialize Endee
client = EndeeClient(url="http://localhost:8080")

def get_endee_context(query: str, collection_name: str = "cotton_knowledge_base", top_k: int = 3):
    try:
        # Convert query into vector
        query_vector = embedding_model.encode(query).tolist()
        
        # Search Endee Database
        collection = client.get_collection(collection_name)
        results = collection.search(
            query_vectors=[query_vector],
            limit=top_k
        )
        
        # Extract Text from Results (assuming metadata holds the 'text')
        context_chunks = []
        if results and len(results) > 0:
            for match in results[0]: # usually returns list of lists
                # Adjust based on exact Endee return structure
                metadata = getattr(match, 'metadata', {})
                if 'text' in metadata:
                    context_chunks.append(metadata['text'])
                    
        return "\n---\n".join(context_chunks)
    except Exception as e:
        print(f"Error querying Endee: {e}")
        return ""

def generate_expert_response(disease_name: str, user_question: str):
    """
    RAG Implementation:
    1. Augment user query with the detected disease context.
    2. Search Endee Vector DB for relevant agricultural data.
    3. Pass Endee context + user question to LLM for final answer.
    """
    search_query = f"Cotton disease {disease_name}. {user_question}"
    
    # 1. Retrieve Context from Endee
    context = get_endee_context(search_query)
    
    # 2. Formulate Prompt
    system_prompt = f"""You are an expert agricultural AI assistant specializing in Cotton crops.
The user has uploaded an image and the AI has detected: {disease_name}.

Use the following retrieved context from our agricultural database to answer the user's question. 
If the context doesn't contain the answer, say "I don't have enough specific information on that, but based on general knowledge..." and then provide a general answer. Keep it concise, helpful, and focused on helping the farmer.

Context from Endee Vector Database:
{context}
"""

    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            return "Error: OPENAI_API_KEY is not set in backend/.env. Please set it to use the Expert AI feature."
            
        print("Sending prompt to OpenAI with Endee Context...")
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generation response: {e}")
        return f"Sorry, I couldn't reach the AI brain right now. Please check the logs. Error: {str(e)}"

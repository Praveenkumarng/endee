import os
from endee_client import EndeeClient
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# Initialize Endee Client
# Ensure Endee is running locally or provide remote URL
client = EndeeClient(url="http://localhost:8080")

# Embedding Model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_or_create_collection(collection_name="cotton_knowledge_base"):
    try:
        # Check if collection exists
        col = client.get_collection(collection_name)
        print(f"Collection {collection_name} exists.")
        return col
    except Exception as e:
        print(f"Creating new collection {collection_name}...")
        col = client.create_collection(
            name=collection_name, 
            dimension=384, # all-MiniLM-L6-v2 outputs 384d vectors
        )
        return col

def process_documents(doc_dir="data/agricultural_docs"):
    print(f"Loading documents from {doc_dir}...")
    loader = PyPDFDirectoryLoader(doc_dir)
    docs = loader.load()
    
    if not docs:
        print("No documents found. Please add PDFs to data/agricultural_docs.")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)
    
    collection = get_or_create_collection()
    
    print(f"Embedding and inserting {len(chunks)} chunks into Endee...")
    
    vectors = []
    metadata = []
    ids = []
    
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk.page_content).tolist()
        vectors.append(embedding)
        metadata.append({"text": chunk.page_content, "source": chunk.metadata.get("source", "unknown")})
        ids.append(f"chunk_{i}")
        
    # Batch insert into Endee
    collection.insert(
        ids=ids,
        vectors=vectors,
        metadata=metadata
    )
    print("Successfully populated Endee Vector DB.")

if __name__ == "__main__":
    # Ensure directory exists
    os.makedirs("data/agricultural_docs", exist_ok=True)
    process_documents()

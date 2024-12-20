from langchain_chroma import Chroma
import json
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_core.documents import Document
import chromadb
from dotenv import load_dotenv
import os
# Load .env file
load_dotenv()

# Initialize Parameters
CHROMA_PATH = os.getenv('DATABASE_CHROMA_PATH')
DATA_PATH = "data/knowledge"

# Define Embeddings
embeddings = HuggingFaceInferenceAPIEmbeddings(api_key=os.getenv('UTIL_HF_TOKEN'),model_name=os.getenv('DATABASE_EMBEDDING_MODEL'))

# Initialize Vector DB
persistent_client = chromadb.PersistentClient()
db = Chroma(
client=persistent_client,
collection_name="knowledge_collection",
embedding_function=embeddings,
)

# Function to Query LLM and RAG
def query(query=""):
    # Retrieve from chroma: Only get the single most similar document from the dataset 
    # (see here for more retrieval options:https://python.langchain.com/v0.2/api_reference/chroma/vectorstores/langchain_chroma.vectorstores.Chroma.html#langchain_chroma.vectorstores.Chroma.as_retriever)  
    retriever = db.as_retriever(search_kwargs={'k': 2})
    result=retriever.invoke(query)
    # Debugging Purpose
    with open("debug.txt", "a") as f:
        f.write('RAG result: \n'+str(result) + "\n")
    return result[0].page_content
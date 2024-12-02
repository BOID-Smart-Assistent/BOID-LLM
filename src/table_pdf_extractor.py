
import pdfplumber
import pandas as pd
import json
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_core.documents import Document
import chromadb
from tqdm import tqdm
import os
from dotenv import load_dotenv
# Load .env file
load_dotenv()

# Initialize Parameters
CHROMA_PATH = os.getenv('DATABASE_CHROMA_PATH')
DATA_PATH = "data/knowledge/unstructured_pdf"

# Define Embeddings
# embeddings = HuggingFaceEmbeddings(api_key=config['util']['hf_token'],model_name=config['database']['embedding_model'])
embeddings = HuggingFaceInferenceAPIEmbeddings(api_key=os.getenv('UTIL_HF_TOKEN'),model_name=os.getenv('DATABASE_EMBEDDING_MODEL'))

# Initialize Vector DB
persistent_client = chromadb.PersistentClient()
db = Chroma(
client=persistent_client,
collection_name="knowledge_collection",
embedding_function=embeddings,
)

        
# Function to extract tables from a PDF file
def extract_table_from_pdf(pdf_file, page_number=0):
    # Open the PDF file
    with pdfplumber.open(pdf_file) as pdf:
        # Select the page to extract table from
        page = pdf.pages[page_number]
        # Extract the table data
        table = page.extract_table()
        
        # Convert the extracted table to a pandas DataFrame
        if table:
            df = pd.DataFrame(table[1:], columns=table[0])  # Use the first row as column headers
            df = df.assign(metadata=df.index)
            return df
        else:
            print("No table found on this page.")
            return None

def embed_with_chroma(df, embedding_model):
    embeddings = []
    # convert each row into a dictionary and then into a JSON string
    df['data'] = df.apply(lambda row: json.dumps(row.to_dict()), axis=1)
    # Process each row in the DataFrame with a progress bar
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        # Create a Document with necessary fields
        document = Document(
            page_content=row['data'],  # Text content for embedding
            id=str(row['metadata'])  # Unique identifier as string
        )

        # Check if the document is new or not
        try:
            # As 'embed_documents' expects a list of documents, we pass a list with one document
            # and then take the first (and only) embedding from the returned list
            embedding = embedding_model.embed_documents([document.page_content])[0]
            embeddings.append((document, embedding))
        except Exception as e:
            print(f"Failed to embed document: {e}")

    return embeddings


# Function to process all PDF files in the given path and embed their content using Chroma
def process_pdfs_in_path(path,embeddings=embeddings):
    """Process all PDF files in the given path and embed their content using Chroma."""
    pdf_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.pdf')]
    for pdf_file in pdf_files:
        with pdfplumber.open(pdf_file) as pdf:
            for page_number in range(len(pdf.pages)):
                df = extract_table_from_pdf(pdf_file, page_number=page_number)
                if df is not None:
                    document_embeddings = embed_with_chroma(df, embeddings)
                    print(f"Processed page {page_number+1} of {pdf_file}")

# if __name__ == '__main__':
#     process_pdfs_in_path(embeddings, './data/knowledge/table_based')



import os
import fitz  # PyMuPDF
import openai
import pickle
import toml

PDF_FOLDER = "/home/ubuntu/search_manual/pdfs"
EMBEDDINGS_FILE = "/home/ubuntu/search_manual/embeddings/open_ai_embeddings.pkl"
CHUNK_SIZE = 500

# Load secrets from .streamlit/secrets.toml
secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
secrets = toml.load(secrets_path)

# OpenAI and Gemini API keys
openai_api_key = secrets["openai"]["api_key"]

# OpenAI client instance (new SDK syntax)
openai_client = openai.OpenAI(api_key=openai_api_key)

def split_into_chunks(text, chunk_size=CHUNK_SIZE):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

all_chunks = []
for filename in os.listdir(PDF_FOLDER):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(PDF_FOLDER, filename)
        txt_path = pdf_path.replace(".pdf", ".txt")
        # Extract PDF to TXT if needed
        if not os.path.exists(txt_path):
            with fitz.open(pdf_path) as doc:
                text = "\n".join(page.get_text() for page in doc)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)
        # Load TXT
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()
        for idx, chunk in enumerate(split_into_chunks(text)):
            all_chunks.append({
                "filename": filename,
                "chunk_index": idx,
                "content": chunk
            })

print(f"Total chunks to embed: {len(all_chunks)}")

for i, chunk in enumerate(all_chunks):
    if "embedding" not in chunk or chunk["embedding"] is None:
        try:
            resp = openai_client.embeddings.create(input=chunk["content"], model="text-embedding-ada-002")
            chunk["embedding"] = resp.data[0].embedding
        except Exception as e:
                print(f"Error on chunk {i}: {e}")
                chunk["embedding"] = None
        with open(EMBEDDINGS_FILE, "wb") as f:
            pickle.dump(all_chunks, f)
    if (i+1) % 10 == 0 or i == len(all_chunks)-1:
        print(f"Embedded {i+1}/{len(all_chunks)} chunks (and progress saved)")

print(f"Done! Embeddings saved to {EMBEDDINGS_FILE}")                                                                                                                                                                                                                                             
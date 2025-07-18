import pickle
from flask import Flask, request, jsonify
import numpy as np
import openai
import os
import toml

# Load secrets from .streamlit/secrets.toml
secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
secrets = toml.load(secrets_path)
openai_api_key = secrets["openai"]["api_key"]
openai_client = openai.OpenAI(api_key=openai_api_key)

EMBEDDING_DIRECTORY = "/home/ubuntu/search_manual/embeddings/"
EMBEDDINGS_FILE = "open_ai_embeddings.pkl"
EMBEDDINGS_PATH = os.path.join(EMBEDDING_DIRECTORY, EMBEDDINGS_FILE)

app = Flask(__name__)

with open(EMBEDDINGS_PATH, "rb") as f:
    pdf_chunks = pickle.load(f)

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_query_embedding(text):
    resp = openai_client.embeddings.create(input=text, model="text-embedding-ada-002")
    return resp.data[0].embedding

@app.route("/search_manual", methods=["POST"])
def search_manual():
    data = request.get_json()
    query = data["query"]
    query_emb = get_query_embedding(query)
    results = []
    for chunk in pdf_chunks:
        # Only compute similarity if chunk has an embedding
        if "embedding" in chunk and chunk["embedding"] is not None:
            similarity = cosine_similarity(query_emb, chunk["embedding"])
            results.append({
                "filename": chunk["filename"],
                "snippet": chunk["content"].replace('\n', ' '),
                "similarity": float(similarity)
            })
    results = sorted(results, key=lambda x: x["similarity"], reverse=True)[:5]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

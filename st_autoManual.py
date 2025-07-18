import streamlit as st
import requests
st.set_page_config(layout="wide")

st.title("🚗 Automotive Manual Helper: Text Embedding UseCase")
st.header("Make-Honda CRV, Year-2026: 605 pages PDF from ~ https://mygarage.honda.com/s/owners-manuals")

# Provider/model selection
providers = {
    "OpenAI": [
        "text-embedding-ada-002",
        # "text-embedding-3-small",
        # "text-embedding-3-large"
    ],
    "Gemini": [
        "embedding-001"
    ]
}

col1, col2 = st.columns(2)
provider = col1.selectbox("LLM ~ Embedding provider:", list(providers.keys()), index=0)
model = col2.selectbox("Embedding model:", providers[provider])

query = st.text_input(
    "Enter your search query (natural language):",
    value="how to unlock door?"
)

if st.button("Search"):
    if query.strip():
        # Updated to use port 5001
        url = "http://EC2_FLASK_SERVER:5000/search_manual"
        payload = {
            "query": query,
            "provider": provider,
            "model": model
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            results = response.json()
            if results:
                st.success("Results:")
                for item in results:
                    st.write(f"📄 **{item['filename']}**")
                    st.write(item['snippet'])
            else:
                st.warning("No matching PDFs found.")
        else:
            st.error("Server error: " + response.text)
import os
import streamlit as st
import sys

# Ensure src module is reachable
sys.path.insert(0, os.path.abspath('.'))

from src.models import Document
from src.chunking import FixedSizeChunker, SentenceChunker, RecursiveChunker
from src.store import EmbeddingStore
from src.agent import KnowledgeBaseAgent
from src.embeddings import MockEmbedder

# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(page_title="Medical Knowledge Base RAG", page_icon="💊", layout="wide")
st.title("💊 Day 7 Lab: Medical Knowledge RAG Demo")

# Initialize global state to track embedding store instance
if 'store' not in st.session_state:
    st.session_state.store = None
if 'docs' not in st.session_state:
    st.session_state.docs = []

DATA_DIR = 'data'

# =========================================================
# SIDEBAR - DATA & PIPELINE CONFIG
# =========================================================
with st.sidebar:
    st.header("⚙️ RAG Configuration")
    
    st.subheader("1. Chunking Strategy")
    chunk_strat = st.selectbox(
        "Choose strategy:",
        ["SentenceChunker", "FixedSizeChunker", "RecursiveChunker"]
    )
    
    chunk_size = st.number_input("Max chunk size / Sentences", value=3, min_value=1)
    
    # We use MockEmbedder to ensure it runs without API Keys
    st.subheader("2. Embedder")
    st.info("Using **MockEmbedder** for lab environment (deterministic hashing).")

    if st.button("🚀 Process & Index Data"):
        with st.spinner("Processing documents from data/ ..."):
            # Load documents
            raw_docs = []
            if os.path.exists(DATA_DIR):
                for fname in os.listdir(DATA_DIR):
                    if fname.endswith('.md'):
                        with open(os.path.join(DATA_DIR, fname), 'r', encoding='utf-8') as f:
                            raw_docs.append(Document(id=fname, content=f.read(), metadata={"source": fname}))
            
            # Select chunker
            if chunk_strat == "SentenceChunker":
                chunker = SentenceChunker(max_sentences_per_chunk=chunk_size)
            elif chunk_strat == "FixedSizeChunker":
                chunker = FixedSizeChunker(chunk_size=150, overlap=20)
            else:
                chunker = RecursiveChunker(chunk_size=150)
                
            # Chunking
            chunked_docs = []
            for doc in raw_docs:
                chunks = chunker.chunk(doc.content)
                for i, c in enumerate(chunks):
                    chunked_docs.append(Document(id=f"{doc.id}_ch{i}", content=c, metadata=doc.metadata))
            
            st.session_state.docs = chunked_docs
            
            # Indexing
            store = EmbeddingStore(collection_name="st_demo", embedding_fn=MockEmbedder())
            store.add_documents(chunked_docs)
            st.session_state.store = store
            
            st.success(f"Indexed {len(raw_docs)} files into {len(chunked_docs)} chunks!")

# =========================================================
# MAIN PANELS
# =========================================================
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🔍 Retrieval & Generation")
    query = st.text_input("Ask a medical question:", placeholder="e.g. What is diabetic retinopathy?")
    top_k = st.slider("Top K chunks to retrieve:", min_value=1, max_value=10, value=3)
    
    if st.button("Generate Answer"):
        if st.session_state.store is None:
            st.error("Please click 'Process & Index Data' in the sidebar first!")
        elif not query:
            st.warning("Please enter a query.")
        else:
            with st.spinner("Searching and Generating..."):
                store = st.session_state.store
                
                # Mock LLM since no API Key
                def dummy_llm(prompt):
                    return "*(This is a simulated LLM answer based on context, since OpenAI key is not provided)*\n\nThe retrieved context gives the expected definitions and symptoms for the illness mentioned in the query."
                
                agent = KnowledgeBaseAgent(store=store, llm_fn=dummy_llm)
                
                # Retrieve manually just to show chunks
                results = store.search(query, top_k=top_k)
                answer = agent.answer(query, top_k=top_k)
                
                st.subheader("💡 LLM Answer")
                st.info(answer)

with col2:
    st.header("🗂️ Retrieved Chunks view")
    if 'results' in locals() and results:
        for i, res in enumerate(results, 1):
            with st.expander(f"Chunk {i} (Score: {res['score']:.4f}) | File: {res['metadata'].get('source', 'unknown')}", expanded=(i==1)):
                st.markdown(res['content'])
    else:
        st.write("No chunks retrieved yet.")

# =========================================================
# DATABASE STATS
# =========================================================
st.divider()
st.subheader("📊 Database Statistics")
if st.session_state.store is not None:
    st.metric("Total Chunks in Vector Store", st.session_state.store.get_collection_size())
else:
    st.write("Vector store is empty.")

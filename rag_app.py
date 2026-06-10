import streamlit as st
import ollama
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

st.set_page_config(
    page_title="askpdf",
    page_icon="📄",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #0f0f0f;
    }

    .main .block-container {
        padding-top: 0rem;
        max-width: 720px;
    }

    /* navbar */
    .navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 0 1.5rem 0;
        border-bottom: 1px solid #1e1e1e;
        margin-bottom: 2rem;
    }

    .nav-logo {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: -0.02em;
    }

    .nav-logo span {
        color: #a78bfa;
    }

    .nav-badge {
        font-size: 0.7rem;
        color: #555;
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        padding: 3px 10px;
        border-radius: 99px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* hero */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: -0.03em;
        margin-bottom: 0.25rem;
        line-height: 1.1;
    }

    .hero-sub {
        font-size: 1rem;
        color: #555;
        margin-bottom: 2rem;
    }

    .accent { color: #a78bfa; }

    .tag {
        display: inline-block;
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        color: #777;
        font-size: 0.72rem;
        padding: 3px 10px;
        border-radius: 99px;
        margin-right: 6px;
        margin-bottom: 1.5rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .chunk-badge {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        color: #a78bfa;
        font-size: 0.78rem;
        padding: 6px 14px;
        border-radius: 99px;
        display: inline-block;
        margin-bottom: 1.5rem;
    }

    .stChatMessage {
        background: #141414 !important;
        border: 1px solid #1e1e1e !important;
        border-radius: 14px !important;
        padding: 1rem !important;
    }

    [data-testid="stChatMessageContent"] p {
        color: #e0e0e0 !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
    }

    /* input bar fix */
    .stChatInputContainer {
        background: #0f0f0f !important;
        border-top: 1px solid #1e1e1e !important;
        padding: 1rem 0 0.5rem 0 !important;
        position: sticky !important;
        bottom: 0 !important;
    }

    .stChatInputContainer > div {
        background: #1a1a1a !important;
        border: 1px solid #2e2e2e !important;
        border-radius: 14px !important;
        padding: 0.25rem 0.5rem !important;
    }

    textarea[data-testid="stChatInputTextArea"] {
        background: #1a1a1a !important;
        border: none !important;
        border-radius: 14px !important;
        color: #e0e0e0 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        caret-color: #a78bfa !important;
    }

    textarea[data-testid="stChatInputTextArea"]::placeholder {
        color: #444 !important;
    }

    .stChatInputContainer button {
        background: #a78bfa !important;
        border: none !important;
        border-radius: 8px !important;
        color: #0f0f0f !important;
    }

    .stFileUploader {
        background: #141414 !important;
        border: 1px dashed #2a2a2a !important;
        border-radius: 14px !important;
    }

    .stSpinner > div {
        border-top-color: #a78bfa !important;
    }

    .divider {
        border: none;
        border-top: 1px solid #1e1e1e;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def build_index(chunks):
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index

def get_relevant_chunks(question, chunks, index, k=3):
    question_embedding = model.encode([question])
    distances, indices = index.search(np.array(question_embedding), k)
    return [chunks[i] for i in indices[0]]

# navbar
st.markdown("""
<div class="navbar">
    <div class="nav-logo">ask<span>pdf</span></div>
    <div class="nav-badge">beta · local ai</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-title">ask<span class="accent">pdf</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">drop a pdf. ask anything.</div>', unsafe_allow_html=True)
st.markdown('<span class="tag">RAG</span><span class="tag">local AI</span><span class="tag">free</span>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

if uploaded_file:
    if "chunks" not in st.session_state or st.session_state.get("filename") != uploaded_file.name:
        with st.spinner("reading your pdf..."):
            pdf_text = read_pdf(uploaded_file)
            st.session_state.chunks = chunk_text(pdf_text)
            st.session_state.index = build_index(st.session_state.chunks)
            st.session_state.filename = uploaded_file.name
            st.session_state.messages = []

    st.markdown(f'<div class="chunk-badge">✦ {len(st.session_state.chunks)} chunks indexed — {uploaded_file.name}</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("what do you want to know?")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        relevant_chunks = get_relevant_chunks(question, st.session_state.chunks, st.session_state.index)
        context = "\n\n".join(relevant_chunks)

        with st.chat_message("assistant"):
            with st.spinner("thinking..."):
                response = ollama.chat(
                    model="llama3.2",
                    messages=[
                        {"role": "system", "content": f"You are a helpful assistant. Answer questions based on these document excerpts:\n\n{context}"},
                        {"role": "user", "content": question}
                    ]
                )
                answer = response.message.content
                st.write(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

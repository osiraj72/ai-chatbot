import streamlit as st
import ollama
from pypdf import PdfReader

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

st.title("PDF Chatbot")
st.write("Upload a PDF and ask questions about it")

uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

if uploaded_file:
    pdf_text = read_pdf(uploaded_file)
    st.success("PDF loaded! Ask me anything.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    question = st.chat_input("Ask a question about the PDF")
    
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        
        history = [{"role": "system", "content": f"You are a helpful assistant. Answer questions based on this document:\n\n{pdf_text}"}]
        history += st.session_state.messages
        
        response = ollama.chat(
            model="llama3.2",
            messages=history
        )
        
        answer = response.message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)
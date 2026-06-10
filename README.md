# AI Chatbot Projects

A collection of AI projects built with Python, Ollama, and Streamlit.

## Projects

### 1. Chatbot (`chatbot.py`)
A conversational AI chatbot with memory and personality.
- Built with Ollama and llama3.2
- Maintains conversation history
- Runs completely locally

### 2. PDF Chatbot (`app.py`)
A web app that lets you upload a PDF and ask questions about it.
- Built with Streamlit
- Conversation memory
- Clean chat UI

### 3. RAG Chatbot (`rag_chatbot.py`)
A smarter PDF Q&A system using proper RAG.
- Splits PDF into chunks
- Uses FAISS vector database
- Finds relevant context before answering

### 4. AI Agent (`agent.py`)
An AI agent that can search the web to answer questions.
- Uses DuckDuckGo search
- Multi-step reasoning
- Real time information

## Setup

1. Install Ollama from ollama.com
2. Run `ollama pull llama3.2`
3. Install dependencies: `pip install -r requirements.txt`
4. Run any project with `python filename.py`

## Tech Stack
- Python
- Ollama (local AI)
- Streamlit
- FAISS
- SentenceTransformers
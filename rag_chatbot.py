import ollama
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def read_pdf(file_path):
    reader = PdfReader(file_path)
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
    return index, embeddings

def get_relevant_chunks(question, chunks, index, k=3):
    question_embedding = model.encode([question])
    distances, indices = index.search(np.array(question_embedding), k)
    return [chunks[i] for i in indices[0]]

pdf_text = read_pdf(input("Enter PDF filename: "))
print("Processing PDF...")
chunks = chunk_text(pdf_text)
index, embeddings = build_index(chunks)
print(f"PDF loaded! Created {len(chunks)} chunks. Ask me anything.\n")

while True:
    question = input("You: ")
    if question == "quit":
        break
    
    relevant_chunks = get_relevant_chunks(question, chunks, index)
    context = "\n\n".join(relevant_chunks)
    
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": f"Document excerpts:\n{context}\n\nQuestion: {question}"}]
    )
    
    print(f"AI: {response.message.content}\n")
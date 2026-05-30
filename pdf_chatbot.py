import ollama
from pypdf import PdfReader

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def ask_question(pdf_text, question):
    prompt = f"""You are a helpful assistant. Use the following document to answer the question.
    
Document:
{pdf_text}

Question: {question}

Answer based only on the document above."""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.message.content

file_path = input("Enter PDF filename: ")
pdf_text = read_pdf(file_path)

while True:
    question = input("You: ")
    if question == "quit":
        break
    answer = ask_question(pdf_text, question)
    print(f"AI: {answer}\n")
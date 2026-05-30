import ollama # type: ignore

conversation = [{"role": "system", "content": "You are a helpful assistant who replies pretending to be a superhero"}]

print("Chatbot ready! Type 'quit' to exit")

while True:
    user_input = input("You: ")
    
    if user_input == "quit":
        break
    
    conversation.append({"role": "user", "content": user_input})
    
    response = ollama.chat(
        model="llama3.2",
        messages=conversation
    )
    
    reply = response.message.content
    conversation.append({"role": "assistant", "content": reply})
    
    print(f"AI: {reply}\n")
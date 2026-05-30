from groq import Groq

client = Groq(api_key="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")

conversation = [{"role": "system", "content": "You are a helpful assistant who replies pretending to be a superhero"}]

print("Chatbot ready! Type 'quit' to exit")

while True:
    user_input = input("You: ")
    
    if user_input == "quit":
        break
    
    conversation.append({"role": "assistant", "content": user_input})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation
    )
    
    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})
    
    print(f"AI: {reply}\n")
import ollama
from ddgs import DDGS

def search_web(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
    return "\n".join([r['body'] for r in results])
def run_agent(user_goal):
    print(f"\nAgent working on: {user_goal}\n")
    
    search_prompt = f"""Given this user request: {user_goal}

Write a short web search query (3-5 words) to find relevant information.
Reply with ONLY the search query, no explanation, no quotes."""
    

    
    search_query_response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": search_prompt}]
    )
    
    search_query = search_query_response.message.content.strip()
    print(f"Searching for: {search_query}")
    
    search_results = search_web(search_query)
    print(f"Found information, generating response...\n")

    
    
    final_prompt = f"""User goal: {user_goal}

Information found from web search:
{search_results}

Now help the user achieve their goal using this information."""

    final_response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": final_prompt}]
    )
    
    return final_response.message.content

print("AI Agent ready!")
print("Type 'quit' to exit\n")

while True:
    goal = input("What do you want me to do? ")
    if goal == "quit":
        break
    result = run_agent(goal)
    print(f"\nAgent: {result}\n")
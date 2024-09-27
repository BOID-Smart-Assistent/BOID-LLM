from rag_crawler import query
from openai import OpenAI
import json

# Load the config file
def load_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config
config = load_config('config.json')
# Define colors for printing
green_color = "\033[92m"
reset_color = "\033[0m"
blue_color = "\033[94m"

def llm_processor( question):
     
    # Point to the LLM local server
    client = OpenAI(base_url=config['llm-api-helper']['base_url'], api_key=config['llm-api-helper']['api_key'])

    completion = client.chat.completions.create(
    model=config['llm-api-helper']['model'],
    messages=[
        {"role": "system", "content": "Help to give the best answer based on user input"},
        {"role": "user", "content": f"context:{query(question)} \n question: {question}"}
    ],
    temperature=0.2,
    )

    answer = completion.choices[0].message.content.strip()
    
        
    return f"AI Helper response> {answer}"




question=input(f"{blue_color}Type your question > ").strip()
print(f"RAG Result as the context: \n{query(question)}")
print(llm_processor(question))


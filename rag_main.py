import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# importing all key information from Foundry, will not work on your machine, 
# unless you connect it to a model deployment and add all this information to a .env file, so dont worry about it
# if you're interested in doing so let me know I can help you
endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
client = OpenAI(
  api_key=os.environ['AZURE_OPENAI_API_KEY'],
  base_url=f"{endpoint.rstrip('/')}/openai/v1/",
  )

model = os.environ['AZURE_OPENAI_DEPLOYMENT']

# This is the main RAG function of the program, implements keyword search from a local file
# is not the corporate definition of rag but keyword search is a completely valid for
def search_local_data(prompt):
    context = []
    with open("07-building-chat-applications/python/f1_data.txt") as file:
        for line in file:
            words = prompt.lower().split()
            for word in words:
                if len(word) > 2:
                    if word in line.lower():
                        context.append(line.strip())
                        break
    return "\n".join(context)

print("Chatbot active, type 'quit' to exit\n")

# exit if quit by user
while True:
    prompt = input("Your Prompt: ")
    if prompt.lower() == "quit":
        break
    
    local_context = search_local_data(prompt)

    system_instructions = "You are an strict Formula 1 assistant. You must only answer the user's question " \
    "using the data and information provided in the 'Verified Local Data section below. If the answer cannot be found " \
    "entirely using the data given, answer simply with 'Answer cannot be found using local data.'"

# prompting model with prompt and instructions, getting response and printing it out
    if local_context:
        system_instructions += local_context
    response = client.responses.create(
        model=model,
        input = [{"role":"system", "content":system_instructions},
               {"role":"user","content":prompt},],
        store=False,)        
    print(f"AI: {response.output_text}\n")
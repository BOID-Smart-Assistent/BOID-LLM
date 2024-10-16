from openai import OpenAI
import json
import datetime
# from llm_helper import llm_processor
import os
# from unstructured_pdf_extractor import prep_knowledege
# from table_pdf_extractor import process_pdfs_in_path
# from rag_crawler import query
from datetime import datetime
now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")
# Load the config file
def load_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config
config = load_config('config.json')


# Point to the local server DATA COLLECTOR
client_collector = OpenAI(base_url=config['llm-api-collector']['base_url'], api_key=config['llm-api-collector']['api_key'])

# LLM input 
# Load the user_profile.json, schedule.json, and rules_example.txt files
with open('./data/context/schedule.json', 'r') as file:
    schedule = file.read()
with open('./data/context/boid_case_sample.txt', 'r') as file:
    boid_case = file.read()
with open('./data/context/boid_output_sample.txt', 'r') as file:
    boid_output = file.read()
user_profile=load_config('./data/context/user_profile.json')

# # Uncomment this when running the script for the first time
# # Add all table based data into database
# process_pdfs_in_path( './data/knowledge/table_based')
# # Add all text based data into database
# prep_knowledege()

print("the model used for this program is: ", config['llm-api-collector']['model'])

# def getObligation(existing_obligations=obligations):
#     new_obligations=""
#     zs_obligation = [   
#         {"role": "system", "content": "You are an assistant that want to collect obligations from user. Be concise."}, 
#         {"role": "user", "content": "Tell that this is the existing obligations: "+existing_obligations+". Ask the user if there are any other obligations. Be concise.Use this format ''' 'OBLIGATION': <insert obligation keywords> ''' to summarize the obligations at the end of the conversation when user confirm that no obligation added. No additional word beside the requested format. "},
#         ]
#     while True:
#         completion = client_collector.chat.completions.create(
#             model=config['llm-api-collector']['model'],
#             messages=zs_obligation,
#             temperature=0.1,
#             stream=True,
#         )
#         new_message = {"role": "assistant", "content": ""}
        
#         for chunk in completion:
#             if chunk.choices[0].delta.content:
#                 print(chunk.choices[0].delta.content, end="", flush=True)
#                 new_message["content"] += chunk.choices[0].delta.content
#         print()
#         user_input=input("> ")
#         zs_obligation.append({"role": "user", "content":user_input })
#         if 'OBLIGATION' in new_message['content']:
#             new_obligations=new_message['content']
#             break
#     return new_obligations
def getDesire(user_input=None,debug=False):
    desires=""
    cot_desire = [   
        {"role": "system", "content": "You are an assistant that convert only like topics into desired topics."}, 
        {"role": "user", "content": f"Convert following input --> like: quantum, ethics ; dislike: robotics, education \n reference: {schedule} become this format --> DESIRES: <insert title>. Output only the requested format and exact title from reference that match with 'like' keywords."},
        {"role": "assistant", "content": "DESIRES: Quantum Computing Basics,Quantum Cryptography, Quantum Machine Learning, Quantum Algorithms, Data Ethics in AI, AI and Society"},
        # {"role": "user", "content": f"Now convert these keywords {input('like and dislike keywords:')} into desires."},
        ]
    if debug==True:
        cot_desire.append({"role": "user", "content": f"Now convert these keywords {input('like and dislike keywords:')} into desires."})
    else:
        cot_desire.append({"role": "user", "content": f"Now convert these keywords {user_input} into desires."})
        
    completion = client_collector.chat.completions.create(
        model=config['llm-api-collector']['model'],
        messages=cot_desire,
        temperature=0.1,
        stream=True,
    )
    new_message = {"role": "assistant", "content": ""}
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content
    print()
    logging(new_message['content'])
    if 'DESIRES' in new_message['content']:
        desires=new_message['content'].split(': ')[1]
    else:
        user_input=input("> ")
        cot_desire.append({"role": "user", "content":user_input })
            
    return desires
def generateUserContext(obligations,desires, schedule):
    user_context="The user's obligations are: "+obligations+". The user's desires are: "+desires+". Based on the schedule, the participant believe that the schedule are this following \n "+schedule
    logging('USER_CONTEXT:'+'\n'+user_context+'\n')
    return user_context
def boidGenerator(input,boid_case=boid_case,boid_output=boid_output):
    print("Generating BOID Logic...")  
    ## Few Shot Prompt to give context for BOID Logic
    fsl_boid=[
    {"role": "system", "content": "Forget about previous BOID LOGIC generation. Answer in a consistent style"},
    {"role": "user", "content": "Convert the following USER_CONTEXT into BOID LOGIC: \n"+boid_case},
    {"role": "assistant", "content": boid_output},
    {"role": "user", "content": input+"\n"}
    ]
    completion = client_collector.chat.completions.create(
        model=config['llm-api-collector']['model'],
        messages=fsl_boid,
        temperature=0.1,
        stream=True,
    )
    new_message = {"role": "assistant", "content": ""}
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content
    logging(new_message['content'])
    return new_message
# create function to write strings to a file called chat_hsitory_timestamp.txt
def logging(string):
    with open('./history_log/chat_history_'+timestamp+'.txt', 'a') as file:
        file.write(string+'\n')
def process_input(input_string):
    obligations=user_profile['participant']['obligations']
    logging('OBLIGATION:'+obligations)
    if len(obligations)==0:
        return "Please add at least one obligation"
    else:
        desires=getDesire(user_input=input_string)
        if len(desires)==0:
            return "Please add at least one desire"
        else:
            user_context=generateUserContext(obligations,desires, schedule) 
            if len(user_context)==0:
                return "Please add at least one user context"
            else:
                oneLine_user_context=user_context.replace("\n","")
                response=boidGenerator(oneLine_user_context)
    return response['content']

if __name__ == "__main__":
    # boidGenerator()
    obligations=user_profile['participant']['obligations']
    logging('OBLIGATION:'+obligations)
    if len(obligations)==0:
        print("Please add at least one obligation")
    else:
        desires=getDesire(debug=True)
        if len(desires)==0:
            print("Please add at least one desire")
        else:
            user_context=generateUserContext(obligations,desires, schedule) 
            print("These are the user context:\n",user_context)
            if len(user_context)==0:
                print("Please add at least one user context")
            else:
                oneLine_user_context=user_context.replace("\n","")
                # print(f"This is the input for the boid generator: \n {oneLine_user_context}")
                boidGenerator(oneLine_user_context)
            




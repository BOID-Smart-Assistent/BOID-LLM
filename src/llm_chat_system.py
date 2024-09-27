from openai import OpenAI
import json
import datetime
# from llm_helper import llm_processor
import os
from unstructured_pdf_extractor import prep_knowledege
from table_pdf_extractor import process_pdfs_in_path
from rag_crawler import query


# Load the config file
def load_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config
config = load_config('config.json')

# For log purpose
timestamp = datetime.datetime.now().timestamp()

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

obligations=user_profile['participant']['obligations']
def getObligation(existing_obligations=obligations):
    new_obligations=""
    zs_obligation = [   
        {"role": "system", "content": "You are an assistant that want to collect obligations from user. Be concise."}, 
        {"role": "user", "content": "Tell that this is the existing obligations: "+existing_obligations+". Ask the user if there are any other obligations. Be concise.Use this format ''' 'OBLIGATION': <insert obligation keywords> ''' to summarize the obligations at the end of the conversation when user confirm that no obligation added. No additional word beside the requested format. "},
        ]
    while True:
        completion = client_collector.chat.completions.create(
            model=config['llm-api-collector']['model'],
            messages=zs_obligation,
            temperature=0.1,
            stream=True,
        )
        new_message = {"role": "assistant", "content": ""}
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
                new_message["content"] += chunk.choices[0].delta.content
        print()
        user_input=input("> ")
        zs_obligation.append({"role": "user", "content":user_input })
        if 'OBLIGATION' in new_message['content']:
            new_obligations=new_message['content']
            break
    return new_obligations
def getDesire():
    desires=""
    cot_desire = [   
        {"role": "system", "content": "You are an assistant that want to collect desire or interest from user. Be concise."}, 
        {"role": "user", "content": f"Do it step by step and do not repeat yourself. \
            1.Ask the user their desire about the conference topics not the timeslot, start with day 1 until end of days from the reference. \
            2.Use this reference: {schedule}. Then suggest topics for each day.Be concise and precise following the reference. \
            3.Use this format to summary each day before continue to next day ''' <insert numbering> <insert day here>: <insert topics here> ''' \
            4.Use this format ''' 'DESIRES': <insert desires keywords> ''' to summarize the desires at the end of the conversation when user confirm that no desires added. No additional word beside the requested format start with DESIRES. "},
        ]
    while True:
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
        user_input=input("> ")
        cot_desire.append({"role": "user", "content":user_input })
        if 'DESIRES' in new_message['content']:
            desires=new_message['content']
            break
    return desires
def generateUserContext(obligations,desires, schedule):
    user_context="The user's obligations are: "+obligations+". The user's desires are: "+desires+". Based on the schedule, the participant believe that the schedule are this following \n "+schedule
    return user_context
def boidGenerator(boid_case=boid_case,boid_output=boid_output):
    ## Few Shot Prompt to give context for BOID Logic
    fsl_boid=[
    {"role": "system", "content": "Answer in a consistent style"},
    {"role": "user", "content": "Convert the following USER_CONTEXT into BOID LOGIC: \n"+boid_case},
    {"role": "assistant", "content": boid_output},
    {"role": "user", "content": input("> ")+"\n"}
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
    return new_message


if __name__ == "__main__":
    obligations=getObligation()
    if len(obligations)==0:
        print("Please add at least one obligation")
    else:
        desires=getDesire()
        if len(desires)==0:
            print("Please add at least one desire")
        else:
            user_context=generateUserContext(obligations,desires, schedule) 
            print("These are the user context:\n",user_context)
            boidGenerator(user_context)
            




from flask import Flask, request, jsonify
import llm_chat_system
from dotenv import load_dotenv
import os
# Load .env file
load_dotenv()

app = Flask('llmboidapi')

@app.route('/userid/<userid>', methods=['GET'])
def chat(userid):
    try:
        response = llm_chat_system.process_input(userid=userid)
    except:
        response = 'ERROR: Please activate the LM studio and select the model'
    return jsonify({'response': response})

if __name__ == '__main__':
    print('Running module:{__name__}')
    app.run(host=os.getenv("UTIL_IP"),port=os.getenv("UTIL_PORT"))
    
    
## from local gitbash: curl -X GET  http://localhost:80/userid/<userid>
## from local browser: http://localhost:80/userid/<userid>
## from public browser: http://publicip:80/userid/<userid>
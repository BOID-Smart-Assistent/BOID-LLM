from flask import Flask, request, jsonify
import llm_chat_system

app = Flask('llmboidapi')

@app.route('/userid/<userid>', methods=['GET'])
def chat(userid):
    try:
        response = llm_chat_system.process_input(online=True, userid=userid)
    except:
        response = 'ERROR: Please activate the LM studio and select the model'
    return jsonify({'response': response})

if __name__ == '__main__':
    print('Running module:{__name__}')
    app.run(host="0.0.0.0",port=80)
    
## from gitbash: curl -X POST -H "Content-Type: application/json" -d '{"input": "input: quantum"}' http://localhost:80/chat
## from browser: http://localhost:80/chat?input='quantum'
from flask import Flask, request, jsonify
import llm_chat_system

app = Flask('llmboidapi')

@app.route('/chat', methods=['GET','POST'])
def chat():
    if request.method == 'POST':
        user_input = request.json.get('input')
    elif request.method == 'GET':
        # Retrieve input from query parameter for GET requests
        user_input = request.args.get('input')
    try:
        response = llm_chat_system.process_input(user_input)
    except:
        response='ERROR: Please activate the LM studio and select the model'
    return jsonify({'response': response})

if __name__ == '__main__':
    print('Running module:{__name__}')
    app.run(host="0.0.0.0",port=80)
    
## from gitbash: curl -X POST -H "Content-Type: application/json" -d '{"input": "input: quantum"}' http://localhost:80/chat
## from browser: http://localhost:80/chat?input='quantum'
from flask import Flask, request, jsonify
import llm_chat_system

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('input')
    response = llm_chat_system.process_input(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run()
    
## from gitbash: curl -X POST -H "Content-Type: application/json" -d '{"input": "input: quantum"}' http://localhost:5000/chat
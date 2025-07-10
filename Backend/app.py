from flask import Flask, jsonify, request
from flask_cors import CORS
from database import *
from query_openrouter import query_openrouter

app = Flask(__name__)
CORS(app)

models = [
    'deepseek/deepseek-chat-v3-0324:free',
    'google/gemini-2.0-flash-exp:free',
    'deepseek/deepseek-r1-0528-qwen3-8b:free',
    'openrouter/cypher-alpha:free',
    'deepseek/deepseek-r1-0528:free',
    'qwen/qwen3-32b:free',
    'google/gemma-3-27b-it:free',
    'qwen/qwq-32b:free',
    'deepseek/deepseek-r1:free',
    'mistralai/mistral-nemo:free',
]
active_model = models[2]

# Работа с чатами
@app.route('/api/chats', methods=['GET'])
def get_dialogs():
    return jsonify(dialog_list_request(dict_return=True))

@app.route('/api/chats', methods=['POST'])
def add_chat():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Название чата не введено"})
    id = add_new_dialog(data['chat_name'])
    return jsonify({'chat': {'id': id,'title': data['chat_name']}})


@app.route('/api/chats/<int:id>', methods=['DELETE'])
def delete_chat(id):
    remove_dialog(id)
    return jsonify({"message": "Чат удалено"})

@app.route('/api/chats/<int:id>', methods=['PUT'])  
def edit_chat_name(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Изменённое имя не введено"})
    if 'content' in data:
        edit_dialog_name(id, data['content'])
        return jsonify({"message": "Имя чата отредактировано"})
    else: return jsonify({"message": "Не вижу 'content'"})

# Работа с сообщениями
@app.route('/api/messages/<int:chat_id>', methods=['GET'])
def get_messages(chat_id):
    return jsonify(message_list_request(chat_id, dict_return=True))

@app.route('/api/messages', methods=['POST'])
def add_message():

    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Название сообщение не введено"})
    
    if data['sender']:
        id = message_insert(data['chat_id'], data['sender'], data['content'])
        return jsonify({'message': {'id': id,'content': data['content'], 'sender': 'user', 'conversation_id': data['chat_id']}})
    
    else:
        ai_answer = query_openrouter(data['content'],active_model)
        id = message_insert(data['chat_id'], False, ai_answer)
        return jsonify({'message': {'id': id,'content': ai_answer, 'sender': 'ai', 'conversation_id': data['chat_id']}})


@app.route('/api/messages/<int:id>', methods=['DELETE'])  
def delete_message(id):
    message_delete(id)
    return jsonify({"message": "Сообщение удалено"})

@app.route('/api/messages/<int:id>', methods=['PUT'])  
def edit_message(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Изменённое сообщение не введено"})
    if 'content' in data:
        edit_message_request(id, data['content'])
        return jsonify({"message": "Сообщение отредактировано"})
    else: return jsonify({"message": "Не вижу 'content'"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
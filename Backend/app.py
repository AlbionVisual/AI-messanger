from flask import Flask, jsonify, request
from flask_cors import CORS
from database import *
from query_openrouter import query_openrouter

app = Flask(__name__)
CORS(app)

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


@app.route('/api/chats/<int:id>', methods=['DELETE'])  #Новый маршрут DELETE /api/chats/<int:id> принимает id чата как параметр URL.
def delete_chat(id):
    remove_dialog(id)
    return jsonify({"message": "Чат удалено"})


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
        id = message_insert(data['chat_id'], data['sender'], data['text'])
        return jsonify({'message': {'id': id,'content': data['text'], 'sender': True, 'conversation_id': data['chat_id']}})
    
    else:
        ai_answer = query_openrouter(data['text'])
        id = message_insert(data['chat_id'], False, ai_answer)
        return jsonify({'message': {'id': id,'content': ai_answer, 'sender': False, 'conversation_id': data['chat_id']}})


@app.route('/api/messages/<int:id>', methods=['DELETE'])  
def delete_message(id):
    message_delete(id)
    return jsonify({"message": "Сообщение удалено"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
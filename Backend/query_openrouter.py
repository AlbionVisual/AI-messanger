import requests
import json
from dotenv import load_dotenv
import os

def query_openrouter(message, model_type = 'deepseek/deepseek-r1-0528-qwen3-8b:free'):

    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')

    if not openai_api_key:
        print("not found api key in env file")
        return

    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f'Bearer {openai_api_key}',
        "Content-Type": "application/json",
        "HTTP-Referer": "", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "", # Optional. Site title for rankings on openrouter.ai.
    },
    data=json.dumps({
        "model": model_type,
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": message
            },
            {
                "type": "image_url",
                "image_url": {
                "url": ""
                }
            }
            ]
        }
        ],
        
    })
    )
    return response.content

if __name__ == "__main__":
    with open("output.txt","w") as file:
        resp = query_openrouter("Привет! Как дела? Мне нужно проверить запрос по API ключу, надеюсь ты не против?\n\nЕсли тебе скучно можешь ответить на вопрос: что возвращает requests.Post, как получить ответ и какой он будет?")
        unicode_string = resp.decode('utf-8')
        parsed_data = json.loads(unicode_string)

        print(parsed_data['choices'][0]['message']['content'])
        if resp:
            file.write(str(parsed_data['choices'][0]['message']['content']))
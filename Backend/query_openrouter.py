import requests
import json
from dotenv import load_dotenv
import os

def query_openrouter(message : str, model_type = 'deepseek/deepseek-r1-0528-qwen3-8b:free') -> str:
    """
    @brief Делает запрос в openrouter
    @param message строка для отправке в API Openrouter
    @param model_type необязательный параметр определяющий id LLM-ки
    @returns ответ нейронной сети, либо структура ошибки
    """

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
    unicode_string = response.content.decode('utf-8')
    parsed_data = json.loads(unicode_string)
    if parsed_data and parsed_data['choices'] and parsed_data['choices'][0] and parsed_data['choices'][0]['message']:
        return parsed_data['choices'][0]['message']['content']
    else:
        return parsed_data

if __name__ == "__main__":
    resp = query_openrouter("Привет! Как дела? Мне нужно проверить запрос по API ключу, надеюсь ты не против?\n\nЕсли тебе скучно можешь ответить на вопрос: что возвращает requests.Post, как получить ответ и какой он будет?")
    print(resp)
### Query open router cheetsheet

Для использования импортировать функцию:

```python
from query_openrouter.py import query_openrouter
```

А также в файл .env вставить рабочий API ключ: `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`

Входные аргументы:

```python
def query_openrouter(message : str, model_type = 'deepseek/deepseek-r1-0528-qwen3-8b:free') -> str
```

`message` - строка-сообщение для отправки в API Openrouter
`model_type` - необязательный параметр определяющий id LLM-ки для использования в запросе (по умолчанию используется deepseek)

Использование:

```python
from query_openrouter import query_openrouter
print(query_openrouter("Как работает fetch в Javascript и как он связывается с бэкендом?"))
```

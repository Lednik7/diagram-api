# Diagram API

Simple API for creating architecture diagrams through natural language using LLM.

## Features

- FastAPI for async API
- OpenRouter LLM API integration (Claude 3.5 Sonnet)
- LLM agent with tools for diagrams package
- Gradio assistant web interface
- Supports 45+ components (AWS, GCP, Azure)
- Assistant with context and memory
- Docker containerization
- Stateless architecture

## Установка

1. Установите UV:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Склонируйте проект:
```bash
git clone <repo-url>
cd diagram-api
```

3. Настройте окружение:
```bash
cp .env.example .env
# Добавьте ваш OPENROUTER_API_KEY в .env
```

4. Установите зависимости:
```bash
uv sync
```

5. Запустите API сервер:
```bash
uv run python main.py
```

API доступен на http://localhost:8000

6. Запустите веб-интерфейс ассистента (опционально):
```bash
# В новом терминале
uv run python gradio_app.py
```

Веб-интерфейс доступен на http://localhost:7860

## Docker

```bash
# Настройте .env с вашим API ключом
docker-compose up --build
```

## API

### POST /generate-diagram

Создает диаграмму из текстового описания.

**Запрос:**
```json
{
  "description": "Create a web application with load balancer and database"
}
```

**Ответ:**
```json
{
  "image_data": "base64_encoded_png_image",
  "message": "Diagram generated successfully"
}
```

### Другие endpoints

- `GET /` - Информация о сервисе
- `GET /health` - Проверка работоспособности
- `GET /docs` - Swagger документация

## Пример использования

### Веб-интерфейс (рекомендуется)
1. Запустите API сервер: `uv run python main.py`
2. Запустите веб-интерфейс: `uv run python gradio_app.py`
3. Откройте http://localhost:7860
4. Общайтесь с ассистентом в чате или генерируйте диаграммы напрямую

### API напрямую
```python
import requests

response = requests.post(
    "http://localhost:8000/generate-diagram",
    json={"description": "Web app with load balancer, servers and database"}
)

image_data = response.json()["image_data"]
# Декодируйте base64 и сохраните PNG
```

### Ассистент API
```python
response = requests.post(
    "http://localhost:8000/assistant",
    json={"message": "Create a microservices architecture"}
)

data = response.json()
print(data["response"])  # Ответ ассистента
if data.get("image_data"):  # Диаграмма сгенерирована
    # Обработать изображение
```

## Требования

- Python 3.11+
- OpenRouter API ключ
- Graphviz (для диаграмм)

## Ограничения

- Создает фиксированную 3-tier архитектуру
- Только AWS компоненты
- LLM используется только для генерации заголовка
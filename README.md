# RAG Documentation Assistant

RAG-система для ответов на технические вопросы по документации Docker, FastAPI и scikit-learn.  
Ассистент ищет релевантные фрагменты в индексированной документации и генерирует ответ с указанием источников.
---

## Возможности

- Ответы на how-to вопросы по трём популярным инструментам DevOps/Python
- Поиск по 20+ страницам документации с помощью FAISS и эмбеддингов
- Генерация ответов через DeepSeek (или любой OpenAI-совместимый API) с системным промптом
- Веб-интерфейс на Streamlit с отображением источников
- Готовый Docker Compose для быстрого развёртывания
- Метрика Recall@3 ≥ 0.76 на тестовых вопросах

---

## Технологический стек

| Компонент        | Технология                               |
|------------------|------------------------------------------|
| Поиск            | FAISS (IndexFlatIP)                      |
| Эмбеддинги       | sentence-transformers / all-mpnet-base-v2 |
| Генерация ответа | DeepSeek API (OpenAI-совместимый)        |
| API              | FastAPI + Uvicorn                        |
| Интерфейс        | Streamlit                                |
| Контейнеризация  | Docker + Docker Compose                  |
| Тестирование     | pytest                                   |

---

## Запуск с Docker Compose

1. Убедитесь, что у вас установлен Docker Desktop и запущен.

2. Клонируйте репозиторий и перейдите в его корень:

   git clone <your-repo-url>
   cd rag-devops-docs-bot

3. Соберите и запустите оба сервиса:

   docker-compose up --build

4. Дождитесь загрузки модели эмбеддингов (это может занять 30–60 секунд).  
   После запуска будут доступны:

   | Сервис     | Адрес                          |
   |------------|--------------------------------|
   | UI         | http://localhost:8501          |
   | API        | http://localhost:8000          |
   | Swagger UI | http://localhost:8000/docs     |

5. Откройте http://localhost:8501 в браузере и задайте вопрос (на английском, например, "How to create a pipeline in sklearn?").

---

## Запуск тестов

Тесты можно выполнить двумя способами:

### Локально (требуется установленный faiss-cpu)

pip install -r requirements.txt
python -m pytest tests/

### Внутри контейнера API

docker exec -it rag-devops-docs-bot-api-1 pytest tests/

---

## Структура проекта

├── app/
│   ├── main.py          # FastAPI приложение
│   ├── models.py        # Pydantic схемы
│   └── utils.py         # загрузка индекса, search, ask
├── data/docs/           # индексируемые документы
├── ui/
│   └── app.py           # Streamlit интерфейс
├── tests/
│   └── test_api.py      # 8 тестов для API
├── faiss_index.bin      # предварительно построенный индекс FAISS
├── faiss_meta.pkl       # метаданные чанков
├── Dockerfile.api       # сборка API
├── Dockerfile.ui        # сборка UI
├── docker-compose.yml   # оркестрация
├── requirements.txt     # зависимости
└── README.md

---

## Конфигурация

- API-ключ DeepSeek уже встроен в `app/utils.py`. При необходимости замените его там же.
- Для использования другой LLM измените `base_url` и `LLM_MODEL` в `utils.py`.

---

## Результаты качества

- Recall@1 = 0.571  
- Recall@3 = 0.762 (целевое значение ≥ 0.65)  
- Recall@5 = 0.905  

---

## Лицензия

Проект создан в рамках учебного курса «AI/ML-engineering» и предназначен для демонстрационных целей.

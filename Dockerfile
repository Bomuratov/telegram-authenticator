# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем проект FastAPI
COPY . .
# Открываем порт для FastAPI
EXPOSE 8000

# Запускаем сервер через Uvicorn
# Добавить  для запуска воркеров
# CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "main:fapp", "--bind", "0.0.0.0:8001", "--timeout", "120"]

CMD ["uvicorn", "main:fapp", "--host", "0.0.0.0", "--port", "8000", "--reload"]


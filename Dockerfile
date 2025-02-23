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
EXPOSE 8001

# Запускаем сервер через Uvicorn
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "main:fapp", "--bind", "0.0.0.0:8001", "--timeout", "120"]




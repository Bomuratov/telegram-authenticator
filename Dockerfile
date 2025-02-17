# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY telegram-authenticator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект FastAPI
COPY telegram-authenticator /app

# Открываем порт для FastAPI
EXPOSE 8001

# Запускаем сервер через Uvicorn
CMD ["uvicorn", "main:fapp", "--host", "0.0.0.0", "--port", "8001"]

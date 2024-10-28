## Этот проект разработан для отправки кодов верификации

## Установка и развертывание

### Создание виртуального окружения

#### Для развертывания вам надо создать виртуалный окружение c помощью комманды

**macOS / Linux:**
```python3 -m venv venv```

**Windows:**
`bash` python -m venv venv

**Активироватть его:**

**macOs / Linux**
```bash source venv/bin/activate ```

**Windows**
```bash venv/script/activate ```

**Установить пакетный менеджер Poetry:**
```bash pip install poetry ```

**Установить все необходимые библиотеки с коммандой:**

```bash poetry install ```


**Coздать переменный окружение .env добавить туда переменные переменные должны начинатся с заглавный буквой SET**

SET-BOT-TOKEN=ТУТ ТОКЕН ВАШЕГО ТЕЛЕГРАМ БОТА
SET-BOT-WEBHOOK_PATH=УКАЖИТЕ /bot/
SET-BOT-WEBHOOK_URL=ТУТ ВАШ СЕРВЕР КОТОРЫЙ ИМЕЕТ SSL СЕРТИФИКАТ
SET-DB-URL=ТУТ URL POTSGRESQL

**Запустить миграции баз данных с коммандой**

```bash alembic revision --autogenerate -m "first commit" ```

```bash alembic upgrade head```

**Запустить сервер**

```bash uvicorn main:app --reload --host УКАЖИТЕ HOST --port УКАЖИТЕ PORT```
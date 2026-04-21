# import requests

# headers = {
#         'Content-Type': 'application/json',
#     }
# def send_code(url, user_id, data):
#     data={
#         "user_id": user_id,
#         "data": data
#     }
#     try:
#         response = requests.post(url, json=data, headers=headers)
#         response.raise_for_status()
#         return response.json()

#     except requests.exceptions.RequestException as e:
#         print(f'Произошла ошибка: {e}')
#         print(f'Статус: {response.status_code}, Тело ответа: {response.text}')
#         return None

# print(send_code(url="https://api.aurora-api.uz/fastapi/send_code/", user_id="998881836222", data="123456"))


# # worker_processes 1;

# # events {
# #     worker_connections 1024;
# # }

# # http {
# #     include /etc/nginx/mime.types;
# #     default_type application/octet-stream;

# #     sendfile on;
# #     tcp_nopush on;
# #     tcp_nodelay on;
# #     keepalive_timeout 65;

# #     upstream django {
# #         server aurora-backend:8000;  # Имя сервиса из docker-compose
# #     }

# #     upstream fast {
# #         server aurora-backend:8000;  # Имя сервиса из docker-compose
# #     }

# #     server {
# #         listen 80;
# #         server_name api.aurora-api.uz;

# #         # Для certbot
# #         location /.well-known/acme-challenge/ {
# #             root /var/www/certbot;
# #         }

# #         # Перенаправление на HTTPS
# #         location / {
# #             return 301 https://$host$request_uri;
# #         }
# #     }

# #     server {
# #         listen 443 ssl;
# #         server_name api.aurora-api.uz;

# #         # Путь к сертификатам, которые будут созданы Certbot
# #         ssl_certificate /etc/letsencrypt/live/api.aurora-api.uz/fullchain.pem;
# #         ssl_certificate_key /etc/letsencrypt/live/api.aurora-api.uz/privkey.pem;
# #         ssl_protocols TLSv1.2 TLSv1.3;
# #         ssl_ciphers 'HIGH:!aNULL:!MD5';
# #         ssl_prefer_server_ciphers on;

# #         location / {
# #             proxy_pass http://django;
# #             proxy_set_header Host $host;
# #             proxy_set_header X-Real-IP $remote_addr;
# #             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
# #             proxy_set_header X-Forwarded-Proto $scheme;
# #         }

# #         location /fast {
# #             proxy_pass http://fastapi;
# #             proxy_set_header Host $host;
# #             proxy_set_header X-Real-IP $remote_addr;
# #             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
# #             proxy_set_header X-Forwarded-Proto $scheme;
# #         }
# #     }
# # }

DATABASE = {
    "dbname": "aurora",
    "user": "aurora",
    "password": "admin",
    "host": "127.0.0.1",
    "port": "5432",
}

import psycopg2
from config import settings


def get_chat_id_by_phone(phone: str):
    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()

    # Чистый SQL-запрос
    sql = "SELECT email FROM authentication_usermodel WHERE username = %s;"
    cur.execute(sql, (phone,))  # Передача параметра безопасным способом

    result = cur.fetchone()  # Получаем первую строку
    cur.close()
    conn.close()

    return result[0] if result else None  # Возвращаем chat_id или None


print(get_chat_id_by_phone(phone="test"))



{
    "created_by": "Умид Бомуротов",
    "products": [
        {
            "id": 18,
            "name": "Цезарь",
            "photo": "https://new.aurora-api.uz/media/Olivia/category/%D0%A1%D0%B0%D0%BB%D0%B0%D1%82%D1%8B/%D0%A6%D0%B5%D0%B7%D0%B0%D1%80%D1%8C_nPgQyvn.jpeg",
            "price": 2000,
            "discount": True,
            "quantity": 1,
        }
    ],
    "total_price": 7000,
    "lat": "39.7470289",
    "long": "64.4022198",
    "user_id": 1,
    "user_phone_number": "+998881836222",
    "orders_chat_id": "-1002641409178",
    "restaurant": {
        "id": 3,
        "name": "Olivia",
        "photo": "https://new.aurora-api.uz/media/Olivia/logo/0889x24izl.webp",
        "address": "Гор Газ (София)",
        "phone": "не указан",
        "lat": "39.763550",
        "long": "64.430128",
    },
    "location": {
        "id": 460,
        "country_ru": "Узбекистан",
        "country_en": "Uzbekistan",
        "state_ru": "Бухарская область",
        "state_en": "Bukhara Region",
        "city_ru": "Бухара",
        "city_en": "Bukhara",
        "county_ru": None,
        "county_en": None,
        "key_zone": "UZ-BU",
        "lat": "39.765387861294485",
        "long": "64.43027615547182",
        "address": "Мустакиллик улица 16",
        "street": None,
        "name": "Sofia Olivia adress",
        "house": None,
        "apartment": "",
        "floor": "",
        "entrance": "",
        "comment": "",
        "is_active": True,
        "delivery_zone": "Bukhara",
        "is_deliverable": True,
        "user": 1,
    },
    "status": "new",
    "destination": {"distance": "1.1 km", "duration": "4 mins"},
    "delivery_price": 0,
    "comment": "",
    "order_coast": "2000",
    "payment_type": "cash",
    "discount_items": [
        {
            "id": 18,
            "name": "Цезарь",
            "photo": "https://new.aurora-api.uz/media/Olivia/category/%D0%A1%D0%B0%D0%BB%D0%B0%D1%82%D1%8B/%D0%A6%D0%B5%D0%B7%D0%B0%D1%80%D1%8C_nPgQyvn.jpeg",
            "quantity": 1,
            "price": 0,
            "originalPrice": 2000,
        }
    ],
    "courier": None,
    "fee": 5000,
    "preparation_time": None,
    "check_info": None,
    "total_profit": None,
    "id": 1946,
    "created_at": "2026-04-21T04:44:48.617Z",
    "updated_at": "2026-04-21T04:44:48.617Z",
    "payment_status": "pending",
    "reviewStatus": "none",
}

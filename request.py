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
    "created_by": "null null",
    "products": [
        {
            "id": 5,
            "name": "Биф Бургер",
            "price": 45000,
            "photo": "https://stage.aurora-api.uz/media/Olivia/category/%D0%91%D1%83%D1%80%D0%B3%D0%B5%D1%80/%D0%91%D0%B8%D1%84_%D0%91%D1%83%D1%80%D0%B3%D0%B5%D1%80.jpg",
            "options": {
                "id": 112,
                "name": "Маленкий",
                "price": 45000,
                "is_active": true
            },
            "quantity": 1
        },
        {
            "id": 6,
            "photo": "https://stage.aurora-api.uz/media/Olivia/category/%D0%91%D1%83%D1%80%D0%B3%D0%B5%D1%80/%D0%A7%D0%B8%D0%B7%D0%B1%D1%83%D1%80%D0%B3%D0%B5%D1%80.jpg",
            "name": "Чизбургер",
            "price": 55000,
            "quantity": 1
        }
    ],
    "total_price": 109000,
    "lat": "39.748301953098725",
    "long": "64.41681353066139",
    "user_id": 79,
    "user_phone_number": "+998991112233",
    "orders_chat_id": -1002641409178,
    "restaurant": {
        "id": 3,
        "name": "Olivia",
        "address": "Chevar",
        "photo": "https://stage.aurora-api.uz/media/Olivia/logo/0889x24izl.webp",
        "phone": "не указан",
        "lat": "39.770515",
        "long": "64.445063"
    },
    "location": {
        "id": 213,
        "country_ru": "Узбекистан",
        "country_en": "Uzbekistan",
        "state_ru": "Бухарская область",
        "state_en": "Bukhara Region",
        "city_ru": "Бухара",
        "city_en": "Bukhara",
        "county_ru": null,
        "county_en": null,
        "key_zone": "UZ-BU",
        "lat": "39.748301953098725",
        "long": "64.41681353066139",
        "address": "Пиридастгир улица, 5Б микрорайон",
        "street": null,
        "name": "Бухара",
        "house": null,
        "apartment": "",
        "floor": "",
        "entrance": "",
        "comment": "",
        "is_active": true,
        "delivery_zone": "Bukhara",
        "is_deliverable": false,
        "user": 79
    },
    "status": "new",
    "destination": {
        "distance": "4.2 km",
        "duration": "11 mins"
    },
    "delivery_price": 4000,
    "comment": "",
    "courier": null,
    "fee": 5000,
    "preparation_time": null,
    "check_info": null,
    "total_profit": null,
    "order_coast": null,
    "id": 1233,
    "created_at": "2026-04-20T03:37:08.308Z",
    "updated_at": "2026-04-20T03:37:08.308Z",
    "payment_type": "card",
    "reviewStatus": "none"
}
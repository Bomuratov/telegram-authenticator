# import requests

# headers = {
#         'Content-Type': 'application/json',
#     }
# def send_code(url, phone, code):
#     data={
#         "phone": phone,
#         "code": code
#     }
#     try:
#         response = requests.post(url, json=data, headers=headers)
#         response.raise_for_status()
#         return response.json()

#     except requests.exceptions.RequestException as e:
#         print(f'Произошла ошибка: {e}')
#         print(f'Статус: {response.status_code}, Тело ответа: {response.text}')
#         return None
    
# print(send_code(url="https://be99-84-54-71-78.ngrok-free.app/send_verification_code/", phone="998881836222", code=123456))











# worker_processes 1;

# events {
#     worker_connections 1024;
# }

# http {
#     include /etc/nginx/mime.types;
#     default_type application/octet-stream;

#     sendfile on;
#     tcp_nopush on;
#     tcp_nodelay on;
#     keepalive_timeout 65;

#     upstream django {
#         server aurora-backend:8000;  # Имя сервиса из docker-compose
#     }

#     upstream fast {
#         server aurora-backend:8000;  # Имя сервиса из docker-compose
#     }

#     server {
#         listen 80;
#         server_name api.aurora-api.uz;

#         # Для certbot
#         location /.well-known/acme-challenge/ {
#             root /var/www/certbot;
#         }

#         # Перенаправление на HTTPS
#         location / {
#             return 301 https://$host$request_uri;
#         }
#     }

#     server {
#         listen 443 ssl;
#         server_name api.aurora-api.uz;

#         # Путь к сертификатам, которые будут созданы Certbot
#         ssl_certificate /etc/letsencrypt/live/api.aurora-api.uz/fullchain.pem;
#         ssl_certificate_key /etc/letsencrypt/live/api.aurora-api.uz/privkey.pem;
#         ssl_protocols TLSv1.2 TLSv1.3;
#         ssl_ciphers 'HIGH:!aNULL:!MD5';
#         ssl_prefer_server_ciphers on;

#         location / {
#             proxy_pass http://django;
#             proxy_set_header Host $host;
#             proxy_set_header X-Real-IP $remote_addr;
#             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#             proxy_set_header X-Forwarded-Proto $scheme;
#         }

#         location /fast {
#             proxy_pass http://fastapi;
#             proxy_set_header Host $host;
#             proxy_set_header X-Real-IP $remote_addr;
#             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#             proxy_set_header X-Forwarded-Proto $scheme;
#         }
#     }
# }

import requests

headers = {
        'Content-Type': 'application/json',
    }
def send_code(url, phone, code):
    data={
        "phone": phone,
        "code": code
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f'Произошла ошибка: {e}')
        print(f'Статус: {response.status_code}, Тело ответа: {response.text}')
        return None
    
print(send_code(url="https://be99-84-54-71-78.ngrok-free.app/send_verification_code/", phone="998881836222", code=123456))
import json
import requests
from datetime import datetime

from config.settings import BACKEND_URL


CREATE_CUSTOMER_URI = BACKEND_URL+'customers/'
TICKET_URI = BACKEND_URL+'tickets/'
GET_TICKETS_BY_TELEGRAM_ID_URI = BACKEND_URL+'tickets/by-user-id/'


def post_request(uri, **kwargs):
    try:
        response = requests.post(uri, json=kwargs)
        status = response.status_code
        content = response.content
    except requests.exceptions.ConnectionError:
        status = 502,
        content = {}
    return status, content


def get_request(uri, **kwargs):
    try:
        response = requests.get(uri, params=kwargs)
        status = response.status_code
        content = response.content
    except requests.exceptions.ConnectionError:
        status = 502,
        content = {}
    return status, content


def is_message_valid(message: str):
    if len(message) <= 3 and not type(message) == str:
        return False
    return True


def create_topic_from_message(message: str):
    topic = message.split(' ')[0]
    return topic


def create_new_user(name: str, telegram_id: int):
    status, content = post_request(CREATE_CUSTOMER_URI, name=name, telegram_id=telegram_id)
    if status == 201:
        return True


def create_ticket(name: str, telegram_id: int, message: str, attachment=None):
    status, content = post_request(TICKET_URI,
                                   message=message,
                                   topic=create_topic_from_message(message),
                                   customer={'name': name, 'telegram_id': telegram_id})

    if attachment:
        import os
        r = requests.get(attachment, allow_redirects=True)

        file_extension = attachment.split('.')[::-1][0]
        file_name = f'attachment_{telegram_id}_{json.loads(content)["number"]}.'+file_extension
        if not os.path.exists('.temp'):
            os.makedirs('.temp')
        open('.temp/'+file_name, 'wb').write(r.content)

        response = requests.patch(TICKET_URI+str(json.loads(content)['number'])+'/',
                                  files={F'attachments': (file_name, open('.temp/'+file_name, 'rb'))})
        os.remove('.temp/'+file_name)
    return status == 201


def get_tickets(telegram_id: int):
    status, content = get_request(GET_TICKETS_BY_TELEGRAM_ID_URI+str(telegram_id))
    return json.loads(content)


def get_ticket_by_number(number):
    status, content = get_request(TICKET_URI+number+'/')
    return json.loads(content)


def get_beautiful_time(dt):
    new_dt = datetime.fromisoformat(dt)
    return new_dt.strftime('%Y-%m-%d %H:%M:%S')

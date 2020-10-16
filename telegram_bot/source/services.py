import json
import requests

from config.settings import BACKEND_URL


CREATE_CUSTOMER_URI = BACKEND_URL+'customers/'
TICKET_URI = BACKEND_URL+'tickets/'
GET_TICKETS_BY_TELEGRAM_ID_URI = BACKEND_URL+'tickets/by-user-id/'


def post_request(uri, **kwargs):
    try:
        print(kwargs)
        response = requests.post(uri, data=kwargs)
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


def is_message_valid(message):
    if (type(message) is not str) or len(message) < 3:
        return False


def create_topic_from_message(message: str):
    topic = message.split(' ')[0]
    return topic


def create_new_user(name: str, telegram_id: int):
    status, content = post_request(CREATE_CUSTOMER_URI, name=name, telegram_id=telegram_id)
    if status == 201:
        return True


def create_ticket(name: str, telegram_id: int, message: str, attachments=None):
    status, content = post_request(TICKET_URI,
                                   topic=create_topic_from_message(message),
                                   message=message,
                                   customer={'name': name, 'telegram_id': telegram_id},
                                   attachments=attachments)
    print(content)
    if status == 201:
        return True


def get_tickets(telegram_id: int):
    status, content = get_request(GET_TICKETS_BY_TELEGRAM_ID_URI, telegram_id=telegram_id)
    print(content)
    return content

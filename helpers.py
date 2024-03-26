import requests
import random
import string
import json
from data import Url, OrderTestData


def register_new_courier_and_return_login_password():

    login_pass = {}

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(Url.BASE_URL+Url.CREATE_COURIER_HANDLE, data=payload)

    if response.status_code == 201:
        login_pass = {
            "login": login,
            "password": password,
            "firstName": first_name,
            "status_code": response.status_code,
            "json": response.json()
        }

    return login_pass


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def courier_login(login, password):
    payload = {
        'login': login,
        'password': password
    }
    response = requests.post(Url.BASE_URL+Url.LOGIN_COURIER_HANDLE, data=payload)
    return response


def courier_delete(courier_id):
    response = requests.delete(f'{Url.BASE_URL}{Url.CREATE_COURIER_HANDLE}/{courier_id}')
    return response


def order_create(color):
    OrderTestData.ORDER['color'] = color
    payload = OrderTestData.ORDER
    response = requests.post(Url.BASE_URL+Url.ORDERS_HANDLE, data=json.dumps(payload))
    return response


def get_orders_ids():
    response = requests.get(Url.BASE_URL + Url.ORDERS_HANDLE)
    response_data = json.loads(response.text)
    order_ids = [order['id'] for order in response_data['orders']]
    return order_ids


def get_orders_numbers():
    response = requests.get(Url.BASE_URL + Url.ORDERS_HANDLE)
    response_data = json.loads(response.text)
    order_numbers = [order['track'] for order in response_data['orders']]
    return order_numbers

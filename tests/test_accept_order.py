import requests
import allure
import helpers
from data import Url, Messages


@allure.story('Тесты принятия заказа')
class TestAcceptOrder:
    @allure.title('Тест успешного принятия заказа')
    def test_successful_order_accepting(self, courier):
        order_id = helpers.get_orders_ids()[0]
        courier_id = helpers.courier_login(courier['login'], courier['password']).json()['id']
        response = requests.put(f'{Url.BASE_URL}{Url.ORDERS_ACCEPT_HANDLE}/{order_id}?courierId={courier_id}')
        assert response.status_code == 200 and response.text == '{"ok":true}', \
            f'Status code: {response.status_code}, Response body: {response.json()}'

    @allure.title('Тест принятия заказа без id курьера')
    def test_order_accepting_without_courier_id(self):
        order_id = helpers.get_orders_ids()[0]
        response = requests.put(f'{Url.BASE_URL}{Url.ORDERS_ACCEPT_HANDLE}/{order_id}')
        assert response.status_code == 400 and response.json()['message'] == Messages.ACCEPTING_ORDER_400, \
            f'Status code: {response.status_code}, Response message: {response.json()['message']}'

    @allure.title('Тест принятия заказа бе id заказа')
    def test_order_accepting_without_order_id(self, courier):
        courier_id = helpers.courier_login(courier['login'], courier['password']).json()['id']
        response = requests.put(f'{Url.BASE_URL}{Url.ORDERS_ACCEPT_HANDLE}/courierId={courier_id}')
        assert response.status_code == 400 and response.json()['message'] == Messages.ACCEPTING_ORDER_400, \
            f'Status code: {response.status_code}, Response message: {response.json()['message']}'

    @allure.title('Тест принятия заказа с несуществующим id курьера')
    def test_order_accepting_with_no_existing_courier_id(self):
        order_id = helpers.get_orders_ids()[0]
        courier_id = 0
        response = requests.put(f'{Url.BASE_URL}{Url.ORDERS_ACCEPT_HANDLE}/{order_id}?courierId={courier_id}')
        assert response.status_code == 404 and response.json()['message'] == Messages.ACCEPTING_ORDER_NO_COURIER_ID_404, \
            f'Status code: {response.status_code}, Response message: {response.json()['message']}'

    @allure.title('Тест принятия заказа с несуществующим id заказа')
    def test_order_accepting_with_no_existing_order_id(self, courier):
        courier_id = helpers.courier_login(courier['login'], courier['password']).json()['id']
        order_id = 0
        response = requests.put(f'{Url.BASE_URL}{Url.ORDERS_ACCEPT_HANDLE}/{order_id}?courierId={courier_id}')
        assert response.status_code == 404 and response.json()['message'] == Messages.ACCEPTING_ORDER_NO_ORDER_ID_404, \
            f'Status code: {response.status_code}, Response message: {response.json()['message']}'



import requests
import allure
import helpers
from data import Url, Messages


@allure.story('Тесты создания курьеров')
class TestCourierCreating:
    @allure.title('Тест успешного создания курьера')
    def test_successful_courier_creating(self):
        payload = {
            'login': helpers.generate_random_string(10),
            'password': helpers.generate_random_string(10),
            'firstName': helpers.generate_random_string(10)
        }
        response = requests.post(Url.BASE_URL+Url.CREATE_COURIER_HANDLE, data=payload)
        courier_id = helpers.courier_login(payload["login"], payload["password"]).json()["id"]
        helpers.courier_delete(courier_id)
        assert response.status_code == 201 and response.json() == {'ok': True}, \
            f'Status code: {response.status_code}, Response body: {response.json()}'

    @allure.title('Негативный тест создания курьера с одинаковым логином')
    def test_courier_creating_using_same_login(self, courier):
        payload = {
            'login': courier['login'],
            'password': helpers.generate_random_string(10),
            'firstName': helpers.generate_random_string(10)
        }
        response = requests.post(Url.BASE_URL+Url.CREATE_COURIER_HANDLE, data=payload)
        assert response.status_code == 409 and response.json()['message'] == Messages.CONFLICT_409, \
            f"Status code: {response.status_code}, Response message: {response.json()['message']}"

    @allure.title('Нагативный тест создание курьера с незаполненым полем "login"')
    def test_courier_creating_with_unfilled_login(self):
        payload = {
            'login': '',
            'password': helpers.generate_random_string(10),
            'firstName': helpers.generate_random_string(10)
        }
        response = requests.post(Url.BASE_URL+Url.CREATE_COURIER_HANDLE, data=payload)
        assert response.status_code == 400 and response.json()['message'] == Messages.CREATE_BAD_REQUEST_400, \
            f"Status code: {response.status_code}, Response message: {response.json()['message']}"

    @allure.title('Нагативный тест создание курьера с незаполненым полем "password"')
    def test_courier_creating_with_unfilled_password(self):
        payload = {
            'login': helpers.generate_random_string(10),
            'password': '',
            'firstName': helpers.generate_random_string(10)
        }
        response = requests.post(Url.BASE_URL+Url.CREATE_COURIER_HANDLE, data=payload)
        assert response.status_code == 400 and response.json()['message'] == Messages.CREATE_BAD_REQUEST_400, \
            f"Status code: {response.status_code}, Response message: {response.json()['message']}"

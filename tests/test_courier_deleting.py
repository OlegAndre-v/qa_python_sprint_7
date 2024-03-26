import allure


import helpers
from data import Messages


@allure.story('Тесты удаления курьера')
class TestCourierDeleting:
    @allure.title('Тест успешного удаления курьера')
    def test_successful_courier_deleting(self, courier):
        courier_id = helpers.courier_login(courier["login"], courier["password"]).json()["id"]
        response = helpers.courier_delete(courier_id)
        assert response.json() == {'ok': True}

    @allure.title('Тест удаления курьера без id')
    def test_courier_deleting_with_no_id(self, courier):
        response = helpers.courier_delete('')
        assert response.status_code == 400 and response.json()['message'] == Messages.DELETING_COURIER_400, \
            f'Status code: {response.status_code}, Response message: {response.json()['message']}'
        
    @allure.title('Тест удаления курьера с не существующим id')
    def test_courier_deleting_with_incorrect_id(self, courier):
        response = helpers.courier_delete('1')
        assert response.status_code == 404 and response.json()['message'] == Messages.DELETING_COURIER_404, \
            f'Status code: {response.status_code}, Response message: {response.json()['message']}'

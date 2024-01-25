import uuid
import requests
import json
from exceptions.BadJsonResponseException import BadJsonResponseException
from exceptions.BadRequestException import BadRequestException
from exceptions.UnauthorizedException import UnauthorizedException


class YandexApiService(object):
    def __init__(self, cookie, park_id):
        self.park_id = park_id
        self.cookie = cookie
        self.headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'X-Park-Id': self.park_id,
            'Cookie': self.cookie,
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'X-Idempotency-Token': str(uuid.uuid4()),
            'Origin': 'https://fleet.taxi.yandex.ru',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'en,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7',
        }

    def request(self, method: str, url: str, headers: dict, data: str = ''):
        response = requests.request(method, url, headers=headers, data=data.encode('utf-8'))
        try:
            response_json = response.json()
        except:
            raise BadJsonResponseException

        if 'Unauthorized' in response.text:
            raise UnauthorizedException

        if 'Bad Request' in response.text:
            raise BadRequestException

        return response_json

    def get_drivers(self, data: dict) -> dict:
        """

        Метод получает всех водителей в парке.
        Возвращает массив со статусом запроса, и ответом от Яндекса

        """

        return self.request(method='POST', url='https://fleet.yandex.ru/api/v1/drivers/list', headers=self.headers,
                            data=json.dumps(data))

    def get_parks(self) -> dict:
        """

        Метод получает идентификаторы всех доступных парков.

        """

        headers = self.headers
        del headers['X-Park-Id']

        return self.request(method='GET', url='https://fleet.yandex.ru/api/fleet/ui/v1/parks/users/profile',
                            headers=headers)

    def get_driver(self, data: dict) -> dict:
        return self.request(method='POST', url='https://fleet.yandex.ru/api/v1/cards/driver/details',
                            headers=self.headers, data=json.dumps(data))

    def get_driver_car(self, data: dict) -> dict:
        return self.request(method='POST', url='https://fleet.yandex.ru/api/v1/cards/car/details', headers=self.headers,
                            data=json.dumps(data))

    def update_car(self, car_id: str, data: dict):
        return self.request(method='POST', url=f"https://fleet.yandex.ru/api/v1/cars/update?carId={car_id}",
                            headers=self.headers, data=json.dumps(data))

    def update_driver(self, data: dict):
        return self.request(method='POST', url='https://fleet.yandex.ru/api/v1/drivers/update', headers=self.headers,
                            data=json.dumps(data, ensure_ascii=False))

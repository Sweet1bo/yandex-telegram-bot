import json
import math

from repositories.DriverRepository import DriverRepository
from services.Api.YandexApiService import YandexApiService

class DriverService(object):
    def __init__(self, cookie: str, park_id: str, driver_id: str):
        self.cookie = cookie
        self.park_id = park_id
        self.driver_id = driver_id
        self.yandex = YandexApiService(cookie, park_id)

    def load_drivers_to_db(self, created_park_id):
        inserted = 0
        data = {
            'limit': 100,
            'page': 1
        }
        drivers = self.yandex.get_drivers(data)
        # [{'accounts': [], 'car': [], 'driver_profile': []}]
        accounts = drivers['driver_profiles']

        if drivers['total'] > 100:
            for i in range(0, math.ceil(drivers['total'] / 100)):
                data['page'] = i + 2
                drivers = self.yandex.get_drivers(data)
                accounts = accounts + drivers['driver_profiles']

        for account in accounts:
            if 'car' in account:
                car_id = account['car']['id']
            else:
                car_id = ''

            DriverRepository.create_driver_with_phones(driver_id=account['driver_profile']['id'], car_id=car_id, park_id=created_park_id, phones=account['driver_profile']['phones'])
            inserted += 1

        return inserted

    def add_nal(self):
        return self.yandex.update_driver({'driver_id': self.driver_id, 'accounts': {'balance_limit': str(1000000)}, 'driver_profile': self.get_driver(self.driver_id)['driver']['driver_profile']})

    def remove_nal(self):
        return self.yandex.update_driver({'driver_id': self.driver_id, 'accounts': {'balance_limit': str(5)}, 'driver_profile': self.get_driver(self.driver_id)['driver']['driver_profile']})

    def get_driver(self, driver_id: str):
        return self.yandex.get_driver({'driver_id': driver_id})
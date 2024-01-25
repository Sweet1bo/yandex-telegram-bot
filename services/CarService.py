import json

from services.Api.YandexApiService import YandexApiService


class CarService(object):
    def __init__(self, cookie, park_id, car_id: str):
        self.car = None
        self.car_id = car_id
        self.yandex = YandexApiService(cookie, park_id)

        self.set_car(car_id)

    def add_branding(self):
        if 'sticker' not in self.car['amenities']:
            self.car['amenities'].append('sticker')

        if 'lightbox' not in self.car['amenities']:
            self.car['amenities'].append('lightbox')

        return self.yandex.update_car(self.car_id, self.create_car_request(self.car))

    def remove_branding(self):
        if 'sticker' in self.car['amenities']:
            del self.car['amenities'][self.car['amenities'].index('sticker')]

        if 'lightbox' in self.car['amenities']:
            del self.car['amenities'][self.car['amenities'].index('lightbox')]

        return self.yandex.update_car(self.car_id, self.create_car_request(self.car))

    def add_booster(self):
        if self.car['booster_count'] == 0:
            self.car['booster_count'] = 1
        else:
            return None

        return self.yandex.update_car(self.car_id, self.create_car_request(self.car))

    def remove_booster(self):
        if self.car['booster_count'] == 1:
            self.car['booster_count'] = 0
        else:
            return None

        return self.yandex.update_car(self.car_id, self.create_car_request(self.car))

    def add_child_seat(self):
        if 'chairs' not in self.car:
            self.car['chairs'] = [{
                'brand': 'Other',
                'categories': [],
                'isofix': False
            }]
        else:
            return None

        return self.yandex.update_car(self.car_id, self.create_car_request(self.car))

    def remove_child_seat(self):
        if 'chairs' in self.car:
            self.car['chairs'] = []
        else:
            return None

        return self.yandex.update_car(self.car_id, self.create_car_request(self.car))

    def set_car(self, car_id: str):
        self.car = self.yandex.get_driver_car({'car_id': car_id})['car']

    def create_car_request(self, car: dict) -> dict:
        if 'is_readonly' in car:
            del car['is_readonly']
        if 'created_date' in car:
            del car['created_date']

        return car

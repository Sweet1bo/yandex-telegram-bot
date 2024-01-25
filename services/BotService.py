import requests
from repositories.BotUserRepository import BotUserRepository
from services.CarService import CarService
from services.DriverService import DriverService


class BotService(object):
    def __init__(self, data):
        self.data = data
        self.car_service = CarService(data['session'].session, data['park'].park_id, self.data['driver'].car_id)
        self.driver_service = DriverService(data['session'].session, data['park'].park_id, data['user'].driver.driver_id)

    def nal(self):
        if not self.data['user'].nal:
            result = self.driver_service.add_nal()
        else:
            self.driver_service.remove_nal()

        return self.update_user('nal')

    def booster(self):
        if not self.data['user'].booster:
            self.car_service.add_booster()
        else:
            self.car_service.remove_booster()

        return self.update_user('booster')

    def child_seat(self):
        if not self.data['user'].kids:
            self.car_service.add_child_seat()
        else:
            self.car_service.remove_child_seat()

        return self.update_user('kids')

    def brand(self):
        if not self.data['user'].brand:
            self.car_service.add_branding()
        else:
            self.car_service.remove_branding()

        return self.update_user('brand')

    def update_user(self, field_name):
        status = not getattr(self.data['user'], field_name)

        BotUserRepository.update_user(self.data['user'].id, {field_name: status})
        return status

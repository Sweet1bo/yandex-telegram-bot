import phonenumbers
from phonenumbers import NumberParseException

from database.models.Driver import Driver
from database.models.Phone import Phone
from helpers import format_phone


class DriverRepository(object):
    @staticmethod
    def create_driver_with_phones(**attributes):
        """

        Метод создает водителя

        :param attributes:
        :return: Driver
        """
        driver = Driver.where({
            'driver_id': attributes['driver_id'],
            'park_id': attributes['park_id'],
        }).first()

        if driver:
            driver.update(car_id=attributes['car_id'],driver_id=attributes['driver_id'],park_id=attributes['park_id'])
        else:
            driver = Driver.create(car_id=attributes['car_id'],driver_id=attributes['driver_id'],park_id=attributes['park_id'])

        for phone in attributes['phones']:
            try:
                phone_number = format_phone(phone)
            except NumberParseException:
                phone_number = phone
                print('                 Найден неверный номер ' + phone)

            phone_row = Phone.where({
                'driver_id': driver.id,
                'phone': phone_number
            }).first()

            if phone_row:
                phone_row.update(driver_id=driver.id, phone=phone_number)
            else:
                Phone.create(driver_id=driver.id, phone=phone_number)

        return driver

    @staticmethod
    def get_driver_by_id(id):
        return Driver.find(id)
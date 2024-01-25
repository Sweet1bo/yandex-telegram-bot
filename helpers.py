import re

import phonenumbers

from exceptions.WrongSelectedParksFormat import WrongSelectedParksFormat


def input_selected_parks():
    selected_parks = input('Парки: ')
    if ',' not in selected_parks:
        print('Некорректно введены парки выходим')
        raise WrongSelectedParksFormat
    return [int(split) for split in re.sub('[^0-9,]', "", selected_parks).split(',')]


def format_phone(phone: str):
    phone_number = str(re.sub("[^0-9+]", "", phone))
    if phone_number[:1] == '+8':
        phone_number = '+7' + phone_number[2:]
    if phone_number[0] == '8':
        phone_number = '+7' + phone_number[1:]
    if phone_number[0] != '+':
        phone_number = '+' + phone_number
    return str(phonenumbers.parse(phone_number).national_number)

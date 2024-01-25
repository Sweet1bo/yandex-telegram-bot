from services.DriverService import DriverService
from services.Api.YandexApiService import YandexApiService
from database.models.Park import Park
from repositories.ParkRepository import ParkRepository
from services.YandexAuthService import YandexAuthService
from exceptions.InvalidSmsCodeException import InvalidSmsCodeException
from helpers import input_selected_parks

while True:
    auth = YandexAuthService()

    login = input('Логин ')
    password = input('Пароль ')

    if auth.login(login, password)['status'] == 'sms_code':
        while True:
            code = input('Введите код подтверждения: ')
            try:
                auth.send_code(code)
                break
            except InvalidSmsCodeException as e:
                print('Вы ввели неверный код, попробуйте еще раз')
    else:
        print('Не получилось войти')
        break

    yandex = YandexApiService(auth.cookie, '')
    parkService = ParkRepository()

    parks = yandex.get_parks()['user']['parks']

    print('Перечислите парки, которые хотите добавить через запятую(1,2,3,4)')
    for i, park in enumerate(parks):
        print(f"{i + 1} - {park['name']}")

    selected_parks = input_selected_parks()

    for i, park in enumerate(parks):
        if i + 1 in selected_parks:
            print('Создаем парк ' + park['name'])
            created_park = parkService.create_park_with_session(auth.cookie, name=park['name'], city=park['city'], park_id=park['id'])
            print('Загружаем водителей из парка ' + park['name'] + ' в базу данных')
            driverService = DriverService(Park.with_('session').where('park_id', park['id']).first().session.session, park['id'], '')
            driverService.load_drivers_to_db(created_park.id)

    print('Успешно загрузили все данные\n')
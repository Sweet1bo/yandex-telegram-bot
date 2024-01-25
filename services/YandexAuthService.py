from services.Api.YandexAuthApiService import YandexAuthApiService
from exceptions.InvalidSmsCodeException import InvalidSmsCodeException


class YandexAuthService(object):
    def __init__(self):
        self.auth = YandexAuthApiService()
        self.cookie = None

    def login(self, login, password) -> dict:
        # Получаем параметры для авторизации
        self.auth.get_uuid()

        # Отправляем логин
        if self.auth.send_login(login):
            # Отправляем пароль
            two_factor = self.auth.send_password(password)
            # Проверяем нужна ли двухфакторная аутентификация
            if two_factor > 0:
                # Подтверждаем вход
                self.auth.submit_auth()
                if two_factor == 3:
                    print('Слишком много попыток входа попробуйте позже')
                elif two_factor == 2:
                    # Подтверждаем номер
                    if self.auth.validate_phone():
                        # Запрашиваем код
                        if self.auth.sms_confirmation():
                            return {'status': 'sms_code'}
                elif two_factor == 1:
                    # Завершаем вход
                    if self.auth.commit_challenge():
                        self.cookie = self.auth.get_cookies()
                        return {'status': 'success'}
            elif two_factor == -1:
                raise Exception('Two factor authentication error')
        else:
            raise Exception('Send login failed')

    def send_code(self, code):
        # Отправляем код
        sent = self.auth.send_code_sms(code)
        if sent == 2:
            # Завершаем вход
            if self.auth.commit_challenge():
                self.cookie = self.auth.get_cookies()
        elif sent == 1:
            raise InvalidSmsCodeException
        else:
            raise Exception('Unexpected error while trying to send an sms code')
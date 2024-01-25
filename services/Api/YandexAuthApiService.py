import requests
from pyquery import PyQuery
from exceptions.SmsLimitExceededException import SmsLimitExceededException

class YandexAuthApiService(object):
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://passport.yandex.ru',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://passport.yandex.ru/auth/welcome?retpath=https%3A%2F%2Ffleet.taxi.yandex.ru',
            'Accept-Language': 'en',
        }

        self.csrf = ""
        self.uuid = ""
        self.track_id = ""
        self.challenge = None

    def get_uuid(self):
        r = self.session.get('https://passport.yandex.ru/auth?retpath=https%3A%2F%2Ffleet.taxi.yandex.ru')

        html = PyQuery(r.text)
        self.csrf = html.find('input[name="csrf_token"]').attr('value')
        self.uuid = html.find('.passp-register-button a[data-t="button:pseudo"]').attr('href').split("process_uuid=")[1].split("&")[0]

        if len(self.csrf) > 0 and len(self.uuid) > 0:
            return 1

        return 0

    def send_login(self, login: str) -> bool:
        '''
        Данный метод отправляет логин в Яндекс

        :param login:
        :return:
        '''
        r = self.session.post('https://passport.yandex.ru/registration-validations/auth/multi_step/start', data={
            'csrf_token': self.csrf,
            'login': login,
            'process_uuid': self.uuid,
            'retpath': 'https://fleet.taxi.yandex.ru'
        })

        if r.json()['status'] == 'ok':
            self.track_id = r.json()['track_id']
            return True
        return False

    def send_password(self, password: str) -> int:
        '''
        Данный метод отправляет пароль в Яндекс

        :param password:
        :return:
        '''
        r = self.session.post('https://passport.yandex.ru/registration-validations/auth/multi_step/commit_password', data={
            'csrf_token': self.csrf,
            'password': password,
            'track_id': self.track_id,
            'retpath': 'https://fleet.taxi.yandex.ru'
        })

        if r.json()['status'] == 'ok':
            if r.json()['state'] == 'auth_challenge':
                # Нужно подтверждение
                return 2
            if r.json()['state'] == 'change_password':
                # Много попыток входа, нужно решить капчу в аккаунте и затем пробовать
                return 3
            return 1
        elif r.json()['status'] == 'error':
            if 'password.not_matched' in r.json()['errors']:
                # Пароль неверный
                return -1
        return 0

    def submit_auth(self) -> int:
        '''
        Данный метод отправляет запрос на авторизацию

        :return:
        '''
        r = self.session.post('https://passport.yandex.ru/registration-validations/auth/challenge/submit', data={
            'csrf_token': self.csrf,
            'track_id': self.track_id
        })

        if r.json()['status'] == 'ok':
            self.challenge = r.json()['challenge']
            return 1
        # Ошибочный ответ
        return 0

    def validate_phone(self) -> int:
        '''
        Данный метод отправляет запрос на подтверждение номера

        :return:
        '''
        r = self.session.post('https://passport.yandex.ru/registration-validations/auth/validate_phone_by_id', data={
            'csrf_token': self.csrf,
            'track_id': self.track_id,
            'phoneId': str(self.challenge['phoneId'])
        })

        if r.json()['status'] == 'ok':
            return 1
        return 0

    def sms_confirmation(self) -> int:
        '''
        Данный метод отправляет запрос на получение смс

        :return:
        '''
        r = self.session.post('https://passport.yandex.ru/registration-validations/phone-confirm-code-submit', data={
            'csrf_token': self.csrf,
            'track_id': self.track_id,
            'phone_id': str(self.challenge['phoneId']),
            'confirm_method': 'by_sms',
            'isCodeWithFormat': True
        }, headers={
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://passport.yandex.ru',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'en',
        })

        if r.json()['status'] == 'ok':
            return 1
        elif 'sms_limit.exceeded' in r.text:
            raise SmsLimitExceededException
        return 0

    def send_code_sms(self, code) -> int:
        '''
        Данный метод отправляет код полученный от пользователя

        :param code:
        :return:
        '''
        r = self.session.post('https://passport.yandex.ru/registration-validations/phone-confirm-code', data={
            'csrf_token': self.csrf,
            'code': code,
            'track_id': self.track_id
        }, headers={
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://passport.yandex.ru',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            "Referer": "https://passport.yandex.ru/auth/challenge?retpath=https%3A%2F%2Fpassport.yandex.ru%2Fprofile&track_id={}".format(self.track_id),
            'Accept-Language': 'en',
        })

        print(self.track_id)

        if r.json()['status'] == 'ok':
            # Успешно
            return 2
        if r.json()['status'] == 'error' and 'code.invalid' in r.json()['errors']:
            # Неверный код
            return 1
        return 0

    def commit_challenge(self) -> int:
        '''
        Данный метод завершает подтверждение

        :return:
        '''

        r = self.session.post('https://passport.yandex.ru/registration-validations/auth/challenge/commit', data={
            'csrf_token': self.csrf,
            'track_id': self.track_id,
            'challenge': 'phone_confirmation'
        })

        if r.json()['status'] == 'ok':
            return 1
        return 0

    def get_cookies(self) -> str:
        '''
        Данный метод возвращает куки

        :return:
        '''

        cookie_str = ''
        cookie = self.session.cookies.get_dict()
        if 'Cookie' in cookie:
            cookie = cookie['Cookie']

        for key in cookie.keys():
            cookie_str += key + '=' + cookie[key] + ';'

        return cookie_str

    def flush_cookies(self):
        '''
        Данный метод очищает куки

        :return:
        '''
        self.session.cookies.clear()
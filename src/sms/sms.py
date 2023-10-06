import requests
import os

from src.settings import settings

from src.auth.exceptions import SMSOperationException


class SMS_Sender:
    host = settings.SMS_SERVICE_HOST
    sign = settings.SMS_SENDER

    @classmethod
    def test(cls):
        return cls._request('auth').ok

    @classmethod
    def send_sms(cls, phone_number, text):
        if settings.MODE == 'DEV':
            path = 'sms/testsend'
        else:
            path = 'sms/send'
        print(f'sent sms: {text}')
        return cls._request(path, sign=cls.sign, number=phone_number, text=text).ok

    @classmethod
    def _request(cls, path, **params):
        request = requests.session()
        response = request.get(
            os.path.join(cls.host, path),
            auth=(settings.SMS_ACCOUNT_EMAIL, settings.SMS_SERVICE_API_KEY),
            params=params)

        if not response.ok:
            raise SMSOperationException(f'{SMSOperationException.detail} : "{path}" : {response.json()["message"]}')

        return response

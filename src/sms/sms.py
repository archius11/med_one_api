import requests
import os

from src.settings import settings

from src.auth.exceptions import SMSOperationException


class SMS_Sender:
    def __init__(self):
        self.host = settings.SMS_SERVICE_HOST
        self.sign =settings.SMS_SENDER

    def test(self):
        return self._request('auth').ok

    def send_sms(self, phone_number, text):
        if settings.MODE == 'DEV':
            path = 'sms/testsend'
        else:
            path = 'sms/send'
        print(f'sent sms: {text}')
        return self._request(path, sign=self.sign, number=phone_number, text=text).ok

    def _request(self, path, **params):
        request = requests.session()
        response = request.get(
            os.path.join(self.host, path),
            auth=(settings.SMS_ACCOUNT_EMAIL, settings.SMS_SERVICE_API_KEY),
            params=params)

        if not response.ok:
            raise SMSOperationException(f'{SMSOperationException.detail} : "{path}" : {response.json()["message"]}')

        return response

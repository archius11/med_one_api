import aiohttp
import os

from src.settings import settings

from src.auth.exceptions import SMSOperationException


class SMS_Sender:
    host = settings.SMS_SERVICE_HOST
    sign = settings.SMS_SENDER

    @classmethod
    async def test(cls):
        response = await cls._request('auth')
        return response['status_is_ok']

    @classmethod
    async def send_sms(cls, phone_number, text):
        if settings.MODE == 'DEV':
            path = 'sms/testsend'
        else:
            path = 'sms/send'
        print(f'sent sms: {text}')
        response = await cls._request(path, sign=cls.sign, number=phone_number, text=text)
        return response['status_is_ok']

    @classmethod
    async def _request(cls, path, **params):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    os.path.join(cls.host, path),
                    auth=aiohttp.BasicAuth(settings.SMS_ACCOUNT_EMAIL, settings.SMS_SERVICE_API_KEY),
                    params=params
            ) as response:
                response_data = await response.json()
                response_status = response.status
                response_status_is_ok = response.ok

        if not response_status_is_ok:
            raise SMSOperationException(f'{SMSOperationException.detail} : "{path}" : {response_data["message"]}')

        return {
            'data': response_data,
            'status': response_status,
            'status_is_ok': response_status_is_ok,
        }

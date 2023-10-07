import random
from fastapi import HTTPException
from datetime import datetime

from src.auth.models import User
from src.sms import SMS_Sender

from src.settings import settings
from src.auth.settings import auth_settings

from src.redis import RedisClient


class SMS_Verification:

    @classmethod
    async def send_sms_code(cls, user: User):
        await cls._check_last_sent_timeout(user)
        code = cls._generate_new_code()
        text = cls._get_message_text(code)
        if await SMS_Sender.send_sms(user.phone_number, text):
            code_to_send = {
                'code': code,
                'sent_time': int(datetime.now().timestamp())
            }
            await RedisClient.set_dict(cls._get_redis_hash(user), code_to_send, auth_settings.SMS_EXPIRE_SEC)

    @classmethod
    async def delete_code(cls, user: User):
        await RedisClient.del_key(cls._get_redis_hash(user))

    @classmethod
    async def check_sms_code(cls, user: User, code):
        sent_code = await cls._get_sent_code(user)
        if sent_code:
            sent_code = sent_code.decode()
        return sent_code is not None and sent_code == code

    @classmethod
    async def _get_sent_code(cls, user: User):
        return await RedisClient.get_dict_value(cls._get_redis_hash(user), 'code')

    @classmethod
    async def _check_last_sent_timeout(cls, user: User):
        sent_time = await RedisClient.get_dict_value(cls._get_redis_hash(user), 'sent_time')
        if sent_time:
            delta_seconds = int(datetime.now().timestamp()) - int(sent_time)
            if delta_seconds < auth_settings.SMS_RESEND_MIN_DELTA:
                raise HTTPException(status_code=400,
                                    detail=f'Уже было отправлено SMS-сообщение {delta_seconds} секунд назад.'
                                           f'Повторное SMS возможно через минуту.')

    @classmethod
    def _generate_new_code(cls):
        if settings.MODE == 'DEV':
            return '1111'

        return str(random.randint(1000, 9999))

    @classmethod
    def _get_message_text(cls, code):
        return auth_settings.SMS_MESSAGE_TEMPLATE.format(code=code)

    @classmethod
    def _get_redis_hash(cls, user):
        return ':'.join(['sms_code', str(user.id), user.phone_number])

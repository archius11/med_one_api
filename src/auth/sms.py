import random

from src.auth.models import User
from src.sms import SMS_Sender

from src.settings import settings
from src.auth.settings import auth_settings


class SMS_Verification:

    @classmethod
    def send_sms_code(cls, user: User):
        cls._check_last_sent_timeout(user)
        code = cls._generate_new_code()
        text = cls._get_message_text(code)
        SMS_Sender.send_sms(user.phone_number, text)

    @classmethod
    def check_sms_code(cls, user: User, code):
        return cls._get_sent_code(user) == code

    @classmethod
    def _get_sent_code(cls, user: User):
        if settings.MODE == 'DEV':
            return '1111'

        return '1111'

    @classmethod
    def _check_last_sent_timeout(cls, user: User):
        return True

    @classmethod
    def _generate_new_code(cls):
        if settings.MODE == 'DEV':
            return '1111'

        return str(random.randint(1000, 9999))

    @classmethod
    def _get_message_text(cls, code):
        return auth_settings.SMS_MESSAGE_TEMPLATE.format(code=code)

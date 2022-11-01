import os
import pyotp
from decouple import config
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class OTPManager:
    totp = pyotp.TOTP(
        os.getenv('OTP_SECRET_KEY'), interval=int(os.getenv('OTP_EXPIRES'))
    )

    @classmethod
    def generate(cls):
        return cls.totp.now()

    @classmethod
    def verify(cls, otp: str):
        status = cls.totp.verify(otp)
        return status


class EmailManager:
    SENDER = os.getenv('EMAIL_DEFAULT')

    @classmethod
    def __send_message(cls, email: str, subject: str, message: str, html_message: str):
        try:
            send_mail(
                subject=subject,
                from_email=cls.SENDER,
                recipient_list=[email],
                message=message,
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            return {"error": e}

    @staticmethod
    def send_welcome_msg(email):
        otp = OTPManager.generate()
        return EmailManager.dispatch(email=email, message_type="welcome", otp=otp)

    @staticmethod
    def send_otp_msg(email):
        otp = OTPManager.generate()
        return EmailManager.dispatch(email=email, message_type="otp", otp=otp)

    @staticmethod
    def dispatch(email, message_type, otp=None):
        MSG_TYPES = {
            "welcome": {
                "subject": "Verify your account",
                "template": "welcome",
                "message": f"Hi there, welcome to your account. Use this OTP to continue: {otp}."
            },
            "otp": {
                "subject": "OTP Verification",
                "template": "otp",
                "message": f"Hi there, to verify your action, kindly use this OTP to continue: {otp}."
            }
        }

        if not message_type in MSG_TYPES.keys():
            print(f"Invalid message type. Choose from {MSG_TYPES.keys()}")

        subject = MSG_TYPES[message_type]["subject"]
        template = MSG_TYPES[message_type]["template"]
        plain_message = MSG_TYPES[message_type]["message"]
        html_message = render_to_string(f'users/email/{template}.html', {
            "email": email,
            "subject": subject,
            "otp": otp if otp else ''
        })

        #if config("DEBUG", cast=bool) == True:
        if settings.DEBUG == False:
            local_msg = f"EMAIL: {email}, SUBJECT: {subject}, OTP: {otp}"
            print(local_msg)
        else:
            return EmailManager.__send_message(
                email=email,
                subject=subject,
                message=plain_message,
                html_message=html_message)
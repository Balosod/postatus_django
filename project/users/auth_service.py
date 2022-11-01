from . helpers import EmailManager, OTPManager
from . import exceptions as acct_exc
from django.contrib.auth import get_user_model
User = get_user_model()



def verify_OTP(email: str, otp: str):
    try:
        user= User.objects.get(email=email)
    except:
        raise acct_exc.EMAILError()
    if not OTPManager.verify(otp):
        raise acct_exc.OTPError()
    user.is_active = True
    user.save()
    return dict(message="success")


def resend_OTP(email: str):
    try:
        user= User.objects.get(email=email)
    except:
        raise acct_exc.EMAILError()
    EmailManager.send_otp_msg(user.email)
    return dict(message="success")
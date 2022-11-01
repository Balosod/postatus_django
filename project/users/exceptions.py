from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import APIException


class OTPError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    message = _("This otp is invalid or has expired.")
    default_code = "invalid_otp"

    default_detail = {
        "message": message,
        "status": status_code,
        "code": default_code
    }
    
class EMAILError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    message = _("This email is invalid.")
    default_code = "invalid_email"

    default_detail = {
        "message": message,
        "status": status_code,
        "code": default_code
    }

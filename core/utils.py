import pyotp
from datetime import timedelta
from django.utils import timezone  

def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=120) # 2 minutes validity
    return totp.now()

def verify_otp(otp, user):
    if otp == user.mobile_otp:  
        if timezone.now() <= user.otp_generated_at + timedelta(minutes=2):  
            return True  
    return False
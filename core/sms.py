import threading
from melipayamak import Api
from django.conf import settings

def send_otp_sms(phone_number, code):  
    username = settings.MELLI_PAYAMAK_USERNAME
    password = settings.MELLI_PAYAMAK_KEY
    api = Api(username,password)
    sms_rest = api.sms()
    to = f'{phone_number}'
    sms_rest.send_by_base_number(f'{code}', to, settings.MELLI_PAYAMAK_OTP_TEMPLATE)

def send_order_sms(phone_number, order_id):
    username = settings.MELLI_PAYAMAK_USERNAME
    password = settings.MELLI_PAYAMAK_KEY
    api = Api(username,password)
    sms_rest = api.sms()
    to = f'{phone_number}'
    sms_rest.send_by_base_number(f'{order_id}', to, settings.MELLI_PAYAMAK_ORDER_TEMPLATE)

# These functions will thread above functions
def send_otp_sms_threaded(phone_number, code):  
    thread = threading.Thread(target=send_otp_sms, args=(phone_number, code))  
    thread.start()

def send_order_sms_threaded(phone_number, order_id):  
    thread = threading.Thread(target=send_order_sms, args=(phone_number, order_id))  
    thread.start()  
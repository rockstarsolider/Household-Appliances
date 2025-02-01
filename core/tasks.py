from celery import shared_task  
from melipayamak import Api
import os

@shared_task  
def send_sms_task(phone_number, code): 
    username = '09028812713'
    password = os.environ.get("MELLI_PAYAMAK_KEY")
    api = Api(username,password)
    sms_rest = api.sms()
    to = f'{phone_number}'
    sms_rest.send_by_base_number(f'{code}', to, 289850)

@shared_task  
def send_sms_for_order_task(phone_number, order_id): 
    username = '09028812713'
    password = os.environ.get("MELLI_PAYAMAK_KEY")
    api = Api(username,password)
    sms_rest = api.sms()
    to = f'{phone_number}'
    sms_rest.send_by_base_number(f'{order_id}', to, 295377)
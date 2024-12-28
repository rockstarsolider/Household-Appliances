from celery import shared_task  
from kavenegar import *
import os

@shared_task  
def send_sms_task(phone_number, code):  
    try:
        api = KavenegarAPI(os.environ.get('KAVENEGAR_KEY'))
        message = f'لوازم خانگی \n کد تایید: {code} '
        params = { 'sender' : '2000500666', 'receptor': '09178812713', 'message' : message }
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)
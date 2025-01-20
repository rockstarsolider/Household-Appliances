from celery import shared_task  
from kavenegar import *
from melipayamak import Api
import os

# @shared_task  
# def send_sms_task(phone_number, code):  
#     try:
#         api = KavenegarAPI(os.environ.get('KAVENEGAR_KEY'))
#         message = f'لوازم خانگی \n کد تایید: {code} '
#         params = { 'sender' : '2000500666', 'receptor': '09178812713', 'message' : message }
#         response = api.sms_send(params)
#         print(response)
#     except APIException as e: 
#         print(e)
#     except HTTPException as e: 
#         print(e)

@shared_task  
def send_sms_task(phone_number, code):  
    username = '09028812713'
    password = '4b034bd6-9c2c-429e-a215-301a402a7ee5'
    api = Api(username,password)
    sms_rest = api.sms()
    to = '09333253730'
    sms_rest.send_by_base_number(f'{code}', to, 289850)
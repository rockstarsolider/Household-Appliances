from celery import shared_task  
from melipayamak import Api

@shared_task  
def send_sms_task(phone_number, code): 
    username = '09028812713'
    password = '4b034bd6-9c2c-429e-a215-301a402a7ee5'
    api = Api(username,password)
    sms_rest = api.sms()
    to = f'{phone_number}'
    sms_rest.send_by_base_number(f'{code}', to, 289850)
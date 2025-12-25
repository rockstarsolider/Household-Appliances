from django.conf import settings
import requests
import json

if settings.DEBUG:
    ZP_API_REQUEST = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'
    ZP_API_VERIFY = 'https://sandbox.zarinpal.com/pg/v4/payment/verify.json'
    ZP_API_STARTPAY = 'https://sandbox.zarinpal.com/pg/StartPay/'
else:
    ZP_API_REQUEST = 'https://payment.zarinpal.com/pg/v4/payment/request.json'
    ZP_API_VERIFY = 'https://payment.zarinpal.com/pg/v4/payment/verify.json'
    ZP_API_STARTPAY = 'https://www.zarinpal.com/pg/StartPay/'

def send_request(request, order):
    data = {
        "merchant_id": settings.MERCHANT_ID,
        "amount": order.total_price,
        "description": "خرید از طریق درگاه پرداخت",
        "callback_url": settings.CALLBACK_URL,
        "currency":"IRT",
        "metadata": {
            "mobile": order.user.phone_number,
            "order_id": f"{order.id}"
        }
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            json_response = response.json()
            data = json_response.get('data', {})
            if data.get('code') == 100:
                return {
                    'status': True,
                    'url': f"{ZP_API_STARTPAY}{data.get('authority')}",
                    'authority': data.get('authority')
                }
            else:
                return {'status': False, 'code': str(json_response['Status'])}
        else:
            return {'status': False, 'code': f'HTTP {response.status_code}'}
    
    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify(authority, order):
    data = {
        "merchant_id": settings.MERCHANT_ID,
        "amount": order.total_price,
        "authority": authority,
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    try:
        response = requests.post(
            ZP_API_VERIFY,
            json=data,   # ✅ use json= instead of data=json.dumps
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        result = response.json()
        data_response = result.get('data', {})

        if data_response.get('code') == 100:
            return {
                'status': True,
                'ref_id': data_response.get('ref_id'),
            }

        return {
            'status': False,
            'code': data_response.get('code', 'unknown_error'),
        }

    except requests.exceptions.RequestException as e:
        return {
            'status': False,
            'code': f'network_error: {str(e)}',
        }

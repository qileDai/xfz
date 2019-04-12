#encoding: utf-8

import requests


def send(mobile,captcha):
    url = "http://v.juhe.cn/sms/send"
    params = {
        "mobile": mobile,
        "tpl_id": "127646",
        "tpl_value": "#code#="+captcha,
        "key": "224a92383faca07b589f9f36fe86f7ce"
    }
    response = requests.get(url,params=params)
    result = response.json()
    if result['error_code'] == 0:
        return True
    else:
        return False
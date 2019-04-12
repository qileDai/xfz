
#encoding:utf-8
#127646
import requests
from random import randint


def asg_captcha_sender(mobile,code):
        url = "http://v.juhe.cn/sms/send"
        parmams = {
            "mobile":mobile,
            "tpl_id":"127646",
            "tpl_value":"#code#="+code,
            "key":"224a92383faca07b589f9f36fe86f7ce"
        }
        response = requests.get(url,params=parmams)
        response = response.json()
        if response['error_code'] == 0:
            return True
        else:
            return False



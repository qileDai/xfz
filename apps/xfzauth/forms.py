#encoding: utf-8

from django import forms
from apps.forms import FormMixin
from django.core.cache import cache
from .models import User


class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=20,min_length=6,
                               error_messages={"max_length":"密码不能超过20个字符！","min_lemgth":"密码不能小于6个字符"})
    remember = forms.IntegerField(required=False)

class RegisteForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=20,min_length=6,
                                error_messages={"max_length": "密码不能超过20个字符！", "min_lemgth": "密码不能小于6个字符"}
                                )
    password2 = forms.CharField(max_length=20,min_length=6,
                                error_messages={"max_length": "密码不能超过20个字符！", "min_lemgth": "密码不能小于6个字符"}
                                )
    image_catpha = forms.CharField(max_length=4,min_length=4)
    sms_captha = forms.CharField(max_length=4,min_length=4)

    def clean(self):
        cleaned_data = super(RegisteForm, self).clean()

        password1 = cleaned_data.get('password1')
        print(password1)
        password2 = cleaned_data.get('password2')
        print(password2)

        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致！')

        image_catpha = cleaned_data.get('image_catpha')
        print(image_catpha)
        cached_image_catpha = cache.get(image_catpha)
        print(cached_image_catpha)

        if not cached_image_catpha or cached_image_catpha != image_catpha:
            raise forms.ValidationError("图形验证码错误！")

        telephone = cleaned_data.get('telephone')
        print(telephone)
        sms_captcha = cleaned_data.get('sms_captha')
        cached_sms_captcha = cache.get(telephone)

        if not cached_sms_captcha or cached_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError('短信验证码错误！')

        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            forms.ValidationError('该手机号码已经被注册！')

        return cleaned_data















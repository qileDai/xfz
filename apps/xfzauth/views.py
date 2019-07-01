#encoding: utf-8

from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from  .forms import LoginForm
from django.shortcuts import redirect,reverse,render
from django.http import JsonResponse,HttpResponse
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from utils import restful
from utils import smssender
from django.core.cache import cache
from .forms import RegisteForm
from django.core.cache import cache
from django.contrib.auth import get_user_model
User = get_user_model()
@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,username=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return  restful.unauth("您的账号已经被冻结")
        else:
            return  restful.params_error("手机号码或密码错误")
    else:
        errors = form.get_errors()
        return  restful.params_error(message=errors)

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

def image_captcha(request):
    text,image = Captcha.gene_code()
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)

    response = HttpResponse(content_type="image/png")
    response.write(out.read())
    response['Content-length'] = out.tell()

    return response

def sms_captcha(request):
    telephone = request.GET.get("telephone")
    code = Captcha.gene_text()
    cache.set(telephone, code, 5 * 60)
    print("短信验证码：",code)
    # result = aliyunsms.send_sms(telephone,code)
    result = smssender.send(telephone,code)
    if result:
        return restful.ok()
    else:
        return restful.params_error(message="短信验证码发送失败")


@require_POST
def register(request):
    form = RegisteForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get("telephone")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = User.objects.create_user(telephone=telephone,username=username,password=password)
        login(request,user)
        return render(request,'news/index.html')
    else:
        return restful.params_error(message=form.get_errors())














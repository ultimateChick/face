# coding=utf-8
from django.shortcuts import render
from django.contrib.auth import login as sys_login, logout as sys_logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.db import IntegrityError

from account.models import Account
from account.sendemail import *

import json

# Create your views here.


def render_page(request):
    return render(request, template_name="log.html")


def register(request):
    result = {"message": "unknown", "issuccess": False}
    if request.method == "POST":
        form_info = json.loads(request.body.decode())
        username = form_info["username"]
        email = form_info["email"]
        password = form_info["password"]
        repeat_password = form_info["repeat_password"]

        if username and repeat_password and email and password:
            if Account.check_password(password, repeat_password):
                try:
                    validate_email(email)
                    Account.new_account(username=username, email=email, password=password)
                except IntegrityError:
                    result["message"] = u"该用户名已被使用"
                    return JsonResponse(result, status=402)
                except ValidationError:
                    result["message"] = u"邮箱格式错误"
                    return JsonResponse(result, status=402)
                result["issuccess"] = True
                return JsonResponse(result, status=200)
            else:
                result["message"] = u"两次输入的密码不一致"
                return JsonResponse(result, status=402)
        else:
            result["message"] = u"没有填写全部信息"
            return JsonResponse(result, status=402)
    else:
        result["message"] = u"不支持的请求方式"
        return JsonResponse(result, status=405)


def login(request):
    result = {"message": "unknown", "issuccess": False}
    if request.user.is_authenticated():
        sys_logout(request)
    if request.method == "POST":
        form_info = json.loads(request.body.decode())
        username_or_email = form_info["username_or_email"]
        password = form_info["password"]
        issuccess, user = Account.account_login(username_or_email, password)
        if issuccess:
            sys_login(request, user)
            result["issuccess"] = issuccess
            return JsonResponse(result, status=200)
        else:
            print user
            request["message"] = user
            return JsonResponse(result, status=403)


    else:
        result["message"] = "不支持的请求方式"
        return JsonResponse(result, status=405)


def send_active_email(request):
    result = {"message": "unknown", "issuccess": False}
    if request.user.is_authenticated():
        if request.method == "POST":
            username = request.user.username
            sendemails(username)
            result["issuccess"] = True
            return JsonResponse(result, status=200)
        else:
            result["message"] = u"不支持的请求方式"
            return JsonResponse(result, status=405)
    else:
        result["message"] = u"需要登录"
        return JsonResponse(result, status=403)


def activate(request, token):
    result = {"issuccess": False, "message": "unknown"}
    try:
        username = token.confirm_validate_token(token)
    except:
        result["message"] = u"对不起，验证链接已经过期"
        return JsonResponse(result, status=402)
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        result["message"] = u"该用户名不存在，请重新注册"
        return JsonResponse(result, status=402)
    account.isverify = True
    account.save()
    result["issuccess"] = True
    return JsonResponse(result, status=200)

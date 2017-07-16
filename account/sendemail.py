# coding=utf-8
from random import Random
from django.core.mail import send_mail
from face.settings import EMAIL_FROM

from account.models import Account
import token


def sendemails(username):
    email_title = u"邮箱验证"
    token_ = token.generate_validate_token(username)
    to_email = Account.objects.get(username=username).email
    message = "\n".join(u"请点击以下连接完成邮箱验证:http://127.0.0.1:8000/account/active/{0}".format(token_))
    send_mail(email_title, message, EMAIL_FROM, ["{0}".format(to_email)], fail_silently=False)
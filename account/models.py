# coding=utf-8
from django.db import models
from django.contrib.auth import hashers, authenticate
from django.contrib.auth.models import User

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError

import re

# TYPE_CHIOCE = {
#     "email": 1,
#     "username": 2
# }

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(verbose_name=u"用户名", max_length=255, unique=True)
    password = models.CharField(verbose_name=u"密码", max_length=255, blank=True, null=True)
    email = models.EmailField(verbose_name=u"注册邮箱", unique=True)
    isverify = models.BooleanField(verbose_name=u"邮箱是否已验证", default=False)

    @staticmethod
    def new_account(username, password, email):
        user_query = User.objects.filter(username=username)
        if user_query:
            raise IntegrityError
        else:
            new_user = User.objects.create_user(username=username, password=password)
            new_account = Account.objects.create(user=new_user, username=username, email=email)
            new_account.build_password(password)

    @staticmethod
    def account_login(username_or_email, password):
        try:
            validate_email(username_or_email)
            account = Account.objects.get(email=username_or_email)
            result_ = account.verify_password(password)
            if result_:
                username = account.username
                user = authenticate(username=username, password=password)
                if user:
                    return True, user
                else:
                    return False, u"账号异常"
            else:
                return False, u"密码错误"
        except Account.DoesNotExist:
            return False, u"用户不存在"
        except ValidationError:
            account = Account.objects.get(username=username_or_email)
            result_ = account.verify_password(password)
            if result_:
                user = authenticate(username=username_or_email, password=password)
                if user:
                    return True, user
                else:
                    return False, u"账号异常"
            else:
                return False, u"密码错误"

    @staticmethod
    def check_password(password, rpassword):
        if password == rpassword:
            return True
        else:
            return False

    @staticmethod
    def check_username(username):
        pattern = re.compile("([~!@#$%^&\\*()_+\\-=;':\",\\./<>?|\\s]|drop|delete|truncate|and|or)")
        result = pattern.search(username)
        return not result

    def build_password(self, raw_password):
        enpassword = hashers.make_password(raw_password)
        self.password = enpassword
        self.save()

    def verify_password(self, raw_password):
        result = hashers.check_password(raw_password, self.password)
        return result

    # @staticmethod
    # def check_type(uname_or_email):
    #     if uname_or_email.contain("@"):
    #         return TYPE_CHIOCE["email"]
    #     else:
    #         return TYPE_CHIOCE["username"]


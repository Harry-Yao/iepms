import re
from django import forms
# from captcha.fields import CaptchaField

__author__ = 'harry yao'
__date__ = '2017/11/27 11:22'


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, min_length=5)
    type = forms.IntegerField(required=True)
    college = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    re_password = forms.CharField(required=True, min_length=5)
    # captcha = CaptchaField(error_messages={"invalid": "验证码错误"})







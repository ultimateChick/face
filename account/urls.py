from django.conf.urls import include, url

from account.views import *
from account.sendemail import *

urlpatterns = [
    url(r"^login/$", view=login),
    url(r"^register/$", view=register),
    url(r"^active/(.+)$", view=activate),
    url(r"^sendemail/$", view=sendemails)
]
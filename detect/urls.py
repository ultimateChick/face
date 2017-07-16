from django.conf.urls import url

from detect.views import *

urlpatterns = [
    url(r"", view=detect)
]
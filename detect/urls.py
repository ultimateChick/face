from django.conf.urls import url

from detect.views import *

urlpatterns = [
    url(r"^$", view=detect),
    # url(r"test", view=request_detect)
]
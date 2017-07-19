from django.conf.urls import url

from detect.views import *

urlpatterns = [
    url(r"^$", view=render_detect_page),
    url(r"^api/$", view=detect)
    # url(r"test", view=request_detect)
]
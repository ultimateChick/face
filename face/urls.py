"""face URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib.staticfiles import views
from django.contrib import admin

from account.views import render_page
from detect.views import render_detect_page, render_main_page, render_compare_page
# from face.settings import STATIC_ROOT


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include("account.urls")),
    url(r'^detect/', include("detect.urls")),
    url(r'^compare/', include("compare.urls")),
    url(r'^$', view=render_page),
    url(r"^home/$", view=render_main_page),
    url(r"^detect/$", view=render_detect_page),
    # url(r"^compare/$", view=render_compare_page),
    # url(r'^static/(?P<path>.*)$', views.serve, {'document_root': STATIC_ROOT}),
]

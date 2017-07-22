from django.conf.urls import url

from compare.views import render_compare_page

urlpatterns = [
    url(r"^$", view=render_compare_page)
]
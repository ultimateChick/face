from django.conf.urls import url

from compare.views import render_compare_page, compare


urlpatterns = [
    url(r"^$", view=render_compare_page),
    url(r"^api/$", view=compare)
]
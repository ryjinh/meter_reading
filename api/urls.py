"""
URLConf for the REST API
"""
from django.urls import path
from . import views


urlpatterns = [
    path("v1/mpan/<str:mpan_core>/readings/", views.readings_by_mpan),
]

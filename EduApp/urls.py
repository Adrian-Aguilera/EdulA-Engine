from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test, name='test'),
    path("get-request", views.get_option, name="getoption"),
    path("get-response", views.get_response, name="message input")
]
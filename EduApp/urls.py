from django.urls import path
from . import views

urlpatterns = [
    path("get-general-chat", views.get_general_chat, name="chat general"),
    path("get-response-av", views.get_response_AV, name="chat av"),
]
from django.urls import path
from . import views

urlpatterns = [
    path("general/chat", views.get_general_chat, name="chat general"),
    path("Asistente/chat", views.get_response_AV, name="chat av"),
    path('admin/Model/create', views.createModelCustom, name="modelCustom"),
]
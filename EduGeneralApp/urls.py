from django.urls import path
from .views import GeneralEdula

urlpatterns = [
    path("general/chat", GeneralEdula.get_general_chat, name="chat general"),
]
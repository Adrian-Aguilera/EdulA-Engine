from django.urls import path
from .views import AVEdula
urlpatterns = [
    path("asistente/chat", AVEdula.get_response_AV, name="chat av"),
]
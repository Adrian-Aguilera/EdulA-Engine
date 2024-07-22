from django.urls import path
from .views import GeneralEdula, AVEdula, DataToChromaDB

urlpatterns = [
    path("general/chat", GeneralEdula.get_general_chat, name="chat general"),
    path("asistente/chat", AVEdula.get_response_AV, name="chat av"),
    path("info/config/activacion/general", DataToChromaDB.activateGeneralMode, name='activacion de configuracion')
]
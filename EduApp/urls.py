from django.urls import path
from .views import GeneralEdula, DataToChromaDB

urlpatterns = [
    path("general/chat", GeneralEdula.get_general_chat, name="chat general"),
    path("info/config/activacion/general", DataToChromaDB.activateGeneralMode, name='activacion de configuracion')
]
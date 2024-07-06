from django.urls import path
from .views import CustomModel
urlpatterns = [
    path('Model/create', CustomModel.createModelCustom, name="modelCustom"),
]
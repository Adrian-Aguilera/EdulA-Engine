from django.urls import path
from .views import CustomModel
urlpatterns = [
    path('admin/Model/create', CustomModel.createModelCustom, name="modelCustom"),
]
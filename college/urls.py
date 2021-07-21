from django.urls import path
from .views import userform,dashboard,college

urlpatterns = [
    path('userform/',userform,name='userform'),
    path('dashboard/',dashboard,name='dashboard'),
    path('<str:c_id>/',college,name='college'),
]
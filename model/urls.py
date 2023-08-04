from django.urls import path 
from . import views 


app_name = "model"
urlpatterns = [
    path('', views.index , name='index'),
    path('signup/' , views.signup , name="signup"),
    path('dashboard/' , views.dashboard , name='dashboard')
]
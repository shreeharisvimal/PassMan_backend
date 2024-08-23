from django.urls import path
from . import views


urlpatterns = [
    path('create_new_password/', views.PasswordCreateApi.as_view(), name='create_new_password'),
    path('new_password/', views.PasswordApi.as_view(), name='new_password'),
    path('new_password/<int:id>/', views.PasswordApi.as_view(), name='password-delete'),

]

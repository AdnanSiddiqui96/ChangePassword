from django.urls import path,include
from api.views import *

urlpatterns = [




path('login',login.as_view()),
path('Register',Register.as_view()),



path('Add_Admin',AdminRegister.as_view()),
path('AdminLogin',login.as_view()),
path('change-password', ChangePassword.as_view()),
]



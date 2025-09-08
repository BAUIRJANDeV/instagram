from .views import SignupView,VerifyCodeApiView,GetNewCodeVerify,ChangeInfoUserApi
from django.urls import path

urlpatterns=[
    path('signup/',SignupView.as_view()),
    path('code-verify/',VerifyCodeApiView.as_view()),
    path('new-verify/',GetNewCodeVerify.as_view()),
    path('change-info/',ChangeInfoUserApi.as_view()),

]
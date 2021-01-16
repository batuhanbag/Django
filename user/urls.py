from django.contrib import admin
from django.urls import path, include
from . import views
from django_email_verification import urls as mail_urls
app_name = "user"

urlpatterns = [
    
    path('register/',views.register,name = "register"),
    path('login/',views.loginUser,name = "login"),
    path('logout/',views.logoutUser,name = "logout"),
    path('termscon/',views.Terms,name = "termscon"),
    path('email/', include(mail_urls)),
    path('confirm/',views.confirm,name = "confirm"),
    path('success/',views.success,name = "success"),

]

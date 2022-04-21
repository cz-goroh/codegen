"""codegen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from GenCheck.views import GenerateView, Logout, CheckCode
urlpatterns = [
    path('api/generate/', GenerateView.as_view()),
    path('api/check_code/', CheckCode.as_view()),
    path('admin/', admin.site.urls),
    path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/logout/', Logout.as_view()),
]

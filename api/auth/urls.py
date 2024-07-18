from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('profile/', views.RedactorProfileApiView.as_view({
        'get': 'get',
        'post': 'post',
        'put': 'put',
        'patch': 'patch',
    })),
]

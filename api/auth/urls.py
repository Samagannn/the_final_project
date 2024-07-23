from django.urls import path
from . import views
from account.views import become_candidate, become_admin

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('become_candidate/', become_candidate, name='become_candidate'),
    path('become_admin/', become_admin, name='become_admin'),
    path('profile/', views.RedactorProfileApiView.as_view({
        'get': 'get',
        'post': 'post',
        'put': 'put',
        'patch': 'patch',
    })),
]

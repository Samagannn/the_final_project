from . import views
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import ElectionViewSet, CandidateViewSet, VoterViewSet, VoteViewSet

router = DefaultRouter()
router.register('elections', ElectionViewSet)
router.register('candidates', CandidateViewSet)
router.register('votes', VoteViewSet)
router.register('voter', VoterViewSet)
# router.register('products', views.ProductViewSet)


urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('', include(router.urls)),
]


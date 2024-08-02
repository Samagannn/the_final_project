from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .auth.views import SortedVotesView
from .views import ElectionViewSet, CandidateViewSet, VoterViewSet, VoteViewSet

router = DefaultRouter()
router.register('elections', ElectionViewSet)
router.register('candidates', CandidateViewSet)
router.register('votes', VoteViewSet)
router.register('voter', VoterViewSet)

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('', include(router.urls)),
    path('sorted-votes/', SortedVotesView.as_view(), name='sorted-votes'),
]

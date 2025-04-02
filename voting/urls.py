from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ElectionViewSet, CandidateViewSet, ElectionVoteViewSet,
    PollViewSet, ChoiceViewSet, PollVoteViewSet
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Роутер для ViewSet'ов
router = DefaultRouter()
router.register(r'elections', ElectionViewSet)
router.register(r'candidates', CandidateViewSet)
router.register(r'election-votes', ElectionVoteViewSet)  # Разделение голосов за кандидатов
router.register(r'polls', PollViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'poll-votes', PollVoteViewSet)  # Голосование в опросах

urlpatterns = [
    # Основной API
    path('api/', include(router.urls)),

    # JWT-аутентификация вынесена в /api/auth/
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Подключение маршрутов для управления пользователями
    path('api/user/', include('user.urls')),
]

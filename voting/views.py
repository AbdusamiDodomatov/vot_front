from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Election, Candidate, ElectionVote, Poll, Choice, PollVote
from .serializers import (
    ElectionSerializer, CandidateSerializer, ElectionVoteSerializer,
    PollSerializer, ChoiceSerializer, PollVoteSerializer
)


class ElectionViewSet(viewsets.ModelViewSet):
    """API для выборов"""
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CandidateViewSet(viewsets.ModelViewSet):
    """API для кандидатов"""
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ElectionVoteViewSet(viewsets.ModelViewSet):
    """API для голосов на выборах"""
    queryset = ElectionVote.objects.all()
    serializer_class = ElectionVoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Один пользователь может голосовать только один раз"""
        election_id = request.data.get("election")
        
        if ElectionVote.objects.filter(election_id=election_id, user=request.user).exists():
            return Response({"error": "Вы уже голосовали в этих выборах."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class PollViewSet(viewsets.ModelViewSet):
    """API для опросов"""
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """Только администраторы могут создавать опросы"""
        if not request.user.is_staff:  # Проверяем, является ли пользователь админом
            return Response(
                {"error": "Только администраторы могут создавать опросы."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)


class ChoiceViewSet(viewsets.ModelViewSet):
    """API для вариантов ответов в опросах"""
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PollVoteViewSet(viewsets.ModelViewSet):
    """API для голосов в опросах"""
    queryset = PollVote.objects.all()
    serializer_class = PollVoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Один пользователь может голосовать только один раз в одном опросе"""
        poll_id = request.data.get("poll")

        if PollVote.objects.filter(poll_id=poll_id, user=request.user).exists():
            return Response({"error": "Вы уже голосовали в этом опросе."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

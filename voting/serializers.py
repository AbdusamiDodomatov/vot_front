from rest_framework import serializers
from .models import Election, Candidate, ElectionVote, Poll, Choice, PollVote


class ElectionSerializer(serializers.ModelSerializer):
    """Сериализатор для выборов"""
    class Meta:
        model = Election
        fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):
    """Сериализатор для кандидатов"""
    class Meta:
        model = Candidate
        fields = '__all__'


class ElectionVoteSerializer(serializers.ModelSerializer):
    """Сериализатор для голосов на выборах"""
    class Meta:
        model = ElectionVote
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    """Сериализатор для вариантов ответа в опросах"""
    class Meta:
        model = Choice
        fields = "__all__"


class PollSerializer(serializers.ModelSerializer):
    """Сериализатор для опросов с вложенными вариантами ответа"""
    choices = ChoiceSerializer(many=True, read_only=True, source='choices.all')

    class Meta:
        model = Poll
        fields = "__all__"


class PollVoteSerializer(serializers.ModelSerializer):
    """Сериализатор для голосов в опросах"""
    class Meta:
        model = PollVote
        fields = "__all__"

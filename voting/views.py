from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Choice, PollVote
from django.contrib.auth.decorators import login_required
from django.db.models import Count


def index(request):
    """Главная страница со списком опросов"""
    polls = Poll.objects.all().order_by('-created_at')
    return render(request, 'voting/index.html', {'polls': polls})


def detail(request, pk):
    """Страница одного опроса с вариантами выбора"""
    poll = get_object_or_404(Poll, pk=pk)
    choices = poll.choices.all()
    return render(request, 'voting/detail.html', {'poll': poll, 'choices': choices})


@login_required
def vote(request, pk):
    """Обработка голосования пользователя"""
    poll = get_object_or_404(Poll, pk=pk)

    if PollVote.objects.filter(poll=poll, user=request.user).exists():
        return render(request, 'voting/already_voted.html', {'poll': poll})

    try:
        selected_choice_id = request.POST['choice']
        selected_choice = poll.choices.get(pk=selected_choice_id)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'voting/detail.html', {
            'poll': poll,
            'choices': poll.choices.all(),
            'error_message': "Вы не выбрали вариант.",
        })

    # Создаём голос
    PollVote.objects.create(
        poll=poll,
        choice=selected_choice,
        user=request.user
    )

    return redirect('voting:results', pk=poll.pk)


def results(request, pk):
    """Страница с результатами голосования"""
    poll = get_object_or_404(Poll, pk=pk)
    
    choices = poll.choices.annotate(
        vote_count=Count('votes')
    )

    total_votes = PollVote.objects.filter(poll=poll).count()

    return render(request, 'voting/results.html', {
        'poll': poll,
        'choices': choices,
        'total_votes': total_votes
    })



def create_poll(request):
    return render(request, 'voting/create.html')

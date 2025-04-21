from django.shortcuts import render, get_object_or_404, redirect
from .models import Election, Choice, Vote
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def vote_list(request):
    elections = Election.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())
    user_votes = Vote.objects.filter(user=request.user)
    voted_ids = [v.election_id for v in user_votes]
    return render(request, 'voting/vote_list.html', {
        'elections': elections,
        'voted_ids': voted_ids,
    })

@login_required
def vote_detail(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    if not election.is_active():
        messages.error(request, 'Ovoz berish mumkin emas.')
        return redirect('voting:vote_list')

    if Vote.objects.filter(user=request.user, election=election).exists():
        messages.info(request, 'Siz allaqachon ovoz bergansiz.')
        return redirect('voting:vote_list')

    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, pk=choice_id, election=election)

        # Засчитываем голос
        Vote.objects.create(user=request.user, election=election, choice=choice)
        choice.votes += 1
        choice.save()

        messages.success(request, 'Sizning ovozingiz qabul qilindi.')
        return redirect('voting:vote_list')

    return render(request, 'voting/vote_detail.html', {
        'election': election,
    })



def election_list(request):
    elections = Election.objects.all()
    user_votes = Vote.objects.filter(user=request.user)
    voted_ids = user_votes.values_list('election_id', flat=True)
    votes_dict = {vote.election_id: vote for vote in user_votes}

    return render(request, 'voting/election_list.html', {
        'elections': elections,
        'voted_ids': voted_ids,
        'votes_dict': votes_dict,  
    })

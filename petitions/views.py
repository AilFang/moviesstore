from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PetitionForm
from .models import Petition, Vote

def petition_list(request):
    petitions = Petition.objects.all().order_by('-created_at')
    return render(request, 'petitions/petition_list.html', {'petitions':petitions})
def petition_detail(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(petition=petition, user=request.user)
        except Vote.DoesNotExist:
            user_vote = None
    return render(request, 'petitions/petition_detail.html', {
        'petition': petition,
        'user_vote': user_vote,
    })

@login_required
def petition_create(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.created_by = request.user
            pet.save()
            return redirect('petitions:detail', pk=pet.pk)
    else:
        form = PetitionForm()
    return render(request, 'petitions/petition_form.html', {'form': form})

@login_required
def petition_vote(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    if request.method == 'POST':
        choice = request.POST.get('choice')
        if choice not in (Vote.CHOICE_YES, Vote.CHOICE_NO):
            # invalid choice, redirect
            return redirect('petitions:detail', pk=pk)
        vote, created = Vote.objects.update_or_create(
            petition=petition,
            user=request.user,
            defaults={'choice': choice}
        )
        return redirect('petitions:detail', pk=pk)
    return redirect('petitions:detail', pk=pk)
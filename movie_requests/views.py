from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MovieRequestForm
from .models import MovieRequest

@login_required
def movie_requests(request):
    # Handle new request submission
    if request.method == "POST" and "add_request" in request.POST:
        form = MovieRequestForm(request.POST)
        if form.is_valid():
            movie_request = form.save(commit=False)
            movie_request.user = request.user
            movie_request.save()
            return redirect("movie_requests")
    else:
        form = MovieRequestForm()

    # Handle deletion
    if request.method == "POST" and "delete_request" in request.POST:
        request_id = request.POST.get("request_id")
        movie_request = get_object_or_404(MovieRequest, id=request_id, user=request.user)
        movie_request.delete()
        return redirect("movie_requests")

    # Fetch only the current user's requests
    user_requests = MovieRequest.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "movie_requests/movie_requests.html", {
    "form": form,
    "user_requests": user_requests
    })


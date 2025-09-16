from django import forms
from .models import MovieRequest

class MovieRequestForm(forms.ModelForm):
    class Meta:
        model = MovieRequest
        fields = ["movie_name", "description"]

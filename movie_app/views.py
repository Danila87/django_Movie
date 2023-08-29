from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
# Create your views here.


class AllMovies(ListView):
    pass


class AllPersons(ListView):
    pass


class MainView(DetailView):
    pass


class AboutMovie(DetailView):
    pass


class AboutPerson(DetailView):
    pass


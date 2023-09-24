from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import ModelFormMixin
from django.db.models import Q

from datetime import date
from . import forms
from . import models
# Create your views here.


def main_view(request):
    user = request.user
    context = {'user': user}
    return render(request, 'index.html', context=context)


# TODO Нужно создать отдельный класс для выведения фильтра
class AllMovies(ListView):

    model = models.Movie
    template_name = 'all_movie.html'
    context_object_name = 'movies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = models.Country.objects.all()
        context['genres'] = models.Genre.objects.all()
        context['ratings_mpaa'] = self.model.RATING_MPAA
        return context

    def get_queryset(self):
        if self.request.GET:
            order_field = self.request.GET['filter']
            return models.Movie.objects.all().order_by(order_field)
        else:
            return models.Movie.objects.all()


class AllMoviesFilter(AllMovies):

    def get_queryset(self):

        movies = models.Movie.objects.all()

        if self.request.GET.get('date_start') and self.request.GET.get('end_date'):
            date_start = self.request.GET.get('date_start')
            end_date = self.request.GET.get('end_date')
            movies = movies.filter(data_release__range=(date_start, end_date))

        elif self.request.GET.get('date_start'):
            movies = movies.filter(data_release__gte=self.request.GET.get('date_start'))

        elif self.request.GET.get('end_date'):
            movies = movies.filter(data_release__lte=self.request.GET.get('end_date'))

        for key in self.request.GET:

            if not self.request.GET.get(key):
                continue

            if key == 'country':
                movies = movies.filter(country__in=self.request.GET.getlist(key))
                continue

            if key == 'genre':
                movies = movies.filter(genre__in=self.request.GET.getlist(key)).distinct()
                continue

            if key == 'world_rating':
                movies = movies.filter(world_rating__gte=self.request.GET.get(key))
                continue

            if key == 'rating_mpaa':
                print(self.request.GET.getlist(key))
                movies = movies.filter(rating_mpaa__in=self.request.GET.getlist(key))
                continue

        return movies


class AllRewards(ListView):
    pass


class AboutReward(DetailView):
    pass


class AllPersons(ListView):
    pass


class AboutMovie(ModelFormMixin, DetailView):

    model = models.Movie

    template_name = 'detail_movie.html'
    slug_url_kwarg = 'slug_movie'

    context_object_name = 'movie'

    form_class = forms.ReviewForm
    date_today = date.today()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        persons_for_type = {}

        for type_p in models.TypePerson.objects.all():

            type_key = type_p

            if len(self.object.persons.filter(movieperson__type_person=type_p)) > 1:
                type_key = str(type_p.name)+'ы'

            persons_for_type[type_key] = self.object.persons.filter(movieperson__type_person=type_p)

        context['all_persons'] = persons_for_type
        context['type_persons'] = models.TypePerson.objects.all()

        reviews = self.object.reviews
        context['movie_reviews'] = reviews

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.film = self.get_object()
            data.date_review = self.date_today
            data.user = self.request.user
            data.save()
            return HttpResponseRedirect(request.path)


class AboutPerson(DetailView):

    model = models.Person

    template_name = 'detail_person.html'
    context_object_name = 'person'
    slug_url_kwarg = 'slug_person'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        all_movies_with_types = {}

        if self.request.GET:
            movies = self.object.all_films.filter(movieperson__type_person=self.request.GET['filter'])
            context['selected_type'] = models.TypePerson.objects.get(id=self.request.GET['filter'])
        else:
            movies = self.object.all_films

        for movie in movies:

            types_person = []

            for type_p in movie.movieperson_set.filter(person_id=self.object):
                types_person.append(type_p.type_person)

            all_movies_with_types[movie] = types_person

        context['all_movies'] = all_movies_with_types
        context['types_person'] = self.object.type_person.all()

        return context


class LoginUser(LoginView):

    template_name = 'account/login.html'
    form_class = forms.AuthenticationUserForm

    def get_success_url(self):
        return reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['width'] = '4'
        return context


class RegisterUser(CreateView):

    form_class = forms.FormRegisterUser

    template_name = 'account/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['width'] = '6'
        return context


class UserProfile(DetailView):
    pass


class UserProfileSettings(DetailView):
    pass


def user_logout(request):
    logout(request)
    return redirect('all_movies')

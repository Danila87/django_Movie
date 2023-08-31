from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from . import forms
# Create your views here.


def main_view(request):
    user = request.user
    context = {'user': user}
    return render(request, 'index.html', context=context)


class AllMovies(ListView):
    pass


class AllRewards(ListView):
    pass


class AboutReward(DetailView):
    pass


class AllPersons(ListView):
    pass


class AboutMovie(DetailView):
    pass


class AboutPerson(DetailView):
    pass


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
    return redirect('main')

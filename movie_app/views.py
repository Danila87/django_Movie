from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
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


class LoginUser:
    pass


class RegisterUser:
    pass

class UserProfile:
    pass


class UserProfileSettings:
    pass


def user_logout(request):
    return None
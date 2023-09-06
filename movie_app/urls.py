from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.main_view, name='main'),

    path('movie/', views.AllMovies.as_view(), name='all_movies'),
    path('movie/filter', views.AllMoviesFilter.as_view(), name='all_movie_filter'),
    path('persons/', views.AllPersons.as_view(), name='all_persons'),
    path('rewards/', views.AllRewards.as_view(), name='all_rewards'),

    path('account/', include([

        path('login', views.LoginUser.as_view(), name='login'),
        path('registration', views.RegisterUser.as_view(), name='registration'),
        path('logout', views.user_logout, name='logout'),
        path('profile', views.UserProfile.as_view(), name='user_profile'),
        path('profile_settings', views.UserProfileSettings.as_view(), name='user_settings')

    ])),

    path('movie/<slug:slug_movie>', views.AboutMovie.as_view(), name='about_movie'),
    path('persons/<slug:slug_person>', views.AboutPerson.as_view(), name='about_person'),
    path('rewards/<slug:slug_rewars>', views.AboutReward.as_view(), name='about_reward'),

]
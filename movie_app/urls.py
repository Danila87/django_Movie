from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.main_view, name='main'),

    path('movie/', views.AllMovies.as_view(), name='all_movies'),
    path('persons/', views.AllPersons.as_view(), name='all_persons'),
    path('rewards/', views.AllRewards.as_view(), name='all_rewards'),

    path('account/', include([

        path('account/login', views.LoginUser.as_view(), name='login'),
        path('account/registration', views.RegisterUser.as_view(), name='registration'),
        path('account/logout', views.user_logout, name='logout'),
        path('account/profile', views.UserProfile.as_view(), name='user_profile'),
        path('account/profile_settings', views.UserProfileSettings.as_view(), name='user_settings')

    ])),

    path('movie/<slug:slug_movie>', views.AboutMovie.as_view(), name='about_movie'),
    path('persons/<slug:slug_person>', views.AboutPerson.as_view(), name='about_person'),
    path('rewards/<slug:slug_rewars>', views.AboutReward.as_view(), name='about_reward'),

]
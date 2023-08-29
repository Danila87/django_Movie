from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('movie/', views.AllMovies.as_view(), name='all_views'),
    path('persons/', views.AllPersons.as_view(), name='all_persons'),
    path('movie/<slug:slug_movie>', views.AboutMovie.as_view(), name='about_movie'),
    path('persons/<slug:slug_person>', views.AboutPerson.as_view(), name='about_person'),
]
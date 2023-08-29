from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=30)


class Genre(models.Model):
    name = models.CharField(max_length=30)


class TypePerson(models.Model):
    name = models.CharField(max_length=30)


class Person(models.Model):

    MALE = 'M'
    FEMALE = 'F'

    GENDERS = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    ]

    name = models.CharField(max_length=30)
    gender = models.CharField(choices=GENDERS, max_length=1)
    description = models.TextField()
    date_born = models.DateField()
    place_born = models.CharField(max_length=100)

    img = models.ImageField(upload_to='person_photo/%Y/%m/%d')
    slug = models.SlugField(default='')

    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    type_person = models.ManyToManyField(TypePerson)


class Reward(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to='rewards_photo/%Y/%m/%d', null=True, blank=True)


class Movie(models.Model):

    MPAA_G = 'G'
    MPAA_PG = 'PG'
    MPAA_PG13 = 'PG13'
    MPAA_R = 'R'
    MPAA_NC13 = 'NC17'

    RATING_MPAA = [
        (MPAA_G, 'Рейтинг G — Нет возрастных ограничений'),
        (MPAA_PG, 'Рейтинг PG — Рекомендуется присутствие родителей'),
        (MPAA_PG13, 'Рейтинг PG-13 — Детям до 13 лет просмотр не желателен'),
        (MPAA_R, 'Рейтинг R — Лицам до 17 лет обязательно присутствие взрослого'),
        (MPAA_NC13, 'Рейтинг NC-17 — Лицам до 18 лет просмотр запрещен')
    ]

    name = models.CharField(max_length=50)
    tagline = models.CharField(max_length=200)
    description = models.TextField(null=True)

    img = models.ImageField(upload_to='movie_photos/%Y/%m/%d', null=True, blank=True)
    video = models.FileField(upload_to='movie_video/%Y/%m/%d', null=True, blank=True)

    slug = models.SlugField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    genre = models.ManyToManyField(Genre)

    persons = models.ManyToManyField(Person)

    budget = models.IntegerField(null=True, blank=True)
    fees = models.IntegerField(null=True, blank=True)

    data_release = models.IntegerField()  # Тут важен именно год, а не точная дата поэтому Integer

    world_rating = models.FloatField(null=True, blank=True)
    user_rating = models.FloatField(null=True, blank=True)

    rating_mpaa = models.CharField(max_length=4, choices=RATING_MPAA)

    rewards = models.ManyToManyField(Reward)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='Пользователь удален')
    text_review = models.TextField()
    date_review = models.DateField()
    user_rating = models.FloatField()
    film = models.ForeignKey(Movie, on_delete=models.CASCADE)
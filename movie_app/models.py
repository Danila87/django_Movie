from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from datetime import date
from django.utils.text import slugify
from .service import transliteration
# Create your models here.


class Country(models.Model):

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Genre(models.Model):

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TypePerson(models.Model):

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


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
    slug = models.SlugField(null=True, blank=True)

    genre = models.ManyToManyField(Genre)
    type_person = models.ManyToManyField(TypePerson)

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('about_person', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(transliteration(self.name))
        super(Person, self).save(*args, **kwargs)

    @property
    def all_films(self):
        return self.movie_set.all()

    @property
    def age(self):
        now_year = date.today().year
        return now_year - self.date_born.year


class Reward(models.Model):

    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to='rewards_photo/%Y/%m/%d', null=True, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('about_reward', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Reward, self).save(*args, **kwargs)

    @property
    def all_film(self):
        return self.movie_set.all()


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
    tagline = models.CharField(max_length=200, default='-')
    description = models.TextField(null=True)

    img = models.ImageField(upload_to='movie_photos/%Y/%m/%d', null=True, blank=True)
    trailer = models.FileField(upload_to='movie_video_trailer/%Y/%m/%d', null=True, blank=True)
    video = models.FileField(upload_to='movie_video/%Y/%m/%d', null=True, blank=True)

    slug = models.SlugField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    genre = models.ManyToManyField(Genre)

    persons = models.ManyToManyField(Person, through='MoviePerson')

    budget = models.IntegerField(null=True, blank=True)
    fees = models.IntegerField(null=True, blank=True)

    data_release = models.IntegerField()

    world_rating = models.FloatField(null=True, blank=True)
    user_rating = models.FloatField(null=True, blank=True)

    rating_mpaa = models.CharField(max_length=4, choices=RATING_MPAA)

    rewards = models.ManyToManyField(Reward, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

    def get_url(self):
        return reverse('about_movie', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(transliteration(self.name))
        super(Movie, self).save(*args, **kwargs)

    @property
    def current_user_rating(self):
        return self.user_rating

    @current_user_rating.setter
    def current_user_rating(self, new_value, *args, **kwargs):

        overall_rating = 0

        for review in self.reviews:
            overall_rating += review.user_rating

        if len(self.review_set.all()) == 1:
            self.user_rating = new_value

        else:
            self.user_rating = overall_rating / (len(self.review_set.all()))

        super(Movie, self).save(*args, **kwargs)

    @property
    def reviews(self):
        return self.review_set.all()


class Review(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='Пользователь удален')
    text_review = models.TextField()
    date_review = models.DateField()
    user_rating = models.FloatField()
    film = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        super(Review, self).save(*args, **kwargs)

        self.film.current_user_rating = self.user_rating


class MoviePerson(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    type_person = models.ForeignKey(TypePerson, on_delete=models.PROTECT)
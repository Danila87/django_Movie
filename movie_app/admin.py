from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Reward)
admin.site.register(models.Genre)
admin.site.register(models.Country)


class MembershipInline(admin.TabularInline):
    model = models.MoviePerson
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]


class PersonAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]


class TypePersonAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]


admin.site.register(models.Movie, MovieAdmin)
admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.TypePerson, TypePersonAdmin)
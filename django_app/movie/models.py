from django.db import models

from mysite import settings
from mysite.utils.models import BaseModel


class Genre(models.Model):
    genre = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.genre


class Grade(models.Model):
    grade = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.grade


class MakingCountry(models.Model):
    making_country = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.making_country


class Actor(models.Model):
    # 다음 배우 id
    daum_id = models.IntegerField(unique=True, primary_key=True)
    name_kor = models.CharField(max_length=100)
    name_eng = models.CharField(max_length=100, blank=True)
    profile_url = models.TextField()


# class ActorRole(models.Model):
#     role = models.CharField(max_length=30)


class Director(models.Model):
    # 다음 배우 id
    daum_id = models.IntegerField(unique=True, primary_key=True)
    name_kor = models.CharField(max_length=100)
    name_eng = models.CharField(max_length=100)
    profile_url = models.TextField()


class Movie(models.Model):
    # 다음 영화 id
    daum_id = models.IntegerField(unique=True, primary_key=True)
    # 영화 제목
    title_kor = models.CharField(max_length=100)
    title_eng = models.CharField(max_length=100, blank=True)
    # M2M 정보
    genre = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor, through='MovieActor')
    director = models.ManyToManyField(Director)
    # 기타정보
    making_country = models.ManyToManyField(MakingCountry)
    grade = models.ForeignKey(Grade)
    created_year = models.IntegerField()
    img_url = models.TextField()
    run_time = models.CharField(max_length=30)
    synopsis = models.TextField()
    # 옵션정보
    # accumulated_viewers = models.IntegerField(blank=True)
    Release_date = models.CharField(max_length=30, blank=True)


class MovieImages(models.Model):
    movie = models.ForeignKey(Movie)
    url = models.CharField(max_length=100)


class MovieActor(models.Model):
    movie = models.ForeignKey(Movie)
    actor = models.ForeignKey(Actor)
    # actor_role = models.ForeignKey(ActorRole)
    character_name = models.CharField(max_length=30)


class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    movie = models.ForeignKey(Movie)
    star = models.IntegerField()
    content = models.CharField(max_length=100, blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CommentLike', related_name='comment_set_like_users')

    class Meta:
        unique_together = (('author', 'movie'),)


class CommentLike(BaseModel):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class FamousLine(BaseModel):
    movie = models.ForeignKey(Movie)
    actor = models.ForeignKey(Actor)
    content = models.CharField(max_length=100)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='FamousLike')


class FamousLike(BaseModel):
    famous_line = models.ForeignKey(FamousLine)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class BoxOfficeMovie(models.Model):
    movie = models.ForeignKey(Movie)
    ticketing_rate = models.FloatField(max_length=10)
    img_url = models.TextField()


class Magazine(BaseModel):
    movie = models.ForeignKey(Movie)
    title = models.CharField(max_length=300)
    content = models.TextField()
    author = models.CharField(max_length=30)
    magazine_created_date = models.DateField()

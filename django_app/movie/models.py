from django.db import models

from mysite import settings
from mysite.utils.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator


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
    daum_id = models.IntegerField(unique=True)
    name_kor = models.CharField(max_length=100)
    name_eng = models.CharField(max_length=100, blank=True)
    profile_url = models.TextField()

    def __str__(self):
        return self.name_kor


# class ActorRole(models.Model):
#     role = models.CharField(max_length=30)


class Director(models.Model):
    # 다음 배우 id
    daum_id = models.IntegerField(unique=True)
    name_kor = models.CharField(max_length=100)
    name_eng = models.CharField(max_length=100)
    profile_url = models.TextField()

    def __str__(self):
        return self.name_kor


class Movie(models.Model):
    # 다음 영화 id
    daum_id = models.IntegerField(unique=True)
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
    main_trailer = models.TextField()
    videos = models.TextField()
    run_time = models.CharField(max_length=30)
    synopsis = models.TextField()
    # 옵션정보
    # accumulated_viewers = models.IntegerField(blank=True)
    Release_date = models.CharField(max_length=30, blank=True)


    @property
    def star_average(self):
        try:
            movie_star = [comment.star for comment in Comment.objects.filter(movie_id=self.pk)]
            average = sum(movie_star) / len(movie_star)
            return average
        except:
            return float()

    def __str__(self):
        return self.title_kor


class MovieImages(models.Model):
    movie = models.ForeignKey(Movie)
    url = models.CharField(max_length=100)


class MovieActor(models.Model):
    movie = models.ForeignKey(Movie)
    actor = models.ForeignKey(Actor)
    # actor_role = models.ForeignKey(ActorRole)
    character_name = models.CharField(max_length=30)

    def __str__(self):
        return self.character_name


class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    movie = models.ForeignKey(Movie)
    star = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    content = models.CharField(max_length=100, blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CommentLike', related_name='comment_set_like_users')

    class Meta:
        unique_together = (('author', 'movie'),)

    def __str__(self):
        return 'commnt' + self.movie.__str__() + '|' + self.author.__str__()

    @property
    def likes_count(self):
        return self.commentlike_set.count()

    @property
    def movie_title(self):
        return Movie.objects.get(id=self.movie.pk).title_kor


class CommentLike(BaseModel):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.comment.__str__() + '|' + self.user.__str__()


class FamousLine(BaseModel):
    movie = models.ForeignKey(Movie)
    actor = models.ForeignKey(Actor)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='FamousLineAuthor')
    content = models.CharField(max_length=100)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='FamousLike')

    def __str__(self):
        return 'famousLine' + self.movie.__str__() + '|' + self.author.__str__()

    @property
    def likes_count(self):
        return self.famouslike_set.count()

    @property
    def movie_title(self):
        return Movie.objects.get(id=self.movie.pk).title_kor

    @property
    def actor_kor_name(self):
        return Actor.objects.get(id=self.actor.pk).name_kor

    @property
    def actor_character_name(self):
        return MovieActor.objects.get(movie=self.movie, actor=self.actor).character_name


class FamousLike(BaseModel):
    famous_line = models.ForeignKey(FamousLine)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class BoxOfficeMovie(BaseModel):
    rank = models.IntegerField(default=0)
    movie = models.ForeignKey(Movie)
    release_date = models.DateField()
    ticketing_rate = models.FloatField(max_length=10)

    @property
    def movie_title(self):
        return Movie.objects.get(id=self.movie.pk).title_kor


class Magazine(BaseModel):
    #duam_id
    mag_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    img_url = models.TextField()
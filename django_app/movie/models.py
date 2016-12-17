from django.db import models

from mysite import settings
from mysite.utils.models import BaseModel


class Genre(models.Model):
    content = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.content


class Grade(models.Model):
    content = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.content


class MakingCountry(models.Model):
    content = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.content


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


class Movie(BaseModel):
    # 다음 영화 id
    daum_id = models.IntegerField(unique=True)
    # 영화 제목
    title_kor = models.CharField(max_length=100)
    title_eng = models.CharField(max_length=100, blank=True)
    # M2M 정보
    genre = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor, through='MovieActor')
    director = models.ManyToManyField(Director)
    # 평가내용
    star_sum = models.FloatField(default=0.0)
    comment_count = models.IntegerField(default=0)
    star_average = models.FloatField(default=0.0)
    # 기타정보
    making_country = models.ManyToManyField(MakingCountry)
    grade = models.ForeignKey(Grade)
    created_year = models.IntegerField()
    main_image_url = models.TextField()
    img_url = models.TextField()
    main_trailer = models.TextField()
    videos = models.TextField()
    run_time = models.CharField(max_length=30)
    synopsis = models.TextField()
    # 옵션정보
    # accumulated_viewers = models.IntegerField(blank=True)
    # Release_date = models.CharField(max_length=30, blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='MovieLike', related_name='movie_set_like_users')
    likes_count = models.IntegerField(default=0)
    comment_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Comment', related_name='movie_set_comment_users')

    def __str__(self):
        return self.title_kor

    # @property
    # def likes_count(self):
    #     return self.movielike_set.count()

    @property
    def score_created_year(self):
        import datetime
        current_year = datetime.datetime.now().year
        year = self.created_year
        base_score = 5
        while base_score > 0:
            if year == current_year:
                return base_score
            else:
                current_year -= 1
                base_score -= 1
        return base_score

    @property
    def score_star_average(self):
        star_average = self.star_average
        base_score = 5
        star_evaluation = 5.0
        while base_score > 0:
            if star_average == star_evaluation:
                return base_score
            else:
                base_score -= 1
                star_evaluation -= 0.5
        return base_score

    @property
    def score_like_users(self):
        like_users = len(self.like_users.all())
        base_score = 5
        like_users_evaluation = 10
        while base_score > 0:
            if like_users >= like_users_evaluation:
                return base_score
            else:
                base_score -= 1
                like_users_evaluation -= 2
        return base_score


class MovieImages(models.Model):
    movie = models.ForeignKey(Movie)
    url = models.TextField()


class MovieActor(models.Model):
    movie = models.ForeignKey(Movie)
    actor = models.ForeignKey(Actor)
    # actor_role = models.ForeignKey(ActorRole)
    character_name = models.CharField(max_length=30)

    def __str__(self):
        return self.character_name


class Comment(BaseModel):
    STAR_CHOICES = (
        (0.0, 0),
        (0.5, 0.5),
        (1.0, 1),
        (1.5, 1.5),
        (2.0, 2),
        (2.5, 2.5),
        (3.0, 3),
        (3.5, 3.5),
        (4.0, 4),
        (4.5, 4.5),
        (5.0, 5),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    movie = models.ForeignKey(Movie)
    star = models.FloatField(choices=STAR_CHOICES)
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


class MovieLike(BaseModel):
    movie = models.ForeignKey(Movie)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.movie.__str__() + '|' + self.user.__str__()


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

    def __str__(self):
        return self.title

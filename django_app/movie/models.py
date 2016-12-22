from django.db import models

from mysite import settings
from mysite.utils.models import BaseModel


class Genre(models.Model):
    """
    영화 장르 모델
    """
    content = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.content


class Grade(models.Model):
    """
    영화 관람등급 모델
    """
    content = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.content


class MakingCountry(models.Model):
    """
    영화 제작국가 모델
    """
    content = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.content


class Actor(models.Model):
    """
    영화배우 모델

    daum_id: 다음영화의 인물 id
    """
    daum_id = models.IntegerField(unique=True)
    name_kor = models.CharField(max_length=100)
    name_eng = models.CharField(max_length=100, blank=True)
    profile_url = models.TextField()

    def __str__(self):
        return self.name_kor


# class ActorRole(models.Model):
#     role = models.CharField(max_length=30)


class Director(models.Model):
    """
    영화감독 모델

    daum_id: 다음영화의 인물 id
    """
    daum_id = models.IntegerField(unique=True)
    name_kor = models.CharField(max_length=100)
    name_eng = models.CharField(max_length=100)
    profile_url = models.TextField()

    def __str__(self):
        return self.name_kor


class Movie(BaseModel):
    """
    1. 영화 모델
    2. 댓글관련 내용은 댓글 작성시 계산됨
    3. 댓글, 좋아요 관련 내용외 모든 정보는 다음영화 서비스에서 크로링하여 저장함
    4. 영화 관련 이미지는 전부 다음영화의 이미지를 url로 저장

    daum_id: 다음영화의 영화 id
    star_sum: 영화의 별점 합계
    comment_count: 영화의 댓글 개수
    star_average: 영화의 평균별점
    """
    daum_id = models.IntegerField(unique=True)
    title_kor = models.CharField(max_length=100)
    title_eng = models.CharField(max_length=100, blank=True)
    genre = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor, through='MovieActor')
    director = models.ManyToManyField(Director)
    star_sum = models.FloatField(default=0.0)
    comment_count = models.IntegerField(default=0)
    star_average = models.FloatField(default=0.0)
    making_country = models.ManyToManyField(MakingCountry)
    grade = models.ForeignKey(Grade)
    created_year = models.IntegerField()
    main_image_url = models.TextField()
    img_url = models.TextField()
    main_trailer = models.TextField()
    videos = models.TextField()
    run_time = models.CharField(max_length=30)
    synopsis = models.TextField()
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
        """
        1. 영화 개봉연도를 0~5점(1점 단위) 점수로 환산
        2. 최근영화일수록 점수가 높음

        :return: 영화 개봉연도 환산점수
        """
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
        """
        영화 평균별점을 0~5점(1점 단위) 점수로 환산

        :return: 영화별점 환산점수
        """
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
        """
        영화 좋아요 갯수를 0~5점(1점 단위) 점수로 환산

        :return: 영화 좋아요 환산점수
        """
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
    """
    영화 기타 이미지 모델
    """
    movie = models.ForeignKey(Movie)
    url = models.TextField()


class MovieActor(models.Model):
    """
    영화, 배우 중간자 모델

    character_name: 해당영화의 배우 역할명
    """
    movie = models.ForeignKey(Movie)
    actor = models.ForeignKey(Actor)
    # actor_role = models.ForeignKey(ActorRole)
    character_name = models.CharField(max_length=30)

    def __str__(self):
        return self.character_name


class Comment(BaseModel):
    """
    댓글 모델
    """
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
        """
        유저당 1개 영화애 1개 댓글만 작성가능
        """
        unique_together = (('author', 'movie'),)

    def __str__(self):
        return 'commnt' + self.movie.__str__() + '|' + self.author.__str__()

    @property
    def likes_count(self):
        """
        댓글 좋아요 갯수
        """
        return self.commentlike_set.count()

    @property
    def movie_title(self):
        """
        댓글이 속한 영화의 한글제목 출력
        """
        return Movie.objects.get(id=self.movie.pk).title_kor


class CommentLike(BaseModel):
    """
    1. 댓글의 좋아요 중간자 모델
    2. base model 상속을 위해 별도 중간자 만듦
    """
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.comment.__str__() + '|' + self.user.__str__()


class MovieLike(BaseModel):
    """
    1. 영화의 좋아요 중간자 모델
    2. base model 상속을 위해 별도 중간자 만듦
    """
    movie = models.ForeignKey(Movie)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.movie.__str__() + '|' + self.user.__str__()


class FamousLine(BaseModel):
    """
    1. 명대사 모델
    2. 영화, 배우, 유저 3개 모델과 relation
    """
    movie = models.ForeignKey(Movie)
    actor = models.ForeignKey(Actor)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='FamousLineAuthor')
    content = models.CharField(max_length=100)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='FamousLike')

    def __str__(self):
        return 'famousLine' + self.movie.__str__() + '|' + self.author.__str__()

    @property
    def likes_count(self):
        """
        명대사 좋아요 갯수
        """
        return self.famouslike_set.count()

    @property
    def movie_title(self):
        """
        명대사가 속한 영화의 한글제목 출력
        """
        return Movie.objects.get(id=self.movie.pk).title_kor

    @property
    def actor_kor_name(self):
        """
        명대사가 속한 배우의 한글이름 출력
        """
        return Actor.objects.get(id=self.actor.pk).name_kor

    @property
    def actor_character_name(self):
        """
        명대사에 속한 배우의 역할명 출력
        """
        return MovieActor.objects.get(movie=self.movie, actor=self.actor).character_name

    @property
    def actor_img_url(self):
        """
        명대사에 속한 영화배우의 프로필 사진 출력
        """
        return Actor.objects.get(id=self.actor.pk).profile_url


class FamousLike(BaseModel):
    """
    1. 명대사의 좋아요 중간자 모델
    2. base model 상속을 위해 별도 중간자 만듦
    """
    famous_line = models.ForeignKey(FamousLine)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class BoxOfficeMovie(BaseModel):
    """
    1. 박스오피스 모델
    2. 모든 영화가 가질 필요없는 정보들을 별도로 저장함
    3. 박스오피스 정보는 1일 1회 다음 영화 서비스에서 상위 10개씩 크롤링하여 저장함 (누적)
    """
    rank = models.IntegerField(default=0)
    movie = models.ForeignKey(Movie)
    release_date = models.DateField()
    ticketing_rate = models.FloatField(max_length=10)

    @property
    def movie_title(self):
        """
        박스오피스에 속한 영화의 한글제목 출력
        """
        return Movie.objects.get(id=self.movie.pk).title_kor


class Magazine(BaseModel):
    """
    매거진 모델

    mag_id: 다음영화 서비스의 매거진 id
    """
    mag_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    img_url = models.TextField()

    def __str__(self):
        return self.title

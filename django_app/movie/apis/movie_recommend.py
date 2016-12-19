import datetime
import random

from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models import Movie
from movie.serializers.movie import MovieSerializer, MovieDetailSerializer, RelatedMovieSerializer
from mysite.utils.custom_pagination import LargeResultsSetPagination


class CarouselMovieRecommend(APIView):
    """
    평점 최상위 10개중에 랜덤으로 2개 출력합니다.
    올해 영화만 출력합니다.
    박스오피스에 없는 영화만 출력합니다.
    """
    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        movies = Movie.objects.filter(boxofficemovie__isnull=True, created_year=now.year).order_by('-star_average')[:10]
        movie_recommend = random.sample(set(movies), 3)
        serializer = MovieDetailSerializer(movie_recommend, many=True)
        return Response(serializer.data)


class MainMovieList(generics.ListAPIView):
    """
    1. genre keyword를 pk로 받아 필터합니다.
    2. 20개 기준으로 pagination 합니다.
    3. 평점 상위 부터 노출됩니다.
    """
    serializer_class = MovieSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = Movie.objects.all().order_by('-star_average')
        genre = self.request.query_params.get('genre', None)
        if genre is not None:
            queryset = queryset.filter(genre=genre)
        return queryset


class FavoriteMovieRecommend(generics.ListAPIView):
    """
    취향 선택시 선택지마다 평점 최상위 6개 영화를 뽑고,
    뽑핀 영화 리스트에서 중복을 제거하고 6개를 랜덤으로 노출시킵니다.
    """
    serializer_class = MovieSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginator = None

    def get_queryset(self):
        genres = self.request.user.favorite_genre.all()
        grades = self.request.user.favorite_grade.all()
        making_countrys = self.request.user.favorite_making_country.all()
        favorite_recommend_movies = []
        for genre in genres:
            movies = Movie.objects.filter(genre=genre).order_by('-star_average')[:6]
            for movie in movies:
                favorite_recommend_movies.append(movie)
        for grade in grades:
            movies = Movie.objects.filter(grade=grade).order_by('-star_average')[:6]
            for movie in movies:
                favorite_recommend_movies.append(movie)
        for making_country in making_countrys:
            movies = Movie.objects.filter(making_country=making_country).order_by('-star_average')[:6]
            for movie in movies:
                favorite_recommend_movies.append(movie)
        # print(len(set(favorite_recommend_movies)))
        if len(set(favorite_recommend_movies)) == 0:
            raise NotAcceptable('취향을 선택해주세요.')
        elif len(set(favorite_recommend_movies)) < 12:
            raise NotAcceptable('취향을 더 선택해주세요.')
        movie_recommend = random.sample(set(favorite_recommend_movies), 6)
        return movie_recommend


class FavoriteMovieRecommendIOS(generics.ListAPIView):
    """
    아이폰 전용 유저취향 영화추천입니다.
    취향 선택시 선택지마다 평점 최상위 20개 영화를 뽑고,
    뽑핀 영화 리스트에서 중복을 제가하고 20개를 랜덤으로 노출시킵니다.
    """
    serializer_class = MovieSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginator = None

    def get_queryset(self):
        genres = self.request.user.favorite_genre.all()
        grades = self.request.user.favorite_grade.all()
        making_countrys = self.request.user.favorite_making_country.all()
        favorite_recommend_movies = []
        for genre in genres:
            movies = Movie.objects.filter(genre=genre).order_by('-star_average')[:20]
            for movie in movies:
                favorite_recommend_movies.append(movie)
        for grade in grades:
            movies = Movie.objects.filter(grade=grade).order_by('-star_average')[:20]
            for movie in movies:
                favorite_recommend_movies.append(movie)
        for making_country in making_countrys:
            movies = Movie.objects.filter(making_country=making_country).order_by('-star_average')[:20]
            for movie in movies:
                favorite_recommend_movies.append(movie)
        # print(favorite_recommend_movies)
        if len(set(favorite_recommend_movies)) == 0:
            raise NotAcceptable('취향을 선택해주세요.')
        elif len(set(favorite_recommend_movies)) < 40:
            raise NotAcceptable('취향을 더 선택해주세요.')
        movie_recommend = random.sample(set(favorite_recommend_movies), 20)
        return movie_recommend


class RelatedMovieView(APIView):
    """
    1. 해당 영화의 각 장르마다 동일한 장르 영화 별점 상위 30개 씩 추출하고 중복 제거
    2. 하기 항목별로 5~1점 부여, 최종 점수는 가중치를 곱해서 합산해서 ordering하고 상위 10개 추출
        1. 개봉연도: 올해 / 1년전 / 2년전 / 3년전 / 4년전 (가중치: *1)
        2. 평균별점: 4.50이상 / 4.49~4.00 / 3.99~3.50 / 3.49~3.00 / 2.99~2.50 (가중치: *5)
        3. 영화좋아요: 10개이상 / 8 / 6 / 4 / 2 (가중치: *10)
    3. 10개 중 4개 랜덤 추출
    4. 현재영화 제목의 첫 단어로 검색하여 일치하는 영화 (시리즈물) 최종 리스트 앞단에 추가
    5. 최종 list 4개 slice 해서 출력

    """
    def get(self, request, *args, **kwargs):
        benchmark_movie = Movie.objects.get(pk=self.kwargs['pk'])

        # 시리즈 확인
        benchmark_movie_title = benchmark_movie.title_kor
        hash_kor = benchmark_movie_title.split()[0]
        series = Movie.objects.exclude(pk=self.kwargs['pk']).filter(title_kor__startswith=hash_kor)
        series = list(series)

        # 1차 장르필터로 모수 추출
        benchmark_movie_genre = benchmark_movie.genre.all()
        base_movie_list = []

        for genre in benchmark_movie_genre:
            movies = Movie.objects.exclude(pk=self.kwargs['pk']).filter(genre=genre).order_by('-star_average')[:30]
            for movie in movies:
                if movie in series:
                    pass
                else:
                    base_movie_list.append(movie)
        base_movie_list_set = set(base_movie_list)
        related_movie_list = []

        # 2차 가중치 필터로 상위 10개 추출
        year_weight = 1
        star_weight = 5
        like_weight = 10

        for movie in base_movie_list_set:
            a = movie.score_created_year
            b = movie.score_star_average
            c = movie.score_like_users
            # print(movie.pk, movie, a, b, c)
            related_movie_list.append((movie, a*year_weight + b*star_weight + c*like_weight))
        related_movie_list.sort(key=lambda tup: tup[1], reverse=True)
        related_movie_list = related_movie_list[:10]

        # 3차 랜덤 필터로 4개 추출
        related_random_four = random.sample(set(related_movie_list), 4)
        related_random_four.sort(key=lambda tup: tup[1], reverse=True)

        # 리스트 출력
        final_list = []
        for movie_tup in related_random_four:
            final_list.append(movie_tup[0])

        # 시리즈가 있으면 우선순위로 출력
        if len(series) != 0:
            final_list = series + final_list
            final_list = final_list[:4]
        serializer = RelatedMovieSerializer(final_list, many=True)
        return Response(serializer.data)

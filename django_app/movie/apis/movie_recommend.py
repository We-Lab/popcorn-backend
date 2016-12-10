import random

from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models import Movie
from movie.serializers.movie import MovieSerializer
from mysite.utils.custom_pagination import LargeResultsSetPagination


class CarouselMovieRecommend(APIView):
    """
    평점 최상위 10개중에 랜덤으로 2개 출력합니다.
    """
    def get(self, request, *args, **kwargs):
        movie = Movie.objects.all().order_by('-star_average')[:10]
        movie_recommend = random.sample(set(movie), 3)
        serializer = MovieSerializer(movie_recommend, many=True)
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
    취향 선택시 선택지마다 평점 최상위 5개 영화를 뽑고,
    뽑핀 영화 리스트에서 중복을 제가하고 5개를 랜덤으로 노출시킵니다.
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
            movies = Movie.objects.filter(genre=genre).order_by('-star_average')[:5]
            for movie in movies:
                favorite_recommend_movies.append(movie)
        for grade in grades:
            movies = Movie.objects.filter(grade=grade).order_by('-star_average')[:5]
            for movie in movies:
                favorite_recommend_movies.append(movie)
        for making_country in making_countrys:
            movies = Movie.objects.filter(making_country=making_country).order_by('-star_average')[:5]
            for movie in movies:
                favorite_recommend_movies.append(movie)
        if len(set(favorite_recommend_movies)) == 0:
            raise NotAcceptable('취향을 선택해주세요.')
        elif len(set(favorite_recommend_movies)) < 5:
            raise NotAcceptable('취향을 더 선택해주세요.')
        movie_recommend = random.sample(set(favorite_recommend_movies), 5)
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
        elif len(set(favorite_recommend_movies)) < 20:
            raise NotAcceptable('취향을 더 선택해주세요.')
        movie_recommend = random.sample(set(favorite_recommend_movies), 20)
        return movie_recommend


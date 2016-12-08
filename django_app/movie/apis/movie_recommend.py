import random

from rest_framework import generics
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
        movie_recommend = random.sample(set(movie), 2)
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

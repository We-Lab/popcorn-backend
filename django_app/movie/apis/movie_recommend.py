import random

from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models import Movie
from movie.serializers.movie import MovieSerializer


class CarouselMovieRecommend(APIView):
    """
    평점 최상위 10개중에 랜덤으로 2개 출력합니다.
    """
    def get(self, request, *args, **kwargs):
        movie = Movie.objects.all().order_by('-star_average')[:10]
        movie_recommend = random.sample(set(movie), 2)
        serializer = MovieSerializer(movie_recommend, many=True)
        return Response(serializer.data)

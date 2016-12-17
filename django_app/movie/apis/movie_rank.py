from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models import Movie
from movie.serializers.movie_rank import RankSerializer


class StarRankView(APIView):
    def get(self, request, *args, **kwargs):
        movie = Movie.objects.all().order_by('-star_average')[:20]
        serializer = RankSerializer(movie, many=True)
        return Response(serializer.data)


class LikeRankView(APIView):
    def get(self, request, *args, **kwargs):
        movie = Movie.objects.all().order_by('-likes_count')[:20]
        serializer = RankSerializer(movie, many=True)
        return Response(serializer.data)

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException, NotAcceptable
from rest_framework.views import APIView
from movie.models import Movie
from rest_framework.response import Response
from apis.daum import movie_search
from movie.serializers.movie import MovieDetailSerializer, MovieSerializer


class MovieSearch(APIView):
    def get(self, request, pk=None):
        keyword = request.GET.get('keyword')
        # keyword = "".join(keyword.split())
        daum_id = request.GET.get('daum_id', '')
        movie = movie_search(keyword)

        if keyword:
            movie = Movie.objects.filter(title_kor__icontains=keyword)
            serializer = MovieSerializer(movie, many=True)
            return Response(serializer.data)
        else:
            raise NotAcceptable('keyword is required')

class MovieDetail(APIView):
    def get(self, request, pk):
        movie = Movie.objects.filter(pk=pk)
        serializer = MovieDetailSerializer(movie, many=True)
        return Response(serializer.data)

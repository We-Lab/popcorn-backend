from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from movie.models import Movie
from rest_framework.response import Response
from apis.daum import movie_search
from movie.serializers.movie import MovieDetailSerializer, MovieSerializer


class MovieSearch(APIView):
    def get(self, request):
        keyword = request.GET.get('keyword', '')
        # keyword = "".join(keyword.split())
        daum_id = request.GET.get('daum_id', '')
        try:
            movie = Movie.objects.filter(daum_id=daum_id)
            serializer = MovieDetailSerializer(movie, many=True)
            return Response(serializer.data)
        except:
            pass

        if Movie.objects.filter(title_kor__icontains=keyword) or Movie.objects.filter(title_eng__icontains=keyword):
            movie = Movie.objects.filter(title_kor__icontains=keyword)
            serializer = MovieSerializer(movie, many=True)
            return Response(serializer.data)
        else:
            movie = movie_search(keyword)
            return Response(movie)

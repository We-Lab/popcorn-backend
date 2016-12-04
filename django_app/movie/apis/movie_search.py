from rest_framework.exceptions import NotAcceptable
from rest_framework.views import APIView
from movie.models import Movie
from rest_framework.response import Response
from apis.daum import movie_search
from movie.serializers.movie import MovieDetailSerializer, MovieSerializer


class MovieSearch(APIView):
    def get(self, request, pk=None):
        keyword = request.GET.get('keyword')
        keyword = "".join(keyword.split())
        title = movie_search(keyword)
        hash_kor = title[0].split()[0]
        hash_eng = title[1].split()[0]

        if Movie.objects.filter(title_kor__icontains=keyword):
            movie = Movie.objects.filter(title_kor__icontains=keyword)
            serializer = MovieSerializer(movie, many=True)
            return Response(serializer.data)
        elif Movie.objects.filter(title_eng__icontains=keyword):
            movie = Movie.objects.filter(title_eng__icontains=keyword)
            serializer = MovieSerializer(movie, many=True)
            return Response(serializer.data)
        elif Movie.objects.filter(title_kor__icontains=hash_kor):
            movie = Movie.objects.filter(title_kor__icontains=hash_kor)
            serializer = MovieSerializer(movie, many=True)
            return Response(serializer.data)
        elif Movie.objects.filter(title_eng__icontains=hash_eng):
            movie = Movie.objects.filter(title_eng__icontains=hash_eng)
            serializer = MovieSerializer(movie, many=True)
            return Response(serializer.data)
        else:
            raise NotAcceptable('keyword is required')


class MovieDetail(APIView):
    def get(self, request, pk):
        movie = Movie.objects.filter(pk=pk)
        serializer = MovieDetailSerializer(movie, many=True)
        return Response(serializer.data)
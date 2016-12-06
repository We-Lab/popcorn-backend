from rest_framework.exceptions import NotAcceptable
from rest_framework.views import APIView
from movie.models import Movie
from rest_framework.response import Response
from apis.daum import movie_search
from movie.serializers.movie import MovieDetailSerializer, MovieSerializer


class MovieSearch(APIView):
    def get(self, request):
        keyword = request.GET.get('keyword')

        title = movie_search(keyword)


        hash_kor = title[0].split()[0]
        try:
            hash_kor1 = title[0].split()[1]
        except:
            hash_kor1 = ''

        try:
            hash_eng = title[1].split()[0]
        except:
            hash_eng = ''

        try:
            hash_eng1 = title[1].split()[1]
        except:
            hash_eng1 = ''

        if Movie.objects.filter(title_kor__icontains=keyword).exists():
            movie = Movie.objects.filter(title_kor__icontains=keyword)
            serializer = MovieSerializer(movie, many=True)
            return Response(serializer.data)
        elif Movie.objects.filter(title_eng__icontains=keyword).exists():
            movie = Movie.objects.filter(title_eng__icontains=keyword)
            serializer = MovieSerializer(movie, many=True)
            return Response(serializer.data)
        elif Movie.objects.filter(title_kor__icontains=hash_kor).exists() and Movie.objects.filter(title_kor__icontains=hash_kor1).exists():
            movie = Movie.objects.filter(title_kor__icontains=hash_kor).filter(title_kor__icontains=hash_kor1)
            serializer = MovieSerializer(movie, many=True)
            return Response(serializer.data)
        elif Movie.objects.filter(title_eng__icontains=hash_eng).exists() and Movie.objects.filter(title_eng__icontains=hash_eng1).exists():
            movie = Movie.objects.filter(title_eng__icontains=hash_eng).filter(title_eng__icontains=hash_eng1)
            serializer = MovieSerializer(movie, many=True)
            return Response(serializer.data)
        else:
            raise NotAcceptable('keyword is required')


class MovieList(APIView):
    def get(self, request):
        movie = Movie.objects.all()
        serializer = MovieDetailSerializer(movie, many=True)
        return Response(serializer.data)


class MovieDetail(APIView):
    def get(self, request, pk):
        movie = Movie.objects.filter(pk=pk)
        serializer = MovieDetailSerializer(movie, many=True)
        return Response(serializer.data[0])
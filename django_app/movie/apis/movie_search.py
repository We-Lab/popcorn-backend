from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.pagination import CursorPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from movie.models import Movie, MovieLike
from apis.daum import movie_search_func
from movie.serializers.movie import MovieDetailSerializer, MovieSerializer, MovieLikeSerializer


class MovieSearch(APIView):
    def get(self, request):
        keyword = request.GET.get('keyword')
        # print('keyword', keyword)
        title = movie_search_func(keyword)
        # print('title', title)

        try:
            hash_kor = title[0].split()[0]
        except:
            hash_kor = ''

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

        # print(hash_kor, hash_kor1, hash_eng, hash_eng1)

        if len(title) == 0:
            raise NotAcceptable('0')
        elif Movie.objects.filter(title_kor__icontains=keyword).exists():
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


class MovieListView(generics.ListAPIView):
    serializer_class = MovieDetailSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = CursorPagination
    queryset = Movie.objects.all()


class MovieDetailView(generics.RetrieveAPIView):
    """
    영화 상세정보를 출력합니다.
    """
    serializer_class = MovieDetailSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        movie_pk = self.kwargs['pk']
        result = Movie.objects.filter(pk=movie_pk)
        if result:
            return result
        raise NotAcceptable('찾는 영화가 없습니다.')


class MovieLikeView(generics.CreateAPIView):
    serializer_class = MovieLikeSerializer
    queryset = MovieLike.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        movie = Movie.objects.get(pk=kwargs['pk'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_like_exist = MovieLike.objects.filter(user=request.user, movie=movie)

        if movie_like_exist.exists():
            movie_like_exist.delete()
            movie.likes_count -= 1
            movie.save()
            return Response(serializer.errors, status=status.HTTP_306_RESERVED)
        serializer.save(movie=movie, user=request.user)
        movie.likes_count += 1
        movie.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

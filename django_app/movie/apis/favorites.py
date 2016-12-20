from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import MyUser
from movie.models import Genre, Grade, MakingCountry
from movie.serializers.favorites import UserFavoritesSerializer
from movie.serializers.movie import GenreSerializer, MakingCountrySerializer, GradeSerializer


class GenreView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginator = None


class GradeView(generics.ListAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginator = None


class MakingCountryView(generics.ListAPIView):
    queryset = MakingCountry.objects.all()
    serializer_class = MakingCountrySerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginator = None


class UserFavorites(generics.ListAPIView):
    serializer_class = UserFavoritesSerializer
    paginator = None

    def get_queryset(self):
        user_pk = self.request.user.pk
        return MyUser.objects.filter(pk=user_pk)


class DeleteFavorite(APIView):
    """
    회원의 취향을 초기화합니다.
    """
    def post(self, request, *args, **kwargs):
        user = MyUser.objects.get(id=self.request.user.pk)

        genre = user.favorite_genre.all()
        user.favorite_genre.remove(*genre)

        grade = user.favorite_grade.all()
        user.favorite_grade.remove(*grade)

        making_country = user.favorite_making_country.all()
        user.favorite_making_country.remove(*making_country)

        return Response({"detail": "유저 취향을 초기화했습니다"})

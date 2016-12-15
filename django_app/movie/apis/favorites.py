from rest_framework import generics
from rest_framework import permissions

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

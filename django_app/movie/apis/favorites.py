from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions

from movie.models import Genre, Grade, MakingCountry
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
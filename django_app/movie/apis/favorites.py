""" 취향 module
1. 유저의 취향 항목을 각각 리스트로 출력합니다. => 메인 페이지와 회원정보 페이지에 사용됩니다.
2. 유저의 취향 리스트도 출력합니다.
3. 취향은 초기화 가능합니다.
"""
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import MyUser
from movie.models import Genre, Grade, MakingCountry
from movie.serializers.favorites import UserFavoritesSerializer
from movie.serializers.movie import GenreSerializer, MakingCountrySerializer, GradeSerializer


class GenreView(generics.ListAPIView):
    """
    장르 리스트 출력
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginator = None


class GradeView(generics.ListAPIView):
    """
    관람등릅 리스트 출력
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginator = None


class MakingCountryView(generics.ListAPIView):
    """
    제작국가 리스트 출력
    """
    queryset = MakingCountry.objects.all()
    serializer_class = MakingCountrySerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginator = None


class UserFavorites(generics.ListAPIView):
    """
    유저의 취향 리스트 출력
    """
    serializer_class = UserFavoritesSerializer
    paginator = None

    def get_queryset(self):
        user_pk = self.request.user.pk
        return MyUser.objects.filter(pk=user_pk)


class DeleteFavorite(APIView):
    """
    유저 취향 초기화
    """
    def post(self, request, *args, **kwargs):
        user = MyUser.objects.get(id=self.request.user.pk)

        # 장르 초기화
        genre = user.favorite_genre.all()
        user.favorite_genre.remove(*genre)

        # 관람등급 초기화
        grade = user.favorite_grade.all()
        user.favorite_grade.remove(*grade)

        # 제작국가 초기화
        making_country = user.favorite_making_country.all()
        user.favorite_making_country.remove(*making_country)

        return Response({"detail": "유저 취향을 초기화했습니다"})

""" 매거진 view module
1. 다음영화에서 크롤링한 매거진을 출력합니다.
2. 메인페이지에 4개의 매거진을 랜덤 출력합니다.
"""
import random

from rest_framework.exceptions import NotAcceptable
from rest_framework.views import APIView
from rest_framework.response import Response
from movie.serializers.magazine import MagazineSerializer
from movie.models import Magazine


class MagazineList(APIView):
    """
    매거진 전체 리스트
    """
    def get(self, request):
        try:
            magazine = Magazine.objects.all()
            serializer = MagazineSerializer(magazine, many=True)
            return Response(serializer.data)
        except:
            raise NotAcceptable('not reachable')


class SampleMagazineAPIView(APIView):
    """
    매거진 4개 랜덤 출력
    """
    def get(self, request, *args, **kwargs):
        try:
            magazines = Magazine.objects.all()
            magazine_samples = random.sample(set(magazines), 4)
            serializer = MagazineSerializer(magazine_samples, many=True)
            return Response(serializer.data)
        except:
            raise NotAcceptable('not reachable')

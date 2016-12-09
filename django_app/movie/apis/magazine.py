import random

from rest_framework.exceptions import NotAcceptable
from rest_framework.views import APIView
from rest_framework.response import Response
from movie.serializers.magazine import MagazineSerializer
from movie.models import Magazine


class MagazineList(APIView):
    def get(self, request):
        try:
            magazine = Magazine.objects.all()
            serializer = MagazineSerializer(magazine, many=True)
            return Response(serializer.data)
        except:
            raise NotAcceptable('not reachable')


class SampleMagazineAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            magazines = Magazine.objects.all()
            magazine_samples = random.sample(set(magazines), 4)
            serializer = MagazineSerializer(magazine_samples, many=True)
            return Response(serializer.data)
        except:
            raise NotAcceptable('not reachable')



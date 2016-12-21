""" 박스오피스 view module
박스오피스 top 10을 출력합니다.
iOS, Web serializer 가 달라 두 개로 코딩합니다.
"""
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models import BoxOfficeMovie
from movie.serializers.box_office import BoxOfficeSerializer, BoxOfficeSerializerIOS


class BoxOfficeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        box_office_reversed = BoxOfficeMovie.objects.all().order_by('-created')[:10]
        box_office = reversed(box_office_reversed)
        serializer = BoxOfficeSerializer(box_office, many=True)
        return Response(serializer.data)


class BoxOfficeAPIViewIOS(APIView):
    def get(self, request, *args, **kwargs):
        box_office_reversed = BoxOfficeMovie.objects.all().order_by('-created')[:10]
        box_office = reversed(box_office_reversed)
        serializer = BoxOfficeSerializerIOS(box_office, many=True)
        return Response(serializer.data)

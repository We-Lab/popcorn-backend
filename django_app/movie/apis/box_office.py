from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models import BoxOfficeMovie
from movie.serializers.box_office import BoxOfficeSerializer


class BoxOfficeAPIView(APIView):

    # 최근에 업데이트된 탑 10위 박스오피스 노출함
    def get(self, request, *args, **kwargs):
        box_office_reversed = BoxOfficeMovie.objects.all().order_by('-created_date')[:10]
        box_office = reversed(box_office_reversed)
        serializer = BoxOfficeSerializer(box_office, many=True)
        return Response(serializer.data)


# class MainPageView(APIView):
#     def get(self, requset, *args, **kwargs):
#         box_office_list = BoxOfficeMovie.objects.all().order_by('created_date')[10:]
#         box_office_detail = BoxOfficeMovie.objects.all().order_by('created_date')[5:]
#         b_list = BoxOfficeListSerializer(box_office_list, many=True).data
#         b_detail = BoxOfficeDetailSerializer(box_office_detail, many=True).data
#
#         ret = {
#             'b_list': b_list,
#             'b_detail': b_detail,
#         }
#         return Response(ret)
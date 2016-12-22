""" custom pagination module

generic pagination을 커스텀화합니다.

"""
from rest_framework.pagination import CursorPagination, PageNumberPagination


class LargeResultsSetPagination(CursorPagination):
    page_size = 20


class RankResultsSetPagination(PageNumberPagination):
    """
    1. 영화 랭킹에 사용되는 pagination
    2. query slice를 위해 page number pagination 사용
    """
    page_size = 20

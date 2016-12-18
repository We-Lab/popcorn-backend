from rest_framework.pagination import CursorPagination, PageNumberPagination


class LargeResultsSetPagination(CursorPagination):
    page_size = 20


class RankResultsSetPagination(PageNumberPagination):
    page_size = 20

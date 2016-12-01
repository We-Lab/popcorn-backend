from django.conf.urls import url

from movie.apis.comment import CommentAPIView, CommentDetailAPIView
from movie.apis.movie_search import MovieSearch

urlpatterns = [
    url(r'', MovieSearch.as_view(), name='movie_search'),
    url(r'^comment/$', CommentAPIView.as_view()),
    url(r'^comment/(?P<comment_id>[0-9]+)/$', CommentDetailAPIView.as_view()),
]
from django.conf.urls import url

from movie.apis.comment import CommentAPIView, CommentDetailAPIView
from movie.apis.movie_search import MovieSearch

urlpatterns = [
    url(r'^$', MovieSearch.as_view(), name='movie_search'),
    url(r'^(?P<movie_id>[0-9]+)/comment/$', CommentAPIView.as_view(), name='comment_list'),
    url(r'^(?P<movie_id>[0-9]+)/comment/(?P<pk>[0-9]+)/$', CommentDetailAPIView.as_view(), name='comment_detail'),
]
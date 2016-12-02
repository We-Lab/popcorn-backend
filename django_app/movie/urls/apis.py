from django.conf.urls import url

from movie.apis.comment import CommentAPIView, CommentDetailAPIView
from movie.apis.movie_search import MovieSearch, MovieDetail

urlpatterns = [
    url(r'^search/$', MovieSearch.as_view(), name='movie_search'),
    url(r'^(?P<pk>[0-9]+)/$', MovieDetail.as_view(), name='database_movie'),
    url(r'^comment/$', CommentAPIView.as_view()),
    url(r'^comment/(?P<comment_id>[0-9]+)/$', CommentDetailAPIView.as_view()),
]
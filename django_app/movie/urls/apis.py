from django.conf.urls import url

from movie.apis.box_office import BoxOfficeAPIView
from movie.apis.comment import CommentAPIView, CommentDetailAPIView, CommentLikeView, TopCommentView
from movie.apis.famous_line import FamousLineAPIView, FamousLineDetailAPIView, FamousLikeView, TopFamousView
from movie.apis.movie_search import MovieSearch, MovieDetail


urlpatterns = [
    url(r'^search/$', MovieSearch.as_view(), name='movie_search'),
    url(r'^(?P<pk>[0-9]+)/$', MovieDetail.as_view(), name='database_movie'),
    url(r'^(?P<movie_id>[0-9]+)/comment/$', CommentAPIView.as_view(), name='comment_list'),
    url(r'^(?P<movie_id>[0-9]+)/comment/top/$', TopCommentView.as_view(), name='comment_top'),
    url(r'^(?P<movie_id>[0-9]+)/famous/$', FamousLineAPIView.as_view(), name='famous_list'),
    url(r'^(?P<movie_id>[0-9]+)/famous/top/$', TopFamousView.as_view(), name='famous_top'),
    url(r'^box_office/', BoxOfficeAPIView.as_view(), name='box_office'),
    url(r'^comment/(?P<comment_id>[0-9]+)/$', CommentDetailAPIView.as_view(), name='comment_detail'),
    url(r'^comment/(?P<comment_id>[0-9]+)/comment_like/', CommentLikeView.as_view(), name='comment_like'),
    url(r'^famous/(?P<famous_id>[0-9]+)/$', FamousLineDetailAPIView.as_view(), name='famous_line_detail'),
    url(r'^famous/(?P<famous_id>[0-9]+)/famous_like/', FamousLikeView.as_view(), name='famous_like'),
]

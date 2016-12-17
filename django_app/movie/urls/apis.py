from django.conf.urls import url

from movie.apis.comment import CommentLikeView, TopCommentView, CommentView, CommentDetailView, MyCommentStarView, \
    StarHistogram
from movie.apis.famous_line import FamousLikeView, TopFamousView, FamousLiseView, \
    FamousLineDetailView
from movie.apis.magazine import MagazineList
from movie.apis.movie_fast_like import MovieFastLike
from movie.apis.movie_rank import StarRankView, LikeRankView
from movie.apis.movie_recommend import RelatedMovieView
from movie.apis.movie_search import MovieSearch, MovieListView, MovieDetailView, MovieLikeView

urlpatterns = [
    # 검색페이지
    url(r'^search/$', MovieSearch.as_view(), name='movie_search'),
    # 영화리스트
    url(r'^list/', MovieListView.as_view(), name='movie_list'),
    # 영화상세
    url(r'^(?P<pk>[0-9]+)/$', MovieDetailView.as_view(), name='movie_detail'),
    url(r'^(?P<pk>[0-9]+)/movie-like/', MovieLikeView.as_view(), name='comment_like'),
    url(r'^(?P<pk>[0-9]+)/related/', RelatedMovieView.as_view(), name='related_movies'),
    # 영화평가
    url(r'^(?P<pk>[0-9]+)/comment/$', CommentView.as_view(), name='comment_list'),
    url(r'^(?P<pk>[0-9]+)/comment/histogram/$', StarHistogram.as_view(), name='star_histogram'),
    url(r'^(?P<pk>[0-9]+)/comment/top/$', TopCommentView.as_view(), name='comment_top'),
    url(r'^(?P<pk>[0-9]+)/comment/my-star/$', MyCommentStarView.as_view(), name='comment_my_star'),
    url(r'^comment/(?P<pk>[0-9]+)/$', CommentDetailView.as_view(), name='comment_detail'),
    url(r'^comment/(?P<pk>[0-9]+)/comment-like/', CommentLikeView.as_view(), name='comment_like'),
    # 영화명대사
    url(r'^(?P<pk>[0-9]+)/famous/$', FamousLiseView.as_view(), name='famous_list'),
    url(r'^(?P<pk>[0-9]+)/famous/top/$', TopFamousView.as_view(), name='famous_top'),
    url(r'^famous/(?P<pk>[0-9]+)/$', FamousLineDetailView.as_view(), name='famous_line_detail'),
    url(r'^famous/(?P<pk>[0-9]+)/famous-like/', FamousLikeView.as_view(), name='famous_like'),
    # 매거진 리스트
    url(r'^magazine/', MagazineList.as_view(), name='magazine_list'),
    # 빠른 좋아요 페이지
    url(r'^fast-like/$', MovieFastLike.as_view(), name='movie_fast_like'),
    # 랭킹
    url(r'^star-rank/$', StarRankView.as_view(), name='star_rank'),
    url(r'^like-rank/$', LikeRankView.as_view(), name='like_rank'),
]

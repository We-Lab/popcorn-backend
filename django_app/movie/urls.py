from django.conf.urls import url

from movie.apis.comment import CommentAPIView, CommentDetailAPIView


urlpatterns = [
    url(r'^comment/$', CommentAPIView.as_view()),
    url(r'^comment/(?P<comment_id>[0-9]+)/$', CommentDetailAPIView.as_view()),
]
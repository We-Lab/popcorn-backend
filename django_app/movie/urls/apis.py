from django.conf.urls import url
from movie.apis.movie_search import MovieSearch

urlpatterns = [
    url(r'', MovieSearch.as_view(), name='movie_search'),
]
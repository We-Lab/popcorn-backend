"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from allauth.account.views import confirm_email
from movie.apis.box_office import BoxOfficeAPIView
from movie.apis.comment import NewCommentAPIView
from movie.apis.favorites import GenreView, MakingCountryView, GradeView
from movie.apis.magazine import SampleMagazineAPIView
from movie.apis.movie_recommend import CarouselMovieRecommend, MainMovieList

urlpatterns = [
    # 어드민페이지
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 메인페이지
    url(r'^main/box_office/$', BoxOfficeAPIView.as_view(), name='box_office'),
    url(r'^main/comments/$', NewCommentAPIView.as_view(), name='new_comments'),
    url(r'^main/magazines/$', SampleMagazineAPIView.as_view(), name='magazine_samples'),
    url(r'^main/movie_recommends/', MainMovieList.as_view(), name='movie_recommends'),
    url(r'^main/movie_recommends/carousel/$', CarouselMovieRecommend().as_view(), name='carousel_movie_recommends'),
    # 취향페이지
    url(r'^favorite/genre/$', GenreView.as_view(), name='favorites'),
    url(r'^favorite/grade/$', GradeView.as_view(), name='favorites'),
    url(r'^favorite/making_country/$', MakingCountryView.as_view(), name='favorites'),
    # 회원페이지
    url(r'^accounts/', include('allauth.urls')),
    url(r'^member/', include('rest_auth.urls')),
    url(r'^member/registration/', include('rest_auth.registration.urls')),
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', confirm_email, name='account_confirm_email'),
    # 테스트페이지
    url(r'^test-api/', include('test_app.urls', namespace='test')),
    # 영화페이지
    url(r'^movie/', include('movie.urls.apis', namespace='movie')),
]

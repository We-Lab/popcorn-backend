from django.conf.urls import url

from test_app.apis import PostViewSet

post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    url(r'^post/$', post_list),
    url(r'^post/(?P<pk>[0-9]+)/', post_detail),
]
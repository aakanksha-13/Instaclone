from django.conf.urls import url
from django.contrib import admin

from pikachu.views import signup_view
from pikachu.views import login_view,feed_view,post_view,like_view, comment_view

urlpatterns = [
    url('post/', post_view),
    url('feed/', feed_view),
    url('like/', like_view),
    url('comment/', comment_view),
    url(r'login/', login_view),
    url(r'', signup_view),

]

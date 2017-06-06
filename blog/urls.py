from django.conf.urls import url

from .views import PostsListView, PostDetailView ,RegisterFormView, LoginFormView, LogoutView
from blog import views

urlpatterns = [
url(r'^blog/$', PostsListView.as_view(), name='list'), # то есть по URL http://имя_сайта/blog/ 
                                               # будет выводиться список постов
url(r'^blog/(?P<pk>\d+)/$', PostDetailView.as_view()), # а по URL http://имя_сайта/blog/число/ 
                                              # будет выводиться пост с определенным номером
url(r'^register/$', RegisterFormView.as_view()),

url(r'^login/$', LoginFormView.as_view()),

url(r'^logout/$', LogoutView.as_view()),
url(r'^sortlikes/$', views.sort_likes, name='sortlikes'),
url(r'^postlist/$', views.post_list, name='post_list'),
url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'), ###############
url(r'^post/new/$', views.post_new, name='post_new'),########################
url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
url(r'^postlist/(?P<username>\d+)/$', views.user_post, name='user_post'),
url(r'^users/$', views.users, name='users'),
url(r'^post/(?P<pk>[0-9]+)/addlike/$', views.add_like, name='add_like'),
url(r'^post/(?P<pk>[0-9]+)/delete/$', views.post_delete, name='post_delete'),
url(r'^searchuser/$', views.search_user, name='search_user'),
url(r'^search/$', views.search, name='search'),
url(r'^searchtext/$', views.searchtext, name='searchtext'),
url(r'^search_text/$', views.search_text, name='search_text'),





]
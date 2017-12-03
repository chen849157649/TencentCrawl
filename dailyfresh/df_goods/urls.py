from django.conf.urls import url
from df_goods import views

urlpatterns = [
    url(r'^$', views.index, name='index'),  # 这个路径是ip后什么也没用，输入ip就到首页
    url(r'^goods/(?P<goods_id>\d+)/$', views.detail, name='detail'),
    url(r'^list/(?P<type_id>\d+)/(?P<page>\d+)/$', views.list, name='list'),
]

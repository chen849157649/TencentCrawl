from django.conf.urls import url
from df_user import views
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^register_handle/$', views.register_handle, name='register_handle'),
    url(r'^check_user_exist/$', views.check_user_exist, name='check_user_exist'),
    url(r'^active/(?P<token>.*)/$', views.user_active, name='user_active'),

    url(r'^login/$', views.login, name='login'),
    url(r'^login_check/$', views.login_check, name='login_check'),
    url(r'^login_out/$', views.login_out, name='login_out'),
    url(r'^online/$', views.user_online, name='user_online'),

    url(r'^center_info/$',views.center_info, name='center_info'),
    url(r'^center_order/$', views.center_order, name='center_order'),
    url(r'^center_site/$', views.center_site, name='center_site'),

    url(r'^address_handle/$', views.address_handle, name='address_handle'),
]

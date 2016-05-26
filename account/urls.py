from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from account import views
from rest_framework import renderers


urlpatterns = [
    url(r'^accounts/$', views.account_list),

    url(r'^accounts/(?P<pk>[0-9]+)/$', views.account_detail),
    url(r'^accounts/fund/(?P<pk>[0-9]+)/$', views.account_fund_detail),

    url(r'^stock/$', views.stock_detail),
    url(r'^stock/sell/$', views.stock_sell),

    
    url(r'^follow/$', views.follow_detail),
    url(r'^mirror/$', views.mirror_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)

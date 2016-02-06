from django.conf.urls import patterns, include, url
from littesnail.central_process import handleRequest

from . import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^weixin/$', handleRequest),
    url(r'^test_wiki/$', views.test_wiki, name='test_wiki'),
    url(r'^test_travel/$', views.test_travel, name='test_travel'),
    url(r'^test_food/$', views.test_food, name='test_food'),
    url(r'^test_youdao/$', views.test_youdao, name='test_youdao'),
    # url(r'^littesnail/', include('littesnail.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

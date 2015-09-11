from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OTAutoSearch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ot/',include('OTobjects.urls',namespace="OTobjects")),
    #url(r'^accounts/', include('registration_email.backends.default.urls')),
)

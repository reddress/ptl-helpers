from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pontual.views.home', name='home'),
    # url(r'^pontual/', include('pontual.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'pontual.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pedidos/', include('pedidos.urls')),
    url(r'^people/', include('people.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url="/static/favicon.ico")),
)

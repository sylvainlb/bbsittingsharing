from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views import generic
from models import BBSitting, Parent
from forms import UpdateProfileForm
from views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', generic.TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^info$', generic.TemplateView.as_view(template_name="info.html"), name="info"),
    url(r'^new$', login_required(CreateView.as_view(model=BBSitting)), name="new"),
    url(r'^search/(?P<pk>\d+)$', SearchView.as_view(), name="detail"),
    url(r'^agenda$', login_required(generic.ListView.as_view(model=BBSitting)), name="agenda"),
    url(r'^(?P<pk>\d+)/book$', BookView.as_view(), name="book"),
    url(r'^(?P<pk>\d+)/validate/(?P<booking_pk>\d+)$', ValidateView.as_view(), name="validate"),
    url(r'^friends$', FriendsView.as_view(), name="friends"),
    url(r'^refer$', ReferView.as_view(), name="refer"),
    url(r'^users/(?P<slug>\w+)/$', login_required(generic.DetailView.as_view(model=Parent, slug_field='username')), name="profile"),
    url(r'^users/(?P<slug>\w+)/edit$', login_required(generic.UpdateView.as_view(model=Parent, slug_field='username', form_class=UpdateProfileForm)), name="profile_edit"),
    url(r'^register/$', RegisterView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # for user pictures
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$'%settings.MEDIA_URL[1:], 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

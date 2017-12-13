# coding=utf-8
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from Prog.views import employee_views, groups_views, journal_views, contact_admin
from registration.backends.simple import urls
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = [
    # employee urls
    url(r'^$', employee_views.employee_list, name='home'),
    url(r'^employee/add/$', employee_views.employee_add, name='employee_add'),
    url(r'^employee/edit/(?P<pk>\d+)/$', employee_views.EmployeeUpdateView.as_view(), name='employee_edit'),
    url (r'^employee/delete/(?P<pk>\d+)/$', employee_views.EmployeeDeleteView.as_view (), name ='employee_delete'),

    # Groups urls
    url(r'^groups/$', groups_views.groups_list, name='groups'),
    url(r'^groups/add/$', groups_views.groups_add, name='groups_add'),
    url(r'^groups/edit/(?P<pk>\d+)/$', groups_views.GroupUpdateView.as_view(), name='groups_edit'),
    url(r'^groups/delete/(?P<pk>\d+)/$', groups_views.GroupDeleteView.as_view(), name='groups_delete'),
    
    # Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', journal_views.JournalView.as_view(), name='journal'),
    # Contact Admin Form
    url(r'^contact-admin/$', contact_admin.contact_admin, name='contact_admin'),

    # User Related urls
    url(r'^users/profile/$', login_required(TemplateView.as_view(template_name='registration/profile.html')), name='profile'),
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'},name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'),name='registration_complete'),
    url(r'^users/', include(urls,namespace='users')),

    url(r'^admin/', include(admin.site.urls)),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from dj_task_manager.views import index, tasks_filter, ajax_add_task, ajax_remove_task, ajax_finish_task, ajax_render_task, api, admin_users, admin_rem_user, edit_task

# Uncomment the next two lines to enable the admin:
# 
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^accounts/', include('registration.urls')),
    (r'^tasks/edit/$', edit_task),
    (r'^tasks-filter/([a-z]+)/$', tasks_filter),
    (r'^ajax/add_task/$', ajax_add_task),
    (r'^ajax/render_task/$', ajax_render_task),
    (r'^ajax/rem_task/$', ajax_remove_task),
    (r'^ajax/finish_task/$', ajax_finish_task),
    (r'^admin/$', admin_users),
    (r'^admin/rem_user/$', admin_rem_user),
    (r'^api/$', api),
)
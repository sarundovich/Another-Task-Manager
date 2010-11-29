#!/usr/bin/env python
# coding: utf8

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from json import dumps
from functools import wraps
import datetime
from dj_task_manager.models import Task
from dj_task_manager.forms import NewTaskForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def ajax_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.is_ajax():
            return func(request, *args, **kwargs)
        else:
            raise Http404
    return inner


#+++common actions

def index(request):
    if request.user.is_authenticated():
        tasks = Task.objects.filter(user_id = request.user.id).order_by('deadline')
        
        return render_to_response('tasks.html', 
                                  {'tasks': tasks, 'user': request.user}, 
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('index.html', 
                                  {'user': request.user}, 
                                  context_instance=RequestContext(request))

@login_required        
def tasks_filter(request, filter):
    if filter == 'prior':
        tasks = Task.objects.filter(high_priority=True).order_by('deadline')
    elif filter == 'today':
        tasks = Task.objects.filter(deadline=get_today_date()).order_by('deadline')
    elif filter == 'tomorrow':
        tasks = Task.objects.filter(deadline=get_today_date() + datetime.timedelta(days=1)).order_by('deadline')
    elif filter == 'finished':
        tasks = Task.objects.filter(done=True).order_by('deadline')
    elif filter == 'outdated':
        tasks = Task.objects.exclude(deadline__gte=get_today_date() - datetime.timedelta(days=1)).order_by('deadline')
    else:
        raise Http404
    
    return render_to_response('tasks.html', 
                                  {'tasks': tasks, 'user': request.user, 'filter': filter}, 
                                  context_instance=RequestContext(request))

#---end of common actions

#+++ajax actions (tasks)

@ajax_required 
def ajax_add_task(request):
    form = NewTaskForm(request.POST)
    if form.is_valid():
        post_data = form.cleaned_data
        task = Task(name = post_data.get('name'),
                        deadline = post_data.get('deadline'), 
                        high_priority = True if request.POST.get('is_hi_prior') == 'true' else False,
                        done = False, 
                        user_id = request.user.id)
        task.save()
        return HttpResponse(dumps({'success': True, 'task_id': task.id}))
    else:
        return HttpResponse(dumps({'success': False}))

@ajax_required 
def ajax_render_task(request):
    task = get_task_by_id(get_task_id(request.POST))
    today = get_today_date()
    outdated = True if task.deadline < today  else False
    task_html = render_to_string('tags/task.html', {'task': task, 'outdated': outdated})
    out_json = dumps({'success': True, 'task_html': task_html})
    return HttpResponse(out_json)

@ajax_required
def ajax_remove_task(request):
    task = get_task_by_id(get_task_id(request.POST))
    task.delete()
    return HttpResponse(dumps({'success': True}))
    
@ajax_required    
def ajax_finish_task(request):
    task = get_task_by_id(get_task_id(request.POST))
    task.done = False if task.done else True
    task.save()
    return HttpResponse(dumps({'success': True, 'is_done': task.done}))

@ajax_required       
def edit_task(request):
    try:
        tid = int(request.POST.get('id').split('-')[-1])
    except ValueError:
        return HttpResponse(dumps({'success': False}))
    value = request.POST.get('value')
    task = Task.objects.get(id=tid)
    task.name = value
    task.save()
    return HttpResponse(task.name)

#---end of ajax actions

@login_required
def admin_users(request):
    if request.user.is_superuser:
        users = User.objects.all().order_by('id')
        return render_to_response('admin_users.html', 
                                  {'users': users}, 
                                  context_instance=RequestContext(request))
    else:
        raise Http404

@ajax_required
@login_required
def admin_rem_user(request):
    try:
        uid = int(request.POST.get('user_id'))
    except ValueError:
        raise Http404
    user = User.objects.get(id=uid)
    user.delete()
    return HttpResponse(dumps({'success': True}))

def api(request):
    raise Http404

#+++ helper funcs

def get_task_id(request_data):
    try:
        return int(request_data.get('task_id'))
    except ValueError:
        raise Http404
    
def get_task_by_id(tid):
    return Task.objects.get(id=tid)

def get_today_date():
    return datetime.date.today()

def _task_to_dict(task):
    return {'name': task.name, 'done': task.done, 
            'deadline': task.deadline.isoformat() if task.deadline is not None else ''}
    
#--- end of helper funcs
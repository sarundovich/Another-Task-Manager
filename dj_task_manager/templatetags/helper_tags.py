#!/usr/bin/env python
# coding: utf8

from django import template
import datetime

register = template.Library()

@register.inclusion_tag('tags/main_menu.html')
def render_main_menu(user):
    return {'user': user}

@register.inclusion_tag('tags/task.html')
def render_task(task):
    today = datetime.date.today()
    outdated = True if task.deadline < today  else False
    return {'task': task, 'outdated': outdated}
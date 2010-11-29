#!/usr/bin/env python
# coding: utf8

from django.db import models

class Task(models.Model):
    user_id = models.IntegerField()
    name = models.TextField()
    high_priority = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    deadline = models.DateField()
    
    def __str__(self):
        return 'Task: %s <%s>' % (self.name, self.done)
    
    def __unicode__(self):
        return u'Task: %s <%s>' % (self.name, self.done)
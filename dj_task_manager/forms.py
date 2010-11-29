#!/usr/bin/env python
# coding: utf8

from django import forms

class NewTaskForm(forms.Form):
    deadline = forms.DateField()
    name = forms.CharField()
    priority = forms.CheckboxInput()
    
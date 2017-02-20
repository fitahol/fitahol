#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '29/12/2015'
__author__ = 'deling.ma'
"""
from django import forms

from schedule.models import Event
from schedule.widgets import SpectrumColorPicker


class EventAdminForm(forms.ModelForm):
    class Meta:
        exclude = []
        model = Event
        widgets = {
          'color_event': SpectrumColorPicker,
        }

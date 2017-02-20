#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '29/12/2015'
__author__ = 'deling.ma'
"""
from django.conf import settings
from django.shortcuts import _get_queryset


def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.
    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.
    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_config(key, default=None):
    """
    Get settings from django.conf if exists,
    return default value otherwise
    example:
    ADMIN_EMAIL = get_config('ADMIN_EMAIL', 'default@email.com')
    """
    return getattr(settings, key, default)

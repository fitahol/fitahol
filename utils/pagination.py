#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '12/12/2016'
__author__ = 'deling.ma'
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param, remove_query_param


class ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        if "appservice" in self.request.META["HTTP_USER_AGENT"] or \
                "https" in self.request.META.get('HTTP_REFERER'):
            url = url.replace("http", "https")
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        if "appservice" in self.request.META["HTTP_USER_AGENT"] or \
                "https" in self.request.META.get('HTTP_REFERER'):
            url = url.replace("http", "https")
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

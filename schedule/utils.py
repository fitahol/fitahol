#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '29/12/2015'
__author__ = 'deling.ma'
"""
import heapq
import pytz

from django.conf import settings
from django.utils import timezone
from django.utils.module_loading import import_string


class EventListManager(object):
    """
    This class is responsible for doing functions on a list of events. It is
    used to when one has a list of events and wants to access the occurrences
    from these events in as a group
    """

    def __init__(self, events):
        self.events = events

    def occurrences_after(self, after=None, tzinfo=pytz.utc):
        """
        It is often useful to know what the next occurrence is given a list of
        events.  This function produces a generator that yields the
        the most recent occurrence after the date ``after`` from any of the
        events in ``self.events``
        """
        from schedule.models import Occurrence

        if after is None:
            after = timezone.now()
        occ_replacer = OccurrenceReplacer(
            Occurrence.objects.filter(event__in=self.events))
        generators = [event._occurrences_after_generator(after) for event in
                      self.events]
        occurrences = []

        for generator in generators:
            try:
                heapq.heappush(occurrences, (next(generator), generator))
            except StopIteration:
                pass

        while True:
            if len(occurrences) == 0:
                raise StopIteration

            generator = occurrences[0][1]

            try:
                next_occurence = \
                heapq.heapreplace(occurrences, (next(generator), generator))[0]
            except StopIteration:
                next_occurence = heapq.heappop(occurrences)[0]
            yield occ_replacer.get_occurrence(next_occurence)


class OccurrenceReplacer(object):
    """
    When getting a list of occurrences, the last thing that needs to be done
    before passing it forward is to make sure all of the occurrences that
    have been stored in the datebase replace, in the list you are returning,
    the generated ones that are equivalent.  This class makes this easier.
    """

    def __init__(self, persisted_occurrences):
        lookup = [((occ.event, occ.original_start, occ.original_end), occ) for
                  occ in persisted_occurrences]
        self.lookup = dict(lookup)

    def get_occurrence(self, occ):
        """
        Return a persisted occurrences matching the occ and remove it from lookup since it
        has already been matched
        """
        return self.lookup.pop(
            (occ.event, occ.original_start, occ.original_end),
            occ)

    def has_occurrence(self, occ):
        return (occ.event, occ.original_start, occ.original_end) in self.lookup

    def get_additional_occurrences(self, start, end):
        """
        Return persisted occurrences which are now in the period
        """
        return [occ for _, occ in list(self.lookup.items()) if
                (occ.start < end and occ.end >= start and not occ.cancelled)]


def get_model_bases():
    from django.db.models import Model
    baseStrings = getattr(settings, 'SCHEDULER_BASE_CLASSES', None)
    if baseStrings is None:
        return [Model]
    else:
        return [import_string(x) for x in baseStrings]

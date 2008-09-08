import logging

import mx.DateTime
from Acquisition import aq_inner
from Acquisition import Explicit
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet

from xm.tracker.browser.interfaces import ITaskViewlet
from xm.tracker.config import UNASSIGNED
from xm.tracker.utils import round_time_to_minutes

logger = logging.getLogger('taskviewlets')


class TaskListManager(Explicit):

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.__parent__ = view

    def update(self):
        context = aq_inner(self.context)
        tracker_view = getMultiAdapter(
            (context, self.request), name=u'tracker')
        # XXX make a separate function instead of doing this in update()?
        self.tracker = tracker_view.tracker()

        rows = []
        tasks = self.tracker.tasks[:]

        tasks.append(self.tracker.unassigned)
        for task in tasks:
            self.request['task_uid'] = task.uid
            viewlet = getMultiAdapter(
                (context, self.request, self.__parent__, self),
                IViewlet, name=u'xm.tracker.task')
            viewlet.update()
            rows.append(viewlet)
        self.rows = rows

    def render(self, *args, **kw):
        result = u''
        for row in self.rows:
            result += row.render()
        return result


class TaskViewlet(BrowserView):
    """ Base class with common functions for link viewlets.
    """
    implements(ITaskViewlet)
    render = ZopeTwoPageTemplateFile('templates/task.pt')

    # Apparently this is needed to give access to the 'allowed'
    # attribute in case this viewlet gets rendered within a KSS view
    # (while adding a booking using this form), which messes up the
    # Acquisition chain or something...
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, context, request, view, manager):
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.task = None

    def update(self):
        task_uid = self.request.get('task_uid', '')
        self.task = self.view.tracker().get_task(task_uid)

    def total_time(self):
        time = round_time_to_minutes(self.task.total_time())
        return time.strftime('%H:%M')

    def remaining_time(self):
        """Return time left for work.

        Subtract both the already-booked hours and our ready-to-book
        hours. Ignore not-yet-booked hours by others.

        """
        if self.task.uid == UNASSIGNED:
            return None
        tools = getMultiAdapter((self.context, self.request),
                                name=u'plone_tools')
        brains = tools.catalog()({'UID': self.task.uid})
        xm_task = brains[0]

        available = mx.DateTime.DateTimeDeltaFrom(hours=xm_task.estimate)
        our_time = self.task.total_time()
        already_booked = mx.DateTime.DateTimeDeltaFrom(
            hours=xm_task.actual_time)
        remaining = available - our_time - already_booked
        remaining = round_time_to_minutes(remaining)
        if remaining < 0:
            return '-' + remaining.strftime('%H:%M')
        return remaining.strftime('%H:%M')

    def entries(self):
        result = []
        for entry in self.task.entries:
            time = round_time_to_minutes(entry.time)
            result.append(dict(text = entry.text,
                               date = entry.date.strftime('%d-%m'),
                               time = time.strftime('%H:%M')))
        return result

    def tracker_has_started(self):
        tracker = self.view.tracker()
        return bool(tracker.starttime)

    def task_class(self):
        """Return class that is to be set on the task's details div."""
        if self.request.get('open_details'):
            # We want to expand this one.
            return 'task task-details-expanded'
        return 'task'

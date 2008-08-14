from Acquisition import aq_inner
from Acquisition import Explicit
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet

#from xm.tracker.browser.interfaces import ITaskViewlet


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
        for task in self.tracker.tasks:
            viewlet = getMultiAdapter(
                (task, self.request, self.__parent__, self),
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
    implements(IViewlet)
    render = ViewPageTemplateFile('task.pt')

    def __init__(self, context, request, view, manager):
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

    def update(self):
        pass

    def total_time(self):
        return self.context.total_time().strftime('%M:%S')

    def entries(self):
        result = []
        for entry in self.context.entries:
            result.append(dict(text = entry.text,
                               date = entry.date.strftime('%Y-%m-%d'),
                               time = entry.time.strftime('%M:%S')))
        return result

    def tracker_has_started(self):
        tracker = self.view.tracker()
        return bool(tracker.starttime)

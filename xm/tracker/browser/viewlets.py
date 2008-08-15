from Acquisition import aq_inner
from Acquisition import Explicit
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
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
        tasks = self.tracker.tasks[:]
                
        tasks.append(self.tracker.unassigned)
        for task in tasks: 
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
    render = ZopeTwoPageTemplateFile('task.pt')
    
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

    def update(self):
        pass

    def total_time(self):
        return self.context.total_time().strftime('%H:%M')

    def entries(self):
        result = []
        for entry in self.context.entries:
            result.append(dict(text = entry.text,
                               date = entry.date.strftime('%d-%m'),
                               time = entry.time.strftime('%H:%M')))
        return result

    def tracker_has_started(self):
        tracker = self.view.tracker()
        return bool(tracker.starttime)

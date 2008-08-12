from Acquisition import aq_inner
from Acquisition import Explicit
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter

from xm.tracker.browser.interfaces import ITaskListManager


class TaskListManager(Explicit):
    implements(ITaskListManager)
    template = ViewPageTemplateFile('tasklist.pt')
    render = template

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


class TaskViewlet(ViewletBase):
    """
    """
    #render = ViewPageTemplateFile('task.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.entries = self._get_entries()

    def _get_entries(self):
        """
        """
        tracker = getMultiAdapter((self.context, self.request),
                                    name=u'tracker')
        result = []
        for entry in tracker.entries:
            result.append(dict(
                text = entry.text,
                time = entry.time.strftime('%H:%M:%S'), ))
        return result

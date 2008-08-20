from Acquisition import Explicit
from zope.component import adapts
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Interface
from zope.interface import implements
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from xm.tracker import XMTrackerMessageFactory as _
from xm.tracker.browser.tracker import TrackerView
from xm.tracker.browser.interfaces import ITaskEntries


def time_to_seconds(time):
    """ This helper method convert a time string notation like:
    '4:22' to an integer in seconds.

    >>> from xm.tracker.browser.entry import time_to_seconds
    >>> time_to_seconds('4:22')
    15720

    """
    timelist = time.split(':')
    timelist = [int(i) for i in timelist]
    timelist.reverse()
    minutes = timelist[0]
    hours = timelist[1]
    return minutes * 60 + hours * 60 * 60


class RemoveEntry(TrackerView):
    """This view removes an entry for a given task"""

    def __call__(self):
        uid = self.request.get('uid')
        entry_number = int(self.request.get('entry_number'))
        tracker = self.tracker()
        task = tracker.get_task(uid)
        if task is None:
            msg = _(u'msg_no_task_found',
                    default=u'No task found with this UID')
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            self.request.response.redirect('@@tracker')
            return

        try:
            task.entries.pop(entry_number)
        except IndexError:
            msg = _(u'msg_remove_entry_failed',
                    default=u'Failed to remove entry')
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
        else:
            msg = _(u'msg_remove_entry_success', default=u'Removed entry')
            IStatusMessage(self.request).addStatusMessage(msg, type="info")
        self.request.response.redirect('@@tracker')


class EntriesProvider(Explicit):
    """This view stores changes for a list of Entries"""
    implements(ITaskEntries)
    adapts(Interface, IDefaultBrowserLayer, Interface)

    render = ZopeTwoPageTemplateFile('entries.pt')
    
    task = None

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.__parent__ = view

    def update(self):
        pass


class EditEntries(TrackerView):

    def __call__(self):
        """ In this call we handle a form which contains a list of entries.
        Each entry has a text and time field which we expect to change.
        """
        uid = self.request.get('uid')
        entry_number = int(self.request.get('entry_number'))
        tracker = self.tracker()
        task = tracker.get_task(uid)
        if task is None:
            msg = _(u'msg_no_task_found',
                    default=u'No task found with this UID')
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            self.request.response.redirect('@@tracker')
            return

import mx.DateTime

from Acquisition import Explicit
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView
from zope.component import adapts
from zope.interface import Interface
from zope.interface import implements
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from xm.tracker import XMTrackerMessageFactory as _
from xm.tracker.browser.interfaces import ITaskEntries
from xm.tracker.browser.ksstracker import get_tracker
from xm.tracker.browser.ksstracker import KSSTaskRefresher
from xm.tracker.browser.viewlets import TaskViewlet
from xm.tracker.browser.tracker import TrackerView
from xm.tracker.utils import round_time_to_minutes


class TimeformattingError(Exception):

    def __str__(self):
        return _(u'time_formatting_error',
                 default='Invalid time format. Must be x:xx or xx:xx')


def time_to_seconds(time):
    """Convert a time string like '4:22' to an integer in seconds.

    A rightly-formatted string is converted to seconds, treating it as
    hour:minutes.

      >>> from xm.tracker.browser.entry import time_to_seconds
      >>> time_to_seconds('4:22')
      15720

    The format has to have the right format:

      >>> time_to_seconds('4:4')
      Traceback (most recent call last):
      ...
      TimeformattingError: ...
      >>> time_to_seconds('4:444')
      Traceback (most recent call last):
      ...
      TimeformattingError: ...
      >>> time_to_seconds(':44')
      Traceback (most recent call last):
      ...
      TimeformattingError: ...
      >>> time_to_seconds('444:44')
      Traceback (most recent call last):
      ...
      TimeformattingError: ...
      >>> time_to_seconds('junk_without_semicolon')
      Traceback (most recent call last):
      ...
      TimeformattingError: ...

    Additionally, the hours and minutes have to be within the correct
    range. We'll test the corner cases that should still be allowed:

      >>> time_to_seconds('0:00')
      0
      >>> time_to_seconds('00:00')
      0
      >>> time_to_seconds('23:59') == 24 * 60 * 60 - 60
      True

    Now the unallowed ones.

      >>> time_to_seconds('44:44') # More than 23 hours
      Traceback (most recent call last):
      ...
      TimeformattingError: ...
      >>> time_to_seconds('-2:44') # Negative hours
      Traceback (most recent call last):
      ...
      TimeformattingError: ...
      >>> time_to_seconds('0:-1') # Negative minutes
      Traceback (most recent call last):
      ...
      TimeformattingError: ...
      >>> time_to_seconds('0:60') # More than 59
      Traceback (most recent call last):
      ...
      TimeformattingError: ...


    """
    if not ':' in time:
        raise TimeformattingError
    timelist = time.split(':')
    hours = timelist[0]
    minutes = timelist[1]
    # Check formatting
    if len(minutes) != 2:
        raise TimeformattingError
    if len(hours) > 2 or len(hours) < 1:
        raise TimeformattingError

    hours = int(hours)
    minutes = int(minutes)

    # Check ranges
    if hours > 23 or hours < 0:
        raise TimeformattingError
    if minutes > 59 or minutes < 0:
        raise TimeformattingError
    return minutes * 60 + hours * 3600


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

    render = ZopeTwoPageTemplateFile('templates/entries.pt')

    task = None

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.__parent__ = view

    def update(self):
        self.entries = []
        for entry in self.task.entries:
            time = round_time_to_minutes(entry.time)
            item = dict(date = entry.date.strftime('%d-%m'),
                        text = entry.text,
                        time = time.strftime('%H:%M'))
            self.entries.append(item)


class EditEntry(KSSTaskRefresher):

    @kssaction
    def edit_entry(self, **kwargs):
        """ In this call we handle a form which contains one entry.
        This entry has a text and time field which we expect to change.
        """
        plone = self.getCommandSet("plone")
        core = self.getCommandSet("core")
        tracker = get_tracker(self.context)
        text = self.request.get('text')
        if not text:
            message = _(u'msg_empty_text',
                        default=u'Empty text, this is not allowed')
            plone.issuePortalMessage(message, msgtype="error")
            return
        time = self.request.get('time')
        uid = self.request.get('uid')
        idx = int(self.request.get('entry_number'))

        task = tracker.get_task(uid)
        entry = task.entries[idx]
        try:
            seconds = time_to_seconds(time)
        except TimeformattingError:
            msg = _(u'Invalid time') + u' (0:00-23:59): ' + unicode(time)
            plone.issuePortalMessage(msg, msgtype='error')
            return
        entry.time = mx.DateTime.DateTimeDeltaFrom(seconds=seconds)
        entry.text = text
        message = _(u'msg_update_entry', default=u'Entry updated')
        plone.issuePortalMessage(message)

        # Refresh entire task to also update the remaining time and so. Keep
        # the details open.
        self.task_refresh(uid=uid, open_details=True)

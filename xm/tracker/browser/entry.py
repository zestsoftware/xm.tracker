from Products.statusmessages.interfaces import IStatusMessage

from xm.tracker.browser.tracker import TrackerView
from xm.tracker import XMTrackerMessageFactory as _

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
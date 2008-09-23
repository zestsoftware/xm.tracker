from Acquisition import aq_inner
from zope.cachedescriptors.property import Lazy
from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView
from zope.component import getMultiAdapter
import mx.DateTime

from xm.tracker import XMTrackerMessageFactory as _
from xm.tracker.browser.tracker import add_entry
from xm.tracker.browser.tracker import AddTasks
from xm.tracker.browser.viewlets import TaskViewlet


def get_tracker(context):
    tracker_view = context.restrictedTraverse('@@tracker')
    return tracker_view.tracker()


class KSSStart(PloneKSSView):
    """kss view for starting the timer"""

    @kssaction
    def start_timer(self):
        tracker = get_tracker(self.context)
        tracker.starttime = mx.DateTime.now()
        zope = self.getCommandSet('zope')
        zope.refreshProvider('#startstop', 'xm.tracker.startstop')
        message = _(u'msg_started_timer',
                    default=u'Started the timer')
        plone = self.getCommandSet("plone")
        plone.issuePortalMessage(message)


class KSSStop(PloneKSSView):
    """kss view for stopping the timer"""

    @kssaction
    def stop_timer(self):
        tracker = get_tracker(self.context)
        tracker.starttime = None
        zope = self.getCommandSet('zope')
        zope.refreshProvider('#startstop', 'xm.tracker.startstop')
        zope.refreshProvider('#timer', 'xm.tracker.timer')
        message = _(u'msg_stopped_timer',
                    default=u'Stopped the timer')
        plone = self.getCommandSet("plone")
        plone.issuePortalMessage(message)


class KSSTaskRefresher(PloneKSSView):
    """kss view for refreshing a task's display.

    Called by kss_track_time to refresh the remaining time and by the 'cancel'
    button of the entry inline-edit to make sure the entries are reset to the
    starting values. The cancel button is the reason for the uid= parameter as
    that's a submitted browser form.

    """

    @kssaction
    def task_refresh(self, uid=None, open_details=None, **kw):
        context = aq_inner(self.context)
        # Refresh task; TODO: identical in entry.py
        view = context.restrictedTraverse('@@tracker')
        self.request['task_uid'] = uid
        if open_details:
            self.request['open_details'] = True
        viewlet = TaskViewlet(context, self.request, view, None)
        viewlet.update()
        html = viewlet.render()
        core = self.getCommandSet("core")
        core.replaceHTML('#task-' + uid, html)
        zope = self.getCommandSet('zope')
        zope.refreshProvider('#timer', 'xm.tracker.timer')


class KSSTrackTime(KSSTaskRefresher):
    """kss view for adding an entry to a task"""

    @kssaction
    def track_time(self, uid, text):
        plone = self.getCommandSet("plone")
        if not text:
            message = _(u'msg_empty_text',
                        default=u'Empty text, this is not allowed')
            plone.issuePortalMessage(message, msgtype='error')
            return
        context = aq_inner(self.context)
        tracker = get_tracker(context)
        task = tracker.get_task(uid)
        if task is None:
            task = tracker.unassigned
        add_entry(tracker, task, text)

        self.task_refresh(uid=uid)

        message = _(u'msg_added_entry', default=u'Added entry')
        plone.issuePortalMessage(message)
        tracker.starttime = mx.DateTime.now()


class KSSSelectTasks(PloneKSSView, AddTasks):
    """KSS view for selecting tasks"""

    @kssaction
    def __call__(self):
        html = self.index() # Uses templates/select.pt
        core = self.getCommandSet("core")
        core.insertHTMLBefore('#content', html)


class KSSSelectTasksForUnassigned(KSSSelectTasks):
    """KSS view for selecting tasks for unassigned entries"""

    @Lazy
    def todo_tasks_per_project(self):
        """Return all available tasks using a helper method from xm itself.

        The only modification regarding KSSSelectTasks' version is a hack to
        select all tasks instead of just our own.

        """
        context = aq_inner(self.context)
        mytask_details = getMultiAdapter(
            (context, self.request), name=u'mytask_details')
        # Small hack that depends on internals of
        # Products.eXtremeManagement.browser.tasks.MyTasksDetailedView.
        del mytask_details.filter['getAssignees'] # Don't filter on ourselves.
        # End of hack.
        return mytask_details.projects()

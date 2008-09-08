from Acquisition import aq_inner
from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
import mx.DateTime

from xm.tracker import XMTrackerMessageFactory as _
from xm.tracker.tracker import Tracker
from xm.tracker.browser.tracker import add_entry
from xm.tracker.browser.tracker import TRACKER_KEY
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
        message = _(u'msg_stopped_timer',
                    default=u'Stopped the timer')
        plone = self.getCommandSet("plone")
        plone.issuePortalMessage(message)


class KSSTrackTime(PloneKSSView):
    """kss view for adding an entry to a task"""

    @kssaction
    def track_time(self, uid, text):
        plone = self.getCommandSet("plone")
        core = self.getCommandSet("core")
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

        # Refresh task; TODO: identical in entry.py
        view = context.restrictedTraverse('@@tracker')
        self.request['task_uid'] = uid
        viewlet = TaskViewlet(context, self.request, view, None)
        viewlet.update()
        html = viewlet.render()
        core.replaceHTML('#task-' + uid, html)

        message = _(u'msg_added_entry', default=u'Added entry')
        plone.issuePortalMessage(message)
        tracker.starttime = mx.DateTime.now()


class KSSSelectTasks(PloneKSSView):
    """KSS view for selecting tasks"""

    def tracker(self):
        # Copied from tracker.TrackerView pending later refactoring.
        context = aq_inner(self.context)
        portal_state = getMultiAdapter(
            (context, self.request), name=u'plone_portal_state')
        if portal_state.anonymous():
            return None
        member = portal_state.member()
        annotations = IAnnotations(member)
        tracker = annotations.get(TRACKER_KEY, None)
        if tracker is None or not hasattr(tracker, 'unassigned'):
            tracker = Tracker()
            annotations[TRACKER_KEY] = tracker

        return tracker

    def todo_tasks_per_project(self):
        """Return our own tasks using a helper method from xm itself.
        """
        # Copied from tracker.AddTasks
        context = aq_inner(self.context)
        mytask_details = getMultiAdapter(
            (context, self.request), name=u'mytask_details')
        return mytask_details.projects()

    @kssaction
    def __call__(self):
        html = self.index() # Uses templates/select.pt
        core = self.getCommandSet("core")
        core.insertHTMLBefore('#content', html)


class KSSSelectTasksForUnassigned(KSSSelectTasks):
    """KSS view for selecting tasks for unassigned entries"""

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

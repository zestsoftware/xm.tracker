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
        context = aq_inner(self.context)
        tracker = get_tracker(context)
        task = tracker.get_task(uid)
        if task is None:
            task = tracker.unassigned
        add_entry(tracker, task, text)
        view = context.restrictedTraverse('@@tracker')
        self.request['task_uid'] = uid
        viewlet = TaskViewlet(context, self.request, view, None)
        viewlet.update()
        html = viewlet.render()
        core = self.getCommandSet("core")
        core.replaceHTML('#task-' + uid, html)
        message = _(u'msg_added_entry', default=u'Added entry')
        plone = self.getCommandSet("plone")
        plone.issuePortalMessage(message)
        tracker.starttime = mx.DateTime.now()


class KSSSelectTasks(PloneKSSView):
    """KSS view for selecting tasks"""

    @kssaction
    def select_tasks(self):
        context = aq_inner(self.context)
        view = context.restrictedTraverse('@@tracker_select_tasks')
        html = view()
        core = self.getCommandSet("core")
        core.insertHTMLBefore('#content', html)


class KSSSelectTasksForUnassigned(PloneKSSView):
    """KSS view for selecting tasks for unassigned entries"""

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
        """For now we just get all to-do tasks here.
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

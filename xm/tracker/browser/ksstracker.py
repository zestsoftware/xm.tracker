import mx.DateTime
from Acquisition import aq_inner
from zope.i18n import translate
from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView

from xm.tracker import XMTrackerMessageFactory as _
from xm.tracker.browser.tracker import add_entry
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
        message = translate(_(u'msg_started_timer',
                              default=u'Started the timer'))
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
        message = translate(_(u'msg_stopped_timer',
                              default=u'Stopped the timer'))
        plone = self.getCommandSet("plone")
        plone.issuePortalMessage(message)


class KSSTrackTime(PloneKSSView):
    """kss view for adding an entry to a task"""
    
    @kssaction
    def track_time(self, uid, text):
        context = aq_inner(self.context)
        tracker = get_tracker(context)
        task = tracker.get_task(uid)
        add_entry(tracker, task, text)
        view = context.restrictedTraverse('@@tracker')
        viewlet = TaskViewlet(task, self.request, view, None)
        viewlet.update()
        html = viewlet.render()
        core = self.getCommandSet("core")
        core.replaceHTML('#task-' + uid, html)
        message = translate(_(u'msg_added_entry', default=u'Added entry'))
        plone = self.getCommandSet("plone")
        plone.issuePortalMessage(message)
    
        
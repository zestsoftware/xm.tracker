import mx.DateTime
from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView

from xm.tracker import XMTrackerMessageFactory as _


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
        message = _(u'msg_started_timer', default=u'Started the timer')
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
        message = _(u'msg_stopped_timer', default=u'Stopped the timer')
        plone = self.getCommandSet("plone")
        plone.issuePortalMessage(message)

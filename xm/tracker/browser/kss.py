from plone.app.kss.plonekssview import PloneKSSView
import mx.DateTime

def get_tracker(context):
    tracker_view = context.restrictedTraverse('@@tracker')
    return tracker_view.tracker()


class KSSStart(PloneKSSView):
    """kss view for starting the timer"""
    @kssaction
    def start_timer(self, text):
        """Add a note"""
        core = self.getCommandSet('core')
        selector = core.getHtmlIdSelector('task')
        tracker = get_tracker(self.context)
        tracker.starttime = mx.DateTime.now()
        message = _(u'msg_stopped_timer',
                    default=u'Stopped the timer')
        self.context.plone_utils.addPortalMessage(message)
        rendered = view.render()
        core.replaceHTML(selector, rendered)


class KSSStop(PloneKSSView):
    """kss view for stopping the timer"""
    @kssaction
    def start_timer(self, text):
        """Add a note"""
        core = self.getCommandSet('core')
        selector = core.getHtmlIdSelector('notes')
        message = simple_add_note(self.context, text)
        view = self.context.restrictedTraverse('@@plonehrm.notes')
        rendered = view.render()
        core.replaceHTML(selector, rendered)
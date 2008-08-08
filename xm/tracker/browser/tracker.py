from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from xm.tracker.tracker import Tracker
from Acquisition import aq_inner


class TrackerView(BrowserView):
    """View a tracker in the context of a Plone Site.
    """

    ANNO_KEY = 'xm-timetracker'

    def __call__(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter(
            (context, self.request), name=u'plone_portal_state')
        self.member = portal_state.member()
        if portal_state.anonymous():
            self.tracker = None
            self.member = None
            return
        annotations = IAnnotations(self.member)
        self.tracker = annotations.get(self.ANNO_KEY, None)
        if self.tracker is None:
            self.tracker = Tracker()
            annotations[self.ANNO_KEY] = self.tracker
        return self.index()

    def tasks(self):
        """ Returns a list of dicts each dict represents a task and has the
            following keys:

              - id
              - title
              - actual
              - remaining
              - entries

            The entries key contains a list of entries which have already been
            tracked. Each entry dict has:

              - id
              - date
              - description
              - time

        """
        pass

    def adhoc_entries(self):
        """ Returns a list of dicts, each dict represents an entry similar to
            the above.
        """
        pass

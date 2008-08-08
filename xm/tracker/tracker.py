"""
XM site       The project management site Zest is using.
Task          Task in the XM site
Booking       Booking for a task in the XM site.
Time Tracker  Separate window that can be opened from the XM site
Tracked task  A task from the XM site that is listed in the Time Tracker main
              screen.
Entry         An amount of time registered for a tracked task in the Time
              Tracker
Ad-hoc Entry  An Entry which is not directly related to a Tracked task,
              but can be booked as a Booking in the XM site
Main timer    The running timer on the top right of the main tracker screen


"""


from Products.CMFPlone.Portal import PloneSite
#from OFS.ObjectManager import ObjectManager
from persistent.list import PersistentList
from zope.annotation.interfaces import IAnnotations
from five import grok
from zope.component import getMultiAdapter


class TrackerIndex(grok.View):
    grok.context(PloneSite)
    grok.name('timetracker')
    ANNO_KEY = 'xm-timetracker'

    def __init__(self, context, request):
        super(TrackerIndex, self).__init__(context, request)
        portal_state = getMultiAdapter(
            (context, request), name=u'plone_portal_state')
        self.member = portal_state.member()
        if portal_state.anonymous():
            self.tracker = None
            return
        annotations = IAnnotations(self.member)
        self.tracker = annotations.get(self.ANNO_KEY, None)
        if self.tracker is None:
            self.tracker = Tracker()
            annotations[self.ANNO_KEY] = self.tracker

    def update(self, command=None):
        """
        if command == 'add':
            self.context[TRACKER_AREA_ID] = TrackerArea()
        if command == 'remove':
            del self.context[TRACKER_AREA_ID]
        """
        pass


class Tracker(grok.Model):

    def __init__(self):
        self.time = None
        self.tracked_tasks = []
        #self.adhoc_task = TrackedTask('ad-hoc')


class TrackedTask(grok.Model):
    """A task from the XM site that is listed in the Time Tracker main screen.
    """

    def __init__(self, title, story=None, project=None, estimate=None):
        self.title = title
        self.story = story
        self.project = project
        self.estimate = estimate
        self.entries = PersistentList()

# class Entry

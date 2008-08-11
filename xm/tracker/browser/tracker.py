from random import random
import mx.DateTime
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.cachedescriptors.property import Lazy
from zope.component import getMultiAdapter
from zope.interface import classImplements
from persistent.list import PersistentList
from Products.PlonePAS.tools.memberdata import MemberData

from xm.tracker.tracker import Tracker
from xm.tracker.tracker import Task
from xm.tracker.tracker import Entry

TRACKER_KEY = 'xm-timetracker'
classImplements(MemberData, IAttributeAnnotatable)


class TrackerView(BrowserView):
    """View a tracker in the context of a Plone Site.
    """

    def tracker(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter(
            (context, self.request), name=u'plone_portal_state')
        if portal_state.anonymous():
            return None
        member = portal_state.member()
        annotations = IAnnotations(member)
        tracker = annotations.get(TRACKER_KEY, None)
        if tracker is None:
            tracker = Tracker()
            annotations[TRACKER_KEY] = tracker

        return tracker

    def time_spent(self):
        now = mx.DateTime.now()
        previous = self.tracker().starttime or now
        time = now - previous
        return time

    def __call__(self):
        # Handle form here.        
        tracker = self.tracker()
        start = self.request.get('start', False)
        stop = self.request.get('stop', False)
        demo = self.request.get('demo', False)
        track = self.request.get('track', False)
        now = mx.DateTime.now()
        if start:
            tracker.starttime = now
        if stop:
            tracker.starttime = None
        if demo:
            tracker.tasks = PersistentList()
            for i in range(3):
                task = Task("Task %d" % i,
                                   story = "Story %d" % i,
                                   project = "Project %d" % i,
                                   estimate = round(random() * 10))
                tracker.tasks.append(task)

        if track:
            task_id = int(self.request.get('task_id', 0))
            if task_id == 0:
                # Handle untracked task with this?
                pass
            task_id -= 1
            text = self.request.get('text')
            task = tracker.tasks[task_id]
            task.entries.append(Entry(text, self.time_spent()))
            # This must be last:
            tracker.starttime = now
        return self.index()


    def track_time(self, task_uid):
        """ Method to track time to a task
        """
        pass

    def stop_timer(self):
        self.tracker().starttime = None


    def tasks(self):
        """
        """
        pass

    def adhoc_entries(self):
        """ Returns a list of dicts, each dict represents an entry similar to
            the above.
        """
        pass

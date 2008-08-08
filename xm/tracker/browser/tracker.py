from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from xm.tracker.tracker import Tracker
from xm.tracker.tracker import TrackedTask
from xm.tracker.tracker import Entry
from Acquisition import aq_inner
from persistent.list import PersistentList
from zope.cachedescriptors.property import Lazy
from random import random
import mx.DateTime


class TrackerView(BrowserView):
    """View a tracker in the context of a Plone Site.
    """

    ANNO_KEY = 'xm-timetracker'

    @Lazy
    def tracker(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter(
            (context, self.request), name=u'plone_portal_state')
        if portal_state.anonymous():
            return None
        member = portal_state.member()
        annotations = IAnnotations(member)
        tracker = annotations.get(self.ANNO_KEY, None)
        if tracker is None:
            tracker = Tracker()
            annotations[self.ANNO_KEY] = tracker
        if tracker.time is None:
            tracker.time = 0.0
        return tracker

    def time_spent(self):
        now = mx.DateTime.now()
        previous = self.tracker.time or now
        return now - previous

    def __call__(self):
        # Handle form here.
        start = self.request.get('start', False)
        stop = self.request.get('stop', False)
        demo = self.request.get('demo', False)
        track = self.request.get('track', False)
        now = mx.DateTime.now()
        if start:
            self.tracker.time = now
        if stop:
            self.tracker.time = None
        if demo:
            self.tracker.time = 0.0
            self.tracker.tracked_tasks = PersistentList()
            for i in range(3):
                task = TrackedTask("Task %d" % i,
                                   story = "Story %d" % i,
                                   project = "Project %d" % i,
                                   estimate = round(random() * 10))
                self.tracker.tracked_tasks.append(task)

        if track:
            task_id = int(self.request.get('task_id', 0))
            if task_id == 0:
                # Handle untracked task with this?
                pass
            task_id -= 1
            text = self.request.get('text')
            tracked_task = self.tracker.tracked_tasks[task_id]
            tracked_task.entries.append(Entry(text, self.time_spent()))
            # This must be last:
            self.tracker.time = now
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

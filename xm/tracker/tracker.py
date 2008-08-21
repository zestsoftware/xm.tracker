"""
XM site       The project management site Zest is using.
XM Task       Task content type in the XM site, added within a Story.
Booking       Booking for a task in the XM site.
Time Tracker  Separate window that can be opened from the XM site
Task          A task from the XM site that is listed in the Time Tracker main
              screen.
Entry         An amount of time registered for a tracked task in the Time
              Tracker
Ad-hoc entry  An entry which is not directly related to an xm task,
              but can be booked as a Booking in the XM site
Main timer    The running timer on the top right of the main tracker screen


"""
from persistent import Persistent
from persistent.list import PersistentList
from zope.interface import implements
import mx.DateTime

from xm.tracker.interfaces import ITracker, ITask, IEntry
from xm.tracker import XMTrackerMessageFactory as _


class Tracker(Persistent):
    """ A tracker that manages a list of tasks
    """
    implements(ITracker)

    def __init__(self):
        self.starttime = None
        self.tasks = PersistentList()
        self.unassigned = BaseTask()

    def get_task(self, uid):
        for task in self.tasks:
            if task.uid == uid:
                return task


class BaseTask(Persistent):
    """A basic task that is listed in the Time Tracker main screen.

    Can be used for tracking entries that have no assigned task yet.
    """
    implements(ITask)

    def __init__(self):
        self.uid = 'unassigned'
        self.title = u'Unassigned'
        self.entries = PersistentList()

    def total_time(self):
        total = sum([entry.time for entry in self.entries])
        if total == 0:
            return mx.DateTime.DateTimeDeltaFromSeconds(0)
        return total


class Task(BaseTask):
    """A task from the XM site that is listed in the Time Tracker main screen.
    """
    implements(ITask)

    def __init__(self, title, uid=None, story=None, project=None,
                 estimate=None):
        self.uid = uid
        self.title = title
        self.story = story
        self.project = project
        self.estimate = estimate
        self.entries = PersistentList()


class Entry(Persistent):
    """ An entry in the timelog
    """
    implements(IEntry)

    def __init__(self, text, time):
        self.text = text
        if isinstance(time, basestring) or isinstance(time, float):
            time = int(time)
        if isinstance(time, int):
            time = mx.DateTime.DateTimeDeltaFromSeconds(time)
        self.time = time
        self.date = mx.DateTime.now()

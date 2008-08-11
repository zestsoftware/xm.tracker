"""
XM site       The project management site Zest is using.
Task          Task in the XM site
Booking       Booking for a task in the XM site.
Time Tracker  Separate window that can be opened from the XM site
Task          A task from the XM site that is listed in the Time Tracker main
              screen.
Entry         An amount of time registered for a tracked task in the Time
              Tracker
Ad-hoc Entry  An Entry which is not directly related to a Tracked task,
              but can be booked as a Booking in the XM site
Main timer    The running timer on the top right of the main tracker screen


"""
from persistent import Persistent
from persistent.list import PersistentList
from zope.interface import implements
from mx.DateTime import now
from mx.DateTime import DateTimeDeltaFromSeconds
from Products.CMFCore.utils import getToolByName

from xm.tracker.interfaces import ITracker, ITask, IEntry


class Tracker(Persistent):
    """ A tracker that manages a list of tasks 
    """
    implements(ITracker)

    def __init__(self):
        self.starttime = None
        self.tasks = PersistentList()


class Task(Persistent):
    """A task from the XM site that is listed in the Time Tracker main screen.
    """
    implements(ITask)
    def __init__(self, title, task_uid=None, story=None, project=None,
                 estimate=None):
        self.task_uid = task_uid
        self.title = title
        self.story = story
        self.project = project
        self.estimate = estimate
        self.entries = PersistentList()
        
    def total_time(self):
        return sum([entry.time for entry in self.entries])
            


class Entry(Persistent):
    """ An entry in the timelog
    """
    implements(IEntry)

    def __init__(self, text, time):
        self.text = text
        delta = DateTimeDeltaFromSeconds(time)
        self.time = delta
        self.date = now()

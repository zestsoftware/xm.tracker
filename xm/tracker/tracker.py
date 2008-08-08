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


#from OFS.ObjectManager import ObjectManager
from persistent.list import PersistentList
from persistent import Persistent
from zope.annotation.interfaces import IAttributeAnnotatable

from Products.PlonePAS.tools.memberdata import MemberData
from zope.interface import classImplements


classImplements(MemberData, IAttributeAnnotatable)



class Tracker(Persistent):

    def __init__(self):
        self.time = 0.0
        self.tracked_tasks = PersistentList()
        #self.adhoc_task = TrackedTask('ad-hoc')


class TrackedTask(Persistent):
    """A task from the XM site that is listed in the Time Tracker main screen.
    """

    def __init__(self, title, story=None, project=None, estimate=None):
        self.title = title
        self.story = story
        self.project = project
        self.estimate = estimate
        self.entries = PersistentList()


class Entry(Persistent):
    
    def __init__(self, text, time):
        self.text = text
        self.time = time

from random import random
import mx.DateTime
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import getMultiAdapter
from zope.interface import classImplements
from persistent.list import PersistentList
from Products.PlonePAS.tools.memberdata import MemberData
from Products.CMFCore.utils import getToolByName

from xm.tracker.tracker import Tracker
from xm.tracker.tracker import Task
from xm.tracker.tracker import Entry
from xm.tracker import XMTrackerMessageFactory as _


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
        return time.strftime("%H:%M:%S")

    def __call__(self):
        # XXX This one will be removed, use separate views
        tracker = self.tracker()
        ### Remove before releasing
        demo = self.request.get('demo', False)
        if demo:
            tracker.tasks = PersistentList()
            for i in range(3):
                task = Task("Task %d" % i,
                            uid = "slk3aJKE@$SKDGAA%d" % i,
                            story = "Story %d" % i,
                            project = "Project %d" % i,
                            estimate = round(random() * 10))
                tracker.tasks.append(task)
            tracker.tasks[0].entries.append(Entry('Did my homework', 86400))
            tracker.tasks[0].entries.append(Entry('Did my thing', 3600))

        return self.index()


class Stop(BrowserView):
    """ This view stops the timer"""

    def __call__(self):
        trackerview = self.context.restrictedTraverse('@@tracker')
        tracker = trackerview.tracker()
        tracker.starttime = None
        message = _(u'msg_stopped_timer',
                    default=u'Stopped the timer')
        self.context.plone_utils.addPortalMessage(message)
        response = self.request.response
        response.redirect('@@tracker')


class Start(BrowserView):
    """ This view starts the timer"""

    def __call__(self):
        trackerview = self.context.restrictedTraverse('@@tracker')
        tracker = trackerview.tracker()
        tracker.starttime = mx.DateTime.now()
        message = _(u'msg_started_timer',
                    default=u'Started the timer')
        self.context.plone_utils.addPortalMessage(message)
        response = self.request.response
        response.redirect('@@tracker')


class TrackTime(BrowserView):
    """ This view stores an entry for a given task"""

    def __call__(self):
        uid = self.request.get('uid')
        text = self.request.get('text')
        trackerview = self.context.restrictedTraverse('@@tracker')
        tracker = trackerview.tracker()
        task = tracker.get_task(uid)
        if task is None:
            message = _(u'msg_no_task_found',
                        default=u'No task found with this UID')
            self.context.plone_utils.addPortalMessage(message)
            response = self.request.response
            response.redirect('@@tracker')
        time = tracker.starttime - mx.DateTime.now()
        task.entries.append(Entry(text, time))
        # Reset the timer's start time
        tracker.starttime = mx.DateTime.now()
        message = _(u'msg_added_entry',
                    default=u'Added entry')
        self.context.plone_utils.addPortalMessage(message)
        response = self.request.response
        response.redirect('@@tracker')


class Book(BrowserView):
    """ This view stores a booking for a given task """

    def __call__(self):
        uid = self.request.get('uid')
        trackerview = self.context.restrictedTraverse('@@tracker')
        tracker = trackerview.tracker()
        task = tracker.get_task(uid)
        if task.entries is None:
            message = _(u'msg_no_entries_found',
                        default=u'No entries found for this task')
        else:
            uid_catalog = getToolByName(self.context, 'uid_catalog')
            brains = uid_catalog({'UID': uid})
            if brains is None:
                message = _(u'msg_no_task_found',
                            default=u'No task found with this UID')
            else:
                xmtask = brains[0].getObject()
                booking = xmtask.invokeFactory(type_name='Booking', id='bogus')
                hours = task.total_time().hours
                minutes = task.total_time().minutes
                description = ''
                for entry in task.entries:
                    description += (entry.text + '\n')
                booking.edit({'setHours': hours,
                              'setMinutes': minutes,
                              'Title': task[0].entries[0],
                              'setDescription': description})
                message = _(u'msg_added_booking',
                            default=u'Added booking to task')
                if self.request.get('bookandclose', None):
                    self.context.portal_workflow.doActionFor(
                        xmtask, 'mark_completed')
                    message = _(u'msg_added_booking_closed_task',
                                default=u'Added booking to task and closed it')
        self.context.plone_utils.addPortalMessage(message)
        response = self.request.response
        response.redirect('@@tracker')

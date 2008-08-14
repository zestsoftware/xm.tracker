from random import random
import math

import mx.DateTime
import transaction
from AccessControl import Unauthorized
from Acquisition import aq_inner, Explicit
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import getMultiAdapter
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import implements
from zope.interface import Interface
from zope.component import adapts
from zope.interface import classImplements
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from persistent.list import PersistentList
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.PlonePAS.tools.memberdata import MemberData
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException

from xm.tracker.tracker import Tracker
from xm.tracker.tracker import Task
from xm.tracker.tracker import Entry
from xm.tracker import XMTrackerMessageFactory as _
from xm.booking.browser.add import create_booking


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


class AddTasks(TrackerView):
    """Make links to real xm tasks in the tracker.
    """

    def __call__(self):
        tracker = self.tracker()
        # Clean the current tasks, for demoing.
        tracker.tasks = PersistentList()
        for xm_task in self.selected_tasks():
            task = Task(xm_task['title'],
                        uid = xm_task['UID'],
                        story = xm_task['story_title'],
                        project = "Project unknown",
                        estimate = xm_task['estimate'])
            tracker.tasks.append(task)

        response = self.request.response
        response.redirect('@@tracker')

    def selected_tasks(self):
        """For now we just get all to-do tasks here.
        """
        context = aq_inner(self.context)
        mytask_details = getMultiAdapter(
            (context, self.request), name=u'mytask_details')
        return mytask_details.tasklist().get('tasks')


class Demo(TrackerView):
    """ This view adds demo data.  Only for development.

    XXX Remove before releasing.
    """

    def __call__(self):
        tracker = self.tracker()
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

        response = self.request.response
        response.redirect('@@tracker')


class StartStopProvider(Explicit):
    """ This view renders the start/stop button of the timer
    """
    adapts(Interface, IDefaultBrowserLayer, Interface)

    render = ZopeTwoPageTemplateFile('startstop.pt')
    
    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.__parent__ = view

    def update(self):
        tracker = self.context.restrictedTraverse('@@tracker').tracker()
        self.is_started = bool(tracker.starttime)



class Stop(TrackerView):
    """ This view stops the timer"""

    def __call__(self):
        tracker = self.tracker()
        tracker.starttime = None
        message = _(u'msg_stopped_timer',
                    default=u'Stopped the timer')
        self.context.plone_utils.addPortalMessage(message)
        response = self.request.response
        response.redirect('@@tracker')


class Start(TrackerView):
    """ This view starts the timer"""

    def __call__(self):
        tracker = self.tracker()
        tracker.starttime = mx.DateTime.now()
        message = _(u'msg_started_timer',
                    default=u'Started the timer')
        self.context.plone_utils.addPortalMessage(message)
        response = self.request.response
        response.redirect('@@tracker')


class TrackTime(TrackerView):
    """ This view stores an entry for a given task"""

    def __call__(self):
        uid = self.request.get('uid')
        text = self.request.get('text')
        tracker = self.tracker()
        task = tracker.get_task(uid)
        if task is None:
            message = _(u'msg_no_task_found',
                        default=u'No task found with this UID')
            self.context.plone_utils.addPortalMessage(message)
            response = self.request.response
            response.redirect('@@tracker')
        current_time = mx.DateTime.now()
        time = current_time - tracker.starttime
        if not text:
            text = task.title
        task.entries.append(Entry(text, time))
        # Reset the timer's start time
        tracker.starttime = current_time
        message = _(u'msg_added_entry',
                    default=u'Added entry')
        self.context.plone_utils.addPortalMessage(message)
        response = self.request.response
        response.redirect('@@tracker')


class Book(TrackerView):
    """ This view stores a booking for a given task """

    def __call__(self):
        uid = self.request.get('uid')
        tracker = self.tracker()
        task = tracker.get_task(uid)
        if len(task.entries) == 0:
            message = _(u'msg_no_entries_found',
                        default=u'No entries found for this task')
            self.redirect_to_tracker(message)
            return

        uid_catalog = getToolByName(self.context, 'uid_catalog')
        brains = uid_catalog({'UID': uid})
        if brains is None:
            message = _(u'msg_no_task_found',
                        default=u'No task found with this UID')
            self.redirect_to_tracker(message)
            return

        xmtask = brains[0].getObject()
        hours = task.total_time().hours
        minutes = task.total_time().minutes
        # make quarters of this.
        # XXX rounding up now to ease testing.
        #minutes = int(round(minutes / 15.0) * 15)
        minutes = int(math.ceil(minutes / 15.0) * 15)
        # Using the title of the first entry as title of the complete
        # booking.
        title = task.entries[0].text
        description = u''
        if len(task.entries) > 1:
            for entry in task.entries:
                description += (entry.text + '\n')
        try:
            create_booking(xmtask, title=title, hours=hours,
                           minutes=minutes, description=description)
        except Unauthorized:
            message = _(u'msg_failed_add_booking',
                        default=u'Not permitted to add booking to task. Check'
                                u' if the task is in the correct state.')
            self.redirect_to_tracker(message)
            return

        message = _(u'msg_added_booking',
                    default=u'Added booking to task')
        # Remove current entries.  No need to book twice...
        task.entries = PersistentList()
        if not self.request.get('book_and_close', None):
            self.redirect_to_tracker(message)
            return

        # The next part is really a separate action so it
        # needs a transaction commit before it.  Without it,
        # the adding of a booking above fails with an
        # Unauthorized error because the xm task is closed
        # below...
        # XXX is this save?  Can anything unforeseen happen?
        # XXX Perhaps just do a redirect instead to a 'Close' view.
        transaction.commit()

        try:
            self.context.portal_workflow.doActionFor(
                xmtask, 'complete')
        except WorkflowException:
            message = _(u'msg_added_booking_failed_to_close_task',
                        default=u'Added booking to task but closing failed.')
            self.redirect_to_tracker(message)
            return

        # Remove the tracked task as it is not needed anymore.
        tracker.tasks.remove(task)
        message = _(u'msg_added_booking_closed_task',
                    default=u'Added booking to task and closed it')
        self.redirect_to_tracker(message)

    def redirect_to_tracker(self, message= None):
        if message is not None:
            self.context.plone_utils.addPortalMessage(message)
        response = self.request.response
        response.redirect('@@tracker')

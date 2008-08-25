from random import random
import math

from AccessControl import Unauthorized
from Acquisition import aq_inner, Explicit
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.PlonePAS.tools.memberdata import MemberData
from Products.statusmessages.interfaces import IStatusMessage
from persistent.list import PersistentList
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.interface import classImplements
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
import mx.DateTime

from xm.booking.browser.add import create_booking
from xm.tracker import XMTrackerMessageFactory as _
from xm.tracker.tracker import Entry
from xm.tracker.tracker import Task
from xm.tracker.tracker import Tracker


TRACKER_KEY = 'xm-timetracker'
classImplements(MemberData, IAttributeAnnotatable)

def add_entry(tracker, task, text):
    current_time = mx.DateTime.now()
    time = current_time - tracker.starttime
    task.entries.append(Entry(text, time))
    # Reset the timer's start time
    tracker.starttime = current_time


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
        if tracker is None or not hasattr(tracker, 'unassigned'):
            tracker = Tracker()
            annotations[TRACKER_KEY] = tracker

        return tracker

    def time_spent(self):
        now = mx.DateTime.now()
        previous = self.tracker().starttime or now
        time = now - previous
        fmt = "%M:%S"
        if time.hours > 1.0:
            fmt = "%H:%M:%S"
        return time.strftime(fmt)

    def seconds_spent(self):
        now = mx.DateTime.now()
        previous = self.tracker().starttime or now
        time = now - previous
        return round(time.seconds)



class AddTasks(TrackerView):
    """Make links to real xm tasks in the tracker.
    """

    def __call__(self):
        tracker = self.tracker()
        # Remove tasks:
        #tracker.tasks = PersistentList()
        selected_task_uids = self.request.get('selected_task_uids', [])
        # Currently, we only support adding tasks to the tracker that
        # are already in the todo-list of this user.
        for project_info in self.todo_tasks_per_project():
            projectbrain = project_info['project']
            xm_tasks = project_info['tasks']
            for xm_task in xm_tasks:
                task_uid = xm_task['UID']
                if len(selected_task_uids) > 0 \
                        and task_uid not in selected_task_uids:
                    # XXX remove task if it was previously selected
                    task = tracker.get_task(task_uid)
                    if task is None:
                        # We cannot remove it because it was already
                        # removed.  No need to bother the user with
                        # this.
                        continue
                    if task.total_time() > 0:
                        # This task still has time that needs to be
                        # booked.  So we do not close it.  The user
                        # should not have been able to deselect it in
                        # the first place.  We could add a warning.
                        continue
                    # Remove the task.
                    tracker.tasks.remove(task)
                    continue
                task = tracker.get_task(task_uid)
                if task is not None:
                    # Task is already in the tracker.
                    continue
                task = Task(xm_task['title'],
                            uid = xm_task['UID'],
                            story = xm_task['story_title'],
                            project = projectbrain.Title,
                            estimate = xm_task['estimate'])
                tracker.tasks.append(task)
        self.request.response.redirect('@@tracker')

    def todo_tasks_per_project(self):
        """For now we just get all to-do tasks here.
        """
        context = aq_inner(self.context)
        mytask_details = getMultiAdapter(
            (context, self.request), name=u'mytask_details')
        return mytask_details.projects()


class SelectTasks(AddTasks):
    """Select real xm tasks for adding to the tracker.
    """

    def __call__(self):
        return self.index()


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
        msg = _(u'msg_stopped_timer', default=u'Stopped the timer')
        IStatusMessage(self.request).addStatusMessage(msg, type="info")
        self.request.response.redirect('@@tracker')


class Start(TrackerView):
    """ This view starts the timer"""

    def __call__(self):
        tracker = self.tracker()
        tracker.starttime = mx.DateTime.now()
        msg = _(u'msg_started_timer', default=u'Started the timer')
        IStatusMessage(self.request).addStatusMessage(msg, type="info")
        self.request.response.redirect('@@tracker')


class TrackTime(TrackerView):
    """ This view stores an entry for a given task"""

    def __call__(self):
        uid = self.request.get('uid')
        text = self.request.get('text')
        if not text:
            msg = _(u'msg_missing_description',
                    default='Entry not added. Please provide a description.')
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            self.request.response.redirect('@@tracker')
            return

        tracker = self.tracker()
        if tracker.starttime is None:
            msg = _(u'msg_no_tracking_without_starttime',
                    default=u'Cannot track time when the tracker has not '
                            u'started.')
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            self.request.response.redirect('@@tracker')
            return

        task = tracker.get_task(uid)
        if task is None:
            # We are dealing with an unassigned entry
            task = tracker.unassigned
        add_entry(tracker, task, text)
        tracker.starttime = mx.DateTime.now()
        msg = _(u'msg_added_entry', default=u'Added entry')
        IStatusMessage(self.request).addStatusMessage(msg, type="info")
        self.request.response.redirect('@@tracker')


class Book(TrackerView):
    """ This view stores a booking for a given task """

    def __call__(self):
        uid = self.request.get('uid')
        tracker = self.tracker()
        task = tracker.get_task(uid)
        if len(task.entries) == 0:
            msg = _(u'msg_no_entries_found',
                    default=u'No entries found for this task')
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            self.request.response.redirect('@@tracker')
            return

        uid_catalog = getToolByName(self.context, 'uid_catalog')
        brains = uid_catalog({'UID': uid})
        if len(brains) == 0:
            msg = _(u'msg_no_task_found',
                    default=u'No task found with this UID')
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            self.request.response.redirect('@@tracker')
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
            msg = _(u'msg_failed_add_booking',
                    default=u'Not permitted to add booking to task. Check'
                            u' if the task is in the correct state.')
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            self.request.response.redirect('@@tracker')
            return

        msg = _(u'msg_added_booking', default=u'Added booking to task')
        IStatusMessage(self.request).addStatusMessage(msg, type="info")
        # Remove current entries.  No need to book twice...
        task.entries = PersistentList()
        if self.request.get('book_and_close', None):
            # When redirecting we get a new request, so the uid
            # parameter gets lost, so we need to add it here ourselves.
            self.request.response.redirect('@@close_task?uid=%s' % uid)
        else:
            self.request.response.redirect('@@tracker')


class CloseTask(TrackerView):
    """This view closes an xm task."""

    def __call__(self):
        uid = self.request.get('uid')
        uid_catalog = getToolByName(self.context, 'uid_catalog')
        brains = uid_catalog({'UID': uid})
        if len(brains) == 0:
            msg = _(u'msg_no_task_found',
                    default=u'No task found with this UID')
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            self.request.response.redirect('@@tracker')
            return

        xmtask = brains[0].getObject()
        try:
            self.context.portal_workflow.doActionFor(xmtask, 'complete')
        except WorkflowException:
            msg = _(u'msg_close_task_failed',
                    default=u'Closing of task failed.')
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            self.request.response.redirect('@@tracker')
            return

        # Remove the tracked task as it is not needed anymore.
        tracker = self.tracker()
        task = tracker.get_task(uid)
        tracker.tasks.remove(task)
        msg = _(u'msg_close_task_success', default=u'Task has been closed.')
        IStatusMessage(self.request).addStatusMessage(msg, type="info")
        self.request.response.redirect('@@tracker')

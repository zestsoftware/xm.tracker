from zope.interface import Interface
from zope.interface import Attribute


class ITracker(Interface):
    """ A tracker will be provided for each member of the site.
    The tracker manages a list of tasks and the starttime of the timer.
    """

    starttime = Attribute("Start Time")
    tasks = Attribute("Tracked Tasks")
    unassigned = Attribute("A Task for unassigned entries")

    def get_task(uid):
        """ Get a task by providing a uid
        """
        pass


class ITask(Interface):
    """A task represents a XMtask from eXtremeManagement. It copies a few
    attributes and stores a list of entries.
    """

    uid = Attribute("UID of the XMTask for adding bookings")
    title = Attribute("Title of the task")
    story = Attribute("Title of the parent story")
    project = Attribute("Title of the project")
    estimate = Attribute("The estimated number of hours")
    entries = Attribute("List of timelog entries for this task")

    def total_time():
        """ Return a DateTimeDelta of the sum of entries for a task
        """
        pass


class IEntry(Interface):
    """ Entries represent what the user has worked on.
    """

    text = Attribute("Description of the work.")
    time = Attribute("The duration of the work.")
    date = Attribute("The date at which the work was done.")

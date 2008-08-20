from zope.contentprovider.interfaces import ITALNamespaceData
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import directlyProvides
from zope.publisher.interfaces.browser import IBrowserView
import zope.schema
from zope.viewlet.interfaces import IViewletManager
from zope.viewlet.interfaces import IViewlet


class ITrackerView(IBrowserView):
    """
    """

    def tracker():
        """ Returns the tracker object stored in an Annotation on the
        MemberData object.
        """
        pass

    def spent_time():
        """ Return a DateTimeDelta
        """
        pass


class ITrackTime(IBrowserView):
    """ Marker interface for the TrackTime view. This view save an entry for
    a given task.
    """


class IBook(IBrowserView):
    """ Marker interface for the Book view, which adds a Booking to the
    associated XMTask.
    """


class ITaskListManager(IViewletManager):
    """Show a list of tasks.
    """


class ITaskViewlet(IViewlet):
    """Show a task.
    """

    task = Attribute("A task object")

    def total_time():
        """ Returns the total time of all entries
        """

    def entries():
        """ Returns a list of entry objects
        """

    def tracker_has_started():
        """ Returns a boolean state for the timer
        """


class ITaskEntries(Interface):
    """ Interface for transferring a task from the TALNamespace to our provider
    """
    task = zope.schema.Text(title=u'A task object')

directlyProvides(ITaskEntries, ITALNamespaceData)

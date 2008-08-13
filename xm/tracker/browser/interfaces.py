from zope.publisher.interfaces.browser import IBrowserView
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

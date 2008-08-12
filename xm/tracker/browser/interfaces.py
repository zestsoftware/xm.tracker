from zope.publisher.interfaces.browser import IBrowserView


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
        
    def track_time(uid):
        """ Method to track time to a task
        """
        pass
        
    def stop_timer():
        """ This method will set the starttime of the tracker to None
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
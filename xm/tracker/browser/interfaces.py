from zope.publisher.interfaces.browser import IBrowserView


class ITrackerView(IBrowserView):
    """
    """
    
    #def tracker():
    #    """ Returns the tracker object stored in an Annotation on the
    #    MemberData object.
    #    """
    #    pass
    
    def spent_time():
        """ Return a DateTimeDelta
        """
        pass

    def tasks():
        """ Returns a list of dicts each dict represents a task and has the
            following keys:

              - id
              - title
              - actual
              - remaining
              - entries

            The entries key contains a list of entries which have already been
            tracked. Each entry dict has:

              - id
              - date
              - description
              - time
        
        """
        pass
        
    def track_time(task_uid):
        """ Method to track time to a task
        """
        
    def stop_timer():
        pass

    def adhoc_entries():
        pass

from zope.publisher.interfaces.browser import IBrowserView


class ITrackerView(IBrowserView):
    """
    """

    def tracked_tasks():
        pass

    def adhoc_entries():
        pass

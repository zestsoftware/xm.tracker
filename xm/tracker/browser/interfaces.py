from zope.publisher.interfaces.browser import IBrowserView


class ITrackerView(IBrowserView):
    """Return management info about all projects.
    Specifically: which iterations can be invoiced.
    """

    def tasks():
        pass

    def adhoc_entries():
        pass

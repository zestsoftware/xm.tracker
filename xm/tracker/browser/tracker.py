from Products.Five.browser import BrowserView


class TrackerView(BrowserView):
    """Return management info about all projects.
    Specifically: which iterations can be invoiced.
    """

    def tasks(self):
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

    def adhoc_entries(self):
        """ Returns a list of dicts, each dict represents an entry similar to
            the above.
        """
        pass

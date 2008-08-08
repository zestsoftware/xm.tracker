from Products.CMFPlone.Portal import PloneSite
from five import grok


class SiteTracker(grok.View):
    grok.context(PloneSite)
    grok.name('groktest')

    def render(self):
        return u"Me Grok view PloneSite."



class TimeEntry(object):
    """docstring for TimeEntry"""

    def __init__(self, arg):
        super(TimeEntry, self).__init__()
        self.arg = arg
        

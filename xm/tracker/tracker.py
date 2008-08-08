from Products.CMFPlone.Portal import PloneSite
from five import grok


TRACKER_AREA_ID = 'xm-time-tracker-area'

class SiteTracker(grok.View):
    grok.context(PloneSite)
    grok.name('xm-add-time-tracker')
    
    def area(self):
        return self.context.get(TRACKER_AREA_ID)

    def area_url(self):
        return self.context.absolute_url() + '/' + TRACKER_AREA_ID

    def update(self, command=None):
        if command == 'add':
            self.context[TRACKER_AREA_ID] = TrackerArea()
        if command == 'remove':
            del self.context[TRACKER_AREA_ID]


class TrackerArea(grok.Model):
    pass


class Index(grok.View):
    #grok.context(TrackerArea)
    pass



class TimeEntry(object):
    """docstring for TimeEntry"""

    def __init__(self, arg):
        super(TimeEntry, self).__init__()
        self.arg = arg
        

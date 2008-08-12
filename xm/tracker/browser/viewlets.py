from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter


class TaskViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('task.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.entries = self._get_entries()

    def _get_entries(self):
        """
        """
        tracker = getMultiAdapter((self.context, self.request),
                                    name=u'tracker')
        result = []
        for entry in tracker.entries:
            result.append(dict(
                text = entry.text,
                time = entry.time.strftime('%H:%M:%S'), ))
        return result

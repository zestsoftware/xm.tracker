from zope.i18nmessageid import MessageFactory
from Products.CMFCore.permissions import setDefaultRoles


XMTrackerMessageFactory = MessageFactory('tracker')

setDefaultRoles("eXtremeManagement: View Tracker",
                ('Projectmanager', 'Employee', 'Manager', 'Member'))


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

from Products.CMFCore.permissions import setDefaultRoles

setDefaultRoles("eXtremeManagement: View Tracker",
                ('Projectmanager', 'Employee'))


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

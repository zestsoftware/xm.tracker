from zope.i18nmessageid import MessageFactory

XMTrackerMessageFactory = MessageFactory('tracker')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

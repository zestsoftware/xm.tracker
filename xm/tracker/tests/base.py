from Products.PloneTestCase import PloneTestCase as ptc
from Products.eXtremeManagement.tests.base import XMLayer


class TestCase(ptc.PloneTestCase):
    layer = XMLayer


class FunctionalTestCase(ptc.FunctionalTestCase, TestCase):
    """Test case for functional (browser) tests.
    """
    layer = XMLayer

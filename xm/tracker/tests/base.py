from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.eXtremeManagement.tests.base import XMLayer


class TestCase(ptc.PloneTestCase):
    layer = XMLayer


class FunctionalTestCase(ptc.FunctionalTestCase, TestCase):
    """Test case for functional (browser) tests.
    """
    layer = XMLayer

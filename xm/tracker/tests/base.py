from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
import xm.tracker
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase.layer import onsetup
from Products.eXtremeManagement.tests.base import XMLayer

ztc.installProduct('Poi')
ztc.installProduct('eXtremeManagement')


@onsetup
def xm_setup():
    """Set up our Plone Site.
    """
    fiveconfigure.debug_mode = True
    import xm.booking
    zcml.load_config('configure.zcml', xm.booking)
    import xm.portlets
    zcml.load_config('configure.zcml', xm.portlets)
    fiveconfigure.debug_mode = False

xm_setup()
ptc.setupPloneSite(products=['Products.eXtremeManagement'])


class TestCase(ptc.PloneTestCase):
    layer = XMLayer


class FunctionalTestCase(ptc.FunctionalTestCase, TestCase):
    """Test case for functional (browser) tests.
    """
    layer = XMLayer

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
import xm.tracker
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

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

ptc.setupPloneSite(products=['Products.eXtremeManagement'])


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             xm.tracker)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

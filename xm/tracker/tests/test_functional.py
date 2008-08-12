import unittest
from zope.testing import doctest
# Not used yet, so avoid loading ztc or ptc.
#from Testing import ZopeTestCase as ztc
#from xm.tracker.tests import base


def test_suite():
    return unittest.TestSuite([

        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'tracker.txt', package='xm.tracker',
        #    test_class=base.TestCase),

        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='xm.tracker',
        #    test_class=base.TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

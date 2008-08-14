import unittest
from zope.testing import doctest
from Testing import ZopeTestCase as ztc
from xm.tracker.tests import base


def test_suite():
    return unittest.TestSuite([

        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'tracker.txt', package='xm.tracker',
        #    test_class=base.TestCase),

        ztc.FunctionalDocFileSuite(
            'browser.txt', package='xm.tracker.tests',
            optionflags=(doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE),
            test_class=base.FunctionalTestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

import unittest
from zope.testing import doctest
from zope.testing import doctestunit
from zope.component import testing


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        doctestunit.DocFileSuite(
            'tracker.txt', package='xm.tracker', optionflags=doctest.ELLIPSIS,
            setUp=testing.setUp, tearDown=testing.tearDown),
        doctestunit.DocFileSuite(
            'entry.py', package='xm.tracker.browser', optionflags=doctest.ELLIPSIS,
            setUp=testing.setUp, tearDown=testing.tearDown),
        doctestunit.DocTestSuite(
            module='xm.tracker.browser.tracker', optionflags=doctest.ELLIPSIS,
            setUp=testing.setUp, tearDown=testing.tearDown),

        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

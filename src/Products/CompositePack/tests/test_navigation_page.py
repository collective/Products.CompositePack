# -*- coding: utf-8 -*-

"""
$Id$
"""

import unittest2 as unittest

from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from Products.CMFPlone.utils import _createObjectByType

from Products.CompositePack.composite.navigationpage import NavigationPage
from Products.CompositePack.composite.navigationpage import INavigationPage
from Products.CompositePack.testing import INTEGRATION_TESTING


class NavigationPageTest(unittest.TestCase):
    """ensure content type implementation"""

    layer = INTEGRATION_TESTING

    def afterSetUp(self):
        self.ctype = 'Navigation Page'
        self.interface = INavigationPage
        self.klass = NavigationPage

        _createObjectByType(self.ctype, self.folder, 'obj')
        self.obj = getattr(self.folder, 'obj')

    def test_created(self):
        self.failUnless('obj' in self.folder.objectIds())

    def test_interface(self):
        self.assertTrue(self.interface.implementedBy(self.klass))
        self.assertTrue(verifyClass(self.interface, self.klass))

        obj = self.klass(None)
        self.assertTrue(self.interface.providedBy(obj))
        self.assertTrue(verifyObject(self.interface, obj))

    def test_edit(self):
        self.obj.setTitle(u'Title')
        self.assertEqual(self.obj.Title(), u'Title')

        self.obj.setDescription(u'Description')
        self.assertEqual(self.obj.Description(), u'Description')

    def test_schemata(self):
        schema = self.obj.Schema()
        field = schema.getField('description')
        self.assertEqual(field.schemata, 'default')

    def test_actions(self):
        self.assertTrue(hasattr(self.obj, 'cp_view'))
        self.assertTrue(hasattr(self.obj, 'design_view'))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

##############################################################################
#
# Copyright (c) 2004 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""
$Id: test_layoutregistry.py,v 1.9 2004/10/29 16:20:08 duncanb Exp $
"""

import os, sys

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

# Load fixture
from Testing import ZopeTestCase
from Products.Archetypes.tests import ArchetypesTestCase

## LinguaPlone addon?
try:
    from Products.LinguaPlone.public import registerType
except ImportError:
    HAS_LINGUA_PLONE = False
else:
    HAS_LINGUA_PLONE = True
    del registerType

# Install our product
if HAS_LINGUA_PLONE:
    ZopeTestCase.installProduct('PloneLanguageTool')
ZopeTestCase.installProduct('Archetypes')
ZopeTestCase.installProduct('ATContentTypes')
ZopeTestCase.installProduct('CompositePage')
ZopeTestCase.installProduct('kupu')
ZopeTestCase.installProduct('CompositePack')

from Acquisition import aq_base, aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName

from Products.CompositePack.config import TOOL_ID
from Products.CompositePack.tool import CompositeTool
from Products.CompositePack.exceptions import CompositePackError

TEST_TYPE = 'ATFile'
TEST_TYPE_2 = 'ATEvent'
TEST_TYPES = (TEST_TYPE, TEST_TYPE_2)

class LayoutRegistryTest(ArchetypesTestCase.ArcheSiteTestCase):

    def afterSetUp(self):
        super(ArchetypesTestCase.ArcheSiteTestCase, self).afterSetUp()
        self.loginPortalOwner()
        self.qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.qi.installProduct('Archetypes')
        self.qi.installProduct('ATContentTypes')
        self.qi.installProduct('kupu')
        self.qi.installProduct('CompositePack')
        if HAS_LINGUA_PLONE:
            self.qi.installProduct('PloneLanguageTool')
        self.composite_tool = getToolByName(self.portal, TOOL_ID)

    def beforeTearDown(self):
        self.composite_tool.clearLayoutRegistry()
        super(ArchetypesTestCase.ArcheSiteTestCase, self).beforeTearDown()

    def testRegisterType(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPE)
        self.failUnless(ct.isComposite(TEST_TYPE))
        self.failUnless(TEST_TYPE in ct.getRegisteredComposites())
    
    def testUnregisterType(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPE)
        ct.unregisterAsComposite(TEST_TYPE)
        self.failIf(ct.isComposite(TEST_TYPE))
        
    def testRegisterTypes(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPES)
        for test_type in TEST_TYPES:
            self.failUnless(ct.isComposite(test_type))
            self.failUnless(test_type in ct.getRegisteredComposites())
        
    def testUnregisterTypes(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPES)
        ct.unregisterAsComposite(TEST_TYPES)
        for test_type in TEST_TYPES:
            self.failIf(ct.isComposite(test_type))
        
    def testRegisterTwice(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPE)
        self.assertRaises(CompositePackError, ct.registerAsComposite, TEST_TYPE)

    def testRegisterLayout(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPE)
        layout = ct.registerLayout('test_layout', 'Test', 'test_layout')
        self.assertEquals(layout, ct.getLayoutById('test_layout'))

    def testUnregisterLayout(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPE)
        layout = ct.registerLayout('test_layout', 'Test', 'test_layout')
        ct.unregisterLayout('test_layout')
        self.assertEquals(None, ct.getLayoutById('test_layout'))
        layout = ct.registerLayout('test_layout', 'Test', 'test_layout')
        layout.registerForType(TEST_TYPE)
        ct.unregisterLayout('test_layout')
        self.failIf('test_layout' in [layout.getId() for layout in ct.getRegisteredLayoutsForType(TEST_TYPE)])

    def testUnregisterDefaultLayoutOfTool(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPE)
        layout = ct.registerLayout('test_layout', 'Test', 'test_layout')
        layout.registerForType(TEST_TYPE)
        ct.setDefaultLayout('test_layout')
        self.assertRaises(CompositePackError, ct.unregisterLayout, 'test_layout')

    def testRegisterLayoutForType(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPE)
        layout = ct.registerLayout('test_layout', 'Test', 'test_layout')
        layout.registerForType(TEST_TYPE)
        self.failUnless(layout in ct.getRegisteredLayoutsForType(TEST_TYPE))
        #it can be registered twice !
        layout.registerForType(TEST_TYPE)
        self.failUnless(layout.isRegisteredForType(TEST_TYPE))
        self.failIf(layout.isDefaultForType(TEST_TYPE))
        self.failUnless(layout in ct.getRegisteredLayoutsForType(TEST_TYPE))

    def testUnregisterLayoutForType(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPE)
        layout = ct.registerLayout('test_layout', 'Test', 'test_layout')
        layout.registerForType(TEST_TYPE)
        layout.unregisterForType(TEST_TYPE)
        self.failIf(layout.isRegisteredForType(TEST_TYPE))
        self.failIf(layout in ct.getRegisteredLayoutsForType(TEST_TYPE))

    def testRegisterDefaultLayoutForType(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPE)
        layout = ct.registerLayout('test_layout', 'Test', 'test_layout')
        layout.registerForType(TEST_TYPE)
        layout.setDefaultForType(TEST_TYPE)
        self.assertEquals(layout, ct.getDefaultLayoutForType(TEST_TYPE))
        self.failUnless(layout.isDefaultForType(TEST_TYPE))

    def testUnRegisterDefaultLayoutForType(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPE)
        layout = ct.registerLayout('test_layout', 'Test', 'test_layout')
        layout.registerForType(TEST_TYPE)
        layout.setDefaultForType(TEST_TYPE)
        self.assertRaises(CompositePackError, layout.unregisterForType, TEST_TYPE)

    def testClearDefaultLayout(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPE)
        layout = ct.registerLayout('test_layout', 'Test', 'test_layout')
        layout.registerForType(TEST_TYPE)
        layout.setDefaultForType(TEST_TYPE)
        layout.clearDefaultForType(TEST_TYPE)
        self.assertRaises(CompositePackError, ct.getDefaultLayoutForType, TEST_TYPE)
        self.failUnless(ct.noDefaultLayoutForType(TEST_TYPE))
    
    def testForceUnRegisterDefaultLayout(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPE)
        layout = ct.registerLayout('test_layout', 'Test', 'test_layout')
        layout.registerForType(TEST_TYPE)
        layout.setDefaultForType(TEST_TYPE)
        layout.unregisterForType(TEST_TYPE, force=True)
        self.assertRaises(CompositePackError, ct.getDefaultLayoutForType, TEST_TYPE)

    def testDefaultLayoutNotRegistered(self):
        ct = self.composite_tool
        ct.registerAsComposite(TEST_TYPE)
        self.assertRaises(CompositePackError, ct.getDefaultLayoutForType, TEST_TYPE)

    def testDefaultLayoutNotRegisteredUsesToolDefault(self):
        ct = self.composite_tool
        layout = ct.registerLayout('test_layout', 'Test', 'test_layout')
        ct.setDefaultLayout('test_layout')
        ct.registerAsComposite(TEST_TYPE)
        self.assertEquals(ct.getDefaultLayoutForType(TEST_TYPE),
                          layout)

    def testLayoutsForTypeNotRegisteredReturnAll(self):
        ct = self.composite_tool
        layouts = ct.layouts.objectValues()
        self.assertEquals(ct.getRegisteredLayoutsForType(TEST_TYPE), layouts)
        layout = ct.registerLayout('test_layout', 'Test', 'test_layout')
        ct.registerLayoutForType(layout, TEST_TYPE)
        self.assertEquals(ct.getRegisteredLayoutsForType(TEST_TYPE), [layout])

def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LayoutRegistryTest))
    return suite

if __name__ == '__main__':
    framework(descriptions=1, verbosity=1)

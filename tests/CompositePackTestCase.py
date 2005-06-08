##############################################################################
#
# Copyright (c) 2004 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""
$Id: CompositePackTestCase.py,v 1.2 2005/02/26 16:21:44 godchap Exp $
"""
# Load fixture
from Products.PloneTestCase import PloneTestCase

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
    PloneTestCase.installProduct('PloneLanguageTool')
PloneTestCase.installProduct('Archetypes')
PloneTestCase.installProduct('MimetypesRegistry')
PloneTestCase.installProduct('PortalTransforms')
PloneTestCase.installProduct('ATContentTypes')
PloneTestCase.installProduct('CompositePage')
PloneTestCase.installProduct('kupu')
PloneTestCase.installProduct('CompositePack')
PloneTestCase.setupPloneSite()

from cStringIO import StringIO
from cPickle import load, dump
from Acquisition import aq_base, aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName

class CompositePackTestCase(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        super(PloneTestCase.PloneTestCase, self).afterSetUp()
        self.qi = getToolByName(self.portal, 'portal_quickinstaller')
        if HAS_LINGUA_PLONE:
            self.qi.installProduct('PloneLanguageTool')
        self.qi.installProduct('ATContentTypes')
        self.qi.installProduct('kupu')
        self.qi.installProduct('CompositePack')
        self.composite_tool = getToolByName(self.portal, 'composite_tool')

    def beforeTearDown(self):
        self.composite_tool.clearLayoutRegistry()
        self.composite_tool.clearViewletRegistry()
        super(PloneTestCase.PloneTestCase, self).beforeTearDown()

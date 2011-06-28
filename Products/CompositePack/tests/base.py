##############################################################################
#
# Copyright (c) 2004-2006 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""
$Id$
"""
# Load fixture
from Products.PloneTestCase.ptc import PloneTestCase
from Products.CMFPlone.utils import getToolByName

from Products.CompositePack.config import get_ATCT_TYPES
from Products.CompositePack.config import PROJECTNAME
from Products.CompositePack.tests.layer import SimpleLayer

DEPENDENCIES = (
    'Archetypes',
    'MimetypesRegistry',
    'PortalTransforms',
    'ATContentTypes',
    'kupu',
    'GenericSetup',
    'CompositePack',
    'CompositePage',
)


class CompositePackTestCase(PloneTestCase):

    layer = SimpleLayer

    def afterSetUp(self):
        self.installCompositePack()
        self.composite_tool = getToolByName(self.portal, 'composite_tool')
        self.FILE_TYPE = get_ATCT_TYPES(self.portal)['File']
        self.EVENT_TYPE = get_ATCT_TYPES(self.portal)['Event']

    def installCompositePack(self):
        self.addProduct(PROJECTNAME)

    def beforeTearDown(self):
        self.composite_tool.clearLayoutRegistry()
        self.composite_tool.clearViewletRegistry()
        super(PloneTestCase, self).beforeTearDown()

class CompositeGSTestCase(CompositePackTestCase):

    def installCompositePack(self):
        self.loginAsPortalOwner()
        self.gs = self.portal.portal_setup
        self.gs.runAllImportStepsFromProfile('profile-Products.CompositePack:default')
        # Delete the GS logs to prevent conflicts.
        for obj_id in self.gs.objectIds():
            self.gs._delObject(obj_id)


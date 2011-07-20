# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2004-2011 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################

"""
$Id$
"""

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from Products.CMFCore.utils import getToolByName

from Products.CompositePack.testing import INTEGRATION_TESTING


class TestIndexes(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']

        self.composite_tool = getToolByName(self.portal, 'composite_tool')
        self.catalog = getToolByName(self.portal, 'portal_catalog')

    def test_no_container_indexed(self):
        #check catalog works ok
        before = len(self.catalog(portal_type='File'))
        self.folder.invokeFactory('File', 'test_file')
        self.assertEqual(before + 1, len(self.catalog(portal_type='File')))
        #check none of the software (viewlets, layouts,...) has been indexed
        self.failIf(len(self.catalog(portal_type="CompositePack Layout Container")))
        self.failIf(len(self.catalog(portal_type="CompositePack Viewlet Container")))

    def test_index_navigation_page(self):
        before = len(self.catalog())
        self.portal.invokeFactory('Navigation Page', 'page')
        page = self.portal._getOb('page')
        # 1 = page (no filled_slots or composite elements)
        self.assertEquals(len(self.catalog()), before + 1)

    def test_index_layout(self):
        before = len(self.catalog())
        ct = self.composite_tool
        layout = ct.registerLayout('test_layout', 'Test', 'test_layout')
        self.assertEquals(len(self.catalog()), before)

    def test_index_viewlet(self):
        before = len(self.catalog())
        ct = self.composite_tool
        layout = ct.registerViewlet('test_viewlet', 'Test', 'test_viewlet')
        self.assertEquals(len(self.catalog()), before)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

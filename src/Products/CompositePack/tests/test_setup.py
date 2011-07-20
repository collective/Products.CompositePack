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
$Id: test_setup.py 725 2011-06-21 02:44:41Z hvelarde $
"""

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from Products.CompositePack import config
from Products.CompositePack.testing import INTEGRATION_TESTING

TYPES = (
    'CompositePack Element',
    'CompositePack Fragments',
    'CompositePack Layout',
    'CompositePack Layout Container',
    'CompositePack Skin Method',
    'CompositePack Titles',
    'CompositePack Viewlet',
    'CompositePack Viewlet Container',
    'Navigation Page',
    'Pack Composite',
    )

FACTORY_TYPES = (
    'Navigation Page',
    )

SKINS = (
    'compositepack',
    'compositepack_design',
    'compositepack_layouts',
    #'compositepack_layouts_azax',
    'compositepack_viewlets',
    )

CSS = (
    'compo.css',
    'editstyles.css',
    'pdstyles.css',
    )

JS = (
    'pdlib.js',
    'plone_edit.js',
    'compopagedrawer.js',
    )


class TestInstall(unittest.TestCase):
    """ensure product is properly installed"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_dependencies_installed(self):
        portal_qi = self.portal.portal_quickinstaller
        for p in config.PRODUCT_DEPENDENCIES:
            self.failUnless(portal_qi.isProductInstalled(p),
                            '%s is not installed' % p)

    def test_types(self):
        portal_types = self.portal.portal_types
        for t in TYPES:
            self.failUnless(t in portal_types.objectIds(),
                            '%s content type not installed' % t)

    def test_portal_factory_enabled(self):
        portal_factory = self.portal.portal_factory
        for t in FACTORY_TYPES:
            self.failUnless(t in portal_factory.getFactoryTypes().keys(),
                            '%s content type not factory-enabled' % t)

    def test_default_page_types(self):
        properties = self.portal.portal_properties.site_properties
        self.failUnless('Navigation Page' in properties.getProperty('default_page_types'))

    def test_tool(self):
        self.failUnless(hasattr(self.portal, config.TOOL_ID),
                        'Tool not installed')

    def test_skins(self):
        portal_skins = self.portal.portal_skins
        for s in SKINS:
            self.failUnless(s in portal_skins.objectIds(),
                            '%s skin not installed' % s)

    def test_stylesheets(self):
        portal_css = self.portal.portal_css
        for css in CSS:
            self.failUnless(css in portal_css.getResourceIds(),
                            '%s stylesheet not installed' % css)

    def test_javascripts(self):
        portal_js = self.portal.portal_javascripts
        for js in JS:
            self.failUnless(js in portal_js.getResourceIds(),
                            '%s javascript not installed' % js)


class TestUninstall(unittest.TestCase):
    """ensure product is properly uninstalled"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal_qi = getattr(self.portal, 'portal_quickinstaller')
        self.portal_qi.uninstallProducts(products=[config.PROJECTNAME])

    def test_product_uninstalled(self):
        self.failIf(self.portal_qi.isProductInstalled(config.PROJECTNAME))

    def test_tool_uninstalled(self):
        self.failIf(hasattr(self.portal, config.TOOL_ID),
                    'Tool not uninstalled')

    def test_types(self):
        portal_types = self.portal.portal_types
        for t in TYPES:
            self.failIf(t in portal_types.objectIds(),
                        '%s content type not uninstalled' % t)

    def test_skins(self):
        portal_skins = self.portal.portal_skins
        for s in SKINS:
            self.failIf(s in portal_skins.objectIds(),
                        '%s skin not uninstalled' % s)

    def test_stylesheets(self):
        portal_css = self.portal.portal_css
        for css in CSS:
            self.failIf(css in portal_css.getResourceIds(),
                        '%s stylesheet not uninstalled' % css)

    def test_javascripts(self):
        portal_js = self.portal.portal_javascripts
        for js in JS:
            self.failIf(js in portal_js.getResourceIds(),
                        '%s javascript not uninstalled' % js)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

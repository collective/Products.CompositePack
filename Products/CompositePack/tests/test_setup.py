# -*- coding: utf-8 -*-

"""
$Id: test_setup.py 725 2011-06-21 02:44:41Z hvelarde $
"""

import unittest

from Products.PloneTestCase.ptc import PloneTestCase

from Products.CompositePack.config import PROJECTNAME, TOOL_ID
from Products.CompositePack.config import PRODUCT_DEPENDENCIES
from Products.CompositePack.tests.layer import CompositePackLayer
from Products.CompositePack.tests.layer import SimpleLayer

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


class TestInstall(PloneTestCase):
    """ensure product is properly installed"""

    layer = SimpleLayer

    def afterSetUp(self):
        #self.addProduct('CompositePack')
        self.addProfile('Products.CompositePack:default')
        portal_quickinstaller = self.portal.portal_quickinstaller
        self.failUnless(portal_quickinstaller.isProductInstalled(PROJECTNAME),
                            '%s not installed' % PROJECTNAME)

    def test_dependencies_installed(self):
        portal_quickinstaller = self.portal.portal_quickinstaller
        for p in PRODUCT_DEPENDENCIES:
            self.failUnless(portal_quickinstaller.isProductInstalled(p),
                            '%s not installed' % p)

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

    def test_tool(self):
        self.failUnless(hasattr(self.portal, TOOL_ID), 'Tool not installed')

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


class TestUninstall(PloneTestCase):
    """ensure product is properly uninstalled"""

    layer = CompositePackLayer

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_product_uninstalled(self):
        self.failIf(self.qi.isProductInstalled(PROJECTNAME))

    def test_tool_uninstalled(self):
        self.failIf(hasattr(self.portal, TOOL_ID), 'Tool not uninstalled')

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

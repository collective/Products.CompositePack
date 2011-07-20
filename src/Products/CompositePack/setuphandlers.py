# -*- coding: utf-8 -*-

"""
$Id$
"""

from cStringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.CompositePack import config


def install_dependencies(site, out):
    """Install required products
    """
    qi = getToolByName(site, 'portal_quickinstaller')
    for product in config.PRODUCT_DEPENDENCIES:
        if not qi.isProductInstalled(product):
            if qi.isProductInstallable(product):
                qi.installProduct(product)
            else:
                raise "Product %s not installable" % product


def setup_portal_factory(site, out):
    factory = getToolByName(site, 'portal_factory')
    types = factory.getFactoryTypes().keys()
    if 'Navigation Page' not in types:
        out.write('Navigation Page setup in portal_factory\n')
        types.append('Navigation Page')
        factory.manage_setPortalFactoryTypes(listOfTypeIds=types)
    if 'Navigation Titles' not in types:
        out.write('Navigation Titles setup in portal_factory\n')
        types.append('Navigation Titles')
        factory.manage_setPortalFactoryTypes(listOfTypeIds=types)
    if 'Navigation Page HTML' not in types:
        out.write('Navigation Page HTML setup in portal_factory\n')
        types.append('Navigation Page HTML')
        factory.manage_setPortalFactoryTypes(listOfTypeIds=types)


def importVarious(context):
    """Miscellanous steps import handle
    """
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('Products.CompositePack_various.txt') is None:
        return

    out = StringIO()
    site = context.getSite()

    install_dependencies(site, out)
    setup_portal_factory(site, out)

    return out.getvalue()

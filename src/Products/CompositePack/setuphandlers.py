# -*- coding: utf-8 -*-

"""
$Id$
"""

from Products.CMFCore.utils import getToolByName
from Products.CompositePack import config


def install_dependencies(site):
    """Install required products
    """
    qi = getToolByName(site, 'portal_quickinstaller')
    for product in config.PRODUCT_DEPENDENCIES:
        if not qi.isProductInstalled(product):
            if qi.isProductInstallable(product):
                qi.installProduct(product)
            else:
                raise "Product %s not installable" % product


def importVarious(context):
    """Miscellanous steps import handle
    """
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('Products.CompositePack_various.txt') is None:
        return

    site = context.getSite()

    install_dependencies(site)

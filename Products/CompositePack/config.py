# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2004-2006 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""Product configuration : constants

$Id$
"""
import os
import Globals
import warnings

HAS_ATCT = True
PLONE21 = True
PLONE25 = True

try:
    from Products import azax
    from Products import Five
except ImportError:
    #warnings.warn('CompositePack performance impaired: Five and Azax recommended', DeprecationWarning)
    HAVEAZAX = False
else:
    HAVEAZAX = True

from Products.CMFCore.utils import getToolByName

if HAS_ATCT and not PLONE21:
    try:
        from Products.ATContentTypes.ATNewsItem import ATNewsItem
    except ImportError:
        from Products.ATContentTypes.types.ATNewsItem import ATNewsItem

    def isSwitchedToATCT(portal):
        pt = getToolByName(portal, 'portal_types')
        news = pt.getTypeInfo('News Item')
        if news.Metatype() == ATNewsItem.meta_type:
            return 1
        else:
            return 0

try:
    from Products.GenericSetup import tool
except ImportError:
    HAS_GS = False
else:
    HAS_GS = True
    del tool


def get_ATCT_TYPES(self):
    result = {}
    if PLONE21 or (HAS_ATCT and isSwitchedToATCT(self)):
        result["Document"] = "Document"
        result["Image"] = "Image"
        result["File"] = "File"
        result["Event"] = "Event"
        result["NewsItem"] = "News Item"
        result["Topic"] = "Topic"
        result["Link"] = "Link"
    elif HAS_ATCT and not isSwitchedToATCT(self):
        result["Document"] = "ATDocument"
        result["Image"] = "ATImage"
        result["File"] = "ATFile"
        result["Event"] = "ATEvent"
        result["NewsItem"] = "ATNewsItem"
        result["Topic"] = "ATTopic"
        result["Link"] = "ATLink"
    return result


def get_COMPOSABLES_ATCT(self):
    result = get_ATCT_TYPES(self)
    return result.values()

PROJECTNAME = 'CompositePack'
ADD_CONTENT_PERMISSION = 'Add CompositePack content'
GLOBALS = globals()

# listing of Archetypes, ATContentTypes as dependencies is no longer needed
PRODUCT_DEPENDENCIES = ('kupu', )

TOOL_ID = 'composite_tool'
TOOL_NAME = 'CompositePack Tool'
TOOL_ICON = 'composite.gif'

COMPOSABLE = 'composable'

VIEWLETS = 'viewlets'
LAYOUTS = 'layouts'


INSTALL_DEMO_TYPES = 0  # Install the demo types

zmi_dir = os.path.join(Globals.package_home(globals()), 'www')

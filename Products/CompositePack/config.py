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

import warnings

from App.Common import package_home

HAS_ATCT = True

try:
    from Products import azax
    from Products import Five
except ImportError:
    #warnings.warn('CompositePack performance impaired: Five and Azax recommended', DeprecationWarning)
    HAVEAZAX = False
else:
    HAVEAZAX = True

from Products.CMFCore.utils import getToolByName


def get_ATCT_TYPES(self):
    result = {}
    if HAS_ATCT:
        result["Document"] = "Document"
        result["Image"] = "Image"
        result["File"] = "File"
        result["Event"] = "Event"
        result["NewsItem"] = "News Item"
        result["Topic"] = "Topic"
        result["Link"] = "Link"
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

zmi_dir = os.path.join(package_home(globals()), 'www')

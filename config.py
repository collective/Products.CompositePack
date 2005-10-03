##############################################################################
#
# Copyright (c) 2004 CompositePack Contributors. All rights reserved.
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

try:
    from Products import ATContentTypes
    HAS_ATCT = True
except ImportError:
    HAS_ATCT = False
    
try:
    from Products.CMFPlone.migrations.v2_1 import rcs
except ImportError:
    PLONE21 = False
else:
    PLONE21 = True

if HAS_ATCT and not PLONE21:
    from Products.ATContentTypes.Extensions.toolbox import isSwitchedToATCT

def get_ATCT_TYPES(self):
    result = {}
    if PLONE21:
        result["Document"] = "Document"
        result["Image"] = "Image"
        result["File"] = "File"
        result["Event"] = "Event"
        result["NewsItem"] = "News Item"
        result["Topic"] = "Topic"
        result["Link"] = "Link"
        result["Favorite"] = "Favorite"
    elif HAS_ATCT and not isSwitchedToATCT(self):
        result["Document"] = "ATDocument"
        result["Image"] = "ATImage"
        result["File"] = "ATFile"
        result["Event"] = "ATEvent"
        result["NewsItem"] = "ATNewsItem"
        result["Topic"] = "ATTopic"
        result["Link"] = "ATLink"
        result["Favorite"] = "ATFavorite"
    return result

def get_COMPOSABLES_ATCT(self):
    result = get_ATCT_TYPES(self)
    del result["Favorite"]
    return result.values()

PROJECTNAME = 'CompositePack'
ADD_CONTENT_PERMISSION = 'Add CompositePack content'
GLOBALS = globals()

TOOL_ID = 'composite_tool'
TOOL_NAME = 'CompositePack Tool'
TOOL_ICON = 'composite.gif'

COMPOSABLE = 'composable'

VIEWLETS = 'viewlets'
LAYOUTS = 'layouts'

INSTALL_DEMO_TYPES = 0 ##Install the demo types

zmi_dir = os.path.join(Globals.package_home(globals()),'www')


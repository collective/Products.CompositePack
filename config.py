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

print "\n\n\n\n"
try:
    from Products import ATContentTypes
    HAS_ATCT = True
except ImportError:
    HAS_ATCT = False
if HAS_ATCT:
    print "with ATCT"
    
try:
    from Products.CMFPlone.migrations.v2_1 import rcs
except ImportError:
    PLONE21 = False
else:
    PLONE21 = True
if PLONE21:
    print "Plone 2.1"

if HAS_ATCT and not PLONE21:
    from Products.ATContentTypes.Extensions.toolbox import isSwitchedToATCT

print "\n\n\n\n"

if PLONE21:
    DOCUMENT_TYPE = "Document"
    IMAGE_TYPE = "Image"
    FILE_TYPE = "File"
    EVENT_TYPE = "Event"
    NEWS_TYPE = "News Item"
    TOPIC_TYPE = "Topic"
    LINK_TYPE = "Link"
    FAVORITE_TYPE = "Favorite"
elif HAS_ATCT:
    if isSwitchedToATCT():
        DOCUMENT_TYPE = "Document"
        IMAGE_TYPE = "Image"
        FILE_TYPE = "File"
        EVENT_TYPE = "Event"
        NEWS_TYPE = "News Item"
        TOPIC_TYPE = "Topic"
        LINK_TYPE = "Link"
        FAVORITE_TYPE = "Favorite"
    else:    
        DOCUMENT_TYPE = "ATDocument"
        IMAGE_TYPE = "ATImage"
        FILE_TYPE = "ATFile"
        EVENT_TYPE = "ATEvent"
        NEWS_TYPE = "ATNewsItem"
        TOPIC_TYPE = "ATTopic"
        LINK_TYPE = "ATLink"
        FAVORITE_TYPE = "ATFavorite"

ATCT_TYPES = [DOCUMENT_TYPE, LINK_TYPE, EVENT_TYPE, TOPIC_TYPE, 
              IMAGE_TYPE, FILE_TYPE, NEWS_TYPE]

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


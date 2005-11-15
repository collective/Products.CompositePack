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
import warnings

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

try:
    from Products import azax 
    from Products import Five
except ImportError:
    warnings.warn('CompositePack performance impaired: Five and Azax recommended', DeprecationWarning)
    HAVEAZAX = False
else:
    HAVEAZAX = True

PROJECTNAME = 'CompositePack'
ADD_CONTENT_PERMISSION = 'Add CompositePack content'
GLOBALS = globals()

TOOL_ID = 'composite_tool'
TOOL_NAME = 'CompositePack Tool'
TOOL_ICON = 'composite.gif'

ATCT_TYPES = ['ATDocument', 'ATNewsItem', 'ATEvent', 'ATFile', 'ATImage',
              'ATTopic', 'ATLink']
MIGRATED_ATCT_TYPES = ['Document', 'News Item', 'Event', 'File', 'Image',
                       'Topic', 'Link']
COMPOSABLE = 'composable'

VIEWLETS = 'viewlets'
LAYOUTS = 'layouts'

INSTALL_DEMO_TYPES = 0 ##Install the demo types

zmi_dir = os.path.join(Globals.package_home(globals()),'www')


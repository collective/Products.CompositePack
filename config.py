##############################################################################
#
# Copyright (c) 2004 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""Product configuration : constants

$Id: config.py,v 1.14 2005/02/26 16:21:43 godchap Exp $
"""
import os
import Globals

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

INSTALL_DEMO_TYPES = 1 ##Install the demo types

zmi_dir = os.path.join(Globals.package_home(globals()),'www')


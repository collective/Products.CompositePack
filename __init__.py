##############################################################################
#
# Copyright (c) 2004 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""Product initialization module.

$Id: __init__.py,v 1.9.2.1 2004/12/21 11:00:14 godchap Exp $
"""

# Kickstart Install to make sure it works
from Products.CompositePack.Extensions import Install
del Install

from Products.Archetypes.public import *
from Products.Archetypes import listTypes
from Products.CompositePack.config import *
from Products.CompositePack import design
from Products.CMFCore import utils as cmf_utils
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CompositePage import tool as base_tool

registerDirectory('skins', GLOBALS)
base_tool.registerUI('plone', design.PloneUI())

def initialize(context):

    from Products.CompositePack import tool, viewlet
    from Products.CompositePack.composite import archetype
    from Products.CompositePack.viewlet import container
    from Products.CompositePack.composite import navigationpage
    from Products.CompositePack.composite import titles

    if INSTALL_DEMO_TYPES:
        from Products.CompositePack.demo import ATComposableDocument

    # register archetypes content with the machinery
    content_types, constructors, ftis = process_types(listTypes(PROJECTNAME),
                                                      PROJECTNAME)

    tools = (tool.CompositeTool,)

    cmf_utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types = content_types,
        permission = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti = ftis).initialize(context)

    registerClasses(context, PROJECTNAME, ['CompositePack Element',
                                           'CompositePack Portal Element',
                                           'CompositePack Viewlet',
                                           'CompositePack Layout',
                                           'CompositePack Titles',
                                           'CompositePack Viewlet Container',
                                           'CompositePack Layout Container'])

    context.registerClass(
        tool.CompositeTool,
        meta_type=TOOL_NAME,
        constructors=(tool.manage_addCompositeTool,),
        icon = TOOL_ICON)

    cmf_utils.ToolInit(TOOL_NAME,
                       tools = tools,
                       product_name = PROJECTNAME,
                       icon=TOOL_ICON
                   ).initialize(context)

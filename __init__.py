##############################################################################
#
# Copyright (c) 2004-2006 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""Product initialization module.

$Id$
"""

# Kickstart Install to make sure it works
from Products.CompositePack.Extensions import Install
del Install

from Products.CMFCore import utils as cmf_utils
from Products.CMFCore.DirectoryView import registerDirectory

from Products.CMFPlone import MigrationTool
import Products.CMFPlone.interfaces

from Products.Archetypes.public import *
from Products.Archetypes import listTypes

from Products.CompositePage import tool as base_tool

from Products.CompositePack.config import *
from Products.CompositePack import design, patch
from Products.CompositePack.ConfigurationMethods import GeneralSetup

if PLONE25:
    from Products.GenericSetup import EXTENSION
    from Products.GenericSetup import profile_registry

registerDirectory('skins', GLOBALS)
try:
    del base_tool._uis['plone'] # So we can refresh the product :(
except KeyError:
    pass

base_tool.registerUI('plone', design.PloneUI())

def initialize(context):
    from Products.CompositePack import tool, viewlet
    from Products.CompositePack.composite import archetype
    from Products.CompositePack.viewlet import container
    from Products.CompositePack.composite import navigationpage
    from Products.CompositePack.composite import titles
    from Products.CompositePack.composite import fragments

    if INSTALL_DEMO_TYPES:
        from Products.CompositePack.demo import ATCompositeDocument

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
                                           'CompositePack Viewlet',
                                           'CompositePack Layout',
                                           'CompositePack Titles',
                                           'CompositePack Fragments',
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

    if PLONE25:
        profile_registry.registerProfile(
            name='default',
            title='Composite Site',
            description='Profile for Composite Pack',
            path='profiles/default',
            product='CompositePack',
            profile_type=EXTENSION,
            for_=Products.CMFPlone.interfaces.IPloneSiteRoot)

    MigrationTool.registerSetupWidget(GeneralSetup)

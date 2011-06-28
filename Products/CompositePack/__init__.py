# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2004-2006 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################

"""
$Id$
"""

from Products.Archetypes.atapi import listTypes
from Products.Archetypes.atapi import process_types
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory

from Products.CompositePage import tool as base_tool

from Products.CompositePack import config
from Products.CompositePack import design
from Products.CompositePack import tool

tools = (tool.CompositeTool, )

registerDirectory('skins', config.GLOBALS)
base_tool.registerUI('plone', design.PloneUI())


def initialize(context):

    from Products.CompositePack import viewlet
    from Products.CompositePack.composite import archetype
    from Products.CompositePack.composite import fragments
    from Products.CompositePack.composite import navigationpage
    from Products.CompositePack.composite import portlets
    from Products.CompositePack.composite import titles
    from Products.CompositePack.viewlet import container

    if config.INSTALL_DEMO_TYPES:
        from Products.CompositePack.demo import ATCompositeDocument

    content_types, constructors, ftis = process_types(
            listTypes(config.PROJECTNAME),
            config.PROJECTNAME)

    utils.ContentInit(
            "%s Content" % config.PROJECTNAME,
            content_types=content_types,
            permission=config.ADD_CONTENT_PERMISSION,
            extra_constructors=constructors,
            fti=ftis,
            ).initialize(context)

    utils.ToolInit(config.TOOL_NAME,
            tools=tools,
            icon=config.TOOL_ICON,
            ).initialize(context)

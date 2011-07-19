# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2004-2011 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""Composable Document:

$Id$
"""

from Products.CompositePack.config import PROJECTNAME
from Products.CompositePack.public import registerType

from Products.ATContentTypes.types.ATDocument import ATDocument


class ATCompositeDocument(ATDocument):
    """A basic, Archetypes-based Composite Page
    """
    meta_type = portal_type = 'Composite Document'
    archetype_name = 'Composite Document'

    right_slots = ['here/document_sidebar_view/macros/empty']

registerType(ATCompositeDocument, PROJECTNAME)

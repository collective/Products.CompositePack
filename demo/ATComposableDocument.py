##############################################################################
#
# Copyright (c) 2004 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""Composable Document:

$Id: ATComposableDocument.py,v 1.3 2004/09/28 14:46:01 godchap Exp $
"""

from Products.Archetypes.public import BaseSchema
from Products.ATContentTypes.types.ATDocument import ATDocument

from Products.CompositePack.config import PROJECTNAME
from Products.CompositePack.public import registerType

class ATComposableDocument(ATDocument):
    """A basic, Archetypes-based Composite Page
    """
    meta_type = portal_type = 'Composable Document'
    archetype_name = 'Composable Document'

registerType(ATComposableDocument, PROJECTNAME)

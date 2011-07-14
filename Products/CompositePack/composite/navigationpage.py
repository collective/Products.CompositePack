# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2004-2006 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################

"""Navigation Page :

$Id$
"""

from Acquisition import aq_base
from AccessControl import ClassSecurityInfo
from zope.interface import Interface
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.CompositePack.config import PROJECTNAME
from Products.CompositePack.composite import packcomposite

from Products.CMFPlone.interfaces.structure import INonStructuralFolder


class INavigationPage(Interface):
    """ Marker interface
    """

    def SearchableText():
        """Return text for indexing"""

schema = atapi.BaseSchema.copy()

schema['title'].storage = atapi.AnnotationStorage()
schema['description'].storage = atapi.AnnotationStorage()

#finalizeATCTSchema(schema, folderish=True, moveDiscussion=False)


class NavigationPage(atapi.BaseFolder):
    """A page composed of content selected manually."""
    # Add INonStructuralFolder to tell Plone that even though
    # this type is technically a folder, it should be treated as a standard
    # content type. This ensures the user doesn't perceive a Navigation Page
    # as a folder.
    implements((INavigationPage, INonStructuralFolder))

    security = ClassSecurityInfo()
    portal_type = 'Navigation Page'
    schema = schema

    _at_rename_after_creation = True

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # What's this for?
    actions = packcomposite.actions

    def SearchableText(self):
        """Return text for indexing"""
        # Want title, description, and all Title and fragment content.
        # Fragments are converted from HTML to plain text.
        texts = [self.Title(), self.Description()]

        # FIXME: cp_container is not a valid attribute at this time
        #if getattr(aq_base(self.cp_container), 'titles', None) is not None:
        #    titles = self.cp_container.titles.objectValues()
        #    for o in titles:
        #        if hasattr(o, 'ContainerSearchableText'):
        #            texts.append(o.ContainerSearchableText())

        return " ".join(texts)

atapi.registerType(NavigationPage, PROJECTNAME)

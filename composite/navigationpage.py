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
from Products.Archetypes.public import BaseSchema

from Products.CompositePack.config import PROJECTNAME
from Products.CompositePack.composite import packcomposite
from Products.CompositePack.public import BaseContent, registerType

class NavigationPage(BaseContent):
    """A page composed of content selected manually."""
    meta_type = portal_type = 'Navigation Page'
    archetype_name = 'Navigation Page'
    security = ClassSecurityInfo()
    
    typeDescription= 'A page composed of content selected manually.'
    typeDescMsgId  = 'description_edit_navigation_page'
    
    _at_rename_after_creation = True
    
    schema = BaseSchema.copy()
    # Move the description field into the edit view.
    schema['description'].isMetadata = False
    schema['description'].schemata = 'default'
    actions = packcomposite.actions
    
    factory_type_information={
            'content_icon':'composite.gif',
            }

    def SearchableText(self):
        """Return text for indexing"""
        # Want title, description, and all Title and fragment content.
        # Fragments are converted from HTML to plain text.
        texts = [self.Title(), self.Description()]
        if getattr(aq_base(self.cp_container), 'titles', None) is not None:
            titles = self.cp_container.titles.objectValues()
            for o in titles:
        	      if hasattr(o, 'ContainerSearchableText'):
        		    texts.append(o.ContainerSearchableText())

        return " ".join(texts)

    security.declareProtected('View', 'modified')
    def modified(self):
        """Last modified date for the nav page is last modified date for the catalog """
        pc = self.portal_catalog
        top = pc.searchResults(sort_on='modified', sort_order='reverse', sort_limit=1)
        if len(top):
            return top[0].modified
        return BaseContent.modified(self)

registerType(NavigationPage, PROJECTNAME)

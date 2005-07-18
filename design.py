##############################################################################
#
# Copyright (c) 2004 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""Plone UI for Composite Page design view.

$Id$
"""
import os
import re
import Globals
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base, aq_inner, aq_parent
from Products.CompositePage.designuis import CommonUI
from Products.CompositePage.rawfile import RawFile
from Products.CMFCore.FSDTMLMethod import FSDTMLMethod
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

_plone = os.path.join(os.path.dirname(__file__), 'plone')


start_of_contentmenu_search = re.compile("(<li[^>]*(>[^>]*){0,2}action(Plural|Singular|Menu)[^>]*)", re.IGNORECASE).search

class PloneUI(CommonUI):
    """Page design UI meant to fit Plone.

    Adds Plone-specific scripts and styles to a page.
    """
    security = ClassSecurityInfo()

    workspace_view_name = 'view'

    security.declarePublic('plone_edit_js')
    plone_edit_js = RawFile('plone_edit.js', 'text/javascript', _plone)
    pdlib_js = RawFile('pdlib.js', 'text/javascript', _plone)
    target_image = RawFile('target_image.gif', 'image/gif', _plone)
    target_image_hover = RawFile('target_image.gif', 'image/gif', _plone)
    target_image_active = RawFile('target_image.gif', 'image/gif', _plone)

    editstyles_css = FSDTMLMethod("editstyles.css", os.path.join(_plone,
        "editstyles.css"))
    pdstyles_css = FSDTMLMethod("pdstyles.css", os.path.join(_plone,
        "pdstyles.css"))

    header_templates = CommonUI.header_templates + (
        PageTemplateFile('header.pt', _plone),)
    top_templates = CommonUI.top_templates + (
        PageTemplateFile('top.pt', _plone),)
    bottom_templates = (PageTemplateFile('bottom.pt', _plone),)
    contentmenu_templates = (PageTemplateFile('contentmenu.pt', _plone),)

    security.declarePublic("getFragments")
    def getFragments(self, composite):
        """Returns the fragments to be inserted in design mode.
        """
        params = {
            "tool": aq_parent(aq_inner(aq_parent(aq_inner(self)))),
            "ui": self,
            "composite": composite,
            }
        contentmenu = ""
        for t in self.contentmenu_templates:
            contentmenu += str(t.__of__(self)(**params))
        result = CommonUI.getFragments(self, composite)
        result["contentmenu"] = contentmenu
        return result

    security.declarePrivate("render")
    def render(self, composite):
        """Renders a composite, adding scripts and styles.
        """
        text = CommonUI.render(self, composite)
        fragments = self.getFragments(composite)
        if fragments['contentmenu']:
            match = start_of_contentmenu_search(text)
            index = match and match.start(0) or -1
            text = "%s%s%s" % (text[:index], fragments['contentmenu'], text[index:])
        return text

Globals.InitializeClass(PloneUI)

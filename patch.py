##############################################################################
#
# Copyright (c) 2004-2006 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""
$Id: exceptions.py 11303 2005-08-23 16:38:33Z godchap $
"""
# Patch CompositePage so that error messages have an appropriate
# class. This lets us suppress the display for anonymous users.
import Products.CompositePage.slot

error_tag = '''<span class="slot_error">%s
(<a href="%s" onmousedown="document.location=this.href">log</a>)</span>'''
Products.CompositePage.slot.error_tag = error_tag

# Patch CompositePage to add an attribute to the request which we can exclude
# from caching in CacheFu, using the 'composite_design' attr instead of the
# _v_editing that will provide us with cached values.

from Products.CompositePage.composite import CompositeMixin

def design(self, ui=None):
    """Renders the composite with editing features.
    """
    # Never cache a design view.
    req = getattr(self, "REQUEST", None)
    if req is not None:
        req["composite_design"] = True
        req["RESPONSE"].setHeader("Cache-Control", "no-cache")
    ui_obj = self.getUI(ui)
    self._v_editing = 1
    try:
        return ui_obj.render(self)
    finally:
        self._v_editing = 0
        
CompositeMixin.design = design

# Inside a slot we can now check for the attribute in the request to decide
# whether we are in design mode or not.

from cgi import escape
from ZODB.POSException import ConflictError
from Acquisition import aq_inner, aq_parent
from Products.CompositePage.slot import Slot
from Products.CompositePage.slot import target_tag
from Products.CompositePage.slot import edit_tag
from Products.CompositePage.slot import view_tag
from Products.CompositePage.slot import formatException

from Products.CompositePage.interfaces import ICompositeElement

def renderToList(self, allow_add):
    """Renders the items to a list.
    """
    res = ['<div class="slot_header"></div>']
    composite = aq_parent(aq_inner(aq_parent(aq_inner(self))))

    items = self.objectItems()
    editing = self.REQUEST.has_key('composite_design')
    if editing:
        mypath = escape('/'.join(self.getPhysicalPath()))
        myid = self.getId()
        if hasattr(self, 'portal_url'):
            icon_base_url = self.portal_url()
        elif hasattr(self, 'REQUEST'):
            icon_base_url = self.REQUEST['BASEPATH1']
        else:
            icon_base_url = '/'
    for index in range(len(items)):
        name, obj = items[index]

        if editing and allow_add:
            res.append(target_tag % (myid, index, mypath, index))

        try:
            assert ICompositeElement.isImplementedBy(obj), (
                "Not a composite element: %s" % repr(obj))
            text = obj.renderInline()
        except ConflictError:
            # Ugly ZODB requirement: don't catch ConflictErrors
            raise
        except:
            text = formatException(self, editing)


        if editing:
            res.append(self._render_editing(obj, text, icon_base_url))
        else:
            res.append(view_tag % text)

    if editing and allow_add:
        index = len(items)
        res.append(target_tag % (myid, index, mypath, index))

    return res

Slot.renderToList = renderToList

##############################################################################
#
# Copyright (c) 2004 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""CMF/Plone install

$Id: Install.py,v 1.14.2.1 2004/12/21 11:00:16 godchap Exp $
"""

from cStringIO import StringIO
from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CompositePack.config import PROJECTNAME, GLOBALS, TOOL_ID
from Products.CompositePack.config import COMPOSABLE, COMPOSABLE_TYPES
from Products.CompositePack.config import INSTALL_DEMO_TYPES
from Products.CMFCore.utils import getToolByName
from Products.kupu.plone.plonelibrarytool import PloneKupuLibraryTool

KUPU_TOOL_ID = PloneKupuLibraryTool.id

COMPO_TYPE = 'CMF Composite Page'

class toolWrapper:
    def __init__(self, tool):
        self.tool = tool
        
    def registerAsComposite(self, items):
        if type(items) not in (tuple, list):
            items = (items,)

        items = [ item for item in items if not self.tool.isComposite(item) ]
        if items:
            self.tool.registerAsComposite(items)

    def registerAsComposable(self, items):
        if type(items) not in (tuple, list):
            items = (items,)

        items = [ item for item in items if not self.tool.isComposable(item) ]
        if items:
            self.tool.registerAsComposable(items)

    def registerLayout(self, id, description, skin_method):
        layout = self.tool.getLayoutById(id)
        if layout:
            return layout
        return self.tool.registerLayout(id, description, skin_method)

    def registerViewlet(self, id, description, skin_method):
        viewlet = self.tool.getViewletById(id)
        if viewlet:
            return viewlet
        return self.tool.registerViewlet(id, description, skin_method)

    def setViewletsForType(self, type, viewlet_ids, default_viewlet):
        self.tool.setViewletsForType(type, viewlet_ids, default_viewlet)

def install_tool(self, out):
    if not hasattr(self, TOOL_ID):
        self.manage_addProduct['CompositePack'].manage_addCompositeTool()
    tool = toolWrapper(getattr(self, TOOL_ID))

    if INSTALL_DEMO_TYPES:
        tool.registerAsComposite('Composable Document')
    tool.registerAsComposite('Navigation Page')

    tool.registerAsComposable(COMPOSABLE_TYPES)
    tool.registerAsComposable('CompositePack Titles')
    
    ts = tool.registerLayout('two_slots', 'Two slots', 'two_slots')
    try:
        ts.registerForType('Navigation Page')
    except AttributeError:
        raise RuntimeError, "ts=%r" % ts
    ts.setDefaultForType('Navigation Page')

    ts = tool.registerLayout('three_slots', 'Three slots', 'three_slots')
    ts.registerForType('Navigation Page')

    if INSTALL_DEMO_TYPES:
        ds = tool.registerLayout('document_sidebar_view',
                            'Document with sidebar',
                            'document_sidebar_view')
        ds.registerForType('Composable Document')
        ds.setDefaultForType('Composable Document')

    dv = tool.registerViewlet('default_viewlet',
                         'Basic viewlet (getId)',
                         'default_viewlet')
    tool.tool.registerViewletForDefaultSetup(dv)
    tool.tool.setDefaultViewletForDefaultSetup(dv)
    tool.registerViewlet('recent_items',
                         'Recent Items',
                         'recent_items')
    tool.registerViewlet('link_viewlet',
                         'Link Only',
                         'link_viewlet')
    tool.registerViewlet('title_viewlet',
                         'Title',
                         'title_viewlet')
    tool.registerViewlet('title_date_viewlet',
                         'Title and Date',
                         'title_date_viewlet')
    tool.registerViewlet('image_viewlet',
                         'Image',
                         'image_viewlet')
    tool.registerViewlet('image_title_viewlet',
                         'Image with title',
                         'image_title_viewlet')
    tool.registerViewlet('image_caption_viewlet',
                         'Image with caption',
                         'image_caption_viewlet')
    tool.setViewletsForType('Plone Site', ['recent_items'],
                            'recent_items')
    tool.setViewletsForType('CompositePack Titles', ['title_viewlet'],
                            'title_viewlet')
    tool.setViewletsForType('ATImage', ['image_viewlet',
                                        'link_viewlet',
                                        'image_title_viewlet',
                                        'image_caption_viewlet'],
                            'image_viewlet')
    out.write("CompositePack Tool Installed\n")

def uninstall_tool(self, out):
    if hasattr(self, TOOL_ID):
        out.write("CompositePack Tool not removed\n")

def uninstall_kupu_resource(self, out):
    if hasattr(self, KUPU_TOOL_ID):
        kupu_tool = getattr(self, KUPU_TOOL_ID)
        try:
            kupu_tool.deleteResourceTypes([COMPOSABLE])
            out.write("Composable Resource deleted in Kupu Library Tool\n")
        except KeyError:
            pass
    else:
        out.write("Kupu Library Tool not available\n")

def install_customisation(self, out):
    """Default settings may be stored in a customisation policy script so
    that the entire setup may be 'productised'"""

    # Skins are cached during the request so we (in case new skin
    # folders have just been added) we need to force a refresh of the
    # skin.
    self.changeSkin(None)

    scriptname = '%s-customisation-policy' % PROJECTNAME.lower()
    cpscript = getattr(self, scriptname, None)
    if cpscript:
        cpscript = cpscript.__of__(self)

    if cpscript:
        print >>out,"Customising %s" % PROJECTNAME
        print >>out,cpscript()
    else:
        print >>out,"No customisation policy", scriptname

def install_fixuids(self, out):
    # If upgrading from version 0.1.0 the uids may need migrating
    ct = getattr(self, TOOL_ID)
    for id, viewlet in ct.viewlets.objectItems():
        uid = viewlet.UID()
        viewlet.setStableUID()
        if uid != viewlet.UID():
            out.write("Migrated UID for viewlet %s\n" % id)

def install(self):
    out = StringIO()

    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    install_subskin(self, out, GLOBALS)
    install_tool(self, out)
    install_customisation(self, out)
    install_fixuids(self, out)

    out.write("Successfully installed %s.\n" % PROJECTNAME)
    return out.getvalue()

def uninstall(self):
    out = StringIO()
    uninstall_tool(self, out)
    uninstall_kupu_resource(self, out)
    out.write("Successfully uninstalled %s.\n" % PROJECTNAME)
    return out.getvalue()

##############################################################################
#
# Copyright (c) 2004 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""Composite Tool :
   registration of layouts and viewlets
   mapping of content types and viewlets

$Id: tool.py,v 1.24 2004/11/05 10:36:19 duncanb Exp $
"""
from types import TupleType, ListType

import Globals
from Globals import PersistentMapping

from AccessControl import ClassSecurityInfo
from OFS.ObjectManager import BeforeDeleteException
from Acquisition import aq_base

from OFS.Folder import Folder
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PageTemplates.ZopePageTemplate import manage_addPageTemplate

from Products.CMFCore.CMFCorePermissions import ManagePortal
from Products.CMFCore.utils import getToolByName

from Products.kupu.plone.plonelibrarytool import PloneKupuLibraryTool

KUPU_TOOL_ID = PloneKupuLibraryTool.id

from Products.Archetypes.interfaces.referenceable import IReferenceable

from Products.CompositePage.tool import CompositeTool as BaseTool
from Products.CompositePack.config import TOOL_ID, LAYOUTS
from Products.CompositePack.config import VIEWLETS, LAYOUTS
from Products.CompositePack.config import COMPOSABLE
from Products.CompositePack.config import zmi_dir
from Products.CompositePack import CPpermissions
from Products.CompositePack.exceptions import CompositePackError
from Products.CompositePack.LayoutRegistry import LayoutRegistry
from Products.CompositePack.ViewletRegistry import ViewletRegistry
from Products.CompositePack.ViewletRegistry import DEFAULT
from Products.CompositePack.ViewletRegistry import ViewletsForType
from Products.CompositePack.exceptions import CompositePackError

class CompositeTool(Folder, BaseTool):
    """ CompositePack Tool """

    id = TOOL_ID
    meta_type = 'CompositePack Tool'

    security = ClassSecurityInfo()

    #manage_options = (Folder.manage_options[:1] +
    #                  ({'label' : 'Viewlets',
    #                    'action' : 'manage_selectViewlets' },) +
    #                  Folder.manage_options[1:])

    _viewlets_by_type = None # PersistentMapping
    _default_viewlets = ('default_viewlet', 'link_viewlet')
    _default_default = 'default_viewlet'
    _default_layout = ''
    
    def __init__(self):
        Folder.__init__(self)
        BaseTool.__init__(self)
        self._layout_registry = LayoutRegistry()
        self._viewlet_registry = ViewletRegistry()
    
    def __repr__(self):
        return "CompositePack Tool"

    security.declarePublic("moveAndDelete")
    def moveAndDelete(self, move_source_paths="", move_target_path="",
                      move_target_index="", delete_source_paths="",
                      composite_path="", REQUEST=None):
        """Move and/or delete elements.
        """
        if move_source_paths:
            checkin_message = 'Move element'
        if delete_source_paths:
            checkin_message = 'Delete element'
        portal = getToolByName(self, 'portal_url').getPortalObject()
        compo = portal.restrictedTraverse(composite_path)
        compo.cp_container.incrementVersion(checkin_message)
        BaseTool.moveAndDelete(self, move_source_paths, move_target_path,
                               move_target_index, delete_source_paths, REQUEST)


    ## Viewletsmanagement
    
    def registerAsComposable(self, items):
        if type(items) not in (TupleType, ListType):
            items = (items, )
        for item in items:
            self._viewlet_registry.registerContentType(item)
        self.updateKupuLibraryTool()

    def unregisterAsComposable(self, items):
        if type(items) not in (TupleType, ListType):
            items = (items, )
        for item in items:
            self._viewlet_registry.unregisterContentType(item)
        self.updateKupuLibraryTool()

    def getRegisteredComposables(self):
        return self._viewlet_registry.getContentTypes()

    def isComposable(self, type):
        return self._viewlet_registry.isContentTypeRegistered(type)

    def updateKupuLibraryTool(self):
        try:
            kt = getToolByName(self, KUPU_TOOL_ID)
        except AttributeError:
            raise CompositePackError, 'cannot find kupu library tool'
        resource_list = [resource 
           for resource in self.getRegisteredComposables()    
           if not resource == DEFAULT]
        kt.addResourceType(COMPOSABLE, resource_list) 

    def clearViewletRegistry(self):
        self._viewlet_registry.clear()

    security.declareProtected( ManagePortal, 'registerViewlet' )
    def registerViewlet(self, id, description, skin_method):
        from Products.CompositePack import viewlet
        viewlets = getattr(self, VIEWLETS)
        viewlet.addViewlet(viewlets,
                           id=id,
                           title=description,
                           skin_method=skin_method)
        return getattr(viewlets, id)

    security.declareProtected( ManagePortal, 'unregisterViewlet' )
    def unregisterViewlet(self, id):
        viewlets = getattr(self, VIEWLETS)
        viewlets.manage_delObjects([id])

    def registerViewletForType(self, viewlet, type):
        self._viewlet_registry.registerForType(viewlet.getId(), type)

    def unregisterViewletForType(self, viewlet, type, force=False):
        self._viewlet_registry.unregisterForType(viewlet.getId(), type, force)

    def getViewletById(self, id):
        if hasattr(aq_base(self.viewlets), id):
            return getattr(self.viewlets, id)
        else:
            return None

    def getRegisteredViewletsForType(self, type):
        result = [self.getViewletById(viewlet_id)
                  for viewlet_id in self._viewlet_registry.getForType(type)]
        result = [item for item in result if item]
        return result

    def setDefaultViewletForType(self, viewlet, type):
        self._viewlet_registry.setDefaultForType(viewlet.getId(), type)

    def clearDefaultViewletForType(self, type):
        self._viewlet_registry.setDefaultForType(None, type)

    def getDefaultViewletForType(self, type):
        viewlet_id = self._viewlet_registry.getDefaultForType(type)
        return self.getViewletById(viewlet_id)

    def noDefaultViewletForType(self, type):
        result = False
        try:
            viewlet_id = self._viewlet_registry.getDefaultForType(type)
        except CompositePackError:
            result = True
        return result

    ## viewlets for default setup
    def registerViewletForDefaultSetup(self, viewlet):
        self._viewlet_registry.registerForType(viewlet.getId(), DEFAULT)

    def unregisterViewletForDefaultSetup(self, viewlet, force=False):
        self._viewlet_registry.unregisterForType(viewlet.getId(), DEFAULT, force)

    def getRegisteredViewletsForDefaultSetup(self):
        result = [self.getViewletById(viewlet_id)
                  for viewlet_id in self._viewlet_registry.getForType(DEFAULT)]
        result = [item for item in result if item]
        return result

    def setDefaultViewletForDefaultSetup(self, viewlet):
        self._viewlet_registry.setDefaultForType(viewlet.getId(), DEFAULT)

    def clearDefaultViewletForDefaultSetup(self):
        self._viewlet_registry.setDefaultForType(None, DEFAULT)

    def getDefaultViewletForDefaultSetup(self):
        viewlet_id = self._viewlet_registry.getDefaultForType(DEFAULT)
        return self.getViewletById(viewlet_id)

    def noDefaultViewletForDefaultSetup(self):
        result = False
        try:
            viewlet_id = self._viewlet_registry.getDefaultForType(DEFAULT)
        except CompositePackError:
            result = True
        return result


    ## Layouts management
    
    def registerAsComposite(self, items):
        if type(items) not in (TupleType, ListType):
            items = (items, )
        for item in items:
            self._layout_registry.registerContentType(item)

    def unregisterAsComposite(self, items):
        if type(items) not in (TupleType, ListType):
            items = (items, )
        for item in items:
            self._layout_registry.unregisterContentType(item)

    def getRegisteredComposites(self):
        return self._layout_registry.getContentTypes()

    def isComposite(self, type):
        return self._layout_registry.isContentTypeRegistered(type)

    def clearLayoutRegistry(self):
        self._layout_registry.clear()

    security.declareProtected( ManagePortal, 'registerLayout' )
    def registerLayout(self, id, description, skin_method):
        from Products.CompositePack import viewlet
        layouts = getattr(self, LAYOUTS)
        viewlet.addLayout(layouts,
                           id=id,
                           title=description,
                           skin_method=skin_method)
        return getattr(layouts, id)

    security.declareProtected( ManagePortal, 'unregisterLayout' )
    def unregisterLayout(self, id):
        layouts = getattr(self, LAYOUTS)
        try:
            layouts.manage_delObjects([id])
        except BeforeDeleteException:
            raise CompositePackError, 'cannot unregister default layout'

    def registerLayoutForType(self, layout, type):
        # If the type is not registered yet, implicitly register it.
        if not self._layout_registry.isContentTypeRegistered(type):
            self._layout_registry.registerContentType(type)
        self._layout_registry.registerForType(layout.getId(), type)

    def unregisterLayoutForType(self, layout, type, force=False):
        self._layout_registry.unregisterForType(layout.getId(), type, force)

    def getLayoutById(self, id):
        if hasattr(aq_base(self.layouts), id):
            return getattr(self.layouts, id)
        else:
            return None

    def getRegisteredLayoutsForType(self, type):
        layouts = self._layout_registry.getForType(type)
        if layouts is None:
            layouts = self.layouts.objectIds()
        result = [self.getLayoutById(layout_id)
                for layout_id in layouts]
        result = [item for item in result if item]
        return result

    def setDefaultLayoutForType(self, layout, type):
        self._layout_registry.setDefaultForType(layout.getId(), type)

    def clearDefaultLayoutForType(self, type):
        self._layout_registry.setDefaultForType(None, type)

    def getDefaultLayoutForType(self, type):
        layout_id = self._layout_registry.queryDefaultForType(type, default=None)
        if not layout_id:
            layout_id = self.getDefaultLayout()
        return self.getLayoutById(layout_id)

    def noDefaultLayoutForType(self, type):
        result = False
        try:
            layout_id = self._layout_registry.getDefaultForType(type)
        except CompositePackError:
            result = True
        return result

    security.declareProtected( ManagePortal, 'manage_selectViewlets')
    def manage_selectViewlets(self, REQUEST, manage_tabs_message=None):
        """Manage association between types and viewlets.
        """
        vbt = self._viewlets_by_type
        ti = self._listTypeInfo()
        types_info = []
        # Viewlet IDs. All viewlets are available for
        # all content types for now, but this may change in the
        # future.
        viewlet_info = [{'id':ob.getId(), 'title':ob.title_or_id()}
                        for ob in self.viewlets.objectValues()]
        viewlet_info.sort(lambda x, y: cmp(x['title'], y['title']))
        available_viewlets = viewlet_info[:]
        viewlet_info.insert(0, {'id':DEFAULT, 'title':'use Default Setup'})
        for t in ti:
            id = t.getId()
            title = t.Title()
            if title == id:
                title = None
            if vbt is not None and vbt.has_key(id):
                viewlets = vbt[id].viewlets
                default_per_type = vbt[id].default
            else:
                viewlets = (DEFAULT,)
                default_per_type = DEFAULT
            types_info.append({'id': id,
                               'title': title,
                               'viewlets': viewlets,
                               'default':default_per_type,
                               'viewlet_info':viewlet_info})

        return self._manage_selectViewlets(
            REQUEST, default_viewlets=self._default_viewlets,
            default_default=self._default_default,
            types_info=types_info,
            available_viewlets=available_viewlets)

    _manage_selectViewlets = PageTemplateFile('selectViewlets.pt',
        zmi_dir)

    security.declareProtected( ManagePortal, 'manage_changeViewlets')
    def manage_changeViewlets(self, default_viewlets, default_default, \
                              props=None, REQUEST=None):
        """ Changes which viewlets apply to objects of which type.
        """
        if props is None:
            props = REQUEST
        # Set up the default viewlets.
        self.setDefaultViewlets(default_viewlets, default_default)
        ti = self._listTypeInfo()
        # Set up the viewlets by type.
        for t in ti:
            type = t.getId()
            field_name = 'viewlets_%s' % type
            viewlet_ids = tuple(props.get(field_name, (DEFAULT,)))
            field_name = 'default_%s' % type
            default_viewlet = props.get(field_name, DEFAULT).strip()
            self.setViewletsForType(type, viewlet_ids, default_viewlet)
        if REQUEST is not None:
            return self.manage_selectViewlets(REQUEST,
                            manage_tabs_message='Changed.')

    security.declareProtected( ManagePortal, 'setDefaultViewlets' )
    def setViewletsForType(self, type, viewlet_ids, default_viewlet):
        """ Setup viewlets used by type.
        """
        if viewlet_ids == (DEFAULT, ):
            self._viewlet_registry.setTypeUseDefaultSetup(type)
            viewlet_ids = self._viewlet_registry.getForType(type)
            viewlets = [self.getViewletById(viewlet_id)
                        for viewlet_id in viewlet_ids]
        else:
            self._viewlet_registry.clearForType(type)
            viewlets = [self.getViewletById(viewlet_id)
                        for viewlet_id in viewlet_ids]
            for viewlet in viewlets:
                self.registerViewletForType(viewlet, type)
        if default_viewlet == DEFAULT:
            default_viewlet = self.getDefaultViewletForDefaultSetup()
            if default_viewlet in viewlets:
                self._viewlet_registry.setTypeUseDefaultFromDefaultSetup(type)
            else:
                raise CompositePackError, 'default_viewlet not among viewlet_ids'
        else:
            default_viewlet = self.getViewletById(default_viewlet)
            if default_viewlet in viewlets:
                self.setDefaultViewletForType(default_viewlet, type)
            else:
                raise CompositePackError, 'default_viewlet not among viewlet_ids'

    def old_setViewletsForType(self, type, viewlet_ids, default_viewlet):
        vbt = self._viewlets_by_type
        if vbt is None:
            self._viewlets_by_type = vbt = PersistentMapping()
        if viewlet_ids == (DEFAULT,) and default_viewlet == DEFAULT:
            # Remove from vbt.
            if vbt.has_key(type):
                del vbt[type]
        else:
            viewlet_ids = filter(lambda x: x != DEFAULT, viewlet_ids)
            ids = []
            for viewlet_id in viewlet_ids:
                if viewlet_id:
                    if not self.getViewletById(viewlet_id):
                        raise ValueError, ('"%s" is not a '
                                           'registered viewlet.' %
                                           viewlet_id)
                    ids.append(viewlet_id)
            if default_viewlet == DEFAULT:
                if self._default_default not in viewlet_ids:
                    raise ValueError, (
                        'For type %s, the default viewlet (%s) '
                        'is not among viewlets '
                        '(%s).' % (type, self._default_default, viewlet_ids))
            elif not ((not viewlet_ids and
                       default_viewlet in self._default_viewlets) or
                      default_viewlet in viewlet_ids):
                if not viewlet_ids:
                    viewlet_ids = self._default_viewlets
                raise ValueError, (
                    'For type %s, the default viewlet '
                    '(%s) is not among viewlets '
                    '(%s).' % (type, default_viewlet, viewlet_ids))
            vft = ViewletsForType()
            if not ids:
                ids = (DEFAULT,)
            vft.viewlets = tuple(ids)
            vft.default = default_viewlet
            vbt[type] = vft

    security.declareProtected( ManagePortal, 'setDefaultViewlets' )
    def setDefaultViewlets(self, viewlet_ids, default_viewlet):
        """ Setup viewlets used by types for which nothing has been setup.
        """
        self._viewlet_registry.clearForType(DEFAULT)
        viewlets = [self.getViewletById(viewlet_id)
                    for viewlet_id in viewlet_ids]
        for viewlet in viewlets:
            self.registerViewletForDefaultSetup(viewlet)
        default_viewlet = self.getViewletById(default_viewlet)
        if default_viewlet in viewlets:
            self.setDefaultViewletForDefaultSetup(default_viewlet)
        else:
            raise CompositePackError, 'default_viewlet not among viewlet_ids'

    def old_setDefaultViewlets(self, viewlet_ids, default_viewlet):
        ids = []
        for viewlet_id in viewlet_ids:
            if viewlet_id:
                if not self.getViewletById(viewlet_id):
                    raise ValueError, (
                        'Default setup : "%s" is not a registered viewlet.'
                        % viewlet_id)
                ids.append(viewlet_id)
        if default_viewlet not in ids:
            raise ValueError, ('The default viewlet (%s) of the default '
                               'setup should be among the '
                               'viewlets (%s).' % (default_viewlet,
                                                   viewlet_ids))
        self._default_viewlets = tuple(ids)
        self._default_default = default_viewlet

    security.declarePrivate( '_listTypeInfo' )
    def _listTypeInfo(self):
        """ List the portal types which are available.
        """
        pt = getToolByName(self, 'portal_types', None)
        at = getToolByName(self, 'archetype_tool', None)
        if (pt is None) or (at is None):
            return ()
        else:
            meta_types = [ty['meta_type'] for ty in at.listRegisteredTypes()
                     if IReferenceable.isImplementedByInstancesOf(ty['klass'])]
            tis = [t for t in pt.objectValues()
                   if t.content_meta_type in meta_types]
            tis.sort(lambda a, b: cmp(a.Title(), b.Title()))
            return tis

    def getDefaultLayout(self):
        layout_id = self._default_layout
        if self.getLayoutById(layout_id) is None:
            raise CompositePackError, ("Default layout %s is no more "
                                       "registered" % layout_id)
        return layout_id

    def setDefaultLayout(self, layout_id):
        if self.getLayoutById(layout_id) is None:
            raise CompositePackError, ("%s is not a registered "
                                       "layout" % layout_id)
        self._default_layout = layout_id

    def getViewletsFor(self, obj=None):
        """ Get viewlets for a given object """
        type_id = None
        if obj is not None:
            type_id = obj.getTypeInfo().getId()
        return self.getViewletsForType(type_id)

    def getViewletsForType(self, portal_type=None):
        """ Get viewlets for a given type

        Return a dict where:

          - 'default' value is the default viewlet struct
          - 'viewlets' value is a list of structs with
            the other viewlets

        Each struct is composed of:

          - Viewlet id
          - Viewlet title
          - Viewlet object

        May return None.
        """
        try:
            default = self.getDefaultViewletForType(portal_type).getId()
        except CompositePackError:
            default = self.getDefaultViewletForDefaultSetup().getId()

        viewlets = {}
        registered_viewlets = self.getRegisteredViewletsForType(portal_type)
        if not registered_viewlets:
            registered_viewlets = self.getRegisteredViewletsForDefaultSetup()

        for viewlet in registered_viewlets:
            id = viewlet.getId()
            viewlets[id] = {'id':id,
                            'title':viewlet.title_or_id(),
                            'viewlet':viewlet
                            }
        viewlets_info = viewlets.values()
        if viewlets.has_key(default):
            default_viewlet = viewlets[default]
            del viewlets[default]
            viewlets_info = viewlets.values()
        else:
            default_viewlet = viewlets_info.pop()

        return {'default':default_viewlet, 'viewlets':viewlets_info}

    def old_getViewletsForType(self, portal_type=None):
        vbt = self._viewlets_by_type
        if vbt is not None:
            info = vbt.get(portal_type)
            if info is None:
                # Return default viewlets
                default = self._default_default
                viewlets = self._default_viewlets
            else:
                default = info.default
                if default == DEFAULT:
                    default = self._default_default
                viewlets = info.viewlets
                if viewlets == (DEFAULT,):
                    viewlets = self._default_viewlets
        else:
            # Return default viewlets
            default = self._default_default
            viewlets = self._default_viewlets
        v_names = tuple(viewlets) + (default,)
        v_names = filter(lambda x: x != DEFAULT, v_names)
        viewlets = {}
        for name in v_names:
            viewlet = self.getViewletById(name)
            if viewlet is None:
                continue
            viewlets[name] = {'id':name,
                              'title':viewlet.title_or_id(),
                              'viewlet':viewlet
                              }
        if not viewlets:
            return None
        viewlets_info = viewlets.values()
        if viewlets.has_key(default):
            default_viewlet = viewlets[default]
            del viewlets[default]
            viewlets_info = viewlets.values()
        else:
            default_viewlet = viewlets_info.pop()
        return {'default':default_viewlet, 'viewlets':viewlets_info}

    def findSnippets(self, **kwargs):
        """ Find snippets for use as Composite Element targets

        Those can include:
           - Filesystem Composite Snippets
           - Registered Viewlets

        In the case where a 'context' keyword argument is passed,
        the viewlets returned are only those that apply to the context.
        """
        st = getToolByName(self, 'portal_skins')
        ct = getToolByName(self, 'portal_catalog')
        f_params = {'search_sub':1}
        c_params = {'portal_type':'CompositePack Viewlet'}
        mt = kwargs.get('meta_type')
        if mt is not None:
            f_params['obj_metatypes'] = mt
        else:
            f_params['obj_metatypes'] = ['Filesystem Composite Snippet']
        text = kwargs.get('SearchableText')
        if mt is not None:
            f_params['obj_searchterm'] = text
            c_params['SearchableText'] = text
        f_res = st.ZopeFind(st, **f_params)
        s_res = ct(**c_params)
        context = kwargs.get('context')
        if context is not None:
            v_info = self.getViewletsFor(context)
            if v_info is not None:
                v_info = v_info.get('default', ()) + v_info.get('viewlets', ())
                v_ids = [v['id'] for v in v_info]
                s_res = filter(lambda b: b.id in v_ids, s_res)
        result = [t for p, t in f_res]
        templates = [b.getObject().getTemplate() for b in s_res]
        result.extend(templates)
        return templates

Globals.InitializeClass(CompositeTool)

def manage_addCompositeTool(dispatcher, REQUEST=None):
    """Adds a composite tool to a folder.
    """
    from Products.CompositePack.viewlet import container
    ob = CompositeTool()
    dispatcher._setObject(ob.getId(), ob)
    ob = dispatcher._getOb(ob.getId())
    container.addViewletContainer(ob, id=VIEWLETS,
                                  title='A Container for registered Viewlets')
    container.addLayoutContainer(ob, id=LAYOUTS,
                                  title='A Container for registered Layouts')
    if REQUEST is not None:
        return dispatcher.manage_main(dispatcher, REQUEST)

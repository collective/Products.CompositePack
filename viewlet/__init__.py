##############################################################################
#
# Copyright (c) 2004 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""CompositePack Viewlet :
   placeholder for a method found by acquisition
   this method is used to display a composite element.


$Id: __init__.py,v 1.11 2004/11/03 10:56:45 duncanb Exp $
"""
from AccessControl import ClassSecurityInfo
from OFS.ObjectManager import BeforeDeleteException
from OFS import PropertyManager
from OFS.SimpleItem import Item

from Products.Archetypes.public import *
from Products.Archetypes.utils import insert_zmi_tab_before

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import ManagePortal

from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.CompositePack.viewlet.interfaces import IViewlet
from Products.CompositePack.viewlet.interfaces import ILayout
from Products.CompositePack.config import PROJECTNAME, TOOL_ID
from Products.CompositePack.config import zmi_dir
from Products.CompositePack.exceptions import CompositePackError
from md5 import md5

class SkinMethod(BaseContentMixin, Item):

    meta_type = portal_type = archetype_name = 'CompositePack Skin Method'
    global_allow = 0

    schema = MinimalSchema + Schema((
        StringField(
        'skin_method',
        accessor='getSkinMethod',
        mutator='setSkinMethod',
        widget=StringWidget(label='Skin Method',
                            description=('Method called for rendering '
                                         'the viewlet/layout.'))
        ),
        ))

    def getTemplate(self):
        """ Return the template """
        purl = getToolByName(self, 'portal_url')
        portal = purl.getPortalObject()
        return portal.restrictedTraverse(self.getSkinMethod())

class Viewlet(SkinMethod, PropertyManager.PropertyManager):

    _properties=({'id':'title', 'type': 'string','mode':'wd'},)
    
    __implements__ = BaseContent.__implements__ + (IViewlet,)

    security = ClassSecurityInfo()
    
    meta_type = portal_type = archetype_name = 'CompositePack Viewlet'

    factory_type_information={
            'content_icon':'composite.gif',
            }

    _manage_register_form = PageTemplateFile('registerViewlet.pt',
        zmi_dir)

    manage_options = insert_zmi_tab_before('Dublin Core', 
                                   {'label':'Register',
                                    'action':'manage_register_form'},
                                   BaseContent.manage_options)

    security.declareProtected( ManagePortal, 'manage_register_form' )
    def manage_register_form(self, REQUEST, manage_tabs_message=None):
        '''
        manage registered types for viewlet
        '''
        reg_types_info = list()
        unreg_types_info = list()
        ct = getToolByName(self, TOOL_ID)
        for type in ct.getRegisteredComposables():
            type_info = {}
            type_info['title'] = type
            type_info['default'] = self.isDefaultForType(type)
            type_info['nodefault'] = ct.noDefaultViewletForType(type)
            if self.isRegisteredForType(type):
                reg_types_info.append(type_info)
            else:
                unreg_types_info.append(type_info)
        return self._manage_register_form(REQUEST,
                                          reg_types_info=reg_types_info,
                                          unreg_types_info=unreg_types_info)

    security.declareProtected( ManagePortal, 'manage_add_types' )
    def manage_add_types(self, REQUEST, manage_tabs_message=None, types=None):
        '''
        register types for types
        '''
        if types is None:
           types = []
        self.registerForTypes(types)
        return self.REQUEST.RESPONSE.redirect('manage_register_form')

    security.declareProtected( ManagePortal, 'change_register' )
    def change_register(self, REQUEST, manage_tabs_message=None, types=[]):
        '''
        change registration for registered types
        '''
        for type in types:
            setting = REQUEST.get(type, None)
            if setting is not None:
                if setting.has_key('selected'):
                    self.registerForType(type)
                    if setting.has_key('default'):
                        self.setDefaultForType(type)
                    else:
                        if self.isDefaultForType(type):
                            self.clearDefaultForType(type)
                else:
                    self.unregisterForType(type, force=True)
            else:
                self.unregisterForType(type, force=True)
        #return self.manage_register_form(REQUEST)
        return self.REQUEST.RESPONSE.redirect('manage_register_form')

    def registerForTypes(self, list):
        for type in list:
            self.registerForType(type)

    def registerForDefaultSetup(self):
        ct = getToolByName(self, TOOL_ID)
        ct.registerViewletForDefaultSetup(self)

    def unregisterForDefaultSetup(self, force=False):
        ct = getToolByName(self, TOOL_ID)
        ct.unregisterViewletForDefaultSetup(self, force)
        
    def setDefaultForDefaultSetup(self):
        ct = getToolByName(self, TOOL_ID)
        ct.setDefaultViewletForDefaultSetup(self)

    def clearDefaultForDefaultSetup(self):
        ct = getToolByName(self, TOOL_ID)
        ct.clearDefaultViewletForDefaultSetup()

    def isRegisteredForDefaultSetup(self):
        ct = getToolByName(self, TOOL_ID)
        return self in ct.getRegisteredViewletsForDefaultSetup()

    def isDefaultForDefaultSetup(self):
        ct = getToolByName(self, TOOL_ID)
        try:
            return self == ct.getDefaultViewletForDefaultSetup()
        except CompositePackError:
            return False

    def registerForType(self, type):
        ct = getToolByName(self, TOOL_ID)
        ct.registerViewletForType(self, type)

    def unregisterForType(self, type, force=False):
        ct = getToolByName(self, TOOL_ID)
        ct.unregisterViewletForType(self, type, force)
        
    def setDefaultForType(self, type):
        ct = getToolByName(self, TOOL_ID)
        ct.setDefaultViewletForType(self, type)

    def clearDefaultForType(self, type):
        ct = getToolByName(self, TOOL_ID)
        ct.clearDefaultViewletForType(type)

    def isRegisteredForType(self, type):
        ct = getToolByName(self, TOOL_ID)
        return self in ct.getRegisteredViewletsForType(type)

    def isDefaultForType(self, type):
        ct = getToolByName(self, TOOL_ID)
        try:
            return self == ct.getDefaultViewletForType(type)
        except CompositePackError:
            return False

    def setStableUID(self):
        '''Set a UID generated from the viewlet's path'''
        path = []
        ct = getToolByName(self, TOOL_ID)
        
        obj = self
        while obj != ct:
            path.append(obj.getId())
            obj = obj.aq_parent
        path.append(obj.getId())

        uid = md5(self.meta_type + ' ' + '/'.join(path)).hexdigest()
        if uid != self.UID():
            # XXX Archetypes bug: _setUID sometimes randomises UID unless we clear
            # the copy flag
            self._v_is_cp = None
            self._setUID(uid)
        
    def manage_afterAdd(self, item, container):
        SkinMethod.manage_afterAdd(self, item, container)
        self.setStableUID()

    def manage_afterClone(self, item):
        SkinMethod.manage_afterClone(self, item)
        self.setStableUID()

class Layout(SkinMethod):

    __implements__ = BaseContent.__implements__ + (ILayout,)

    security = ClassSecurityInfo()
    
    meta_type = portal_type = archetype_name = 'CompositePack Layout'

    factory_type_information={
            'content_icon':'composite.gif',
            }

    _manage_register_form = PageTemplateFile('registerLayout.pt',
        zmi_dir)

    manage_options = insert_zmi_tab_before('Dublin Core', 
                                   {'label':'Register',
                                    'action':'manage_register_form'},
                                   BaseContent.manage_options)

    security.declareProtected( ManagePortal, 'manage_register_form' )
    def manage_register_form(self, REQUEST, manage_tabs_message=None):
        '''
        manage registered types for layout
        '''
        reg_types_info = list()
        unreg_types_info = list()
        ct = getToolByName(self, TOOL_ID)
        for type in ct.getRegisteredComposites():
            type_info = {}
            type_info['title'] = type
            type_info['default'] = self.isDefaultForType(type)
            type_info['nodefault'] = ct.noDefaultLayoutForType(type)
            if self.isRegisteredForType(type):
                reg_types_info.append(type_info)
            else:
                unreg_types_info.append(type_info)
        return self._manage_register_form(REQUEST,
                                          reg_types_info=reg_types_info,
                                          unreg_types_info=unreg_types_info)

    security.declareProtected( ManagePortal, 'manage_add_types' )
    def manage_add_types(self, REQUEST, manage_tabs_message=None, types=None):
        '''
        register types for layout
        '''
        if types is None:
           types = []
        self.registerForTypes(types)
        return self.REQUEST.RESPONSE.redirect('manage_register_form')

    security.declareProtected( ManagePortal, 'change_register' )
    def change_register(self, REQUEST, manage_tabs_message=None, types=[]):
        '''
        change registration for registered types
        '''
        for type in types:
            setting = REQUEST.get(type, None)
            if setting is not None:
                if setting.has_key('selected'):
                    self.registerForType(type)
                    if setting.has_key('default'):
                        self.setDefaultForType(type)
                    else:
                        if self.isDefaultForType(type):
                            self.clearDefaultForType(type)
                else:
                    self.unregisterForType(type, force=True)
            else:
                self.unregisterForType(type, force=True)
        #return self.manage_register_form(REQUEST)
        return self.REQUEST.RESPONSE.redirect('manage_register_form')

    def registerForType(self, type):
        ct = getToolByName(self, TOOL_ID)
        ct.registerLayoutForType(self, type)

    def registerForTypes(self, list):
        for type in list:
            self.registerForType(type)

    def unregisterForType(self, type, force=False):
        ct = getToolByName(self, TOOL_ID)
        ct.unregisterLayoutForType(self, type, force)
        
    def setDefaultForType(self, type):
        ct = getToolByName(self, TOOL_ID)
        ct.setDefaultLayoutForType(self, type)

    def clearDefaultForType(self, type):
        ct = getToolByName(self, TOOL_ID)
        ct.clearDefaultLayoutForType(type)

    def isRegisteredForType(self, type):
        ct = getToolByName(self, TOOL_ID)
        return self in ct.getRegisteredLayoutsForType(type)

    def isDefaultForType(self, type):
        ct = getToolByName(self, TOOL_ID)
        try:
            return self == ct.getDefaultLayoutForType(type)
        except CompositePackError:
            return False

    security.declarePrivate('manage_beforeDelete')
    def manage_beforeDelete(self, item, container):
        ct = getToolByName(self, TOOL_ID)
        if ct.getDefaultLayout() == self.getId():
            raise BeforeDeleteException, 'cannot unregister default layout'
        

registerType(SkinMethod, PROJECTNAME)
registerType(Viewlet, PROJECTNAME)
registerType(Layout, PROJECTNAME)

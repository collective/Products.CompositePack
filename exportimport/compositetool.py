"""Plone Properties tool setup handlers.

$Id:$
"""

from zope.app import zapi
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.interfaces import INode
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.utils import ObjectManagerHelpers
from Products.GenericSetup.utils import PropertyManagerHelpers
from Products.GenericSetup.utils import I18NURI
from Products.CMFPlone.PropertiesTool import SimpleItemWithProperties
from Products.CMFPlone.interfaces import IPropertiesTool, ISimpleItemWithProperties

from Products.CompositePack.Extensions.Install from toolWrapper

_FILENAME = 'compositetool.xml'
nodeTypeMap = {'layouts':'CompositePack Layout Container',
               'layout':'CompositePack Layout',
               'viewlet':'CompositePack Viewlet',
               'viewlets':'CompositePack Viewlet Container',
               'classes':'Slot Class Folder',
               'class':'Slot Class',
    }
containers = ['layouts','viewlets','classes']


def importCompositeToolProperties(context):
    """ Import composite tool properties.
    """
    site = context.getSite()
    logger = context.getLogger('composite tool properties')
    ptool = getToolByName(site, 'composite_tool')

    body = context.readDataFile(_FILENAME)
    if body is None:
        logger.info('Composite tool: Nothing to import.')
        return

    importer = zapi.queryMultiAdapter((ptool, context), IBody)
    if importer is None:
        logger.warning('Composite tool: Import adapter misssing.')
        return

    importer.body = body
    logger.info('Composite tool imported.')

def exportCompositeToolProperties(context):
    """ Export composite tool properties.
    """
    site = context.getSite()
    logger = context.getLogger('composite tool properties')
    ptool = getToolByName(site, 'composite_tool', None)
    if ptool is None:
        logger.info('Composite tool: Nothing to export.')
        return

    exporter = zapi.queryMultiAdapter((ptool, context), IBody)
    if exporter is None:
        return 'Composite tool: Export adapter misssing.'

    context.writeDataFile(_FILENAME, exporter.body, exporter.mime_type)
    logger.info('Composite tool properties exported.')


class CompositeToolXMLAdapter(XMLAdapterBase, ObjectManagerHelpers):

    """Node im- and exporter for composite tool.
    """

    __used_for__ = ICompositeTool

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        #self._doc = doc
        node = self._getObjectNode('object')
        #node.setAttribute('xmlns:i18n', I18NURI)
        node.appendChild(self._extractObjects())
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        if self.environ.shouldPurge():
            self._purgeObjects()

        self._initObjects(node)
        
    def _purgeObjects(self):
        """ Keep the following folders:
              -  CompositePack Layout Container
              -  CompositePack Viewlet Container
              -  Slot Class Folder
            but delete all child object inside those folders
        """
        tool = self.context
        for id in tool.objectIds():
            ids =  tool['id'].objectIds()
            tool['id'].delObjects(ids)

    def _createObjectTree(self, node, context):
        """ Create the object treetructure found in the ZMI
        """
        obj_id = str(node.getAttribute('name'))
        obj_type = node.nodeName
        
        # Here we only take care of the content type found in de ZMI as
        # defined in the nodeTypeMap.
        if obj_type in nodeTypeMap.keys() and obj_id not in context.objectIds():
            context._setObject(id, obj_type(id))
            if obj_type in ['layout','viewlet']:
                obj.setTitle(obj_title)
                skin_method = str(node.getAttribute('skin_method'))
                
                
            if obj_type == 'layout':
                obj.setTitle(obj_title)
                
            if node.childNodes:
                for child in node.childNodes:
                    _createObject(child, obj)

    def _configureComposables(self, node, context):
        """ Configure the mapping between content types and layouts
        """
        if obj_type == 'composables':

    def _configureComposites(self, node, context):
        """ Configure the mapping between content types and layouts
        """
        if obj_type == 'composites':

    def _initObjects(self, node):
        """ Import subobjects from the DOM tree.
            Directly under a compositetool we are allowed to create:
                -  CompositePack Layout Container
                -  CompositePack Viewlet Container
                -  Slot Class Folder
            Within each container only one type of object can be created
                -  CompositePack Layout
                -  CompositePack Viewlet
                -  Slot Class
                
            Base on the nodeName of the DOM we create the corresponding type of object.
            
        """

        self.tool = toolWrapper(self.context)
        
        for child in node.Childnodes:
            if child.nodeName == 'object':
                obj_id = str(node.getAttribute('name'))
                obj_type = str(node.getAttribute('name'))
                
            if child.nodeName == 'composables':
                self._configureComposites(child, tool)

        self._createObjectTree(node, self.context)
        self._configureComposables(node, tool)

        for child in node.childNodes:
            # Make sure that if we deprecate a node it is not added.
            if child.hasAttribute('deprecated'):
                continue

            # For each child we check if the 
                tool._createObject(node, tool nodeTypeMap[obj_type](obj_id))
                if child.childNodes is not None:
                    
                
            obj_type = child.nodName
            if obj_id not in parent.objectIds():
                
##                 Original _initObjects code:
##                 meta_type = str(child.getAttribute('meta_type'))
##                 for mt_info in Products.meta_types:
##                     if mt_info['name'] == meta_type:
##                         parent._setObject(obj_id, mt_info['instance'](obj_id))
##                         break
##                 else:
##                     raise ValueError('unknown meta_type \'%s\'' % obj_id)

            if child.hasAttribute('insert-before'):
                insert_before = child.getAttribute('insert-before')
                if insert_before == '*':
                    parent.moveObjectsToTop(obj_id)
                else:
                    try:
                        position = parent.getObjectPosition(insert_before)
                        parent.moveObjectToPosition(obj_id, position)
                    except ValueError:
                        pass
            elif child.hasAttribute('insert-after'):
                insert_after = child.getAttribute('insert-after')
                if insert_after == '*':
                    parent.moveObjectsToBottom(obj_id)
                else:
                    try:
                        position = parent.getObjectPosition(insert_after)
                        parent.moveObjectToPosition(obj_id, position+1)
                    except ValueError:
                        pass

            obj = getattr(self.context, obj_id)
            importer = zapi.queryMultiAdapter((obj, self.environ), INode)
            if importer:
                importer.node = child


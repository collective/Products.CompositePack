from zope.app import zapi
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.utils import ObjectManagerHelpers
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects

from Products.CompositePack.interfaces import ICompositeTool
from Products.CompositePack.Extensions.Install import toolWrapper

nodeTypeMap = {'layouts':'CompositePack Layout Container',
               'layout':'CompositePack Layout',
               'viewlet':'CompositePack Viewlet',
               'viewlets':'CompositePack Viewlet Container',
               'classes':'Slot Class Folder',
               'class':'Slot Class',
    }
containers = ['layouts','viewlets','classes']


class CompositeToolXMLAdapter(XMLAdapterBase, ObjectManagerHelpers):
    """
    Node im- and exporter for composite tool.
    """
    __used_for__ = ICompositeTool

    name = 'composite_tool'

    def _exportNode(self):
        """
        Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        node.appendChild(self._extractCompositeConfiguration())
        self._logger.info("Composite settings exported.")
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        if self.environ.shouldPurge():
            self._purgeObjects()

        self._initObjects(node)
        self._logger.info("Composite settings imported.")
        
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

    def _extractCompositeConfiguration(self):
        """
        Generate the compositetool.xml from the current configuration.
        """
        fragment = self._doc.createDocumentFragment()
        tool = self.context

        # Lets start with the composites.
        compositesElement = self._doc.createElement('composites')
        compositesElement.setAttribute('name', 'composites')
        for composite in tool.getRegisteredComposites():
            child = self._doc.createElement('composite')
            child.setAttribute('name', composite)
            compositeElement = compositesElement.appendChild(child)

            layoutsForType = tool.getRegisteredLayoutsForType(composite)
            layoutsForType = [l.getId() for l in layoutsForType]
            for layout in layoutsForType:
                child = self._doc.createElement('c_layout')
                child.setAttribute('name', layout)
                default_layout = tool.getDefaultLayoutForType(composite).getId()
                if default_layout == layout and len(layoutsForType) > 1:
                    child.setAttribute('default', 'True')
                compositeElement.appendChild(child)
        fragment.appendChild(compositesElement)

        # Now for the composables.
        composablesElement = self._doc.createElement('composables')
        composablesElement.setAttribute('name', 'composites')
        for composable in tool.getRegisteredComposables():
            child = self._doc.createElement('composable')
            child.setAttribute('name', composable)
            composableElement = composablesElement.appendChild(child)

            viewletsForType = tool.getRegisteredViewletsForType(composable)
            viewletsForType = [v.getId() for v in viewletsForType]
            for viewlet in viewletsForType:
                child = self._doc.createElement('c_viewlet')
                child.setAttribute('name', viewlet)
                default_viewlet = tool.getDefaultViewletForType(composable).getId()
                if default_viewlet == viewlet and len(viewletsForType) > 1:
                    child.setAttribute('default', 'True')
                composableElement.appendChild(child)
        fragment.appendChild(composablesElement)

        # Let's add some viewlet!
        viewletsElement = self._doc.createElement('viewlets')
        viewletsElement.setAttribute('name', 'viewlets')
        for viewlet in tool.getAllViewlets():
            child = self._doc.createElement('viewlet')
            child.setAttribute('name', viewlet.getId())
            child.setAttribute('title', viewlet.Title())
            child.setAttribute('skin_method', viewlet.getSkinMethod())
            viewletsElement.appendChild(child)
        fragment.appendChild(viewletsElement)

        # Let's add some layouts!
        layoutsElement = self._doc.createElement('layouts')
        layoutsElement.setAttribute('name', 'layouts')
        for layout in tool.getAllLayouts():
            child = self._doc.createElement('layout')
            child.setAttribute('name', layout.getId())
            child.setAttribute('title', layout.Title())
            child.setAttribute('skin_method', layout.getSkinMethod())
            layoutsElement.appendChild(child)
        fragment.appendChild(layoutsElement)

        return fragment

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

    def _configureComposites(self, node, context):
        """ Configure the mapping between content types and layouts
        """

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



def importCompositeTool(context):
    """ Import composite tool properties.
    """
    site = context.getSite()
    logger = context.getLogger('composite tool properties')
    ptool = getToolByName(site, 'composite_tool')

    body = context.readDataFile('compositetool.xml')
    if body is None:
        logger.info('Composite tool: Nothing to import.')
        return

    importer = zapi.queryMultiAdapter((ptool, context), IBody)
    if importer is None:
        logger.warning('Composite tool: Import adapter misssing.')
        return

    importer.body = body
    logger.info('Composite tool imported.')

def exportCompositeTool(context):
    """ Export composite tool properties.
    """

    site = context.getSite()
    logger = context.getLogger('composite tool properties')
    tool = getToolByName(site, 'composite_tool', None)
    if tool is None:
        logger.info('Composite tool: Nothing to export.')
        return

    exportObjects(tool, '', context)
    logger.info('Composite tool properties exported.')


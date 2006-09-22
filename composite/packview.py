from Products.Five import BrowserView

from Products.azax.azaxview import AzaxBaseView

class PackView(BrowserView):

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)

    def createCompositeElement(self, destination, target_index):
        factory = destination.manage_addProduct['CompositePack'].manage_addElement

        new_id = self.context.generateUniqueIdForCSS()
#        new_id = ''.join(new_id.split('.'))
        new_id = factory(id=new_id)
        destination.moveObjectToPosition(new_id, int(target_index))
        new_el = getattr(destination, new_id)
        return new_el

    def createTitleElement(self, title):
        titles = self.context.titles
        factory = titles.manage_addProduct['CompositePack'].manage_addTitles
        new_id = self.context.generateUniqueId()
        new_id = factory(id=new_id)
        new_title = getattr(titles, new_id)
        new_title.setTitle(title)
        return new_title

    def createHTMLFragmentElement(self):
        titles = self.context.titles
        factory = titles.manage_addProduct['CompositePack'].manage_addFragments
        new_id = self.context.generateUniqueId()
        new_id = factory(id=new_id)
        new_fragment = getattr(titles, new_id)
        return new_fragment
    
    def calculatePosition(self, destination, target_id):
        element_id = target_id[len(destination.getId())+8:]
        if element_id == 'cp_top':
            position = 0
        else:
            position = destination.getObjectPosition(element_id) + 1
        print position
        return position
    
    def calculateIdFromPosition(self, destination, position):
        if position == 0:
            return 'cp_top'
        else:
            try:
                return destination.objectIds()[position-1]
            except IndexError:
                import pdb; pdb.set_trace() 
    
    def deleteElement(self, uri):
        parts = uri.split('/')
        slot_path = '/'.join(parts[2:-1])
        
        element_id = parts[-1]
        
        portal = self.context.portal_url.getPortalObject()
        slot = portal.restrictedTraverse(slot_path)
        slot.manage_delObjects([element_id])

        selector = '#%s_%s' % (slot.getId(), element_id)
        self.deleteNodeAfter(selector)
        self.deleteNode(selector)
        return self.render()
        
    def moveElement(self, target_path, target_id, uri):
        portal = self.context.portal_url.getPortalObject()

        parts = uri.split('/')
        source_slot_path = '/'.join(parts[2:-1])
        source_element_id = parts[-1]
        source_slot = portal.restrictedTraverse(source_slot_path)
        
        parts = target_path.split('/')
        
        target_slot_path = '/'.join(parts[2:])
        target_slot = portal.restrictedTraverse(target_slot_path)
        target_node_css = '#%s' % target_id
        target_index = self.calculatePosition(target_slot, target_id)
        
        cpt = portal.restrictedTraverse('composite_tool')
        cpt.moveAndDelete(uri, target_path, target_index)
        
        node_id = '%s_%s' % (source_slot.getId(), source_element_id)
        node_css = '#%s' % node_id
        self.deleteNodeAfter(node_css)
        self.deleteNode(node_css)

        moved_element = target_slot.restrictedTraverse(source_element_id)
        
        added_text = target_slot.getEditingViewlet(moved_element)
        added_text = (added_text +
            target_slot.getTargetAfterViewlet(moved_element))
        self.insertHTMLAfter(target_node_css, added_text)
        
        selector = "#%s" % target_slot.getViewletHtmlId(moved_element)
        self.setupElement(selector)
        selector = "#%s" % target_slot.getIdOfTargetAfterViewlet(moved_element)
        self.setupTarget(selector)
        return self.render()

    def setupElement(self, selector):
        command = self.addCommand('cpSetupElement', selector)

    def setupTarget(self, selector):
        command = self.addCommand('cpSetupTarget', selector)

    def addTitle(self, title, target_path, target_id):

        portal = self.context.portal_url.getPortalObject()
        destination = portal.restrictedTraverse(target_path)
        
        target_index = self.calculatePosition(destination, target_id) 
        
        new_el = self.createCompositeElement(destination, target_index)
        
        new_title = self.createTitleElement(title)
        new_title.setComposite(new_el.UID())

        uid = new_title.UID()
        new_el.setTarget(uid)

        added_text = destination.getEditingViewlet(new_el)
        added_text = added_text + destination.getTargetAfterViewlet(new_el)
        #import pdb; pdb.set_trace() 
        selector = '#%s' % target_id
        self.insertHTMLAfter(selector, added_text)
        
        selector = "#%s" % destination.getViewletHtmlId(new_el)
        self.setupElement(selector)
        selector = "#%s" % destination.getIdOfTargetAfterViewlet(new_el)
        self.setupTarget(selector)
        return self.render()

    def addFragment(self, target_path, target_id):
        portal = self.context.portal_url.getPortalObject()
        destination = portal.restrictedTraverse(target_path)
        
        target_index = self.calculatePosition(destination, target_id) 

        new_el = self.createCompositeElement(destination, target_index)
        
        new_fragment = self.createHTMLFragmentElement()
        new_fragment.setComposite(new_el.UID())

        uid = new_fragment.UID()
        new_el.setTarget(uid)

        added_text = destination.getEditingViewlet(new_el)
        added_text = added_text + destination.getTargetAfterViewlet(new_el)
        selector = '#%s' % target_id
        self.insertHTMLAfter(selector, added_text)
        
        selector = "#%s" % destination.getViewletHtmlId(new_el)
        self.setupElement(selector)
        selector = "#%s" % destination.getIdOfTargetAfterViewlet(new_el)
        self.setupTarget(selector)
        return self.render()

    def addContent(self, target_path, target_id, uri):
        portal_url_tool = self.context.portal_url
        portal = portal_url_tool.getPortalObject()
        destination = portal.restrictedTraverse(target_path)
        
        target_index = self.calculatePosition(destination, target_id) 
        
        new_el = self.createCompositeElement(destination, target_index)
        
        uid = uri.split('/')[-1]
        new_el.setTarget(uid)

        added_text = destination.getEditingViewlet(new_el)
        added_text = added_text + destination.getTargetAfterViewlet(new_el)
        selector = '#%s' % target_id
        self.insertHTMLAfter(selector, added_text)
        
        selector = "#%s" % destination.getViewletHtmlId(new_el)
        self.setupElement(selector)
        selector = "#%s" % destination.getIdOfTargetAfterViewlet(new_el)
        self.setupTarget(selector)
        return self.render()


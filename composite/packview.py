from Products.azax import AzaxBaseView


class PackView(AzaxBaseView):

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
        element_id = target_id[len(destination.getId())+1:]
        if element_id == 'cp_top':
            position = 0
        else:
            position = destination.getObjectPosition(element_id) + 1
        print position
        return position
    
    def addTitle(self):
        request = self.request

        target_path = request.target_path
        portal = self.context.portal_url.getPortalObject()
        destination = portal.restrictedTraverse(target_path)
        
        target_id = request.target_id
        
        target_index = self.calculatePosition(destination, target_id) 
        
        title = request.title

        new_el = self.createCompositeElement(destination, target_index)
        
        new_title = self.createTitleElement(title)
        new_title.setComposite(new_el.UID())

        uid = new_title.UID()
        new_el.setTarget(uid)


        added_text = destination.getEditingViewlet(new_el)
        added_text = added_text + destination.getTargetAfterViewlet(new_el)
        #import pdb; pdb.set_trace() 
        selector = '#%s' % target_id
        self.addAfter(selector, added_text)
        
        code = 'plone_updateAfterAdd(Azax.getLastResults());'
        self.executeCode(selector, code)
        return self.render()

    def addFragment(self):
        request = self.request

        target_path = request.target_path
        portal = self.context.portal_url.getPortalObject()
        destination = portal.restrictedTraverse(target_path)
        
        target_id = request.target_id
        
        target_index = self.calculatePosition(destination, target_id) 

        new_el = self.createCompositeElement(destination, target_index)
        
        new_fragment = self.createHTMLFragmentElement()
        new_fragment.setComposite(new_el.UID())

        uid = new_fragment.UID()
        new_el.setTarget(uid)


        added_text = destination.getEditingViewlet(new_el)
        added_text = added_text + destination.getTargetAfterViewlet(new_el)
        selector = '#%s' % target_id
        self.addAfter(selector, added_text)
        
        code = 'plone_updateAfterAdd(Azax.getLastResults());'
        self.executeCode(selector, code)
        return self.render()

    def addContent(self):
        request = self.request

        target_path = request.target_path
        portal_url_tool = self.context.portal_url
        portal = portal_url_tool.getPortalObject()
        destination = portal.restrictedTraverse(target_path)
        
        target_id = request.target_id
        
        target_index = self.calculatePosition(destination, target_id) 
        
        uri = request.uri

        new_el = self.createCompositeElement(destination, target_index)
        
        uid = uri.split('/')[-1]
        new_el.setTarget(uid)


        added_text = destination.getEditingViewlet(new_el)
        added_text = added_text + destination.getTargetAfterViewlet(new_el)
        selector = '#%s' % target_id
        self.addAfter(selector, added_text)
        
        code = 'plone_updateAfterAdd(Azax.getLastResults());'
        self.executeCode(selector, code)
        return self.render()

    

##parameters=compopage_path, target_path, target_index


portal = context.portal_url.getPortalObject()

destination = portal.restrictedTraverse(target_path)
factory = destination.manage_addProduct['CompositePack'].manage_addPortalElement

new_id = context.generateUniqueId()
new_id = factory(id=new_id)
destination.moveObjectToPosition(new_id, int(target_index))

compo = portal.restrictedTraverse(compopage_path)
compo.cp_container.incrementVersion('Add title')
pageDesignUrl = compo.absolute_url() + '/design_view'

return context.REQUEST.RESPONSE.redirect(pageDesignUrl)

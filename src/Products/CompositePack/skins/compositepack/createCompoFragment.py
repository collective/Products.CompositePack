## Script (Python) "createCompoFragment"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=compopage_path, target_path, target_index
##title=
##
portal = context.portal_url.getPortalObject()

destination = portal.restrictedTraverse(target_path)
compo = portal.restrictedTraverse(compopage_path)
new_id = context.generateUniqueId()
new_id = destination.invokeFactory('CompositePack Element', id=new_id)
destination.moveObjectToPosition(new_id, int(target_index))
new_el = getattr(destination, new_id)


new_id = context.generateUniqueId()
new_id = compo.cp_container.titles.invokeFactory('CompositePack Fragments', id=new_id)
new_fragment = getattr(compo.cp_container.titles, new_id)
new_fragment.setComposite(new_el.UID())

uid = new_fragment.UID()
new_el.setTarget(uid)

pageDesignUrl = compo.absolute_url() + '/design_view'
return context.REQUEST.RESPONSE.redirect(pageDesignUrl)


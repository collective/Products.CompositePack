## Script (Python) "createCompoTitle"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=compopage_path, target_path, target_index, title
##title=
##
portal = context.portal_url.getPortalObject()

destination = portal.restrictedTraverse(target_path)

compo = portal.restrictedTraverse(compopage_path)
new_id = compo.cp_container.generateUniqueIdForCSS()
new_id = destination.invokeFactory('CompositePack Element', id=new_id)
destination.moveObjectToPosition(new_id, int(target_index))
new_el = getattr(destination, new_id)

new_id = context.generateUniqueId()
new_id = compo.cp_container.titles.invokeFactory('CompositePack Titles', id=new_id)
new_titles = getattr(compo.cp_container.titles, new_id)
new_titles.setTitle(title)
new_titles.setComposite(new_el.UID())

uid = new_titles.UID()
new_el.setTarget(uid)

pageDesignUrl = compo.absolute_url() + '/design_view'

return context.REQUEST.RESPONSE.redirect(pageDesignUrl)

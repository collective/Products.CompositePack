kukit.cr.makeSelectorCommand('cpSetupTarget', function(oper) {
    plone_setUpSlotTarget(oper.node);
    kukit.logDebug('CP target setup');
});

kukit.cr.makeSelectorCommand('cpSetupElement', function(oper) {
    plone_setUpSlotElement(oper.node);
    kukit.logDebug('CP element setup');
});

kukit.logDebug('CP commands registered')

/* kukit.pdlib = {};

kukit.pdlib.ContextMenuEvent = function() {
};

kukit.pdlib.ContextMenuEvent.prototype.__bind_click__ = function(name, parms, func_to_bind, node, eventrule) {
    parms = kukit.pl.completeParms(parms, ['menuId'], {}, 'pdlib:contextMenu event binding');
    this.menuId = parms.menuId;
    // Just bind the event via the native event binder
    kukit.pl.NativeEventBinder.prototype.__bind__('click', {}, func_to_bind, node);
};

kukit.pdlib.ContextMenuEvent.prototype.__default_click__ = function(name, parms, node, e) {
    kukit.logDebug('onContextMenuClick');
    pd_itemOnContextMenu(node, e, this.menuId, null);
};

kukit.er.eventRegistry.register('pdlibContextMenu', 'click', kukit.pdlib.ContextMenuEvent, '__bind_click__', '__default_click__');

kukit.logDebug('CP context menu registered') */

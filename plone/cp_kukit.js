kukit.cr.makeSelectorCommand('cpSetupTarget', function(node) {
    plone_setUpSlotTarget(node);
    kukit.logDebug('CP target setup');
});

kukit.cr.makeSelectorCommand('cpSetupElement', function(node) {
    plone_setUpSlotElement(node);
    kukit.logDebug('CP element setup');
});

kukit.logDebug('CP commands registered')

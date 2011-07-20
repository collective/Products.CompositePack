# -*- coding: utf-8 -*-

"""
$Id$
"""

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.testing import z2


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.CompositePack
        self.loadZCML(package=Products.CompositePack)

        # Install product and call its initialize() function
        z2.installProduct(app, 'Products.kupu')
        z2.installProduct(app, 'Products.CompositePack')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'Products.CompositePack:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'Products.CompositePack')

    #def beforeTearDown(self):
        #self.composite_tool.clearLayoutRegistry()
        #self.composite_tool.clearViewletRegistry()


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='Products.CompositePack:Integration',
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='Products.CompositePack:Functional',
    )

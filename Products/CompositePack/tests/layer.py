# -*- coding: utf-8 -*-

"""
$Id: base.py 720 2011-06-20 19:23:35Z saiba $
"""

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import ptc
from Products.PloneTestCase import layer
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.CMFPlone.utils import getToolByName

from Products.CompositePack.config import get_ATCT_TYPES

import collective.testcaselayer.ptc

ptc.setupPloneSite()


class CompositePackLayerOLD(layer.PloneSite):
    """Configure Products.CompositePack"""

    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        import Products.CompositePack
        zcml.load_config('configure.zcml', Products.CompositePack)
        fiveconfigure.debug_mode = False
        ztc.installProduct('kupu')
        ztc.installProduct('CompositePage')
        ztc.installProduct('CompositePack')

    @classmethod
    def tearDown(cls):
        pass


class SimpleIntegrationTestLayer(collective.testcaselayer.ptc.BasePTCLayer):

    def afterSetUp(self):
        self.addProduct('kupu')

SimpleLayer = SimpleIntegrationTestLayer([collective.testcaselayer.ptc.ptc_layer])


class IntegrationTestLayer(collective.testcaselayer.ptc.BasePTCLayer):

    def afterSetUp(self):
        # Install the CompositePack product
        self.addProduct('kupu')
        #self.addProduct('CompositePack')
        self.addProfile('Products.CompositePack:default')

        self.composite_tool = getToolByName(self.portal, 'composite_tool')
        self.FILE_TYPE = get_ATCT_TYPES(self.portal)['File']
        self.EVENT_TYPE = get_ATCT_TYPES(self.portal)['Event']

    #def beforeTearDown(self):
        #self.composite_tool.clearLayoutRegistry()
        #self.composite_tool.clearViewletRegistry()

CompositePackLayer = IntegrationTestLayer([collective.testcaselayer.ptc.ptc_layer])

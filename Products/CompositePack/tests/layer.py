# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2004-2011 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################

"""
$Id: base.py 720 2011-06-20 19:23:35Z saiba $
"""

from Products.PloneTestCase import ptc
import collective.testcaselayer.ptc

from Products.CMFPlone.utils import getToolByName
from Products.CompositePack.config import get_ATCT_TYPES


ptc.setupPloneSite()


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

Layer = IntegrationTestLayer([collective.testcaselayer.ptc.ptc_layer])

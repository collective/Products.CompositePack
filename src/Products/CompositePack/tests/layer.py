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

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import ptc
from Products.PloneTestCase.layer import onsetup

import collective.testcaselayer.ptc

from Products.CMFPlone.utils import getToolByName
from Products.CompositePack.config import PROJECTNAME, get_ATCT_TYPES


@onsetup
def setup_product():
    """Set up the package and its dependencies.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """
    fiveconfigure.debug_mode = True
    import Products.CompositePack
    zcml.load_config('configure.zcml', Products.CompositePack)
    fiveconfigure.debug_mode = False

# initialize products outside of the deferred (@onsetup) method
ztc.installProduct(PROJECTNAME)

setup_product()
# TODO: kupu must be installed automatically as a dependency
ptc.setupPloneSite(products=['kupu'])


class IntegrationTestLayer(collective.testcaselayer.ptc.BasePTCLayer):

    def afterSetUp(self):
        # Install the CompositePack product
        self.addProfile('Products.CompositePack:default')

        self.composite_tool = getToolByName(self.portal, 'composite_tool')
        self.FILE_TYPE = get_ATCT_TYPES(self.portal)['File']
        self.EVENT_TYPE = get_ATCT_TYPES(self.portal)['Event']

    #def beforeTearDown(self):
        #self.composite_tool.clearLayoutRegistry()
        #self.composite_tool.clearViewletRegistry()

Layer = IntegrationTestLayer([collective.testcaselayer.ptc.ptc_layer])

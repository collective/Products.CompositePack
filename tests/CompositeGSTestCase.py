##############################################################################
#
# Copyright (c) 2004-2006 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""
$Id: CompositeGSTestCase.py 18879 2006-02-02 15:27:55Z jladage $
"""
# Load fixture
from Products.CompositePack.tests.CompositePackTestCase import *

class CompositeGSTestCase(CompositePackTestCase):

    def installCompositePack(self):
        self.loginAsPortalOwner()
        self.gs = self.portal.portal_setup
        self.gs.setImportContext('profile-CompositePack:default')
        self.gs.runAllImportSteps()


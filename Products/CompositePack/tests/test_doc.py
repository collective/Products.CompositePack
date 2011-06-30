##############################################################################
#
# Copyright (c) 2004-2006 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""
$Id$
"""

import os, sys

# Load fixture
from Products.PloneTestCase.ptc import PloneTestCase
from Testing.ZopeTestCase import ZopeDocFileSuite 

from Products.PloneTestCase.layer import ZCMLLayer

from Products.CompositePack.tests.layer import SimpleLayer

class CompositePackDocTestCase(PloneTestCase):

    layer = SimpleLayer


def test_suite():
   import unittest
   suite = unittest.TestSuite()
   suite.addTest(ZopeDocFileSuite('../doc/doc.txt', test_class=CompositePackDocTestCase))
   suite.layer = ZCMLLayer

   return suite

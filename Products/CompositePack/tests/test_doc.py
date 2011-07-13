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
$Id$
"""

import unittest

from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import ZCMLLayer
from Testing.ZopeTestCase import ZopeDocFileSuite


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(ZopeDocFileSuite('../doc/doc.txt',
                  test_class=PloneTestCase.PloneTestCase))
    suite.layer = ZCMLLayer
    return suite

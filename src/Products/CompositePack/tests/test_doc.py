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

import doctest
import unittest

from plone.testing import layered

from Products.CompositePack.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('../doc/doc.txt'), layer=FUNCTIONAL_TESTING),
        doctest.DocTestSuite(module='Products.CompositePack'),
    ])
    return suite

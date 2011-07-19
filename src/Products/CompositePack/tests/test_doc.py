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

import unittest2 as unittest
import doctest

from Products.PloneTestCase import PloneTestCase
from Testing import ZopeTestCase as ztc


def test_suite():
    return unittest.TestSuite([
        ztc.ZopeDocFileSuite(
            'doc/doc.txt', package='Products.CompositePack',
            test_class=PloneTestCase.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        ])

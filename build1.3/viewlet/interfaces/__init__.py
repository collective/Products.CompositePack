##############################################################################
#
# Copyright (c) 2004-2006 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""Viewlet and layout interfaces.

$Id$
"""
from Interface import Interface
from Interface.Attribute import Attribute

class ILayout(Interface):
    """Interface of Layouts that can be applied to an object.
    """

    def __call__():
        """Returns the template associated with the layout.
        """

class IViewlet(Interface):
    """Interface of Viewlets that can be applied to an object.
    """

    def __call__():
        """Returns the template associated with the viewlet.
        """

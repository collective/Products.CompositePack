##############################################################################
#
# Copyright (c) 2004 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""Viewlet and layout interfaces.

$Id: __init__.py,v 1.3 2004/08/25 17:02:03 godchap Exp $
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

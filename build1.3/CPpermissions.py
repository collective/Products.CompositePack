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
from Products.CMFCore.CMFCorePermissions import setDefaultRoles

DesignCompo = 'Design Composite Page'
setDefaultRoles(DesignCompo, ('Manager',))

ManageCompositePack = 'Manage Composite Pack'
setDefaultRoles(ManageCompositePack, ('Manager',))


##############################################################################
#
# Copyright (c) 2004-2006 CompositePack Contributors. All rights reserved.
#
# This software is distributed under the terms of the Zope Public
# License (ZPL) v2.1. See COPYING.txt for more information.
#
##############################################################################
"""
$Id: exceptions.py 11303 2005-08-23 16:38:33Z godchap $
"""
# Patch CompositePage so that error messages have an appropriate
# class. This lets us suppress the display for anonymous users.
import Products.CompositePage.slot

error_tag = '''<span class="slot_error">%s
(<a href="%s" onmousedown="document.location=this.href">log</a>)</span>'''
Products.CompositePage.slot.error_tag = error_tag

# -*- coding: utf-8 -*-

"""
$Id: base.py 720 2011-06-20 19:23:35Z saiba $
"""

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import ptc
from Products.PloneTestCase import layer
from Products.Five import zcml
from Products.Five import fiveconfigure

ptc.setupPloneSite(
    #extension_profiles=('Products.CompositePack:default', ),
    products=['kupu', 'CompositePack'],
    )


class CompositePackLayer(layer.PloneSite):
    """Configure Products.CompositePack"""

    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        import Products.CompositePack
        zcml.load_config('configure.zcml', Products.CompositePack)
        fiveconfigure.debug_mode = False
        ztc.installProduct('kupu')
        ztc.installProduct('CompositePage')
        ztc.installProduct('CompositePack')

    @classmethod
    def tearDown(cls):
        pass

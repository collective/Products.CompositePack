import os, sys
if __name__ == '__main__':
   execfile(os.path.join(sys.path[0], 'framework.py'))

# Load fixture
from Products.CompositePack.tests import CompositePackTestCase

from Products.PloneTestCase import PloneTestCase
from Testing.ZopeTestCase import ZopeDocFileSuite 

def test_suite():
   import unittest
   suite = unittest.TestSuite()
   suite.addTest(ZopeDocFileSuite('../doc/doc.txt', test_class=PloneTestCase.PloneTestCase))
   return suite

if __name__ == '__main__':
   framework()


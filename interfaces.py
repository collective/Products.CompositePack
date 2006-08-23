from zope.interface import Interface
from zope.interface import Attribute

#
#   Composite tool interface
#
class ICompositeTool(Interface):
    """ Manage composite properties of the site as a whole.
    """
    id = Attribute('id', 'Must be set to "composite_tool"')


class IPackComposite(Interface):
    pass

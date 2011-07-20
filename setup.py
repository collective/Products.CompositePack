# -*- coding: utf-8 -*-

"""
$Id$
"""

from setuptools import setup, find_packages
import os

version = '2.0dev'

setup(name='Products.CompositePack',
      version=version,
      description='CompositePack product',
      long_description=open("README.txt").read() + "\n\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Topic :: Software Development",
        ],
      keywords='web application server zope zope2 cmf plone',
      author="Godefroid Chappelle",
      author_email="gotcha@bubblenet.be",
      url="http://pypi.python.org/pypi/Products.CompositePack",
      license="ZPL 2.1 (http://www.zope.org/Resources/License/ZPL-2.1)",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'Products.kupu',
        'Products.CompositePage',
        ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

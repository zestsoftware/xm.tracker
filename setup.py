from setuptools import setup, find_packages
import os

versionfile = open(os.path.join('xm', 'tracker', 'version.txt'))
version = versionfile.read().strip()
versionfile.close()

setup(name='xm.tracker',
      version=version,
      description="This package provides a time tracker based on the concepts of gtimelog",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='xm timetracker',
      author='Jean-Paul Ladage',
      author_email='j.ladage@zestsoftware.nl',
      url='https://svn.plone.org/svn/collective/xm.timetracker',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['xm'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'egenix-mx-base',
          'kss.plugin.timer',
          'kss.plugin.cns',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

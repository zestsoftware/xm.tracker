from setuptools import setup, find_packages
import os.path

history = open('CHANGES.rst').read().strip()
readme = open('README.txt').read().strip()
install = open(os.path.join('docs', 'INSTALL.txt')).read().strip()

long_description = readme + '\n\n' + history + '\n\n' + install

setup(name='xm.tracker',
      version='1.0.6',
      description="A time tracker based on the concepts of gtimelog",
      long_description=long_description,
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords='xm timetracker',
      author='Jean-Paul Ladage',
      author_email='j.ladage@zestsoftware.nl',
      url='https://plone.org/products/extreme-management-tool/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['xm'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'kss.plugin.timer',
          'egenix-mx-base',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

from setuptools import setup, find_packages
import os


def read_package_file(filename):
    file = open(os.path.join('xm', 'tracker', filename))
    text = file.read().strip()
    file.close()
    return text


version = read_package_file('version.txt')
history = read_package_file('HISTORY.txt')

readmefile = open('README.txt')
readme = readmefile.read().strip()
readmefile.close()

installfile = open(os.path.join('docs', 'INSTALL.txt'))
install = installfile.read().strip()
installfile.close()

long_description = readme + '\n\n' + history + '\n\n' + install

setup(name='xm.tracker',
      version=version,
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
      url='https://svn.plone.org/svn/collective/xm.timetracker',
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
      # -*- Entry points: -*-
      """,
      )

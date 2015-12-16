#!/usr/bin/env python
from distutils.core import setup
import textwrap


setup(
    name='GraphiteSpark',
    version='0.3',
    description='graphitespark',
    author='Danny Lawrence',
    author_email='dannyla@linux.com',
    url='http://www.github.com/daniellawrence/graphite-spark',
    package_dir={'': 'src'},
    packages=[''],
    license="GPL",
    scripts=['bin/graphitespark'],
    classifiers=textwrap.dedent("""
    Development Status :: 5 - Production/Stable
    Intended Audience :: Developers
    License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)
    Operating System :: OS Independent
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.3
    Programming Language :: Python :: 3.4
    Programming Language :: Python :: 3.5
    Topic :: Software Development :: Libraries :: Python Modules
    Topic :: System :: Archiving :: Packaging
    Topic :: System :: Systems Administration
    Topic :: Utilities
    """).strip().splitlines(),
)

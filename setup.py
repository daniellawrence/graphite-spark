#!/usr/bin/env python

from distutils.core import setup

setup(
    name='GraphiteSpark',
    version='0.2',
    description='graphitespark',
    author='Danny Lawrence',
    author_email='dannyla@linux.com',
    url='http://www.github.com/daniellawrence/graphite-spark',
    package_dir={'': 'src'},
    packages=[''],
    scripts=['bin/graphitespark']
)

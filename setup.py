#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='tenant2tenant',
    version='latest',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo priod de>',
    packages=['tenant2tenant'],
    license='GPLv3',
    description='HIS microservice to handle tenant-to-tenant messages.')

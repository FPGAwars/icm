# -*- coding: utf-8 -*-

from setuptools import setup

from icm import (__version__, __title__, __description__, __url__,
                 __author__, __email__, __license__)


setup(
    name=__title__,
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__email__,
    url=__url__,
    license=__license__,
    packages=['icm'],
    package_data={
        'icm': ['commands/*.py']
    },
    install_requires=[
        'click>=6,<7',
        'colorama'
    ],
    entry_points={
        'console_scripts': ['icm=icm.__main__:cli']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python']
)

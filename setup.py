#!/usr/bin/env python

from distutils.core import setup

setup(
    name="simplemysql",
    version=0.1,
    description="An ultra simple wrapper for Python MySQLdb with very basic functionality",
    author="Kailash Nadh",
    url="http://nadh.in/code/simplemysql",
    packages=['simplemysql'],
    download_url="http://github.com/knadh/simplemysql",
    license="GPLv2",
    classifiers=[
        "Development Status :: 0.1 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Internet"
    ],
    install_requires=["mysql-python"]
)

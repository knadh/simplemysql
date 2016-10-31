#!/usr/bin/env python

from setuptools import setup

setup(
	name="simplemysql",
	version="1.02",
	description="An ultra simple wrapper for Python MySQLdb with very basic functionality",
	author="Kailash Nadh",
	author_email="kailash.nadh@gmail.com",
	url="http://nadh.in/code/simplemysql",
	packages=['simplemysql'],
	download_url="http://github.com/knadh/simplemysql",
	license="GPLv2",
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"Programming Language :: Python",
		"Natural Language :: English",
		"License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Topic :: Database",
		"Topic :: Software Development :: Libraries"
	],
	install_requires=["mysql-python"]
)

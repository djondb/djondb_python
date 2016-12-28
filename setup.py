#!/usr/bin/env python

"""
setup.py file for djondb python driver 
"""

from distutils.core import setup, Extension

setup (name = 'pydjondb',
		version = '3.5.612280',
		author      = "Cross",
		author_email = "cross@djondb.com",
		license = "GPL",
		description = """Python driver for djondb""",
		packages = ["pydjondb"],
		url = "http://djondb.com",
		classifiers= [
			"License :: Public Domain",
			"Topic :: Database",
			"Intended Audience :: Developers",
			"Topic :: Software Development"
			]
		)

#!/usr/bin/env python

"""
setup.py file for djondb python driver 
"""

from distutils.core import setup, Extension

pydjondb_module = Extension('_pydjondb',
		sources=['djonpythondriver.cpp'],
		include_dirs=['includes'],
		libraries=['djon-client']
		)

setup (name = 'pydjondb',
		version = '3.5.60324',
		author      = "Cross",
		author_email = "cross@djondb.com",
		license = "GPL",
		description = """Python driver for djondb""",
		ext_modules = [pydjondb_module],
		py_modules = ["pydjondb"],
		url = "http://djondb.com",
		classifiers= [
			"License :: Public Domain",
			"Topic :: Database",
			"Intended Audience :: Developers",
			"Topic :: Software Development"
			]
		)

#!/usr/bin/env python

from distutils.core import setup

setup(name="reSTEd",
      version="0.0.1",
      description="reStructuredTextEditor",
      author="Jon Dawson",
      author_amail="chips@jondawson.org.uk",
      url="http://github.com/dawsonjon/reSTEd",
      py_modules=["docwin"],
      scripts=["rested.py"],
      requires=["wx", "docutils"],
      )

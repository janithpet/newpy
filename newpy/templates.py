import datetime

templates = [
	{
		"type": "normal",
		"name": ".env",
		"location": ".",
		"content": ""
	},
	{
		"type": "normal",
		"name": ".gitignore",
		"location": ".",
		"content":
		"""#Custom
.vscode/**
.env
Pipfile.lock
dist/*
scratch.py
#Boilerplate
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/k:v f
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/
		"""
	},
	{
		"type": "normal",
		"name": ".pre-commit-config.yaml",
		"location": ".",
		"content":
		"""# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
	rev: v3.2.0
	hooks:
	-   id: trailing-whitespace
	-   id: end-of-file-fixer
	-   id: check-yaml
	-   id: check-added-large-files
-   repo: https://github.com/pycqa/isort
	rev: 5.8.0
	hooks:
	- id: isort
		name: isort (python)
	- id: isort
		name: isort (cython)
		types: [cython]
	- id: isort
		name: isort (pyi)
		types: [pyi]
				"""
		},
		{
			"type": "normal",
			"name": "logging_config.ini",
			"location": ".",
			"content":
			"""[loggers]
keys=root

[handlers]
keys=stream_handler

[formatters]
keys=formatter

[logger_root]
level=DEBUG
handlers=stream_handler

[handler_stream_handler]
class=StreamHandler
level=DEBUG
formatter=formatter
args=(sys.stdout,)

[formatter_formatter]
format=%(levelname) -20s %(module)-20s %(process) -6d %(lineno)-5d %(asctime)-10s %(message)-100s
datefmt=%H:%M:%S
class=PROJECT_NAME.ColoredFormatter
			"""
		},
		{	"type": "conditional",
			"condition": "venv",
			"true": {
				"type": "case",
				"condition": "manager",
				"pipenv": {
					"type": "normal",
					"name": "Pipfile",
					"location": ".",
					"content":
					""""""
					},
				"pip": {
					"type": "normal",
					"name": "requirements.txt",
					"location": ".",
					"content":
					""""""
					}
				},
			"false": None,
		},
		{
			"type": "case",
			"condition": "license",
			"mit": {
				"type": "normal",
				"name": "LICENSE",
				"location": ".",
				"content":
				f"""MIT License

Copyright (c) {datetime.datetime.now().year} AUTHOR

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
				"""
				},
				"unlicense": {
					"type": "normal",
					"name": "LICENSE",
					"location": ".",
					"content":
					f"""This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
					"""
					},
				"boost": {
					"type": "normal",
					"name": "LICENSE",
					"location": ".",
					"content":
					f"""Boost Software License - Version 1.0 - August 17th, 2003

Permission is hereby granted, free of charge, to any person or organization
obtaining a copy of the software and accompanying documentation covered by
this license (the "Software") to use, reproduce, display, distribute,
execute, and transmit the Software, and to prepare derivative works of the
Software, and to permit third-parties to whom the Software is furnished to
do so, all subject to the following:

The copyright notices in the Software and this entire statement, including
the above license grant, this restriction and the following disclaimer,
must be included in all copies of the Software, in whole or in part, and
all derivative works of the Software, unless such copies or derivative
works are solely in the form of machine-executable object code generated by
a source language processor.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
					"""
					},
		},
		{
			"type": "normal",
			"name": "pyproject.toml",
			"location": ".",
			"content": """[build-system]
requires = ["setuptools >= 40.6.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.isort]
profile = "google"
src_paths = ["PROJECT_NAME"]
"""
		},
		{
			"type": "normal",
			"name": "README.md",
			"location": ".",
			"content": """"""
		},
		{
			"type": "normal",
			"name": "setup.cfg",
			"location": ".",
			"content":
			"""# This file is used to configure your project.
# Read more about the various options under:
# http://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files

[metadata]
name = PROJECT_NAME
version = 0.0.1
description = PROJECT_NAME
author = AUTHOR
long-description = file: README.md
long-description-content-type = text/markdown; charset=UTF-8; variant=GFM

[options]
packages = find:

# Add here dependencies of your project (semicolon/line-separated), e.g.
install_requires =
    pre-commit==2.12.1
    isort==5.8.0
    humanfriendly==9.2

# Require a specific Python version, e.g. Python 2.7 or >= 3.4
python_requires = ~=3.8

[options.extras_require]
# Add here additional requirements for extra features, to install with:
# `pip install PROJECT_NAME[test]` like:
# PDF = ReportLab; RXP
# Add here test requirements (semicolon/line-separated)
test =
    pytest
    pytest-xdist

[flake8]
max-line-length = 240
ignore = E111,E114
extend-ignore =
    # Ignore indentation of four errors
    E111

exclude =
    # No need to traverse our git directory
    .git,
    # There's no value in checking cache directories
    __pycache__,
    # The conf file is mostly autogenerated, ignore it
    docs/conf.py,
    # The old directory contains Flake8 2.0
    old,
    # This contains our built documentation
    build,
    # This contains builds of flake8 that we don't want to check
    dist,
    .pytype"""
		},
		{
			"type": "normal",
			"name":"setup.py",
			"location": ".",
			"content": """import setuptools

if __name__ == "__main__":
  setuptools.setup()
"""
		},
		{
			"type": "normal",
			"name": "__init__.py",
			"location": "./PROJECT_NAME/",
			"content": """import logging
import logging.config
import os
import pathlib

from PROJECT_NAME.loggers import ColoredFormatter

logging.config.fileConfig(str(pathlib.Path(__file__).parent.parent.resolve()) + "/logging_config.ini")
logger = logging.getLogger()
"""
		},
		{
			"type": "normal",
			"name": "__init__.py",
			"location": "./PROJECT_NAME/loggers/",
			"content": """from PROJECT_NAME.loggers.colored_formatter import ColoredFormatter"""
		},
		{
			"type": "normal",
			"name": "colored_formatter.py",
			"location": "./PROJECT_NAME/loggers",
			"content": """import logging

from humanfriendly.terminal import ansi_wrap


class ColoredFormatter(logging.Formatter):
	FORMATS = {
		logging.DEBUG: {"color": "green", "bold": True},
		logging.ERROR: {"color": "red", "bold": True},
		logging.WARNING: {"color": "yellow", "bold": True},
		logging.CRITICAL: {"color": "magenta", "bright": True, "bold": True},
		logging.INFO: {"color": "white", "bold": True}
	}

	def __init__(self, fmt, datefmt, *args, **kwargs):
		super().__init__(fmt, datefmt, *args, **kwargs)
		self.fmt = fmt

	def format(self, record):
		record.levelname = ansi_wrap(record.levelname, **self.FORMATS[record.levelno])
		record.msg = ansi_wrap(str(record.msg), **self.FORMATS[record.levelno])
		return super().format(record)
"""
		}

]

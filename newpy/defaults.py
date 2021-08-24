import pathlib
import pickle

files = [
	{
		"name": ".env",
		"location": ".",
		"content": ""
	},
	{
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
		{
			"name": "Pipfile",
			"location": ".",
			"content":
			""""""
		},
		{
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
			"name": "README.md",
			"location": ".",
			"content": """"""
		},
		{
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
			"name":"setup.py",
			"location": ".",
			"content": """import setuptools

if __name__ == "__main__":
  setuptools.setup()
"""
		},
		{
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
			"name": "__init__.py",
			"location": "./PROJECT_NAME/loggers/",
			"content": """from PROJECT_NAME.loggers.colored_formatter import ColoredFormatter"""
		},
		{
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
# with open(str(pathlib.Path(__file__).parent.resolve()) + "/default.pickle", "wb") as f:
# 	pickle.dump(files, f)

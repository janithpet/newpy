# newpy
Creates a new python package. It uses [pipenv](https://pipenv.pypa.io/en/latest/) to manage the virtual environment.

## Installation

Install by running `pip install .` in the root folder.

## Running, and options

Run using `newpy <project name>`.

The following options are available:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --author, -a: Specify the name of the author, and save as the default author

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --author-tmp, -t: Specify that the author name will not save as the default author

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --manager, -m: Specify the python package manager (and virtual environment). Currently supports `pip` or `pipenv`. If `pip` is chosen, the virtual environment will be created using `virtualenv`.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --venv, -v: Creates a virtual environment using the default manager.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --install, -i: Install the new project. If --venv is set, this will be installed in the virtual environment that is created.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --git, -g: Initialises git if this flag is set

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --precommit, -p: Install [pre-commit](https://pre-commit.com/) hooks if this flag is set. This requires the --git flag.

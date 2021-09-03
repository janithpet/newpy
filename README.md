# newpy
Creates a new python package. It uses [pipenv](https://pipenv.pypa.io/en/latest/) to manage the virtual environment.

## Installation

Install by running `pip install .` in the root folder.

## Running, and options

Run using `newpy <project name>`.

The following options are available:

| Option 	| Description 	|
|:---:	|:---:	|
| --author, -a 	| Specify the name of the author, and save as the default author 	|
| --author-tmp, -t 	| [Flag] Specify that the author name will not save as the default author 	|
| --manager, -m 	| Specify the python package manager (and virtual environment). Currently supports `pip` or `pipenv`. If `pip` is chosen, the virtual environment will be created using `virtualenv`. 	|
| --venv, -v 	| [Flag] Creates a virtual environment using the default manager. 	|
| -install, -i 	| [Flag] Install the new project. If --venv is set, this will be installed in the virtual environment that is created. 	|
| --git, -g 	| [Flag] Initialises git if this flag is set 	|
| --precommit, -p 	| [Flag] Install [pre-commit](https://pre-commit.com/) hooks if this flag is set. This requires the --git flag. 	|

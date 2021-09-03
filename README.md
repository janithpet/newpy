# newpy
Creates a new python package.
## Installation

Install by running `pip install .` in the root folder.

## Running, and options

Run using `newpy <project name>`.

The following options are available:
| Option 	| Description 	|
|:---:	|---	|
| --author, -a 	| Specify the name of the author, and save as the default author 	|
| --author-tmp, -t 	| [Flag] Specify that the author name will not save as the default author 	|
| --license, -l 	| Specify the license, and save as the default license. Currently supports `mit`, `unlicense` and `boost` 	|
| --license-tmp, -k 	| [Flag] Specify that the license will not be set as default 	|
| --manager, -m 	| Specify the python package manager (and virtual environment). Currently supports `pip` or `pipenv`. If `pip` is chosen, the virtual environment will be created using `virtualenv`. 	|
| --venv, -v 	| [Flag] Creates a virtual environment using the default manager. 	|
| -install, -i 	| [Flag] Install the new project. If --venv is set, this will be installed in the virtual environment that is created. 	|
| --git, -g 	| [Flag] Initialises git if this flag is set 	|
| --precommit, -p 	| [Flag] Install [pre-commit](https://pre-commit.com/) hooks if this flag is set. This requires the --git flag. 	|

The first time `newpy` is run, it will ask for a default name and package manager; these will be stored for future use.

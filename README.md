# newpy
Creates a new python package.

## Installation

Install by running `pip install .` in the root folder.

## Running, and options

Run using `newpy <project name>`.

When run for the first time, you will be asked to set the default author, python manager (`pip` or `pipenv`), and license (`mit`, `unlicense` and `boost`). 

The default values can be changed to using the options below. 

The following options are available:
| Option 	| Description 	|
|:---:	|---	|
| --author, -a 	| Specify the name of the author, and save as the default author 	|
| --author-tmp, -t 	| [Flag] Specify that the author name will not save as the default author 	|
| --license, -l 	| Specify the license, and save as the default license. Currently supports `mit`, `unlicense` and `boost` 	|
| --license-tmp, -k 	| [Flag] Specify that the license will not be set as default 	|
| --manager, -m 	| Specify the python package manager (and virtual environment). Currently supports `pip` or `pipenv`. If `pip` is chosen, the virtual environment will be created using `virtualenv`. 	|
| --venv, -v 	| [Flag] Creates a virtual environment using the default manager. 	|
| --install, -i 	| [Flag] Install the new project. If --venv is set, this will be installed in the virtual environment that is created. 	|
| --git, -g 	| [Flag] Initialises git if this flag is set 	|
| --precommit, -p 	| [Flag] Install [pre-commit](https://pre-commit.com/) hooks if this flag is set. This requires the --git flag. 	|

### Example 
Suppose you run:

`newpy hello_world -vipg -at 'Random Author' -m pipenv`

This will:

 - Create a project `hello_world`,
 - Set the default manager to `pipenv`,
 - Create a virtual environment,
 - Install the current project in this virtual environment,
 - Create and install pre-commit hooks,
 - Initialise git, and
 - Temporarily set the author to `Random Author`; i.e. it won't override the default author.


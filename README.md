# newpy
Creates a new python package. It uses [pipenv](https://pipenv.pypa.io/en/latest/) to manage the virtual environment.

## Installation

Install by running `pip install .` in the root folder.

## Running, and options

Run using `newpy <project name>`.

The following options are available:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --author, -a: Specify the name of the author

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --git, -g: Initialises git if this flag is set

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --precommit, -p: Install [pre-commit](https://pre-commit.com/) hooks if this flag is set


### Default Author

Note that the default author is set to my name. This can be changed by replacing ADD NEW DEFAULT NAME HERE in the following bit of code in `newpy/newpy.py`:

```
{
	"name": ["--author", "-a"],
	"dest": "author",
	"default": "<ADD NEW DEFAULT NAME HERE>",
	"help": "The name of the author of the project"
}
```

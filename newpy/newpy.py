import argparse
import os
import pathlib
import pickle
import subprocess

from newpy import logger
from newpy.templates import templates

parser = argparse.ArgumentParser()

arguments = [
	{
        "name": ["project_name"],
        "type": str,
        "help": "The name of the new python project"
    },
    {
        "name": ["--author", "-a"],
        "dest": "author",
        "default": "Janith Petangoda",
        "help": "The name of the author of the project"
    },
	{
        "name": ["--git", "-g"],
        "dest": "git",
		"action": "store_const",
		"const": True,
        "default": False,
        "help": "Initialise git"
    },
	{
        "name": ["--precommit", "-p"],
        "dest": "precommit",
		"action": "store_const",
		"const": True,
        "default": False,
        "help": "Install pre-commit hooks"
    },
]

[parser.add_argument(*argument["name"], **{k:v for k, v in argument.items() if k != "name"}) for argument in arguments]

arguments = parser.parse_args()

def main():
	project_path = f"{os.getcwd()}/{arguments.project_name}"

	logger.info(f"Creating project {project_path}")
	try:
		os.mkdir(f"./{arguments.project_name}")
	except FileExistsError:
		pass
	os.chdir(project_path)

	for file in templates:
		for key in file.keys():
			file[key] = file[key].replace("PROJECT_NAME", arguments.project_name)
			file[key] = file[key].replace("AUTHOR", arguments.author)
			file[key] = file[key].replace("PROJECT_PATH", project_path)

		assert os.getcwd() == project_path
		try:
			os.makedirs(file["location"])
		except FileExistsError:
			pass
		os.chdir(file["location"])

		logger.debug(f"Saving {file['name']} at {file['location']}")
		with open(file["name"], "w") as f:
			f.write(file["content"])
		os.chdir(project_path)

	assert os.getcwd() == project_path

	logger.info("Installing pipenv libraries, including current project")
	subprocess.run(["pipenv install"], shell=True)
	subprocess.run(["pipenv install -e ."], shell=True)

	if arguments.precommit:
		logger.info("Installing pre-commit hooks")
		subprocess.run(["bash", "-c", "source $(pipenv --venv)/bin/activate && pre-commit install && exit"])

	if arguments.git:
		logger.info("Initialising git")
		subprocess.run(["git init"], shell=True)
		subprocess.run(["git add ."], shell=True)
		subprocess.run(["git commit -am 'first commit'"], shell=True)

import argparse
from functools import partial
import json
import os
import pathlib
import subprocess
from typing import Dict

from newpy import logger
from newpy.storage import Storage
from newpy.templates import templates
from newpy.utilities import retrieve

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
        "default": None,
        "help": "Set name of the author of the project"
    },
	{
		"name": ["--author-tmp", "-t"],
		"dest": "author_tmp",
		"action": "store_true",
		"help": "Set name of the author of the project temporarily"
	},
	{
		"name": ["--license", "-l"],
		"dest": "license",
		"default": None,
        "help": "Set LICENSE of the project; currently supports the MIT License, Unlicensed and the Boost Software License 1.0"
	},
	{
		"name": ["--license-tmp", "-k"],
		"dest": "license_tmp",
		"action": "store_true",
		"help": "Set LICENSE of the project temporarily"
	},
	{
        "name": ["--create-venv", "-v"],
        "dest": "venv",
		"action": "store_const",
		"const": True,
        "default": False,
        "help": "Install in local environment"
    },
	{
        "name": ["--install", "-i"],
        "dest": "install",
		"action": "store_const",
		"const": True,
        "default": False,
        "help": "Install in local environment"
    },
	{
        "name": ["--manager", "-m"],
        "dest": "manager",
		"default": None,
        "help": "Name of the python package manager. Usually pip or pipenv"
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

retrieve_author = partial(retrieve, arg="author", tmp=True)
retrieve_manager = partial(retrieve, arg="manager", tmp=False)
retrieve_license = partial(retrieve, arg="license", tmp=True)

def update_template(d: Dict, project_name, author, project_path):
	for key in d.keys():
		d[key] = d[key].replace("PROJECT_NAME", project_name)
		d[key] = d[key].replace("AUTHOR", author)
		d[key] = d[key].replace("PROJECT_PATH", project_path)
	return d


def operate_on_file(file: Dict, project_name, author, project_path, locals):
	if file is None:
		return None
	elif file["type"] == "case":
		file = file[locals[file["condition"]]]
		return operate_on_file(file, project_name=project_name, author=author, project_path=project_path, locals=locals)
	elif file["type"] == "conditional":
		if locals[file["condition"]]:
			file = file["true"]
		else:
			file = file["false"]
		return operate_on_file(file, project_name=project_name, author=author, project_path=project_path, locals=locals)

	file = update_template(file, project_name=project_name, author=author, project_path=project_path)

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


def main():
	storage: Storage = Storage.from_json(str(pathlib.Path(__file__).parent.resolve()) + "/storage/storage.json")
	author = retrieve_author(arguments, storage)
	logger.debug(f"Author is set to {author}")

	manager = retrieve_manager(arguments, storage)
	logger.debug(f"Manager is set to {manager}")

	license = retrieve_license(arguments, storage)
	logger.debug(f"License is set to {license}")
	venv = arguments.venv




	project_path = f"{os.getcwd()}/{arguments.project_name}"

	logger.info(f"Creating project {project_path}")
	try:
		os.mkdir(f"./{arguments.project_name}")
	except FileExistsError:
		pass
	os.chdir(project_path)

	for file in templates:
		operate_on_file(file, project_name=arguments.project_name, author=author, project_path=project_path, locals=locals())

	assert os.getcwd() == project_path


	if arguments.venv:
		logger.info(f"Installing virtual environment")
		if manager == "pipenv":
			subprocess.run(["pipenv install"], shell=True)
		elif manager == "pip":
			subprocess.run(["virtualenv .venv"], shell=True)

	if arguments.install:
		logger.info(f"Installing {manager} current project")

		if arguments.venv:
			if manager == "pipenv":
				subprocess.run(["bash", "-c", "source $(pipenv --venv)/bin/activate && pipenv install -e . && exit"])
			elif manager == "pip":
				subprocess.run(["bash", "-c", "source .venv/bin/activate && pip install -e . && exit"])
		else:
			subprocess.run([f"{manager} install -e ."], shell=True)

	if arguments.git:
		logger.info("Initialising git")
		subprocess.run(["git init"], shell=True)
		subprocess.run(["git add ."], shell=True)
		subprocess.run(["git commit -am 'first commit'"], shell=True)

		if arguments.precommit:
			logger.info("Installing pre-commit hooks")
			if manager == "pipenv":
				subprocess.run(["bash", "-c", "source $(pipenv --venv)/bin/activate && pre-commit install && exit"])
			elif manager == "pip":
				subprocess.run(["bash", "-c", "source .venv/bin/activate && pre-commit install && exit"])

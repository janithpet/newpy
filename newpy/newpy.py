import argparse
import os
import pathlib
import pickle
import subprocess

from newpy import logger

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
        "help": "Name of the author of the project"
    },
	{
        "name": ["--git", "-g"],
        "dest": "git",
		"action": "store_const",
		"const": True,
        "default": False,
        "help": "Name of the author of the project"
    },
	{
        "name": ["--precommit", "-p"],
        "dest": "precommit",
		"action": "store_const",
		"const": True,
        "default": False,
        "help": "Name of the author of the project"
    },
]

[parser.add_argument(*argument["name"], **{k:v for k, v in argument.items() if k != "name"}) for argument in arguments]

arguments = parser.parse_args()

def main():
	logger.debug("Loading files")

	with open(str(pathlib.Path(__file__).parent.resolve()) + "/default.pickle", "rb") as f:
		files = pickle.load(f)

	logger.debug("Adjusting files for current project")

	project_path = f"{os.getcwd()}/{arguments.project_name}"

	for file in files:
		for key, value in file.items():
			file[key] = file[key].replace("PROJECT_NAME", arguments.project_name)
			file[key] = file[key].replace("AUTHOR", arguments.author)
			file[key] = file[key].replace("PROJECT_PATH", project_path)

	logger.debug("Creating project folder")
	try:
		os.mkdir(f"./{arguments.project_name}")
	except FileExistsError:
		pass
	os.chdir(project_path)

	logger.debug("Creating files")

	for file in files:
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

	logger.debug("Installing pipenv libraries, including current project")
	subprocess.run(["pipenv install"], shell=True)
	subprocess.run(["pipenv install -e ."], shell=True)


	if arguments.precommit:
		logger.debug("Installing pre-commit hooks")
		subprocess.run(["bash", "-c", "source $(pipenv --venv)/bin/activate && pre-commit install && exit"])

	if arguments.git:
		logger.debug("Initialising git")
		subprocess.run(["git init"], shell=True)
		subprocess.run(["git add ."], shell=True)
		subprocess.run(["git commit -am 'first commit'"], shell=True)

	os.system("exit")

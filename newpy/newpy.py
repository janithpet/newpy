import argparse
from functools import partial
import os
import pathlib
import subprocess
from typing import Dict, Any

from newpy import logger
from newpy.storage import Storage
from newpy.templates import templates
from newpy.utilities import retrieve

parser = argparse.ArgumentParser()

arguments = [
    {
        "name": ["project_name"],
        "type": str,
        "nargs": "?",
        "default": None,
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
        "name": ["--venv_name"],
        "dest": "venv_name",
                "default": None,
        "help": "Name of virtual environment; for manager = venv or pyenv."
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

[parser.add_argument(*argument["name"], **{k: v for k, v in argument.items() if k != "name"}) for argument in arguments]

arguments = parser.parse_args()

retrieve_author = partial(retrieve, arg="author", tmp=True)
retrieve_manager = partial(retrieve, arg="manager", tmp=False)
retrieve_license = partial(retrieve, arg="license", tmp=True)

def handle_subprocess_result(result: subprocess.CompletedProcess, process_description: str, log_if_successful: bool = False) -> bool:
	if result is None:
		return

	if result.stderr != "":
		if result.returncode != 0:
			logger.error(f"Could not {process_description}")
			logger.error(f"{result.stderr.strip()}")
		else:
			logger.warning(f"Could not {process_description}")
			logger.warning(f"{result.stderr.strip()}")
	if result.stdout != "" and log_if_successful:
		if result.returncode == 0:
			logger.info(result.stdout.strip())


def update_template(d: Dict, project_name, author, project_path):
    for key in d.keys():
        d[key] = d[key].replace("PROJECT_NAME", project_name)
        d[key] = d[key].replace("AUTHOR", author)
        d[key] = d[key].replace("PROJECT_PATH", project_path)
    return d


def operate_on_file(file: Dict, project_name: str, author: str, project_path: str, locals: Dict[str, Any]):
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
    logger.info(f"Author is set to {author}")

    manager = retrieve_manager(arguments, storage)
    logger.info(f"Manager is set to {manager}")

    license = retrieve_license(arguments, storage)
    logger.info(f"License is set to {license}")

    venv = arguments.venv
    precommit = arguments.precommit

    current_dir_name = os.getcwd().split(os.path.sep)[-1]

    if arguments.project_name is not None:
        project_path = f"{os.getcwd()}/{arguments.project_name}"
        project_name = os.path.basename(project_path)

        assert project_name != "", "Please remove any trailing '/'."

        if os.path.exists(project_path):
            logger.error(f"{project_path} already exists")
            exit()
        logger.info(f"Creating project {project_path}")
        try:
            os.mkdir(project_path)
        except FileExistsError:
            pass
        os.chdir(project_path)

        for file in templates:
            operate_on_file(file, project_name=project_name, author=author, project_path=project_path, locals=locals())

        assert os.getcwd() == project_path

        if arguments.venv:
            result = None
            _venv_name = arguments.venv_name if arguments.venv_name else current_dir_name + "." + project_name

            logger.info(f"Installing virtual environment")
            if manager == "pipenv":
                result = subprocess.run(["pipenv install"], shell=True, capture_output=True, text=True)
            elif manager == "pip":
                # _venv_name = arguments.venv_name if arguments.venv_name else ".venv"
                result = subprocess.run([f"virtualenv {_venv_name}"], shell=True, capture_output=True, text=True)
            elif manager == "pyenv":
            # _venv_name = current_dir_name + "." + (arguments.venv_name if arguments.venv_name else project_name)
                result = subprocess.run([f"pyenv virtualenv {_venv_name};echo {_venv_name} > .python-version"], shell=True, capture_output=True, text=True)

            handle_subprocess_result(result, "create virtual environment")


        if arguments.install:
            result = None
            logger.info(f"Installing current project using {manager}")
            if arguments.venv:
                if manager == "pipenv":
                    result = subprocess.run(["bash", "-c", "source $(pipenv --venv)/bin/activate && pipenv install -e . && exit"], capture_output=True, text=True)
                elif manager == "pip":
                    _venv_name = arguments.venv_name if arguments.venv_name else ".venv"
                    result = subprocess.run(["bash", "-c", f"source {_venv_name}/bin/activate && pip install -e . && exit"], capture_output=True, text=True)
                elif manager == "pyenv":
                    result = subprocess.run(["pip install -e ."], shell=True, capture_output=True, text=True)
            # else:
            #     subprocess.run([f"{manager} install -e ."], shell=True, capture_output=True, text=True)
            handle_subprocess_result(result, "install project", False)

        if arguments.git:
            result = None
            logger.info("Initialising git")
            subprocess.run(["git init"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git add ."], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git commit -aqm 'first commit'"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if arguments.precommit:
                logger.info("Installing pre-commit hooks")
                if manager == "pipenv":
                    result = subprocess.run(["bash", "-c", "source $(pipenv --venv)/bin/activate && pre-commit install && exit"], capture_output=True, text=True)
                elif manager == "pip":
                    _venv_name = arguments.venv_name if arguments.venv_name else ".venv"
                    result = subprocess.run(["bash", "-c", f"source {_venv_name}/bin/activate && pre-commit install && exit"], capture_output=True, text=True)
                elif manager == "pyenv":
                    _venv_name = current_dir_name + "." + (arguments.venv_name if arguments.venv_name else project_name)
                    result = subprocess.run([f"pre-commit install"], shell=True, capture_output=True, text=True)

                handle_subprocess_result(result, "setup pre-commit")



    else:
        logger.error("Please enter a project_name")

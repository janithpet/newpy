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
            logger.info(f"Installing virtual environment")
            if manager == "pipenv":
                subprocess.run(["pipenv install"], shell=True)
            elif manager == "pip":
                _venv_name = arguments.venv_name if arguments.venv_name else ".venv"
                subprocess.run([f"virtualenv {_venv_name}"], shell=True)
            elif manager == "pyenv":
                _venv_name = current_dir_name + "." + (arguments.venv_name if arguments.venv_name else project_name)
                print(_venv_name)
                subprocess.run([f"pyenv virtualenv {_venv_name};echo {_venv_name} > .python-version"], shell=True)


        if arguments.install:
            logger.info(f"Installing current project using {manager}")
            if arguments.venv:
                if manager == "pipenv":
                    subprocess.run(["bash", "-c", "source $(pipenv --venv)/bin/activate && pipenv install -e . && exit"])
                elif manager == "pip":
                    _venv_name = arguments.venv_name if arguments.venv_name else ".venv"
                    subprocess.run(["bash", "-c", f"source {_venv_name}/bin/activate && pip install -e . && exit"])
                elif manager == "pyenv":
                    print(f"Cannot install project with pyenv. Please run\n\tcd {project_name}; pip install -e .")
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
                    _venv_name = arguments.venv_name if arguments.venv_name else ".venv"
                    subprocess.run(["bash", "-c", f"source {_venv_name}/bin/activate && pre-commit install && exit"])
                elif manager == "pyenv":
                    _venv_name = arguments.venv_name if arguments.venv_name else project_name
                    subprocess.run(["bash", "-c", f"pyenv activate {_venv_name}  && pre-commit install && exit"])

    else:
        logger.error("Please enter a project_name")

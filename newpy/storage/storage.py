from functools import partial
import json
import os
from pathlib import Path
from typing import Any, Callable

from newpy import logger


class Storage:
    def __init__(
        self,
        arguments: dict[str, str | None],
        store_f: Callable[[Any], None],
    ) -> None:
        self._arguments: list[str] = list(arguments.keys())
        self.update(arguments)

        self.store_f = store_f

    def store(self) -> None:
        data = {argument: getattr(self, argument) for argument in self._arguments}

        self.store_f(data)

    def update(self, arguments: dict[str, str | None], store: bool = False) -> None:
        assert all(
            [argument in self._arguments for argument in arguments]
        )  # TODO: Better error message here

        for key, value in arguments.items():
            setattr(self, key, value)

        if store:
            self.store()

    @classmethod
    def from_json(
        cls,
        file_name: Path,
        default: dict[str, str | None] = {
            "author": None,
            "manager": None,
            "license": None,
        },
    ) -> "Storage":
        if not os.path.exists(file_name):
            storage = default
        else:
            with open(file_name, "r+") as f:
                storage = json.load(f)
                assert (
                    type(storage) is dict
                ), f"{file_name} should resolve to a dictionary"

        store_f = partial(Storage._json_store, file_name=file_name)
        return cls(storage, store_f)

    @staticmethod
    def _json_store(data: Any, file_name: Path) -> None:
        with open(file_name, "w+") as f:
            json.dump(data, f)

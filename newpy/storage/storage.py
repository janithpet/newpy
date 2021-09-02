from functools import partial
import json
from typing import Any, Dict, List


class Storage:
	def __init__(self, arguments: Dict, details: Dict) -> None:
		self._arguments: List = list(arguments.keys())
		self.update(arguments)

		self.details = details

	def store(self):
		data = {argument: getattr(self, argument) for argument in self._arguments}

		self.details["store"](data)


	def update(self, arguments: Dict, store: bool = False) -> None:
		assert all([argument in self._arguments for argument in arguments]) #TODO: Better error message here

		for key, value in arguments.items():
			setattr(self, key, value)

		if store: self.store()

	@classmethod
	def from_json(cls, file_name: str) -> Any:
		with open(file_name, "r+") as f:
			storage = json.load(f)
			assert type(storage) is dict, f"{file_name} should resolve to a dictionary"

		details = {
			"type": "json",
			"store": partial(Storage._json_store, file_name=file_name)
		}
		obj = object.__new__(cls)
		obj.__init__(storage, details)

		return obj

	@staticmethod
	def _json_store(data, file_name):
		with open(file_name, "w+") as f:
			json.dump(data, f)

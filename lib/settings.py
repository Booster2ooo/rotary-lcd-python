#!/usr/bin/env python3
import os
import json
import logging
import collections
import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.absolute()

class Settings(collections.UserDict):

	def __init__(self, file_path = '../appsettings.json', mutable = False):
		self.initialized = False
		super().__init__()
		self.mutable = mutable
		self.file_path = ROOT_DIR / file_path
		try:
			with self.file_path.open('r') as file: self.update(json.load(file))
		except FileNotFoundError:
			logging.error('{} not found'.format(self.file_path))
		self.initialized = True

	def __setitem__(self, key, value):
		super().__setitem__(key,value)
		self.serialize()

	def __delitem__(self, key):
		super().__delitem__(key)
		self.serialize()
	
	def serialize(self):
		if self.initialized and self.mutable:
			new = self.file_path.with_suffix('.new.json')
			content = json.dumps(self.data, indent=2)
			with new.open('w') as file:
				file.write(content)
			os.replace(new, self.file_path)


if __name__ == '__main__':
	settings = Settings(mutable=True)
	print(settings)
	settings['new'] = 'test'
	del settings['new']
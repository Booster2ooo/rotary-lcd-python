#!/usr/bin/env python3
import logging.config
from logging import NOTSET
if __name__ == '__main__':
	from settings import Settings

initialized = False

class Logger(logging.getLoggerClass()):

	def __init__(self, name='application', level=NOTSET):
		super().__init__(name, level)

def getLogger(name='application', settings=None):
	if not initialized:
		if not settings:
			raise ValueError('No settings provided, you need to setup the custom logger first')
		else:
			setup(settings)
	return logging.getLogger(name)

def setup(settings):
	global initialized
	if not initialized and 'logging' in settings:
		logging.setLoggerClass(Logger)
		logging.config.dictConfig(settings['logging'])
		initialized = True


if __name__ == '__main__':
	settings = Settings()
	logger = getLogger(settings=settings)
	logger.info('test')
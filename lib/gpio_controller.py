#!/usr/bin/env python3
import RPi.GPIO as GPIO
if __name__ == '__main__':
	from settings import Settings
	from logger import getLogger

class GpioController:

	def __init__(self, settings, logger):
		self.settings = settings
		self.logger = logger
		self.GPIO = GPIO
		self.logger.debug('Initializing GPIO...')
		mode = getattr(self.GPIO, settings["pin_numbering_scheme"])
		self.logger.debug('Using GPIO mode {}'.format(mode))
		self.GPIO.setmode(mode)
		self.logger.debug('GPIO initialized.')

	def __del__(self):
		self.logger.debug('Destructing GPIO...')
		self.GPIO.cleanup()
		self.logger.debug('GPIO destructed.')


if __name__ == '__main__':
	settings = Settings()
	gpio_controller = GpioController(settings)
#!/usr/bin/env python3
from Adafruit_CharLCD import Adafruit_CharLCD
if __name__ == '__main__':
	from settings import Settings
	from logger import getLogger

class Lcd(Adafruit_CharLCD):
	
	def __init__(self, settings, logger):
		self.settings = settings
		self.logger = logger
		self.logger.debug('Initializing LCD...')
		self.reset = settings["lcd"]["pins"]["reset"]
		self.enable = settings["lcd"]["pins"]["enable"]
		self.data4 = settings["lcd"]["pins"]["data4"]
		self.data5 = settings["lcd"]["pins"]["data5"]
		self.data6 = settings["lcd"]["pins"]["data6"]
		self.data7 = settings["lcd"]["pins"]["data7"]
		self.backlight = settings["lcd"]["pins"]["backlight"]
		self.columns = settings["lcd"]["columns"]
		self.rows = settings["lcd"]["rows"]
		super().__init__(
			self.reset
		  , self.enable
		  , self.data4
		  , self.data5
		  , self.data6
		  , self.data7
		  , self.columns
		  , self.rows
		  , self.backlight
		  , False
		)
		self.clear()
		self.set_backlight(1)
		self.logger.debug('LCD initialized.')

	def __del__(self):
		self.logger.debug('Destructing LCD...')
		self.set_backlight(0)
		self.clear()
		self.logger.debug('LCD destructed.')

if __name__ == '__main__':
	# do some tests
	pass
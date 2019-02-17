#!/usr/bin/env python3
from lib.settings import Settings
from lib.logger import getLogger
from lib.gpio_controller import GpioController
from lib.rotary_encoder import RotaryEncoder
from lib.lcd import Lcd
from lib.rotary_display import RotaryDisplay
from time import sleep
import signal

settings = None
logger = None
gpio_controller = None
rotary_encoder = None
lcd = None
rotary_display = None

def release(signal_number = None, frame = None):
	global settings, logger, gpio_controller, rotary_encoder, lcd, rotary_display
	logger.debug('Releasing resources')
	del rotary_display
	del lcd
	del rotary_encoder
	del gpio_controller
	del settings
	del logger

if __name__ == "__main__":
	settings = Settings()
	logger = getLogger(settings=settings)
	gpio_controller = GpioController(settings, logger)
	rotary_encoder = RotaryEncoder(settings, logger, gpio_controller)
	lcd = Lcd(settings, logger)
	rotary_display = RotaryDisplay(settings, logger, rotary_encoder, lcd)
	signal.signal(signal.SIGINT, release)
	signal.pause()
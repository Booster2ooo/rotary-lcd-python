#!/usr/bin/env python3
import threading
from time import sleep
if __name__ == '__main__':
	from rotary_encoder_change import RotaryEncoderChange
	from settings import Settings
	from logger import getLogger
	from lcd import Lcd
else:
	from .rotary_encoder_change import RotaryEncoderChange

class RotaryDisplay:

	def __init__(self, settings, logger, rotary_encoder, lcd):
		self.settings = settings
		self.logger = logger
		self.rotary_encoder = rotary_encoder
		self.lcd = lcd
		self.wait_thread = None
		self.lock = threading.Lock()
		self.logger.debug('Initializing rotary display...')
		self.rotary_encoder.register_callback(self.on_rotary_change)
		self.write()
		self.logger.debug('Rotary display initialized .')
	
	def write(self, message = None):
		if self.lock.acquire(False):
			self.lcd.clear()
			if not message:
				self.lcd.message('waiting...')
			else:
				self.lcd.message('Encoder input:\n{}'.format(message))
			self.lock.release()

	def on_rotary_change(self, change_type):
		if self.wait_thread:
			self.wait_thread.cancel()
			self.wait_thread = None
		if change_type == RotaryEncoderChange.TURNED_LEFT:
			self.write('previous')
		elif change_type == RotaryEncoderChange.TURNED_RIGHT:
			self.write('next')
		elif change_type == RotaryEncoderChange.SWITCH_PRESSED:
			self.write('pressed')
		elif change_type == RotaryEncoderChange.SWITCH_RELEASED:
			self.write('released')
		else:
			self.logger.warn('Unknow rotary change type {}'.format(change_type))
		self.wait_thread = threading.Timer(1.0, self.write)
		self.wait_thread.start()

if __name__ == '__main__':
	# do some tests
	pass
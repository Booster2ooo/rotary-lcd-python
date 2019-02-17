#!/usr/bin/env python3
if __name__ == '__main__':
	from rotary_encoder_change import RotaryEncoderChange
	from settings import Settings
	from logger import getLogger
	from gpio_controller import GpioController
else:
	from .rotary_encoder_change import RotaryEncoderChange

class RotaryEncoder:
	
	def __init__(self, settings, logger, gpio_controller):
		self.settings = settings
		self.logger = logger
		self.GPIO = gpio_controller.GPIO
		self.callbacks = []
		self.logger.debug('Initializing rotary encoder...')
		self.switch_pin = settings["rotary_encoder"]["pins"]["switch"]
		self.clock_pin = settings["rotary_encoder"]["pins"]["clock"]
		self.data_pin = settings["rotary_encoder"]["pins"]["data"]
		self.switch_state = self.GPIO.HIGH
		self.clock_state = self.GPIO.HIGH
		self.logger.debug('Setting pins up...')
		self.GPIO.setup(self.switch_pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
		self.GPIO.setup(self.clock_pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
		self.GPIO.setup(self.data_pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
		self.logger.debug('Binding events...')
		self.GPIO.add_event_detect(self.switch_pin, self.GPIO.BOTH, callback=self.on_switch)
		self.GPIO.add_event_detect(self.clock_pin, self.GPIO.BOTH, callback=self.on_rotary)
		self.logger.debug('Rotary encoder initialized.')

	def register_callback(self, callback):
		self.logger.debug('Registering callback...')
		self.callbacks.append(callback)
		self.logger.debug('Callback registered.')

	def deregister_callback(self, callback):
		self.logger.debug('Deregistering callback...')
		if self.callbacks and callable in self.callbacks:
			self.remove(callback)
		self.logger.debug('Callback deregistered.')

	def emit_change(self, change_type):
		self.logger.debug('Emiting change...')
		if self.callbacks:
			[cb(change_type) for cb in self.callbacks]
		self.logger.debug('Change emitted.')
	
	def on_switch(self, channel):
		switch_state = self.GPIO.input(self.switch_pin)
		if self.switch_state != switch_state:
			self.logger.debug('Switch state changed...')
			self.switch_state = switch_state
			if switch_state:
				self.logger.info('Switch released.')
				self.emit_change(RotaryEncoderChange.SWITCH_RELEASED)
			else:
				self.logger.info('Switch pressed.')
				self.emit_change(RotaryEncoderChange.SWITCH_PRESSED)

	def on_rotary(self, channel):
		clock_state = self.GPIO.input(self.clock_pin)
		if self.clock_state != clock_state:
			self.logger.debug('Rotary state changed...')
			self.clock_state = clock_state
			if clock_state:
				dataState = self.GPIO.input(self.data_pin)
				if (dataState):
					self.logger.info('Rotary turned right.')
					self.emit_change(RotaryEncoderChange.TURNED_RIGHT)
				else:
					self.logger.info('Rotary turned left.')
					self.emit_change(RotaryEncoderChange.TURNED_LEFT)

if __name__ == '__main__':
	# do some tests
	pass
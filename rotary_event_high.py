#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import logging

eventCounter = 0

switchInput = 		27
rotaryClockInput = 	17
rotaryDataInput = 	18

previousSwitchState = 	GPIO.HIGH
previousClockState = 	GPIO.HIGH

def log(msg):
	global eventCounter
	prefix = '[ %s ]'%eventCounter
	logging.debug(prefix + msg)
	print msg

def onSwitch(channel):
	global previousSwitchState, eventCounter
	eventCounter += 1
	switchState = GPIO.input(switchInput)
	if previousSwitchState != switchState:
		if switchState:
			log( '(Switch) Rising edge detected on %s'%channel )
		else:
			log( '(Switch) Falling edge detected on %s'%channel )		
		previousSwitchState = switchState

def onRotary(channel):
	global previousClockState, eventCounter
	eventCounter += 1
	clockState = GPIO.input(rotaryClockInput)
	if previousClockState != clockState:
		previousClockState = clockState
		if clockState:
			log( '(Rotary) Rising edge detected on %s'%channel )
		else:
			log( '(Rotary) Falling edge detected on %s'%channel )
			log( '(Rotary) Detecting direction...' )
			dataState = GPIO.input(rotaryDataInput)
			if (dataState):
				log( '(Rotary) Direction <<' )
			else:
				log( '(Rotary) Direction >>' )

def setup():
	logging.basicConfig(filename='rotary_event.log',level=logging.DEBUG)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(switchInput, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(rotaryClockInput, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(rotaryDataInput, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(switchInput, GPIO.BOTH, callback=onSwitch)
	GPIO.add_event_detect(rotaryClockInput, GPIO.BOTH, callback=onRotary)

try:
	log( 'Starting program' )
	setup()
	while True:
		time.sleep(0.01)
except KeyboardInterrupt: 
	log( 'Program interupted' )
finally:
	log( 'Releasing GPIO' )
	GPIO.cleanup()
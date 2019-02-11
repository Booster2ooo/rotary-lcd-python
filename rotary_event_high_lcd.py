#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import logging
import Adafruit_CharLCD as LCD

# Raspberry Pi pin configuration:
lcd_rs           = 26  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en           = 19
lcd_d4           = 13
lcd_d5           = 6
lcd_d6           = 5
lcd_d7           = 11
lcd_backlight    = 9
switchInput      = 27
rotaryClockInput = 17
rotaryDataInput  = 18

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# LCD instance
# lcd = None

# Action index, supposedly used by in log() 
actionIndex = 0

# Default rotary encoder states
previousSwitchState = 	GPIO.HIGH
previousClockState = 	GPIO.HIGH

def log(msg):
	global actionIndex
	prefix = '[ %s ]'%actionIndex
	logging.debug(prefix + msg)
	print msg

def onSwitch(channel):
	global previousSwitchState, actionIndex
	actionIndex += 1
	switchState = GPIO.input(switchInput)
	if previousSwitchState != switchState:
		if switchState:
			log( '(Switch) Rising edge detected on %s'%channel )
		else:
			log( '(Switch) Falling edge detected on %s'%channel )		
		previousSwitchState = switchState
		if(switchState == GPIO.HIGH):
			lcd.clear()
			lcd.message("Encoder input:\npressed")

def onRotary(channel):
	global previousClockState, actionIndex
	actionIndex += 1
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
				lcd.clear()
				lcd.message("Encoder input:\nprevious")
			else:
				log( '(Rotary) Direction >>' )
				lcd.clear()
				lcd.message("Encoder input:\nnext")

def init_lcd():
	global lcd
	lcd = LCD.Adafruit_CharLCD(
		lcd_rs, 
		lcd_en, 
		lcd_d4, 
		lcd_d5, 
		lcd_d6, 
		lcd_d7,
        lcd_columns,
		lcd_rows,
		lcd_backlight,
		False
	)
	lcd.clear()
	lcd.blink(True)
	time.sleep(2.0)
	lcd.blink(False)

def init_rotary():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(switchInput, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(rotaryClockInput, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(rotaryDataInput, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(switchInput, GPIO.BOTH, callback=onSwitch)
	GPIO.add_event_detect(rotaryClockInput, GPIO.BOTH, callback=onRotary)

def setup():
	logging.basicConfig(filename='rotary_event.log',level=logging.DEBUG)
	log( 'Initializing...' )
	GPIO.cleanup()
	init_lcd()
	init_rotary()
	lcd.set_backlight(0)
	lcd.message('Encoder input:')
	time.sleep(2.0)
	lcd.set_backlight(1)
	log( 'Initialized' )

try:
	log( 'Starting program' )
	setup()
	while True:
		time.sleep(0.01)
except KeyboardInterrupt: 
	log( 'Program interupted' )
finally:
	log( 'Releasing resources' )
	if lcd is not None:
		lcd.clear()
	GPIO.cleanup()
	time.sleep(0.5)
	log( 'Resources released' )
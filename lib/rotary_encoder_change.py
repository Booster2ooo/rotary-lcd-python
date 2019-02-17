from enum import Enum

class RotaryEncoderChange(Enum):
	TURNED_LEFT = 0
	TURNED_RIGHT = 1
	SWITCH_PRESSED = 2
	SWITCH_RELEASED = 3
register = {
	"ABS_POS": (0x01, 22),
	"EL_POS": (0x02, 9),
	"MARK": (0x03, 22),
	"SPEED": (0x04, 20),
	"ACC": (0x05, 12),
	"DEC": (0x06, 12),
	"MAX_SPEED": (0x07, 10),
	"MIN_SPEED": (0x08, 12),
	"FS_SPD": (0x15, 10),
	"KVAL_HOLD": (0x09, 8),
	"KVAL_RUN": (0x0A, 8),
	"KVAL_ACC": (0x0B, 8),
	"KVAL_DEC": (0x0C, 8),
	"INT_SPD": (0x0D, 14),
	"ST_SLP": (0x0E, 8),
	"FN_SLP_ACC": (0x0F, 8),
	"FN_SLP_DEC": (0x10, 8),
	"K_THERM": (0x11, 4),
	"ADC_OUT": (0x12, 5),
	"OCD_TH": (0x13, 4),
	"STALL_TH": (0x14, 7),
	"STEP_MODE": (0x16, 8),
	"ALARM_EN": (0x17, 8),
	"CONFIG": (0x18, 16),
	"STATUS": (0x19, 16)
}

import time
import Slush

# initalizes the board and all its functions
board = Slush.sBoard()
time.sleep(1)

# initalizes the motor on the board
motor = Slush.Motor(0)
motor.resetDev()
time.sleep(1)

print("Before Settings Values: ", "\n")
for key, value in register.items():
	print(key, ' - ', motor.getParam(value))

# chamge some settings
motor.setCurrent(10, 50, 25, 25)
motor.setMicroSteps(8)
motor.setAccel(10)
motor.setDecel(10)
motor.setMaxSpeed(600)

print("\n\n")
print("Finished Setup", "\n\n")

print("After Settings Values:", "\n")
for key, value in register.items():
	print(key, ' - ', motor.getParam(value))

# free motor
motor.free()

print("\n\n")
print("END", "\n")
import time
import Slush

# initalizes the board and all its functions
board = Slush.sBoard()
print("Initalizing the board and all its functions")
time.sleep(1)

# initalizes the motorOne motor on the board
motorOne = Slush.Motor(0)
motorOne.resetDev()
print("Initalizing motorOne the motor on the board")
time.sleep(1)

# initalizes the motorTwo motor on the board
motorTwo = Slush.Motor(1)
motorTwo.resetDev()
print("Initalizing the motorTwo motor on the board")
time.sleep(1)

# set motorOne motor current hold, run, accel, decel & steps
motorOne.setCurrent(10, 50, 25, 25)
motorOne.setMicroSteps(8)
print("Setting motorOne motor current hold, run, accel, decel & steps")
time.sleep(1)

# set motorTwo motor current hold, run, accel, decel & steps
motorTwo.setCurrent(10, 20, 25, 25)
motorTwo.setMicroSteps(8)
print("Setting motorTwo motor current hold, run, accel, decel & steps")
time.sleep(1)

# configure motorOne motor motion parameters
motorOne.setAccel(100)
motorOne.setDecel(100)
motorOne.setMaxSpeed(600)
print("Configuring motorOne motor motion parameters")
time.sleep(1)

# configure motorTwo motor motion parameters
motorTwo.setAccel(100)
motorTwo.setDecel(100)
motorTwo.setMaxSpeed(600)
print("Configuring motorTwo motor motion parameters")
time.sleep(1)

# move the motorOne motor with move command
print("moving the motorOne motor with move command")
motorOne.move(20000)
while(motorOne.isBusy()):
	continue

# move the motorOne motor in reverse with move command
print("moving the motorOne motor in reverse with move command")
motorOne.move(-20000)
while(motorOne.isBusy()):
	continue

# move the motorTwo motor forward with move command
print("moving the motorTwo motor forward with move command")
motorTwo.move(20000)
while(motorTwo.isBusy()):
	continue

# move the motorTwo motor in reverse with move command
print("moving the motorTwo motor in reverse with move command")
motorTwo.move(-20000)
while(motorTwo.isBusy()):
	continue

# Wait
time.sleep(5)

# free motor
motorOne.free()
motorTwo.free()
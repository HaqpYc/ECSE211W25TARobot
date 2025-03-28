import brickpi3
import time

class Square:
    def __init__(self, square_type: str):
        self.type = square_type  # 'H', 'M', or 'R'
        self.has_furniture = False  # Only relevant for main room ('M')

    def is_accessible(self):
        return self.type in ('H', 'M') and not (self.type == 'M' and self.has_furniture)

    def __repr__(self):
        if self.type == 'M' and self.has_furniture:
            return "F"  # Furniture in main room
        return self.type

BP = brickpi3.BrickPi3()

# Define motor ports (check with hardware wiring)
LEFT_MOTOR = BP.PORT_A
RIGHT_MOTOR = BP.PORT_B

# Motor power (change as per requirement)
FORWARD_SPEED = 50
TURN_SPEED = 30

def move_forward():
    #Move the robot forward
    BP.set_motor_power(LEFT_MOTOR, FORWARD_SPEED)
    BP.set_motor_power(RIGHT_MOTOR, FORWARD_SPEED)

def move_backward():
    #Move the robot backward
    BP.set_motor_power(LEFT_MOTOR, -FORWARD_SPEED)
    BP.set_motor_power(RIGHT_MOTOR, -FORWARD_SPEED)

def turn_right():
    #Turn the robot right
    BP.set_motor_power(LEFT_MOTOR, TURN_SPEED)
    BP.set_motor_power(RIGHT_MOTOR, -TURN_SPEED)

def stop():
    #Stop the robot
    BP.set_motor_power(LEFT_MOTOR, 0)
    BP.set_motor_power(RIGHT_MOTOR, 0)

def get_distance():
    #Read distance from the ultrasonic sensor
    try:
        distance = BP.get_sensor(ULTRASONIC_SENSOR)
        return distance
    except BP.SensorError:
        print("Sensor reading error, returning large distance")
        return 100


from project.utils.brick import *
import time
from math import sqrt
from statistics import mean, stdev

LEFT_MOTOR = Motor("A")
RIGHT_MOTOR = Motor("B")
FIRE_MOTOR = Motor("C")

ULTRASONIC_SENSOR = EV3UltrasonicSensor(1)
COLOR_SENSOR = EV3ColorSensor(2)

FORWARD_SPEED = 50
TURN_SPEED = 30

FIRE_EXTINGUISHING_POSITION = 10

colors = {
    'RED': (95, 11, 5),
    'GREEN': (72, 108, 10),
    'ORANGE': (215, 49, 10),
    'BLACK': (52, 39, 14)
}


# Motion of the robot
def move_forward():
    # Move the robot forward
    BP.set_motor_power(LEFT_MOTOR, FORWARD_SPEED)
    BP.set_motor_power(RIGHT_MOTOR, FORWARD_SPEED)


def move_backward():
    # Move the robot backward
    BP.set_motor_power(LEFT_MOTOR, -FORWARD_SPEED)
    BP.set_motor_power(RIGHT_MOTOR, -FORWARD_SPEED)


def turn_right():
    # Turn the robot right
    BP.set_motor_power(LEFT_MOTOR, TURN_SPEED)
    BP.set_motor_power(RIGHT_MOTOR, -TURN_SPEED)


def turn_left():
    # Turn the robot right
    BP.set_motor_power(LEFT_MOTOR, -TURN_SPEED)
    BP.set_motor_power(RIGHT_MOTOR, TURN_SPEED)


def stop():
    # Stop the robot
    BP.set_motor_power(LEFT_MOTOR, 0)
    BP.set_motor_power(RIGHT_MOTOR, 0)


def turn_at_angle():
    """To drop the foam block on the fire sticker"""
    BP.set_motor_power(LEFT_MOTOR, 0)
    BP.set_motor_power(RIGHT_MOTOR, FORWARD_SPEED)
    time.sleep(0.5)
    stop()


def perform_sweep():
    """
    Perform a side-to-side scan by turning left, then right, then returning to original direction.
    """
    print("sweeping: scanning left")

    # Turn left (rotate in place to the left)
    BP.set_motor_power(LEFT_MOTOR, -FORWARD_SPEED)
    BP.set_motor_power(RIGHT_MOTOR, FORWARD_SPEED)
    time.sleep(0.3)  # adjust this for about 45 degrees
    stop()

    print("sweeping: scanning right")

    # Turn right (rotate in place to the right)
    BP.set_motor_power(LEFT_MOTOR, FORWARD_SPEED)
    BP.set_motor_power(RIGHT_MOTOR, -FORWARD_SPEED)
    time.sleep(0.6)  # 90 degrees right from the previous left-tilted position
    stop()

    print("sweeping: restoring forward direction")

    # Turn back left to original direction
    BP.set_motor_power(LEFT_MOTOR, -FORWARD_SPEED)
    BP.set_motor_power(RIGHT_MOTOR, FORWARD_SPEED)
    time.sleep(0.3)  # back to center
    stop()


def get_distance():
    # Read distance from the ultrasonic sensor
    try:
        distance = ULTRASONIC_SENSOR.get_value()
        return distance
    except BP.SensorError:
        print("Sensor reading error, returning large distance")
        return 100


# Color detection
def normalize(c):
    r, g, b, *_ = c  # Ignore any extra values.
    total = r + g + b
    if total == 0:
        return (0, 0, 0)
    return (r / total, g / total, b / total)


def distance(c1, c2):
    return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2)


def detect(unknown):
    normalized_unknown = normalize(unknown)
    normalized_colors = {color: normalize(val) for color, val in colors.items()}
    distances = {color: distance(normalized_unknown, normalized_colors[color])
                 for color in normalized_colors}
    return min(distances, key=distances.get)


def get_color():
    data = COLOR_SENSOR.get_value()  # Get RGB tuple, e.g., (r, g, b, luminosity)
    if data is None:
        return "NONE"
    return detect(data)


def extinguish_fire():
    FIRE_MOTOR.set_limits(100, 200)
    FIRE_MOTOR.set_position(FIRE_EXTINGUISHING_POSITION)


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


if __name__ == "__main__":
    try:
        print("Distance reading:", get_distance())
        print("Color reading:", get_color())
    except KeyboardInterrupt:
        BP.reset_all()

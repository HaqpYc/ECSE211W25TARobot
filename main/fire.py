from project.utils.brick import *
import brickpi3
import time
import threading
from main import get_distance, get_color, stop, move_forward, move_backward, turn_right, move_fire_motor, \
    ULTRASONIC_SENSOR, COLOR_SENSOR, turn_at_angle, extinguish_fire, perform_sweep, turn_left, LEFT_MOTOR, \
    FORWARD_SPEED, RIGHT_MOTOR

BP = brickpi3.BrickPi3()
# Threshold for ultrasonic sensor (in centimeters)
OBSTACLE_DISTANCE = 10

# A flag to control the monitoring threads
room_active = True

last_color = None


def monitor_obstacles():
    """
    Continuously check the ultrasonic sensor values
    """
    global room_active
    while room_active:
        distance = get_distance()
        if distance < OBSTACLE_DISTANCE:
            print("Obstacle detected by ultrasonic sensor! Distance:", distance)
            stop()
            time.sleep(0.5)
            move_backward()
            time.sleep(1)
            turn_right()
            time.sleep(1)
            stop()
        time.sleep(0.1)


def monitor_fire():
    """
    Continuously check the color sensor values
    """
    global room_active
    global last_color
    while room_active:
        color = get_color()
        if color == "RED":
            print("Fire detected! Activating fire response.")
            stop()
            turn_at_angle()
            extinguish_fire()
            time.sleep(2)
        elif color == "GREEN":
            last_color = "GREEN"
            print("Green detected by color sensor - obstacle present. Taking evasive action.")
            stop()
            move_backward()
            time.sleep(1)
            turn_right()
            time.sleep(1)
            stop()
        time.sleep(0.1)


def turn_relative(angle_deg):
    if angle_deg > 0:
        BP.set_motor_power(LEFT_MOTOR, FORWARD_SPEED)
        BP.set_motor_power(RIGHT_MOTOR, -FORWARD_SPEED)
    else:
        BP.set_motor_power(LEFT_MOTOR, -FORWARD_SPEED)
        BP.set_motor_power(RIGHT_MOTOR, FORWARD_SPEED)

    time.sleep(abs(angle_deg) / 90 * 0.5)  # 0.5s for ~90°, need adjust
    stop()


def avoid_obstacle_locally(current_angle, num):
    pass


def scan(num, min_angle=-60, max_angle=60, step=20):
    """
    Recovers from obstacle detection locally.
    """
    # Start from center and turn left to min_angle
    turn_relative(-abs(min_angle))
    current_angle = min_angle

    while current_angle <= max_angle:

        global last_color
        color = last_color
        if color == "GREEN":
            print("Green detected by color sensor - obstacle present. Taking evasive action.")
            if not -45 < current_angle < 45:
                avoid_obstacle_locally(current_angle, num)
                continue

        # Step right
        last_color = None
        turn_relative(step)
        current_angle += step

    # Return to original orientation
    turn_relative(-current_angle)

    stop()


def move_forward_and_scan(num):
    for i in range(num):
        scan(num)
        move_forward()
        time.sleep(0.2)  # adjust for sweep


def navigation_in_kitchen():
    """
       Navigate a 2x3 room in a Z-pattern, scanning each square with two sweep rounds.
       I assume we need 2n sweeps for each round right now
       Layout:
         [L2][M2][R2]
         [L1][M1][R1]
       Start: M1 (middle bottom)
       M1-L1-L2-L1-M1-M2-R2-R2-M2-M1-R1-R1-M1

    """
    n = 5

    print("Start at M1")
    move_forward_and_scan(n)

    print("Move to L1")
    turn_relative(-90)
    move_forward_and_scan(3 * n)
    turn_relative(90)

    print("Move to L2")
    move_forward_and_scan(4 * n)

    print("U-turn to go to L1")
    turn_relative(-90)
    move_forward_and_scan(n)
    turn_relative(-90)
    move_forward_and_scan(3 * n)

    print("Move to M1")
    turn_relative(-90)
    move_forward_and_scan(2 * n)

    print("Move to M2")
    turn_relative(-90)
    move_forward_and_scan(3 * n)

    print("Move to R2")
    turn_relative(90)
    move_forward_and_scan(3 * n)

    print("U-turn to go to M2")
    turn_relative(90)
    move_forward_and_scan(n)
    turn_relative(90)
    move_forward_and_scan(3 * n)

    print("Move to M1")
    turn_relative(-90)
    move_forward_and_scan(2 * n)

    print("Move to R1")
    turn_relative(-90)
    move_forward_and_scan(3 * n)

    print("U-turn to go to M1")
    turn_relative(90)
    move_forward_and_scan(n)
    turn_relative(90)
    move_forward_and_scan(3 * n)

    print("Turn to Gate")
    turn_relative(-90)

    print("Room scanning complete.")


def run_fire_detection():
    print("Entering room: starting fire and obstacle detection")

    obstacle_thread = threading.Thread(target=monitor_obstacles, daemon=True)
    fire_thread = threading.Thread(target=monitor_fire, daemon=True)

    obstacle_thread.start()
    fire_thread.start()

    try:
        # # Run for 150 secs or till the stop condition occurs
        # start_time = time.time()
        # while time.time() - start_time < 150:
        #     time.sleep(0.1)
        navigation_in_kitchen()
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        global room_active
        room_active = False
        obstacle_thread.join()
        fire_thread.join()
        BP.reset_all()
        print("Fire and Obstacle detection has stopped")


if __name__ == "__main__":
    run_fire_detection()

from project.utils.brick import * 
import brickpi3
import time
import threading
from main import get_distance, get_color, stop, move_forward, move_backward, turn_right, move_fire_motor, ULTRASONIC_SENSOR, COLOR_SENSOR, turn_at_angle, extinguish_fire

BP = brickpi3.BrickPi3()
# Threshold for ultrasonic sensor (in centimeters)
OBSTACLE_DISTANCE = 10

# A flag to control the monitoring threads
room_active = True

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
    while room_active:
        color = get_color()
        if color == "RED":
            print("Fire detected! Activating fire response.")
            stop()
            turn_at_angle()
            extinguish_fire()
            time.sleep(2)
        elif color == "GREEN":
            print("Green detected by color sensor - obstacle present. Taking evasive action.")
            stop()
            move_backward()
            time.sleep(1)
            turn_right()
            time.sleep(1)
            stop()
        time.sleep(0.1)

def run_fire_detection():  
    print("Entering room: starting fire and obstacle detection")
    
    obstacle_thread = threading.Thread(target=monitor_obstacles, daemon=True)
    fire_thread = threading.Thread(target=monitor_fire, daemon=True)
    
    obstacle_thread.start()
    fire_thread.start()
    
    try:
        # Run for 150 secs or till the stop condition occurs 
        start_time = time.time()
        while time.time() - start_time < 150:
            time.sleep(0.1)
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

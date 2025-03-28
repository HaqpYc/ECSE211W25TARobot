import brickpi3
import time

from main import get_distance, stop, move_backward, turn_right, move_forward, ULTRASONIC_SENSOR

# based on the requirement we need to change the threshold value for the sensor (in cm)
OBSTACLE_DISTANCE = 10

BP = brickpi3.BrickPi3()

def run_obstacle_avoidance():
    #Main function to run obstacle avoidance
    try:
        # Set the sensor type to ultrasonic
        BP.set_sensor_type(ULTRASONIC_SENSOR, BP.SENSOR_TYPE.NXT_ULTRASONIC)
        time.sleep(1)  # Give sensor time to initialize

        print("Obstacle avoidance starting...")
        while True:
            distance = get_distance()
            print(f"Distance: {distance} cm")

            if distance < OBSTACLE_DISTANCE:
                stop()
                time.sleep(0.5)
                move_backward()
                time.sleep(1)
                turn_right()
                time.sleep(1)
                stop()
                time.sleep(0.5)
            else:
                move_forward()

            time.sleep(0.1)

    except KeyboardInterrupt:
        BP.reset_all()
    
# Optional: Uncomment to test this file directly
# if __name__ == "__main__":
#     run_obstacle_avoidance()
import RPi.GPIO as GPIO
import time
from time import strftime
from datetime import datetime, timedelta

PIR_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
time.sleep(5)

in_bathroom = False
last_motion_time = 0
motion_start = None
motion_confirm_time = 3  # to prevent mistakes
motion_timeout = 30

try:
    while True:
        motion = GPIO.input(PIR_PIN)

        if motion:
            print("1", end="", flush=True)

            if motion_start is None:
                motion_start = time.time()

            last_motion_time = time.time()

            if not in_bathroom and (time.time() - motion_start) >= motion_confirm_time:
                print(f"\n{strftime('%H:%M:%S')} – the person entered")
                in_bathroom = True
        else:
            print(".", end="", flush=True)

            if motion_start and (time.time() - motion_start) < motion_confirm_time:
                motion_start = None

            if in_bathroom and (time.time() - last_motion_time) > motion_timeout:
                motion_end_time = datetime.fromtimestamp(last_motion_time) + timedelta(seconds=motion_timeout)
                print(f"\n{motion_end_time.strftime('%H:%M:%S')} – the person left")
                in_bathroom = False
                motion_start = None

        time.sleep(1)
except KeyboardInterrupt:
    print("\Bye Bye.")
finally:
    GPIO.cleanup()
    print("\nKończę program.")


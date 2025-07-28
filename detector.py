import RPi.GPIO as GPIO
import time
import csv
import os
from datetime import datetime, timedelta

PIR_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
time.sleep(2)

log_file = "log.csv"
if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as f:
        csv.writer(f).writerow(["entry_time", "exit_time"])

in_bathroom = False
last_motion_time = 0
motion_times = []
entry_time = None
motion_window = 7
motion_timeout = 30

try:
    while True:
        motion = GPIO.input(PIR_PIN)
        now = time.time()

        if motion:
            print("1", end="", flush=True)
            last_motion_time = now
            motion_times.append(now)
            motion_times = [t for t in motion_times if now - t <= motion_window]

            if not in_bathroom and len(motion_times) >= 2:
                entry_time = datetime.now()
                print(f"\n{entry_time.strftime('%H:%M:%S')} – the person entered")
                in_bathroom = True
                motion_times.clear()
        else:
            print(".", end="", flush=True)

            if in_bathroom and (now - last_motion_time) > motion_timeout:
                exit_time = datetime.fromtimestamp(last_motion_time) + timedelta(seconds=motion_timeout)
                print(f"\n{exit_time.strftime('%H:%M:%S')} – the person left")
                with open(log_file, "a", newline="") as f:
                    csv.writer(f).writerow([
                        entry_time.strftime('%Y-%m-%d %H:%M:%S'),
                        exit_time.strftime('%Y-%m-%d %H:%M:%S')
                    ])
                in_bathroom = False
                motion_times.clear()
                entry_time = None

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nBye Bye.")
finally:
    GPIO.cleanup()
    print(".")


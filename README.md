# Presence-monitor

Simple Raspberry Pi project records when someone enters and leaves a room (e.g., a bathroom) using a PIR motion sensor - "HC-SR501". The data is saved to a log.csv file.

### Requirements

 - Raspberry Pi
 - HC-SR501
 - Python 3
 - Rasbian with ssh

### Connection


| PIR PIN | Raspberry Pi PIN |
|---------|------------------|
| VCC     | 5V (4) |
| GND     | GND (pin 6)      |
| OUT     | GPIO4 (pin 7)    |



```
sudo apt update
sudo apt install python3-rpi.gpio
git clone https://github.com/neo-Odys/Presence-monitor.git
cd Presence-monitor
```

### Activation

```
python3 detector.py
```

On the terminal:
1 - motion detected
. - isn't
If there is no movement for 30 secondts - person left
Entry, exit times are recorded in the log.csv



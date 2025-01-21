from microbit import *

# upload the code on the micro:bit using the python version of makecode. 

while True:
    if button_a.is_pressed():
        uart.write("left\n")
    elif button_b.is_pressed():
        uart.write("right\n")
    elif accelerometer.get_x() > 200:
        uart.write("right\n")
    elif accelerometer.get_x() < -200:
        uart.write("left\n")
    else:
        uart.write("stop\n")
    sleep(100)

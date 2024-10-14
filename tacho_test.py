from gpiozero import Button
from time import time, sleep

# Set the GPIO pin connected to the tachometer
tachometer_pin = 15
tachometer = Button(tachometer_pin)

# Variables to track pulse count and time
pulse_count = 0
start_time = time()

# Function to increment the pulse count each time a pulse is detected
def count_pulse():
    global pulse_count
    pulse_count += 1

# Attach the function to the tachometer input (on each rising edge)
tachometer.when_pressed = count_pulse

def calculate_rpm():
    global pulse_count, start_time

    # Calculate the time elapsed
    elapsed_time = time() - start_time

    # Reset the timer and count
    start_time = time()

    # Calculate RPM based on pulse count and time elapsed
    # Adjust the pulse per revolution ratio if necessary
    pulses_per_revolution = 2  # Change this depending on your tachometer's spec

    # RPM formula: (Pulse count / pulses per revolution) / elapsed time in minutes
    rpm = (pulse_count / pulses_per_revolution) / (elapsed_time / 60)

    # Reset pulse count for the next measurement
    pulse_count = 0

    return rpm

while True:
    # Wait for 1 second (adjust depending on how frequently you want to check RPM)
    sleep(2)

    # Calculate and print RPM
    rpm = calculate_rpm()
    print(f"RPM: {rpm}")

import argparse
from gpiozero import PWMOutputDevice,Button
from time import sleep, time
import os

fan_pwm = PWMOutputDevice(14)
tachometer_pin=15
tachometer=Button(tachometer_pin)

pulse_count=0
start_time=time()
lowest_rpm=0 #from observations of tach_test.py
highest_rpm=8500
temp_segment = 0
pwm_segment=0.1

pulses_per_revolution=2

def count_pulse():
	global pulse_count
	pulse_count += 1

tachometer.when_pressed = count_pulse

def calculate_rpm():
	global pulse_count, start_time

	elapsed_time = time() - start_time
	start_time = time()

	if elapsed_time > 0:
		rpm = (pulse_count / pulses_per_revolution) / (elapsed_time / 60)
	else:
		rpm = 0

	pulse_count=0
	
	return rpm


def get_cpu_temp():
	temp = os.popen("vcgencmd measure_temp").readline()
	temp = temp.replace("temp=","").replace("'C\n","")
	return float(temp)



def adjust_pwm_to_temp(temp, lower_threshold, upper_threshold):
	if temp <= lower_threshold + temp_segment:
		fan_pwm.value = 0
		return 0

	if  temp > upper_threshold:
		fan_pwm.value = 1
		return 1

	fan_pwm.value = pwm_segment * ((temp - lower_threshold)// temp_segment)
	return fan_pwm.value

def main(lower_threshold, upper_threshold):
	global temp_segment
	temp_segment = (upper_threshold - lower_threshold)/10
	while True:
		temp = get_cpu_temp()

		current_rpm =calculate_rpm()

		pwm_value = adjust_pwm_to_temp(temp, lower_threshold, upper_threshold)

		#print(f"CPU Temp: {temp:.0f}°C,  Current RPM: {current_rpm:.0f}, PWM: {pwm_value:.5f}")
		sleep(30) 




if __name__ == "__main__":
	parser=argparse.ArgumentParser(description="Fan control with temperature thresholds")
	parser.add_argument('--lower_threshold',type=float,default=50.0, help='Temperature to start increasing the fan speed')
	parser.add_argument('--upper_threshold',type=float,default=65.0, help='Temperature to reach maz fan speed')
	
	args =  parser.parse_args()

	print(args.lower_threshold)
	print(args.upper_threshold)

	main(args.lower_threshold,args.upper_threshold)

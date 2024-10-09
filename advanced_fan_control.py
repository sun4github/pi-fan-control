import argparse
from gpiozero import PWMOutputDevice,Button
from time import sleep, time
import os

fan_pwm = PWMOutputDevice(14)
tachometer_pin=15
tachometer=Button(tachometer_pin)

pulse_count=0
start_time=time()
lowest_rpm=2999
highest_rpm=17000

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

def get_target_rpm(temp, lower_threshold, upper_threshold):
	if temp < lower_threshold:
		return 0
	elif lower_threshold <= temp  <= upper_threshold:
		return lowest_rpm + ((temp-lower_threshold) * (highest_rpm - lowest_rpm) / (upper_threshold - lower_threshold))
	else:
		return highest_rpm


def adjust_pwm_to_rpm(target_rpm, current_rpm):
	error = target_rpm - current_rpm
	k_p = 0.00005
	pwm_adjustment = k_p * error

	new_pwm_value = max(0,min(fan_pwm.value + pwm_adjustment, 1))
	fan_pwm.value = new_pwm_value
	return new_pwm_value

def main(lower_threshold, upper_threshold):
	while True:
		temp = get_cpu_temp()

		target_rpm = get_target_rpm(temp, lower_threshold, upper_threshold)

		current_rpm =calculate_rpm()

		pwm_value = adjust_pwm_to_rpm(target_rpm, current_rpm)

		#print(f"CPU Temp: {temp}C, Target RPM: {target_rpm.Of}, Current RPM: {current_rpm.Of}, PWM:{pwm_value.2f}")
		print(f"CPU Temp: {temp:.0f}°C, Target RPM: {target_rpm:.0f}, Current RPM: {current_rpm:.0f}, PWM: {pwm_value:.3f}")
		sleep(1) 




if __name__ == "__main__":
	parser=argparse.ArgumentParser(description="Fan control with temperature thresholds")
	parser.add_argument('--lower_threshold',type=float,default=50.0, help='Temperature to start increasing the fan speed')
	parser.add_argument('--upper_threshold',type=float,default=75.0, help='Temperature to reach maz fan speed')
	
	args =  parser.parse_args()

	print(args.lower_threshold)
	print(args.upper_threshold)

	main(args.lower_threshold,args.upper_threshold)

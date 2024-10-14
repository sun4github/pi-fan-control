import argparse
from gpiozero import PWMOutputDevice,Button
from time import sleep, time
import subprocess

fan_pwm = PWMOutputDevice(14)
tachometer_pin=15
tachometer=Button(tachometer_pin)

pulse_count=0
start_time=time()
lowest_rpm=0 #from observations of tach_test.py
highest_rpm=8500
temp_segment = 0
pwm_segment=0.1
sampling_interval=30
lower_threshold = 40
upper_threshold = 60


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
	##temp = os.popen("vcgencmd measure_temp").readline()
	result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
	temp_str = result.stdout.split('=')[1].split("'")[0]
	##temp = temp.replace("temp=","").replace("'C\n","")
	return float(temp_str)



def adjust_pwm_to_temp(temp, current_speed):
	target_speed=0
	#print(f"temp_segment: {temp_segment:.2f} lower_threshold: {lower_threshold:.0f} upper_threshold: {upper_threshold:.0f}")
	if temp >= upper_threshold:
		target_speed = min(1, (temp - lower_threshold) / temp_segment)
	elif temp <= lower_threshold:
		target_speed = 0

	if target_speed > current_speed:
		current_speed = min(target_speed, current_speed + pwm_segment)
	elif target_speed <= current_speed:
		current_speed = max(target_speed, current_speed - pwm_segment)

	fan_pwm.value = current_speed
	return fan_pwm.value

def main():
	global temp_segment
	temp_segment = (upper_threshold - lower_threshold)
	#print(f"temp_segment: {temp_segment:.2f}")
	try:
		fan_speed = 0
		while True:
			temp = get_cpu_temp()
			fan_speed = adjust_pwm_to_temp(temp, fan_speed)
			fan_rpm = calculate_rpm()
			#print(f"CPU Temp: {temp:.0f}°C,  Current RPM: {fan_rpm:.0f}, fan speed (pwm): {fan_speed:.1f}")
			sleep(sampling_interval)

	except KeyboardInterrupt:
			fan_pwm.value=0
	finally:
			fan_pwm.value=0




if __name__ == "__main__":
	parser=argparse.ArgumentParser(description="Fan control with temperature thresholds")
	parser.add_argument('--lower_threshold',type=float,default=50.0, help='Temperature under which fan does not run')
	parser.add_argument('--upper_threshold',type=float,default=60.0, help='Temperature above which fan does run')
	
	args =  parser.parse_args()

	print(args.lower_threshold)
	print(args.upper_threshold)

	lower_threshold = args.lower_threshold
	upper_threshold = args.upper_threshold

	main()

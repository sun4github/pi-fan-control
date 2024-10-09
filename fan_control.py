from gpiozero import PWMLED
from signal import pause
import time
import os
import atexit

led = PWMLED(14)
threshold_temp1=40
threshold_temp2=50
threshold_temp3=60

def get_cpu_temp():
    temp_str=os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
    return float(temp_str)/1000

def cleanup():
    led.off()
    print("Cleaning up after the CPU Fan program")
    
atexit.register(cleanup)

#main loop
try:
    while True:        
        cpu_temp = get_cpu_temp()
        print(f"CPU temp: {cpu_temp}")
        
        if cpu_temp >= threshold_temp1:
            led.value=0.3
        elif cpu_temp >= threshold_temp2:
            led.value=0.6
        elif cpu_temp >= threshold_temp3:
            led.value=1
        else:
            led.value=0
            
        time.sleep(20) # check the temp every 10 seconds
        
except KeyboardInterrupt:
    pass

finally:
    cleanup()
    

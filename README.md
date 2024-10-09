1) what technology is used to create the fan control ?
 gpizero package for python3 and python

2) what gpio pins are used ?
       +5v, GND, GPIO14 (PWM), GPIO15 (for tachometer input)

3) where is the program stored permanently ?
in folder /home/suneel/repos/fan_control/

4) why is the fan JST connector that is provided is not being used ?
because it is broken as i tried to shove in the connector the wrong way. For next time keep the yellow wire should be close to the border of outer side of the board to get it right

5) how is the fan service registered and used ?
	a) a new service: sudo nano /etc/systemd/system/fan_control.service
	b) look inside the above service file for reference to the python file (advanced_fan_control.py is used)
	c) enable and start the service:
		sudo systemctl daemon-reload
		sudo systemctl enable fan_control.service
		sudo systemctl start fan_control.service

6) how does the fan_control program work ?
	- verify the cpu temp every 1 second and turns the fan on if temp goes above 50 celsius

7) how to verify the status of the service ?
	- sudo systemctl status fan_control.service 

7) how to verify the current cpu temp ?
	- vcgencmd measure_temp	


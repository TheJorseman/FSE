from gpiozero import Button
button = Button(2)
while True:
	if button.is_pressed:
		import pdb;pdb.set_trace()
		print("Button is pressed")
	else:
		print("Button is not pressed")

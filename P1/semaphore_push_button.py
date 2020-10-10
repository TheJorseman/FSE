from gpiozero import LED, Button
from time import sleep
from threading import Thread,Event
from signal import pause
blink_time = 0.5
blink_iter = 3

red_time = 4
yellow_time = 2
green_time = 5

semaphore_red = LED(13)
semaphore_yellow = LED(19)
semaphore_green = LED(26)

push_button = Button(2)

event = Event()

time_to_stop = 1

def transition(current_LED, next_LED, blink_t=True):
	if blink_t:
		for t in range(2 * blink_iter):
			current_LED.toggle()
			sleep(blink_time)
	current_LED.off()
	next_LED.on()

def led_on(current_LED,LED_time):
	current_LED.on()
	sleep(LED_time)

def semaphore():
	semaphore_red.off()
	semaphore_yellow.off()
	semaphore_green.off()
	while True:
		semaphore_green.on()
		if event.wait(green_time):
			print("Se atiende la interrupcion")
			sleep(time_to_stop)
			interrup()
			continue
		transition(semaphore_green,semaphore_yellow)
		led_on(semaphore_yellow,yellow_time)
		transition(semaphore_yellow,semaphore_red, blink_t=False)
		led_on(semaphore_red,red_time)
		transition(semaphore_red,semaphore_green, blink_t=False)

def interrup():
	transition(semaphore_green,semaphore_yellow)
	led_on(semaphore_yellow,yellow_time)
	transition(semaphore_yellow,semaphore_red, blink_t=False)
	led_on(semaphore_red,red_time)
	transition(semaphore_red,semaphore_green, blink_t=False)
	event.clear()

def button_handler():
	while True:
		push_button.wait_for_press()
		event.set()
		

sem = Thread(target=semaphore)
button = Thread(target=button_handler)

sem.start()
button.start()



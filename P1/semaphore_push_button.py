from gpiozero import LED
from time import sleep
#from signal import pause
from threading import Event,Thread


event = Event()

blink_time = 0.5
blink_iter = 3

red_time = 4
yellow_time = 2
green_time = 5

semaphore_red = LED(13)
semaphore_yellow = LED(19)
semaphore_green = LED(26)

current_LED_name = None

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
		event.wait()
		while not event.is_set():
			current_LED_name = 'green'
			led_on(semaphore_green,green_time)
			transition(semaphore_green,semaphore_yellow)
			current_LED_name = 'yellow'
			led_on(semaphore_yellow,yellow_time)
			transition(semaphore_yellow,semaphore_red, blink_t=False)
			current_LED_name = 'red'
			led_on(semaphore_red,red_time)
			transition(semaphore_red,semaphore_green, blink_t=False)
		#Handler
		interrup(current_LED)

def interrup(current_LED):
	if current_LED == 'green':
		led_on(semaphore_red,red_time)
		transition(semaphore_red,semaphore_green, blink_t=False)
		event.clear()

def button_handler():
	while True:
		button.wait_for_press()
		event.set()

event = Event()

sem = Thread(target=semaphore)
button = Thread(target=button_handler)

sem.start()
button.start()



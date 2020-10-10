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

semaphore_red.off()
semaphore_yellow.off()
semaphore_green.off()

while True:
	led_on(semaphore_green,green_time)
	transition(semaphore_green,semaphore_yellow)
	led_on(semaphore_yellow,yellow_time)
	transition(semaphore_yellow,semaphore_red, blink_t=False)
	led_on(semaphore_red,red_time)
	transition(semaphore_red,semaphore_green, blink_t=False)




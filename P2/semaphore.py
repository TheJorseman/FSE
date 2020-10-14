from gpiozero import LED
from time import sleep
from signal import pause


blink_time = 0.5
blink_iter = 3

red_time = 4
yellow_time = 2
green_time = 5

semaphore_red = LED(13)
semaphore_yellow = LED(19)
semaphore_green = LED(26)

def transition(current_LED, next_LED, blink_t=True):
	"""
	Función que realiza la transición de un estado a otro.
	Permite solo cambiar o realizar un parpadeo para indicar la transición.
	Args:
		current_LED (LED): LED desde el cual se va a cambiar
		next_LED (LED): LED al cual se quiere llegar
		blink_t (bool, optional): Indicia si se tiene que realizar el parpadeo para la transición. Defaults to True.
	"""	
	if blink_t:
		for t in range(2 * blink_iter):
			current_LED.toggle()
			sleep(blink_time)
	current_LED.off()
	next_LED.on()

def led_on(current_LED,LED_time):
	"""
	Enciende un LED

	Args:
		current_LED (LED): LED a encender
		LED_time (float): Tiempo de encendido
	"""	
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



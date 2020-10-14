from gpiozero import LED, Button
from time import sleep
from threading import Thread,Event

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

def semaphore():
	"""
	Funcion que realiza todas las funciones de un semaforo sencillo.
	"""	
	semaphore_red.off()
	semaphore_yellow.off()
	semaphore_green.off()
	while True:
		semaphore_green.on()
		# Con este if lo que se hace es que el Evento espera una cierta cantidad de tiempo en espera de algún cambio.
		# Este cambio se puede activar de forma asincrona desde otro thread o en general desde otra parte.
		# Cuando se activa se 'Atiende la interrupción' y resetea el proceso.
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
	"""
	Función con las instrucciones necesarias para atender la interrupción.
	"""	
	transition(semaphore_green,semaphore_yellow)
	led_on(semaphore_yellow,yellow_time)
	transition(semaphore_yellow,semaphore_red, blink_t=False)
	led_on(semaphore_red,red_time)
	transition(semaphore_red,semaphore_green, blink_t=False)
	event.clear()

def button_handler():
	"""
	Función que detecta cambios en el boton configurado y activa el evento
	"""	
	while True:
		push_button.wait_for_press()
		event.set()
		
# Se inicializan los threads para el semaforo y el handler del boton
sem = Thread(target=semaphore)
button = Thread(target=button_handler)
# Se inician los threads
sem.start()
button.start()

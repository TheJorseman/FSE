import telebot
import re
from gpiozero import LED
from CasaInteligente.tools.regex import regexp

class Telegram(object):

    def __init__(self,name,bot):
        self.name = name
        self.bot = bot
        self.init_message = "Hola soy " + name
        self.disps = {}
        self.commands = []

    def command_start_help(self):
        """
        Regresa todas 

        Args:
            commands ([type]): [description]

        Returns:
            [type]: [description]
        """        
        return init_message + "\n" + "\n".join(self.commands)

    def add_action_message(self,message):
        self.commands.append(message)

    def get_full_name(self,message):
        """
        Regresa el nombre completo del usuario con el que se esta interactuando.

        Args:
            message (json): Respuesta del bot en formato Json

        Returns:
            str: Nombre del usuario
        """    
        user_info = message.from_user.to_dict()
        return user_info["first_name"] + " " + user_info["last_name"] + "\n"

    def set_element(self,disp,command):
        """
        Agrega un dispositivo al diccionario de los dispositivos disponibles..

        Args:
            disp (object): Dispositivo que se desea agregar
            command (str): comando o nombre que tendra la llave 
        """        
        self.disps[command] = disps

    def set_elements(self,disps):
        for disp in disps:
            self.disps[disp.name.lower()] = disp

    def set_on_disps(self,disps):
        """
        Pone en alto los dispositivos seleccionados

        Args:
            disps (list): Lista de objetos a encender

        Returns:
            str: Cadena con los dispositivos encendidos
        """        
        for disp in disps:
            self.disps[disp].on()
        return ",".join(disps)


    def command_on(self,message):
        return_message = ""
        return_message = "Hola " + self.get_full_name(message)
        try:
            disps = self.parse_message(message,"/on",regexp.get_csv())
        except Exception as e:
            return_message += "\n"+ str(e) 
            return return_message
        disps = self.set_on_disps(disps)
        return_message += "Se han encedido el\los dispositivos " + ",".join(disps)
        return return_message

    def command_off(self,message):
        return_message = "Hola " + self.get_full_name(message)
        try:
            disps = parse_message(message,"/off",regexp.get_csv())
        except Exception as e:
            return_message += "\n"+ str(e) 
            return return_message
        disps = self.set_on_disps(disps)
        return_message += "Se han apagado el\los dispositivos " + ",".join(disps)
        return return_message

    def command_show(self,message):
        return_message = "Hola " + self.get_full_name(message)
        return_message += "\nEstos son los dispositivos que puedes manipular \n"
        return_message += ", ".join(self.disps.keys())
        return  return_message

    def parse_message(self,message,command,regex):
        """
        Verifica con expresiones regulares la validez de los comandos y los valores que se mandan para 
        apagar o encender LEDS.

        Args:
            message (json): Respuesta del usuario hacia el bot.
            command (str): comando a evaluar

        Returns:
            object: Si el texto coincide con lo esperado, se devuelve un True y la lista de los GPIO, en caso contrario se regresa 
                        False y un mensaje de error.
        """
        texto = message.text.lower()
        correct_command = re.search(command+regex,texto)
        if not correct_command:
            raise Exception("El mensaje enviado no coincide con lo que se esperaba "+ command)
        disps = texto.replace(command,"").strip().replace(" ","").split(",")
        if not any([match in self.disps.keys() for match in disps]):
            raise Exception("No existen el/los dispositivos " + ",".join([disp if not disp in self.disps.keys() else "" for disp in disps]) )
        return disps if type(disps) == type(list()) else [disps]


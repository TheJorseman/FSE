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
        self.commands = {}

    def command_start_help(self):
        """
        Regresa todas 

        Args:
            commands ([type]): [description]

        Returns:
            [type]: [description]
        """
        text = []  
        for command_text in self.commands.values():
            text.append(command_text["message"])
            text.append(command_text["example"])
        return init_message + "\n" + "\n".join(text)

    def add_action_message(self,command, message, example):
        self.commands[command] = {"message": message, "example": example}

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
        return ", ".join(disps)

    def set_off_disps(self,disps):
        """
        Pone en bajo los dispositivos seleccionados

        Args:
            disps (list): Lista de objetos a encender

        Returns:
            str: Cadena con los dispositivos encendidos
        """        
        for disp in disps:
            self.disps[disp].off()
        return ", ".join(disps)

    def set_value(self,disp,value):
        self.disps[disp].value = value
        return ", ".join([disp])

    def command_on(self,message):
        return_message = ""
        return_message = "Hola " + self.get_full_name(message)
        try:
            disps = self.parse_message(message,"/on",regexp.get_csv())
        except Exception as e:
            return_message += "\n"+ str(e) 
            return return_message
        disps = self.set_on_disps(disps)
        return_message += "Se han encedido el\los dispositivos " + disps
        return return_message

    def command_off(self,message):
        return_message = "Hola " + self.get_full_name(message)
        try:
            disps = self.parse_message(message,"/off",regexp.get_csv())
        except Exception as e:
            return_message += "\n"+ str(e) 
            return return_message
        disps = self.set_off_disps(disps)
        return_message += "Se han apagado el\los dispositivos " + disps
        return return_message

    def command_show(self,message):
        """
        Retorna un string con la informacion de todas las acciones

        Args:
            message (message): json con el mensaje mandado por el usuario

        Returns:
            str: string con la ayuda
        """        
        return_message = "Hola " + self.get_full_name(message)
        return_message += "\nEstos son los dispositivos que puedes manipular \n"
        return_message += ", ".join(self.disps.keys())
        return  return_message

    def command_set_value(self,message):
        return_message = ""
        return_message = "Hola " + self.get_full_name(message)
        try:
            disp,value = self.parse_message_with_args(message,"/setvalue",regexp.disp_with_number_0_1())
        except Exception as e:
            return_message += "\n"+ str(e) 
            return return_message
        disps = self.set_value(disp,value)
        return_message += "Se han establecido el valor de {} al {} ".format(disp,value)
        return return_message   

    def parse_message_with_args(self,message,command,regex):
        self.check_message_structure(message,command,regex)
        texto = message.text.lower()
        values = re.findall(regex,texto)
        if not values:
            raise Exception("No se pudo encontrar una sentencia con la siguiente estructura " + self.commands[command]["example"])
        disp,value = values[0]
        if not disp in self.disps.keys():
            raise Exception("No se pudo encontrar un dispositivo con el nombre " + disp, " ingrese el comando con alguno de los siguientes dispositivos " + "\n".join(self.disps.keys()) )
        return disp,float(value)     

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
        self.check_message_structure(message,command,regex)
        texto = message.text.lower()
        disps = texto.replace(command,"").strip().replace(" ","").split(",")
        if "all" in disps:
            return list(self.disps.keys())
        if not any([match in self.disps.keys() for match in disps]):
            raise Exception("No existen el/los dispositivos " + ",".join([disp if not disp in self.disps.keys() else "" for disp in disps]) )
        return disps

    def check_message_structure(self,message,command,regex):
        texto = message.text.lower()
        correct_command = re.search(command+regex,texto)
        if not correct_command:
            raise Exception("El mensaje enviado no coincide con lo que se esperaba "+ self.commands[command]["example"]) if command in self.commands.keys() else ""
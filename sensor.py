#coding: utf-8

from random import randint

class Sensor ():
    """Abstração dos sensores do trator. É útil para termos jeitos diferentes
    de leitura, seja por arquivo, socket, serial, ou forjado...
    Cada sensor tem também uma descrição, um contexto."""
    def read (self):
        """Realiza uma leitura de sensor"""
        pass

    def context (self, value):
        """Contextualiza o valor, retornando a string correspondente"""
        pass

class FileSensor (Sensor):
    """Sensor em arquivo, lendo 1 byte de cada vez"""
    files = {}

    def __init__ (self, fileName):
        self.fileName = fileName
        # memoiza arquivo, pois caso seja o mesmo, usa o já aberto
        if self.files.get (fileName):
            self.fd = self.files.get (fileName)
        else:
            self.fd = open (fileName)
            self.files[fileName] = self.fd

    def read (self):
        return ord (self.fd.read (1))

    def context (self, value):
        return "{} - {}".format (self.fileName, value)



class RandSensor (Sensor):
    """Sensor rand, para testes"""
    def read (self):
        return randint (20, 25)

    def context (self, value):
        return "rand: {}º".format (value)

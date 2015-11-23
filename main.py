#coding: utf-8

import sensor

# Arquivos dos sensores
numSensores = 4
sensores = []
for i in range (numSensores):
    sensores.append (sensor.RandSensor ())

def leituraSensor (idx):
    """Retorna uma leitura do sensor no índice idx"""
    return ord (sensores[idx].read ()) % 6 + 20

# Twisted pra rede funcionar
# Função install_twisted_reactor deve ser importado antes do Twisted
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class SensorSender (DatagramProtocol):
    def __init__ (self, app, host, port):
        self.app = app
        self.host = host
        self.port = port

    def startProtocol (self):
        self.transport.connect (self.host, self.port)
        Clock.schedule_interval (self.sendSensors, 1)

    def stopProtocol (self):
        Clock.unschedule (self.sendSensors)

    def sendSensors (self, dt):
        string = ''
        for i, s in enumerate (sensores):
            leitura = str (s.read ())
            self.app.sm.get_screen ('telaEnvio').ids['sensores'].children[i].text = s.context (leitura)
            string += '|' + leitura
        self.transport.write (string)

        

    def connectionRefused (self):
        self.app.erroConexao ()

# Kivy, nossa interface gráfica

import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

# carrega o arquivo kivy das telas
Builder.load_file ('telas.kv')

class TelaConexao (Screen):
    """Tela de conexão (tela inicial)"""
    pass

class TelaEnvio (Screen):
    """Tela de leitura do sensor e envio para servidor"""
    pass

class TelaErroConexao (Screen):
    """Tela que mostra que a conexão falhou"""
    pass

class MyApp (App):
    """DataSystemTruck Kivy App"""

    connection = None

    def connect (self, ip, port):
        self.connection = SensorSender (self, ip, int (port))
        reactor.listenUDP (0, self.connection)

    def disconnect (self):
        if self.connection:
            self.connection.transport.stopListening ()
            self.connection = None

    def erroConexao (self):
        self.disconnect ()
        self.sm.current = 'telaErroConexao'

    def build (self):
        sm = ScreenManager ()
        sm.add_widget (TelaConexao (name = 'telaConexao'))
        telaEnvio = TelaEnvio (name = 'telaEnvio')
        for i in range (numSensores):
            telaEnvio.ids['sensores'].add_widget (Label (text = 'sensor' + str (i)))
        sm.add_widget (telaEnvio)
        sm.add_widget (TelaErroConexao (name = 'telaErroConexao'))
        self.sm = sm
        return sm


if __name__ == '__main__':
    MyApp().run()

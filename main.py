#coding: utf-8

# Twisted pra rede funcionar
# Função install_twisted_reactor deve ser importado antes do Twisted
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class SensorSender (DatagramProtocol):
    def __init__ (self, app, name, host, port):
        self.app = app
        self.name = name
        self.host = host
        self.port = port

    def startProtocol (self):
        self.transport.connect (self.host, self.port)
        Clock.schedule_interval (self.sendSensors, 1)

    def stopProtocol (self):
        Clock.unschedule (self.sendSensors)

    def sendSensors (self, dt):
        self.transport.write (self.name)

    def connectionRefused (self):
        self.app.erroConexao ()

# Kivy, nossa interface gráfica

import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from random import randint

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

class MyApp(App):
    """DataSystemTruck Kivy App"""

    connection = None

    def connect (self, ip, port):
        # tenta conectar, retornando se funcionou
        self.connection = SensorSender (self, 'oi', ip, int (port))
        reactor.listenUDP (0, self.connection)
        print 'conectado'

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
        sm.add_widget (TelaEnvio (name = 'telaEnvio'))
        sm.add_widget (TelaErroConexao (name = 'telaErroConexao'))
        self.sm = sm
        return sm


if __name__ == '__main__':
    MyApp().run()

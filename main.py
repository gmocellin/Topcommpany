#coding: utf-8

import sensor

# Arquivos dos sensores
numSensores = 5
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

from uuid import getnode as get_mac

class SensorSender (DatagramProtocol):
    """Conexão UDP que manda info dos sensores"""
    def __init__ (self, app, host, port):
        self.app = app
        self.host = host
        self.port = port

    def startProtocol (self):
        try:
            self.transport.connect (self.host, int (self.port))
            Clock.schedule_interval (self.sendSensors, 1)
        except:
            self.app.erroEndereco ()

    def stopProtocol (self):
        Clock.unschedule (self.sendSensors)

    def sendSensors (self, dt):
        string = self.app.config.get ('conexao', 'nome')
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

#from jnius import autoclass
#PythonActivity = autoclass('org.renpy.android.PythonActivity')
#View = autoclass('android.view.View')
#Params = autoclass('android.view.WindowManager$LayoutParams')

#from android.runnable import run_on_ui_thread

# carrega o arquivo kivy das telas
Builder.load_file ('telas.kv')

class TelaPrincipal (Screen):
    """Tela inicial"""
    pass

class TelaConfiguracao (Screen):
    def loadConfig (self, app):
        config = app.config
        self.ids['nome'].text = config.get ('conexao', 'nome')
        self.ids['ip'].text = config.get ('conexao', 'ip')
        self.ids['port'].text = config.get ('conexao', 'port')

    def saveConfig (self, app):
        config = app.config
        config.set ('conexao', 'nome', self.ids['nome'].text)
        config.set ('conexao', 'ip', self.ids['ip'].text)
        config.set ('conexao', 'port', self.ids['port'].text)
        config.write ()

class TelaEnvio (Screen):
    """Tela de leitura do sensor e envio para servidor"""
    pass

class TelaErroConexao (Screen):
    """Tela que mostra que a conexão falhou"""
    pass

class TelaErroEndereco (Screen):
    """Tela que mostra que o endereço digitado está errado"""
    pass

class MyApp (App):
    """DataSystemTruck Kivy App"""

    connection = None

    def connect (self):
        ip = self.config.get ('conexao', 'ip')
        port = self.config.get ('conexao', 'port')
        self.connection = SensorSender (self, ip, port)
        reactor.listenUDP (0, self.connection)

    def disconnect (self):
        if self.connection:
            self.connection.transport.stopListening ()
            self.connection = None

    def erroConexao (self):
        self.disconnect ()
        self.sm.current = 'telaErroConexao'

    def erroEndereco (self):
        self.sm.current = 'telaErroEndereco'

    def build_config (self, config):
        config.setdefaults ('conexao', {
            'nome' : 'batata',
            'ip' : '127.0.0.1',
            'port' : '10000'
        })

    def build (self):
        sm = ScreenManager ()
        sm.add_widget (TelaPrincipal (name = 'telaPrincipal'))
        sm.add_widget (TelaConfiguracao (name = 'telaConfiguracao'))
        telaEnvio = TelaEnvio (name = 'telaEnvio')
        for i in range (numSensores):
            telaEnvio.ids['sensores'].add_widget (Label (text = 'sensor' + str (i)))
        sm.add_widget (telaEnvio)
        sm.add_widget (TelaErroConexao (name = 'telaErroConexao'))
        sm.add_widget (TelaErroEndereco (name = 'telaErroEndereco'))
        self.sm = sm
        return sm

    def on_pause (self):
        # aceita pausar
        return True

    def on_resume (self):
        pass

    #@run_on_ui_thread
    #def android_setflag(self):
        #PythonActivity.mActivity.getWindow().addFlags(Params.FLAG_KEEP_SCREEN_ON)


if __name__ == '__main__':
    MyApp().run()

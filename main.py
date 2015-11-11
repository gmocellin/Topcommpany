#coding: utf-8

import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

import socket
from random import randint

# socket cliente global
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

# carrega o arquivo kivy das telas
Builder.load_file ('telas.kv')

class TelaConexao (Screen):
    """Tela de conexão (tela inicial)"""
    pass

class TelaEnvio (Screen):
    """Tela de leitura do sensor e envio para servidor"""
    def schedule (self):
        Clock.schedule_interval (self.sendInfo, 1)

    def unschedule (self):
        Clock.unschedule (self.sendInfo)

    def sendInfo (self, dt):
        sensor = str (randint (20, 25))
        self.children[0].children[1].text = sensor + ' graus'
        sock.sendall (sensor)


class MyApp(App):
    """DataSystemTruck Kivy App"""
    def connect (self, ip, port):
        # tenta conectar, retornando se funcionou
        try:
            sock.connect ((ip, int (port)))
            print 'conectei'
            return True
        except:
            sock.close ()
            return False

    def disconnect (self):
        sock.close ()

    def build(self):
        sm = ScreenManager ()
        sm.add_widget (TelaConexao (name = 'telaConexao'))
        sm.add_widget (TelaEnvio (name = 'telaEnvio'))
        return sm


if __name__ == '__main__':
    MyApp().run()

#coding: utf-8

import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

import socket
from random import randint

# socket cliente
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

def sendInfo (dt):
    sock.sendall (str (randint (20, 25)))

class MyApp(App):
    def connect (self, ip, port):
        try:
            sock.connect ((ip, int (port)))
            print 'conectei'
            Clock.schedule_interval (sendInfo, 1)
        except:
            sock.close ()

    def disconnect (self):
        Clock.unschedule (sendInfo)
        sock.close ()

    def build(self):
        sm = ScreenManager ()
        sm.add_widget (Builder.load_file ('telaConexao.kv'))
        sm.add_widget (Builder.load_file ('telaEnvio.kv'))
        return sm


if __name__ == '__main__':
    MyApp().run()

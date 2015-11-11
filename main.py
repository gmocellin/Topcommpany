import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

import socket

# socket cliente
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
endereco = ('localhost', 10000)

kv = """
Screen:
    name: 'tela1'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Escreva o IP'
        TextInput:
            id: ip
            text: 'localhost'
        Label:
            text: 'Escreva a porta'
        TextInput:
            id: port
            text: '10000'
        Button:
            id: connect
            text: 'connect'
            on_release: 
                app.connect (ip.text, port.text)
                root.manager.current = 'tela2'
            size_hint_y: None
            height: '48dp'
"""

kv2 = """
Screen:
    name: 'tela2'
    orientation: 'vertical'
    Button:
        text: 'disconnect'
        on_release:
            app.disconnect ()
            root.manager.current = 'tela1'
"""

def sendInfo (dt):
    sock.sendall ('sensor indica: 15 graus')

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
        sm.add_widget (Builder.load_string (kv))
        sm.add_widget (Builder.load_string (kv2))
        return sm


if __name__ == '__main__':
    MyApp().run()

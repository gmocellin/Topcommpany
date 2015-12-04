#!/usr/bin/env python2
#coding: utf-8

from kivy.support import install_twisted_reactor
install_twisted_reactor()

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

import struct
from kivy.clock import Clock, _default_time as time

class Echo (DatagramProtocol):
    """Receptor UDP que pega infos dos tratores e transporta pro app servidor"""
    def __init__ (self, app):
        self.app = app
        # dicionário de conexões, pra ligarmos quem é quem =P
        self.conexoes = {}

    def writeLogs (self, *args):
        """Salva os Logs de entrada em arquivos correspondentes, um pra cada trator"""
        for nome, buffer in self.conexoes.items ():
            # append, pra ter todos dados
            file = open ('log_' + nome + '.csv', 'a')
            file.writelines (buffer)
            file.close ()
            self.conexoes[nome] = []

    def datagramReceived (self, data, (host, port)):
        """Pra cada pacote recebido, avisa o app e salva no dicionário de conexões"""
        seqNum, msg = struct.unpack ('=I', data[:4])[0], data[4:]
        valores = msg.split ('|')
        nome, valores = valores[0], valores[1:]
        # salva nome no dicionario, se esse ainda nao existir
        listaConexao = self.conexoes.get (nome)
        if listaConexao is None:
            self.app.createTab(nome)
            self.conexoes[nome] = []
            listaConexao = self.conexoes[nome]
        
        timestamp = time ()
        valores = ', '.join (valores)
        string = "%f, %d, %s" % (timestamp, seqNum, valores)
        listaConexao.append (string + '\n')

        self.app.consume (nome, timestamp, seqNum, valores)


from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

kv = r"""
TabbedPanel:
    id: boxConexoes
    tab_pos: 'top_mid'
    do_default_tab: False

    # aba inicial, sobre o programa
    TabbedPanelItem:
        text: 'Sobre'
        Label:
            text: "Cada aba acima representa uma conexão com um trator.\nArquivos de relatório são gerados no formato .csv, um para cada nome de conexão recebido.\nA porta utilizada para recebimento de pacotes é a de número 10000.\n\n\nDesenvolvedores:\n    Nosso\n    Nome\n    E\n    NUSP"

<BoxConexao>:
    ScrollView:
        GridLayout:
            cols: 1
            id: dados
            size_hint: 1, None
            height: self.minimum_height

<MyLabel@Label>:
    size_hint_y: None
    height: self.texture_size[1]
"""

class BoxConexao (TabbedPanelItem):
    """O item das abas, um pra cada conexão (com seu nome =] )"""
    def setNome (self, nome):
        self.nome = nome
        self.text = nome
        self.id = nome

class DataSystemTruckServerApp (App):
    """Aplicação servidora"""
    consommables = ListProperty([])
    conexoes = {}

    def createTab (self, nome):
        # cria a nova aba, troca seu nome, e manda aparecer
        newBox = BoxConexao ()
        newBox.setNome (nome)
        self.conexoes[nome] = newBox
        self.root.add_widget (newBox)

    def build(self):
        # conexao UDP com os tratores
        self.conexao = Echo (self)
        reactor.listenMulticast (10000, self.conexao, listenMultiple = True)
        # escreve os logs a cada 10 segundos, pra nao perder
        Clock.schedule_interval (self.conexao.writeLogs, 10)
        return Builder.load_string(kv)

    def consume (self, nome, timestamp, seqNum, valores):
        """Consome os dados, os escrevendo na aba correspondente"""
        label = Factory.MyLabel (text = "[%f] [%d] '%s'" % (timestamp, seqNum, valores))
        self.conexoes[nome].ids['dados'].add_widget(label)

    def on_stop (self):
        """Se fechar o programa, salva os logs"""
        self.conexao.writeLogs ()

if __name__ == '__main__':
    DataSystemTruckServerApp().run()

import socket
import sys
import threading

class IRC:
    connected = False
    
    def __init__(self, name, server, channel):
        self.name = name
        self.server = server
        self.channel = channel
        self.connected = False
    
    def connect(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.server, 6667))
        self.connection.send(bytes("NICK " + self.name + "\n ", "UTF-8"))
        self.connection.send(bytes("USER "+ self.name +" "+ self.name +" "+ self.name +" :This is a fun bot!\n", "UTF-8"))
    
    def listen(self):
        recived = self.connection.recv(2040).decode("UTF-8")
        
        if(recived.find('PING') != -1):
            self.connection.send(bytes('PONG ' + recived.split() [1] + '\r\n', "UTF-8"))
        return recived
    
    def joinChannel(self, newChannel=None):
        if not self.connected:
            self.connection.send(bytes("JOIN "+ self.channel +"\n", "UTF-8"))
            self.connected = True
        else:
            self.connection.send(bytes("JOIN "+ newChannel +"\n", "UTF-8"))
            self.channel = newChannel

    
    def printMsg(self):
        while True:
            text = self.listen()
            if text:
                msg = text.split(':')
                if len(msg) > 2:
                    print(f'\n {msg[1].split('!')[0]} @ {self.channel}: {msg[2].strip()}')
                    print(f'{self.name} @ {self.channel}: ')
                else: 
                    print(f'\n {text}')
                    print(f'{self.name} @ {self.channel}: ',end=' ')

    def sendMsg(self, msg):
        if(msg[0] == '/'):
            self.sendCommand(msg)
        else:
            self.connection.send(bytes(f"PRIVMSG {self.channel} :{msg} \r\n", "UTF-8"))

    def sendCommand(self, command):
        if('join' in command):
            newChannel = command.split(' ')
            if len(newChannel) >= 2:
                if newChannel[1][0] != '#':
                    newChannel[1] = '#' + newChannel[1]
                print(newChannel[1])
                self.joinChannel(newChannel[1])
        elif('quit' in command):
            self.connection.send(bytes(f"QUIT Xau Xau!\r\n", "UTF-8"))
            exit(0)


def menu():
    print(r""" _____                                                                                                                         _____ 
( ___ )                                                                                                                       ( ___ )
 |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
 |   |  █████  █████            ███████████             █████                        ███████████                               |   | 
 |   | ░░███  ░░███            ░░███░░░░░███           ░░███                        ░░███░░░░░███                              |   | 
 |   |  ░███   ░███  ████████   ░███    ░███  ██████   ███████    ██████             ░███    ░███  ██████   ████████   ██████  |   | 
 |   |  ░███   ░███ ░░███░░███  ░██████████  ░░░░░███ ░░░███░    ███░░███ ██████████ ░██████████  ░░░░░███ ░░███░░███ ███░░███ |   | 
 |   |  ░███   ░███  ░███ ░███  ░███░░░░░███  ███████   ░███    ░███████ ░░░░░░░░░░  ░███░░░░░░    ███████  ░███ ░███░███ ░███ |   | 
 |   |  ░███   ░███  ░███ ░███  ░███    ░███ ███░░███   ░███ ███░███░░░              ░███         ███░░███  ░███ ░███░███ ░███ |   | 
 |   |  ░░████████   ████ █████ ███████████ ░░████████  ░░█████ ░░██████             █████       ░░████████ ░███████ ░░██████  |   | 
 |   |   ░░░░░░░░   ░░░░ ░░░░░ ░░░░░░░░░░░   ░░░░░░░░    ░░░░░   ░░░░░░             ░░░░░         ░░░░░░░░  ░███░░░   ░░░░░░   |   | 
 |   |                                                                                                      ░███               |   | 
 |   |                                                                                                      █████              |   | 
 |   |                                                                                                     ░░░░░               |   | 
 |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
(_____)                                                                                                                       (_____)
""")
    print('Digite: ')
    print('1 - Conectar')
    print('2 - Saber Mais')
    print('3 - Comandos')
    
    while True:
        esc = int(input('$ '))
        if(esc == 1):
            name = input('Digite seu nome: ')

            server = input('Digite o servidor(Padrão: freenode): ')
            server = None if server == '' else server
            
            channel = input('Digite o servidor(Padrão: #python): ')
            channel = None if channel == '' else channel
            
            Start(name)
        
        elif(esc == 2):
            print('\nUnBate-papo é um simples cliente IRC, desenvolvido como trabalho da matéria Redes de Computadores.')
        
        elif(esc == 3):
            print('\nDigite /join +nomeCanal para trocar de canal')
            print('Digite /quit para sair\n')


def Start(name, server='irc.freenode.net', channel='#python'):
    print('Contectando...')
    client = IRC(name, server, channel)
    client.connect()

    while True:
        text = client.listen()
        if '376' in text and not client.connected:
            client.joinChannel()
            threading.Thread(target=client.printMsg).start()
            print('Conectado!')
            break
        
    try:
        while True: 
            client.sendMsg(input(f'{client.name} @ {client.channel}: '))
    except:
        pass


menu()
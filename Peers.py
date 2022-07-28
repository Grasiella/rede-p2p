from email import message
from http import client
import socket
import threading
from rich.console import Console
from rich.table import Table
from teste import tested
import threading
import sys


"""para conectar o Peer"""
IP_PEER = str(sys.argv[1])
PORT = int(sys.argv[2])
peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = peer.connect((IP_PEER,PORT))



enderecos_portas = {}
"""criando repositório de arquivos"""

f = open('meus_arquivos.txt', 'r')
arquivo = f.read()
linhas = arquivo.splitlines()
arquivos = {}

for x in linhas:
    if x != '':
        aux = x.split(' ')
        arquivos[aux[0]] = aux[1]
    

lista_arquivos = ''
for x in arquivos:
    lista_arquivos += x + ' '

"""-------------------------------"""

    
def show_peers(datas):
    table = Table(title="Peers conectados")
    table.add_column("Endereço IP", style='cyan')
    table.add_column("Porta pública", style='cyan')
    for x in datas:
        if x != '':
            aux = x.split(':')
            enderecos_portas[aux[0]] = aux[1]
            table.add_row(aux[0], aux[1])
        
    console = Console()
    console.print('\n',table, '\n')
    
def connect_to_peer(ip, portt, message):
    peer2peer2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = peer2peer2.connect((ip,portt))

    
    while(True):
        if message:
            aux = message.split(' ')
            if aux[0] == 'ls':
                peer2peer2.send(str.encode(aux[0]))
                list_files = str(peer2peer2.recv(2048).decode('utf-8'))
                table = Table(title='Arquivos')
                table.add_column("Nome", style='cyan')
                if list_files != '':
                    aux = list_files.split(' ')
                    for x in aux:
                        table.add_row(x)
                        
                    console = Console()
                    console.print('\n',table, '\n')
                    return
                
                else:
                    print('Não há arquivos disponíveis para acesso!')
                    return            
                
            elif aux[0] == 'get':
                check = True
                peer2peer2.send(str.encode(message))
                file_received = peer2peer2.recv(10000000000)
                name_file = './arquivos_compartilhaveis/baixado_' + aux[1]

                with open(name_file, 'wb') as files:
                    files.write(file_received)

                with open('meus_arquivos.txt', 'a') as files:
                    files.write(''+'baixado_' + aux[1] + ' ' + name_file)
                 
            
                return

def peer_connected(connection, address):
    while(True):
        data = str(connection.recv(1024).decode('utf-8'))
        if data:
            aux = data.split(' ')
            if aux[0] == 'ls':
                connection.send(lista_arquivos.encode())
                
            elif aux[0] == 'get':
                name_file = './arquivos_compartilhaveis/' + aux[1]
		
                with open(name_file, 'rb') as files:
                    print('abriu')
                    data = files.read()
                    connection.send(data)
            
def listening(port, value):
    peer2peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer2peer.bind(('', port))
    peer2peer.listen()
    
    while(True):
        conne, addrr = peer2peer.accept()
        print(addrr,' conectou.')
        threading.Thread(target=peer_connected,args=(conne,addrr)).start()
        
    
def menu():
    port = int(peer.recv(1024).decode('utf-8'))
    
	
    new_thread = threading.Thread(target=listening, args=(port, 1)).start()
    
    while(True):
        x = str(input())
        if x == 'quit':
            peer.sendall(str.encode(x))
            print('Desconectando...')
        
        elif x == 'peers':
            peer.sendall(str.encode(x))
            data = peer.recv(1024).decode('utf-8')
            show_peers(datas = data.split('/'))
            
        elif x.startswith('ls'):
            aux = x.split(' ')
            if (enderecos_portas[aux[1]]):
                connect_to_peer(aux[1], int(enderecos_portas[aux[1]]), 'ls')
            else:
                print('Vizinho não cadastrado na rede!')
        
        elif x.startswith('get'):
            aux = x.split(' ')
            if (enderecos_portas[aux[1]]):
                connect_to_peer(aux[1], int(enderecos_portas[aux[1]]), 'get ' + aux[2])
            else:
                print('Vizinho não cadastrado na rede!')
            
        else:
            tested()
            

menu()
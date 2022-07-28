from audioop import add
from concurrent.futures import thread
from rich.console import Console
from rich.table import Table
import socket
import threading
import sys
from random import randrange

peers = {} 
PORT = int(sys.argv[1])
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('',PORT))

def quit(conn, addr):
    conn.close()
    peers.pop(addr[0])
    print('Peer',addr,'desconectou da rede')
    
def lista_peers(conn, addr):
    lista = ''
    for x in peers:
        lista += x + ':' + str(peers[str(x)]) + '/'
        
    conn.send(str.encode(lista))

def handle_peer(conn,addr):
    while(True):
        data = conn.recv(1024).decode('utf-8')
        if data:
            if data == 'quit':
                quit(conn, addr)
                break
            
            elif data == 'peers':
                lista_peers(conn, addr)
            
            else:
                print('Comando não reconhecido!')
                
def start(port):
    print('Esperando alguém se conectar...')
    server.listen()
    while(True):
        conn, addr = server.accept()
        peers[addr[0]] = port
        conn.send(str(port).encode())
        port += 1
        print(addr[0],' entrou.')
        startThread = threading.Thread(target=handle_peer,args=(conn,addr))
        startThread.start()

port = (randrange(1234, 9999))    
start(port)

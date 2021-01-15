import socket 
import pickle
import threading
import sys

HEADERSIZE = 10
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), 1234))
username_exists = True

nickname = ""

def recive_msg():
    while True:
     
        try:
            message = client_socket.recv(1000)
            msg_str = message.decode('utf-8').strip(' ')
         
            if msg_str.startswith('/nickname'):
                msg_str = msg_str.split(" ") 
                nickname = msg_str[1]
                
            else:
                print(msg_str)
        except:
            print('Opps Server has been closed')
            sys.exit()
 

def write_msg():
    while True:
        msg = f'> : {input("")}'
        if nickname:
           msg = f'{nickname}: {input("")}'
        msg_len = msg.split()
        if len(msg_len) > 2:
           client_socket.send(bytes(msg, "utf-8"))
        



recive_msg_thread = threading.Thread(target=recive_msg)
recive_msg_thread.start()
wirte_msg_thread = threading.Thread(target=write_msg)
wirte_msg_thread.start()


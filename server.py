import socket
import select
import threading


HEADER = 10
IP = "127.0.0.1"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP, PORT))

server.listen(5)

client_list = []
client_nicknames = []



def broadcast(msg):
   
    for client in client_list:
        client.send(msg)

def private_msg(msg, reciver_nickname,senders_nickname):
    msg_turned_to_bytes = bytes(f'[Private_msg]{senders_nickname}  :  {msg}','utf-8')
    index = client_nicknames.index(reciver_nickname)
    reciver_socket_address = client_list[index]
    reciver_socket_address.send(msg_turned_to_bytes)



def handle_msg(client):
    
    while True:
        try:
            message = client.recv(4096).decode('utf-8') ###  k : /private jack xup 
            message_striped_without_nickname = message.strip(' ') #### this removes the username and colon leaving  /private jack xup 
            if message_striped_without_nickname.startswith('/'): 
                msg_list = message_striped_without_nickname.split()
                if msg_list[0] == '/private':
                    if msg_list[1] in client_nicknames:
                        senders_index = client_list.index(client)
                        senders_nickname = client_nicknames[senders_index]
                        reciver_nickname = msg_list[1]
                        senders_message = " ".join(msg_list[2:])
                        private_msg(senders_message,reciver_nickname,senders_nickname )
                    else:
                        client.send(bytes('sorry seems like user does not exist', 'utf-8'))

            else:
                index = client_list.index(client)
                nickname = client_nicknames[index]
                msg = bytes(f'{nickname} : {message}','utf-8')
                broadcast(msg)
    
        except:
            index = client_list.index(client)
            client_list.remove(client)
            nickname = client_nicknames[index]
            message = bytes(f'{nickname} has left the chat','utf-8')
            broadcast(message)
            client_nicknames.remove(nickname)
            break

def verify(client_socket):
    nickname_exist = False
    while not nickname_exist:

        client_socket.send(bytes(f'Please enter a nickname : ', 'utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8').strip(' ')
      

        
        if nickname not in client_nicknames:
            
            client_list.append(client_socket)
            client_nicknames.append(nickname)
            print(client_nicknames)
            client_socket.send(bytes(f'/nickname {nickname}', 'utf-8'))
            notify = bytes(f'{nickname} has joined chat', 'utf-8')
            broadcast(notify)
            nickname_exist = True
            thread = threading.Thread(target=handle_msg, args=(client_socket,))
            thread.start()
        else:
            client_socket.send(bytes(f'Nick name taken ,Please enter a nickname : ', 'utf-8'))
        


def recive_connection():
    while True:
            client_socket , address = server.accept()
            verify_thread = threading.Thread(target=verify, args=(client_socket,))
            verify_thread.start()


thread = threading.Thread(target=recive_connection)
thread.start()
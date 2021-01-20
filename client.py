import socket 
import pickle
import threading
import sys
import tkinter as tk

HEADERSIZE = 10
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = "127.0.0.1"
# ip = "9bae050eba34.ngrok.io"
client_socket.connect((ip, 12345))
username_exists = True

nickname = ""

def recive_msg():
    while True:  
        try: 
            message = client_socket.recv(1024)
            msg_str = message.decode('utf-8').strip(' ')
            if msg_str.startswith('/nickname') and "QUIT" not in msg_str:
                try:
                    nickname_display = msg_str[10:]
                    msg_list.insert(tk.END, msg_str)
                    top.title(f'Chat {nickname_display}')
                except:
                    break
            elif "QUIT" in msg_str:
                try:
                    print(msg_str)
                except:
                    print('error')
                    break
            else:
                try:
                    msg_list.insert(tk.END, msg_str)
                    print(msg_str)
                except:
                    print('error')
                    break

        except :
            server_msg = 'Opps Server something wrong with server try again later'
            msg_list.insert(tk.END, server_msg)
            sys.exit()
            break
 

def write_msg(event=None):
        
        msg = my_msg.get()
        
        my_msg.set(" ")
        if msg != " " and msg != "QUIT":
            client_socket.send(bytes(msg, "utf-8"))
        elif msg == "QUIT":
            client_socket.send(bytes(msg, "utf-8"))
            print('des')
            sys.exit()
            top.destroy()
        

def on_closing(event=None):
        top.destroy()
        client_socket.send(bytes("QUIT", "utf-8"))
        

top = tk.Tk()
top.title('Chat')

message_frame = tk.Frame(top)
my_msg = tk.StringVar()
my_msg.set(" ")
scrollbar = tk.Scrollbar(message_frame)

msg_list = tk.Listbox(message_frame, height=15, width=50, yscrollcommand=scrollbar.set)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
message_frame.pack()

entry_field = tk.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", write_msg )
entry_field.pack()

send_button = tk.Button(top, text='send', command=write_msg)
send_button.pack()


top.protocol("WM_DELETE_WINDOW", on_closing)

recive_msg_thread = threading.Thread(target=recive_msg)
recive_msg_thread.start()
tk.mainloop()


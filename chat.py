import os
import socket
import select
import sys
import threading
from time import sleep

HEADER = 1024
IP = socket.gethostbyname(socket.gethostname()) #gets local IP address for current device connected to the router
PORT = int(sys.argv[1])
FORMAT = 'utf-8'
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating socket. (over the internet, type)
ADDR = (IP, PORT) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(ADDR) #Binding the socket(server) to the address so that anything that connects to this address will hit that socket
server_socket.listen() #listening for connections
sockets_list = [server_socket]
client_list = []
connection_ID = 0

tempClientList = []
tempClientSocket = []

####### Target destination #########
destinationIPInput = ""
destinationPortInput = 0


print(f'Listening for connections on {IP}:{PORT}...')
def server_func():
    try:
        
        while True:
            #read_socket is the socket list and the "_" is an empty list and the exception_sockets is the sockets_list, 
            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
                
            try:
                #accepts the socket connection from a client. Client_socket is the socket itself, and the client_address is the address of the client.
                client_socket, client_address= server_socket.accept()
                #adding client socket to socket list
                sockets_list.append(client_socket)
                #adding client's IP and Port to client_list
                client_list.append(client_socket.getpeername())
                global tempClientList
                global tempClientSocket
                #creating temp variables for the connected clients incase of disconnection
                tempClientList = client_socket.getpeername()
                tempClientSocket = client_socket

                print(f"{client_socket.getpeername()} has Connected")
                #listening for data to see if a client has disconnected.
                def listen_for_data():
                    
                    try:
                        #check to recieve data from client
                        client_socket.recv(4096)
                        
                    except:
                        #no data has been recieved signafying the client has disconnected
                        print(f"A client has Disconnected")
                        try:
                            #removing the disconnected client from our socket list and client list
                            client_list.remove(tempClientList)
                            sockets_list.remove(tempClientSocket)
                        except:
                            print("")
                       
                    
            except:
                print("Connection to client failed")
            #letting the server listen for data on it's own thread
            t4 = threading.Thread(target= listen_for_data)
            t4.start()
            sleep(1)
        
    except:
        print("Server crashed")    

index = None
#creating a list of servers the client is connected to
client_list2 = []
#function for starting a connection using the destination IP and destintion Port as Inputs
def startConnection(destinationIPInput,destinationPortInput):
    try:
        #creating socket for each client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = (destinationIPInput,destinationPortInput)
        #adding the address the client connected to
        client_list2.append(ADDR)
        #getting the index of the client in the client list to later be referenced
        index = client_list2.index(ADDR)
        #connecting client socket to destintion address provided by user
        client_socket.connect(ADDR)
        print(f"Connected to: {ADDR}")
    except:
        print("connection failed")

    #function for listening to messages once a client has connected to a server
    def listen_for_messages():
        try:
            # will not pass this line of code until we recieve data from our client
            client_socket.setblocking(1)
            #recieving data on client socket
            msg = client_socket.recv(HEADER)
            
            while msg:
                #if no data is being recieved the user has disconnected
                if (not msg):
                    print("user has disconnected")
                    #closing the client socket if the user has disconnected
                    client_socket.close()
                    break
                #recieving the message from the client
                msg = client_socket.recv(HEADER)
                print(f"Message Recieved:  {msg.decode(FORMAT)}")
                
        except:
            #if no data is being recieved from the client socket, client has been disconnected
            print(f"Your connection with {client_list2[index]} has been terminated")
            #remove client from their local client list
            client_list2.remove(client_list2[index])
            
    #having clients listening for messages on it's own thread
    t3 = threading.Thread(target= listen_for_messages)
    t3.start()
    sleep(1)
    

        
#function for terminating a connection
def terminateConnection():
    try:
        print("Enter connection ID of connection you would like to close")
        global connection_ID
        #gathering the ID of the connection the user wishes to close
        connection_ID = int(input())
        print(f"terminating #{connection_ID}'s connection")
        #removing target client socket from the list of clients
        client_list.remove(client_list[connection_ID-1])
        #storing the client socket in a temp before closing connection
        temp_socket_list = sockets_list[connection_ID]
        #closing client connection using the socket list
        sockets_list[connection_ID].close()
        #updating the socket list to remove the disconnected client's socket
        sockets_list.remove(temp_socket_list)
        sleep(1)
       
    except:
        print("Client does not exist")

#message for encoding and sending a message to a specific client
def send_msg():
    try:
        #gathering the connection ID the user wishes to send a message to
        print("What is the connection ID for this message")
        connection_ID_msg = int(input())
        #gathering the message that the user wishes to send to the target
        print("what is the message you would like to send")
        message = input()
        #encoding the message given by the user using utf-8
        message = message.encode(FORMAT)
        #creating the header for the message
        message_header = f"{len(message):<{HEADER}}".encode(FORMAT)
        #sending the message header and message from the user to the destination connection id through the socket list
        sockets_list[connection_ID_msg].send(message_header + message)
    except:
        print("Message could not be sent")

#function for creating the list of clients
def client_connections_list():
    try:
        print("\n")
        print("List of connections on this server: ")
        #numbering the list of clients in client list to improve UI for user
        for i in client_list:
            print(client_list.index(i) +1, end=' ')
            print(" ",i)
        #if there are no clients on the client list, inform user
        if(len(client_list) == 0):
            print("There is no one connected to this server")
        print("\n")
        #displaying and numbering the list of servers a client is connected to
        print("List of servers you are connected to: ")
        for i in client_list2:
            print(client_list2.index(i) +1, end=' ')
            print(" ",i)
        #if a client is not connected to any servers, inform the user
        if(len(client_list2) == 0):
            print("You are not connected to any servers \n")
    except:
        print("Could not get client list")
    
    
#function that allows user to get a display of all the actions they can take
def help_menu():
    print("******** Command Manual **************")
    print("Enter the number of the command you would like to run")
    print("1. MyIp")
    print("2. MyPort")
    print("3. Connect <destination> <port no>")
    print("4. List of all the connections")
    print("5. Terminate <connection id>")
    print("6. Send <connection id> <message>")
    print("7. exit")
    print("***************************************")

#starting/creating the server thread as soon as the chat.py file is ran
if __name__ == '__main__':
    t1 = threading.Thread(target=server_func)
    t1.start()
    sleep(1)
    
#allows users to enter the # that represents the command they wish to run
while (True):
    print("Enter Help for a full command Manual!")
    userInput = input().lower()
    if(userInput == 'help'):
        help_menu()
    elif(userInput == "1"):
        print(IP)
    elif(userInput == "2"):
        print(PORT)
    elif(userInput == "3"):
        #gathering user input for which IP and port they would like to connect to
        print("What is the destination IP of your connection")
        destinationIPInput = input()
        print("What is the destination Port number of your connection")
        destinationPortInput = int(input())
        print("")
        #start thread for each connection made
        t2 = threading.Thread(target= startConnection, args=(destinationIPInput,destinationPortInput))
        t2.start()
        sleep(1)
    elif(userInput == "4"):
        client_connections_list()
    elif(userInput == "5"):
        terminateConnection()
    elif(userInput == "6"):
        send_msg()
    elif(userInput == "7"):
        os._exit(0)
    else:
        print("Invalid Command")

    
  


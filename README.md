# Chat-Room


Chat-room is a python based terminal ran program that allows users to do the following commands:
1. enter "help" if they need to see the command menu
2. check their IP address
3. check their port #
4. Connect to other users using their IP address and port number
5. Get a list of all the connections
6. Terminate a connection
7. send messages to anyone based off the connection ID found in the list of all connections
8. exit the program

Here is the command menu:


    print("Enter the number of the command you would like to run")
    print("1. MyIp")
    print("2. MyPort")
    print("3. Connect <destination> <port no>")
    print("4. List of all the connections")
    print("5. Terminate <connection id>")
    print("6. Send <connection id> <message>")
    print("7. exit")
    print("***************************************")


#Prerequisites:
User must install python version 3.10.0 on their computer from https://www.python.org/downloads/ in order to run the files.


#Running The Application:
User must launch a terminal and must enter the command, "python chat.py <port#>". Using the command "python" to run a python file could differ depending on how system variables have been intialized.

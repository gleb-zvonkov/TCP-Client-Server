# Gleb Zvonkov
# October 19, 2021


import socket
import select
import signal
import sys


def header (message):   # create header of 10 bytes for any message
    return f"{len(message):<{10}}".encode()  # length of message is in header, it is to the left


def processMessage(clientSocket):    # method to process message
    headerMessage = clientSocket.recv(10) # recieve the header of 10 bytes
    messageLength = int(headerMessage.decode())  # conver header containing length of message into integer
    message = clientSocket.recv(messageLength)   # recieve message
    return message


def signal_handler(sig, frame):  #handle signal ctrl-c
    disconnectMessage = ('DISCONNECT CHAT/1.0').encode()   #disconnect message
    for clientSocket in clientDictionary: # Iterate over all clients in dictionary
        clientSocket.send(header(disconnectMessage) + disconnectMessage ) # send message with header to each client
    sys.exit(0) # exit


ip = 'localhost' #random ip
port = 1234  #random port
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create server socket
serverSocket.bind((ip, port)) # set up socket
serverSocket.listen(1) # set up socket
print('Will wait for client connections at port', port)

socketArray = [] # list of all sockets
socketArray.append(serverSocket)
clientDictionary = {} # dictionary of clients with key socket and containg username

while True: # infinite loop to recieve and send messages
    signal.signal(signal.SIGINT, signal_handler)  # signal catches when user presses ctrl-c, signal handler function is activated
    allSockets = select.select(socketArray, [], []) [0]  # socket blocking set up
    
    for currentSocket in allSockets:   # loop throught all sockets
    
        if currentSocket == serverSocket: # if new client connected
            clientSocket, addr = serverSocket.accept()  # create newe unqiue client socket
            registrationMessage= processMessage(clientSocket) # receive the registration message
            registrationMessagePart = registrationMessage.decode().split(" ")   # parse the registraion message by space
            
            if ( (registrationMessagePart[0] != 'REGISTER') or (registrationMessagePart[2] != 'CHAT/1.0') ): # if registration message is incorrect
                errorMessage = '400 Invalid registration'.encode() # create error message
                clientSocket.send(header(errorMessage) + errorMessage); # send error message with header to client
                print('400 Invalid registration')
                break # break out of for loop
            
            breakloop= False # to break out of for loop if necessary
            for client in clientDictionary: # loop through all client
                if clientDictionary[client] == registrationMessagePart[1]: # if existant cleint username is equal to new client username
                    errorMessage = '401 Client already registered'.encode()
                    clientSocket.send(header(errorMessage) + errorMessage); # send error message with header to client
                    print('401 Client already registered')
                    breakloop = True # break out of for loop for all client
                    break
            if (breakloop == True):
                break # breakout of for loop for sockets
                
            errorMessage = '200 Registration successful'.encode()
            clientSocket.send(header(errorMessage) + errorMessage);  # if no errors send success message to client
            
            clientDictionary[clientSocket] = registrationMessagePart[1]   #save username of new client
            socketArray.append(clientSocket) # add accept socket to socket list

            print('Accepted connection from:', addr )
            print('Connection to client establish, waiting to recieve messages from user \'' + registrationMessagePart[1] + '\'...' );
            
        else:  # if not new client socket, so socket that has already been registered
            message = processMessage(currentSocket)   # process message
            user = clientDictionary[currentSocket] # retrieve user from client dictionary
            
            disconnectMessage = 'DISCONNECT '+ user + ' CHAT/1.0' # disconnect message that could be sent by client
            if (message.decode() == disconnectMessage): # if client sent disconnect message
                print('Client: '+ user + ' is disconnecting from server')
                socketArray.remove(currentSocket)   # Remove socket client from socket list
                del clientDictionary[currentSocket] # Remove client form client dictironary
                continue # continue loop to next iteration, no need to send print received message or send message to other clients

            print('Received message from user '+ user +':  '+ message.decode() )   # print message recieved from server
            
            for clientSocket in clientDictionary: # Iterate over all clients
                if clientSocket != currentSocket:     # do not send message to current client himself
                    clientSocket.send(header(message) + message) # send message with header to clients
                    
    

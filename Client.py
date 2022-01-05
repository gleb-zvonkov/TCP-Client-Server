# Gleb Zvonkov
# October 19, 2021


import socket
import select
import sys
import errno
import signal
from urllib.parse import urlparse


def messageWithoutHeader ():   # method to remove header from message
    message_header = clientSocket.recv(10)   # only read 10 bytes since header is 10 bytes
    message_length = int(message_header.decode())   # convert header into integer, the integer is the length of the message
    return clientSocket.recv(message_length).decode() # read number of bytes specified in header, return the message


def header (message):  # create header of 10 bytes for any message
    return f"{len(message):<{10}}".encode() # length of message is in header, it is to the left


def signal_handler(sig, frame):   # method to handel crtl-c
    disconnectMessage = ('DISCONNECT '+ usernameInput+' CHAT/1.0').encode()  #disconnect message
    clientSocket.send(header(disconnectMessage) + disconnectMessage) #send disconnect message to server
    sys.exit(0)  # exit, client is finished
    

usernameInput = sys.argv[1] #first argument is username
url= sys.argv[2] #second argument is url
x = urlparse(url).netloc.split(":")  # parese the url and split at :  to get only ip adress and port

print('Connect to server ...')
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #create client socket
try:
    clientSocket.connect((x[0], int(x[1])))   #connect client to server
except (socket.error, socket.gaierror) as e:  # if address of server is invland exception is caught
    print ("ERROR: Invalid Adress")
    sys.exit(1) # exit, client is finished

registrationMessage = ('REGISTER '+ usernameInput+' CHAT/1.0').encode()  #registration message used to connect to server
clientSocket.send(header(registrationMessage) + registrationMessage) # send registration message with header
print('Connection to server established. Sending intro message ...')

errorMessage = messageWithoutHeader () # receive response from server after registration message sent
if (errorMessage == '400 Invalid registration'  or  errorMessage == '401 Client already registered' ): # if server response is error
    print('ERROR:' + errorMessage) # specifiy error
    sys.exit() # exit, client is finished
if (errorMessage == '200 Registration successful'): # if server response is sucesfull then print to indiciate and continue
    print('\nRegistration succesful. Ready for messaging!')

clientSocket.setblocking(False) # client socket not blocking
print ('> ', end="", flush=True ) # printed to maintain chat format

while True: # infinite loop to receiver message and send message forever
    signal.signal(signal.SIGINT, signal_handler)   # if client presses ctrl-c then signal activates signal handler method
    inputExists = select.select([sys.stdin], [], [], 1)[0]  # cause stdin to not block when messages sent
    
    if inputExists: # if client enters message
        input = sys.stdin.readline().rstrip()   # read client input
        message = ('@'+ usernameInput +': ' + input).encode() # create message to be sent with proper format
        clientSocket.send(header(message) + message)  # send message with header

    try:   #error caused since because of non block
        while True:
            message = messageWithoutHeader ()  # get message recieved
            if message == 'DISCONNECT CHAT/1.0':  # if message is disconnect
                print("Server has Disconnected") # print message to show cause of exit
                sys.exit() # if no server no client so exit
            print('>\n'+message) # Print message for client
            print ('> ', end="", flush=True ) # printed to maintain chat format
    except IOError as e:     #catch the error cause by non blocking
        continue  # do nothing
        

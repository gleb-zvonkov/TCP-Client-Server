Gleb Zvonkov 
October 19, 2021

Server 
Server does not take any command line argument. 
No input is taken by server. You can press ctrl-c to stop it.
I ran server via mac terminal with python3.
Server notifies when client name is already in use.
Server notifies when invalid registration, because message  "REGISTER username CHAT/1.0" is not formatted correct.
Server notifies when a client has disconnected. 

Client 
Client takes two command line arguments  the username and a URL containgin port and ip.  
The URL must be in the format  chat://host:port.  For example python3 client.py Gleb chat://192.158.1.38:5432. 
Once client is connected and registered succesfull
Message input is accepted by client. You can press ctrl-c to stop it.
I ran client via mac terminal with python3. 
Client notifies when client name is already in use.
Client notifies when invalid registration, because message  "REGISTER username CHAT/1.0" is not formatted correct.
Client notifies when it attempts to connect to invalid adress.
Client notifies when server has disconnected. 

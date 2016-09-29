import socket   #for sockets
import sys  #for exit
 
try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except (socket.error, msg):
    print ('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
    sys.exit();
 
print ('Socket Created')
 
host = '127.0.0.1'
port = 8888

 
#Connect to remote server
s.connect((host , port))
 
print ('Socket Connected to ' + host + ' on ip ' + str(port))

#Send some data to remote server
message = 'Hello Server!'
 
try :
    #Set the whole string
    #s.sendall(bytes(message, 'UTF-8'))
    s.sendall(message)
except socket.error:
    #Send failed
    print ('Send failed')
    sys.exit()
 
print ('Message send successfully')
 
#Now receive data
reply = s.recv(4096)
 
print (reply)

s.close()

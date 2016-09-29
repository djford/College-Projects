#import socket module
import sys
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
#Fill in start
HOST = 'localhost'
PORT = 8888
try:
    serverSocket.bind((HOST, PORT))
except:
    sys.exit

serverSocket.listen(10)
#Fill in end
while True:
    #Establish the connection
    print ('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()#Fill in start #Fill in end
    try:
        message = connectionSocket.recv(1024)#Fill in start #Fill in end
        print(message)
        if(message != ""):
            filename = message.split()[1]
            print("looking for file ", filename)
            f = open(filename[1:])
            outputdata = f.read() #Fill in start #Fill in end
            #Send one HTTP header line into socket
            #Fill in start
            Myheader = "HTTP/1.1 200 OK\r\n\r\n"
            print (Myheader)
            print(outputdata)
            connectionSocket.sendall(Myheader)
            print (Myheader)
            print(outputdata)
            #Fill in end
            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i])
            connectionSocket.close()
        
    except IOError:
        #Send response message for file not found
        #Fill in start
        Errorheader = "HTTP/1.1 404 Not Found\r\n\r\n"
        print(Errorheader)
        connectionSocket.sendall(Errorheader)
        #Fill in end
    #Close client socket
    #Fill in start
    connectionSocket.close()
    #Fill in end
serverSocket.close()

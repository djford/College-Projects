#import socket module
import sys
import threading
import time
from socket import *
def server(connectionSocket):
    print ("Starting a new thread")
    try:
        message = connectionSocket.recv(1024)
        print(message)
        if(message != ""):
            filename = message.split()[1]
            print("looking for file ", filename)
            f = open(filename[1:])
            outputdata = f.read()
            extension = filename.split(".")[1]
            
            if(extension == "gif"):
                content = "image/gif"
            elif(extension == "jpeg"):
                content = "image/jpeg"
            elif(extension == "png"):
                content = "image/png"
            else:
                content = "text/html"
            
            #Send one HTTP header line into socket
            Myheader = "HTTP/1.1 200 OK\r\nContent-Type: " + content + "\r\n\r\n"
            print (Myheader)
            print(outputdata)
            connectionSocket.sendall(Myheader)
            print (Myheader)
            print(outputdata)
            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i])
            connectionSocket.close()
        
    except IOError:
        if(filename == "/helloworld.html"):
            connectionSocket.send("HTTP/1.1 301 Moved Permanently\r\n Location: http://www.hello_world2.html\r\n\r\n")
            connectionSocket.send("<html><head></head><body><h1>301 Moved Permanently</h1></body></html>\r\n")
        else:
            #Send response message for file not found
             connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
             connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
             #Close client socket
             connectionSocket.close()
    return

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
HOST = 'localhost'
PORT = 8888
try:
   serverSocket.bind((HOST, PORT))
except:
   sys.exit

serverSocket.listen(10)




    
while True:
    #Establish the connection
    print ('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    threads = []
    t = threading.Thread(target=server, args=(connectionSocket,))
    threads.append(t)
    t.start()
    
serverSocket.close()
    

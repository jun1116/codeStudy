from socket import * 
serverName = 'hostname'
serverPort = 12000
clientSocket = socket(socket.AF_INEF, socket.SOCK_DGRAM)
message = raw_input("INPUT LOWERCASE SENTENCE:")
clientSocket.sendto(message, (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage)
clientSocket.close()
#!/usr/bin/python3

import socket
import sys
from fonctions import cleClient, dechiffrementRSA

server_address = socket.gethostbyname("localhost")
server_port = 8790
my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
my_socket.connect((server_address,server_port))

[n_c, d_c] = cleClient()
nom_client = input("Entrez votre nom s'il vous plaît. \n")
print("Ma clé publique n est : "+str(n_c))
if(nom_client == "Oscar"): # Easter Egg lol
	print("Oscar est supposé écouter le canal, pas participer à la conversation... \n")
	sys.exit(1)

while 1 :
	toSend = str(n_c) + "|"
	my_socket.sendall(bytes(toSend, "utf-8"))
	dataRcv = my_socket.recv(4096)
	temp = dataRcv.decode("utf-8")
	print("Vous avez reçu le message suivant : \n"+temp)
	if dataRcv :
		lst = temp.split("|")
		plaintext = dechiffrementRSA(lst, n_c, d_c)
		reponse = input("Voulez-vous voir le message déchiffré ? Répondre par Oui ou Non. \n")
		if(reponse[0] == "O" or reponse[0] == "o"):
			print("Après déchiffrement : " + str(plaintext))
#Pour les smileys, il faut avoir installé fonts-emojione depuis son terminal, par la commande sudo apt install fonts-emojione par exemple
#!/usr/bin/python3

from premier import * # ou * pour tout import

n = int(input("Indiquer la taille du nombre n souhaité. \n")) 
p = premier(creationNombreTaille(n))
q = premier(creationNombreTaille(n))
print("Le premier nombre premier est : "+ str(p))
print("Le second nombre premier est : "+str(q))

n = p * q
print("n = p*q = "+str(n))
euler = (p-1) * (q-1)
print("phi(n) = (p-1) * (q-1) = "+str(euler))
mes = "test de message probablement envoyé sur le réseau"
#print(cipher_rsa(mes))
# On envoie ensuite le msg au serveur qui decipher_rsa(msg) paquet par paquet

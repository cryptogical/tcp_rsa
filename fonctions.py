#!/usr/bin/python3

import random
import subprocess
import re

e=65537
KEY_SIZE = 15

def creationNombreTaille(n):
	tab_entier = []
	random.seed()
	tab_entier.append(random.choice('1379')) #On ne veut pas de nombre pair, d'où le choix de ces chiffres
	for i in range(1,int(n)-1):
		tab_entier.append(random.choice('0123456789')) #On peut peut-être utiliser random.choices pour ne pas avoir à écrire la boucle mais ici ça marche très bien
	tab_entier.append(random.choice('123456789'))
	tab_entier.reverse() # = tab_entier[::-1]
	nombre1 = ""
	for i in range(len(tab_entier)):
		nombre1 += tab_entier[i]
	return nombre1

def premier(n):
	commande = subprocess.run("openssl prime %d " % int(n), shell=True, stdout=subprocess.PIPE)
	exp_reg = re.compile( r"is not prime")
	resultat=exp_reg.search(str(commande.stdout))
	while(resultat):
		tab = list(str(n)) #On crée un tableau dont les éléments possèdent chacun un caractère de n
		n = ""
		if (tab[1] == '0'): #Si à l'étape précédente on avait n=50421 par exemple, alors le prochain nombre sera 042XX, c'est à dire 42XX et ainsi on n'aura un nombre de la taille souhaitée - 1
			tab[1] = random.choice('123456789') #Cette commande évite ce problème
		for i in range(0,len(tab)-2):
			tab[i] = tab[i+1]
			n += tab[i]
		tab[-2] = random.choice('0123456789')
		n += tab[-2]
		tab[-1] = random.choice('1379') #on ne choisit que des nombres impairs. Les nombres pairs ne pouvant pas être premier
		n += tab[-1]
		commande = subprocess.run("openssl prime %d "% int(n), shell=True, stdout=subprocess.PIPE)
		resultat = exp_reg.search(str(commande.stdout))
	return int(n)

def egcd(a,b):
	x,y,u,v = 0,1,1,0
	while(a != 0):
		q,r = b//a , b%a
		m,n = x-u*q , y-v*q
		b,a,x,y,u,v = a,r,u,v,m,n
	pgcd = b
	return pgcd,x,y

def inverseModulo(a,m):
	gcd,x,y = egcd(a,m)
	if gcd != 1:
		return None
	return x%m

def powmod(x,y,n):
	result = 1
	while y > 0:
		if y&1>0:
			result = (result*x)%n
		y >>= 1
		x = (x*x)%n
	return result

def cleServeur():
	p_s = premier(creationNombreTaille(KEY_SIZE))
	q_s = premier(creationNombreTaille(KEY_SIZE))
	d_s = inverseModulo(e, (p_s - 1) * (q_s - 1))
	return [p_s * q_s, d_s]

def cleClient():
	p_c = premier(creationNombreTaille(KEY_SIZE))
	q_c = premier(creationNombreTaille(KEY_SIZE))
	d_c = inverseModulo(e, (p_c - 1) * (q_c - 1))
	return [p_c * q_c, d_c]


def chiffrementRSA(plaintext, key_client):
	lst = [str(ord(k)) for k in plaintext]
	while (len(lst) % 3 != 0):
		lst.append(str(ord('ゑ'))) #Easter Egg : le caractère 'ゑ' est la lettre E en japonais, et est celui le moins utilisé afin de minimiser la perte d'information
	for i in range(0,len(lst)):
		while (len(lst[i]) < 6): 
			lst[i] = "4" + lst[i]
	cipher = ""
	lst2 = []
	for i in range (0,len(lst),3):
		lst2.append(lst[i] + lst[i+1] + lst[i+2])
	for element in lst2:
		cipher += str(powmod(int(element), e, int(key_client))) + "|"
	new_string = cipher[:-1]
	return new_string

def dechiffrementRSA(ciphertext, n_c, d_c):
	decipher = ""
	for element in ciphertext:
		decipher += str(powmod(int(element), int(d_c), int(n_c))) + "|" # effectue c^d % n_c pour déchiffrer et concatène en séparant par "|"
	new_string = decipher[:-1] # on supprime le dernier "|" superflu
	new_string = new_string.split("|")
	decipher = []
	for i in range(0,len(new_string)):
		for j in range(0, len(new_string[i]), 6):
			decipher.append(new_string[i][j] + new_string[i][j+1] + new_string[i][j+2] + new_string[i][j+3] + new_string[i][j+4] + new_string[i][j+5])
			# On créé une nouvelle liste composé des 6 caractères successifs de la liste précédente
	for i in range(0,len(decipher)):
		for j in range(0,len(decipher[i])):
			while(decipher[i][j] == "4" and len(decipher[i]) > 2):  # La deuxième condition sert à ce que les virgules apparaissent. Aucun caractère utf-8 en-dessous de 10 
																	# ne nous intéresse vraiment (ce ne sont pas des caractères)
				decipher[i] = decipher[i][1:]
			else:
				break
	lstDecipher = [chr(int(k)) for k in decipher] # On créer une liste composée des caractères correspondants aux ordres dans la liste decipher
	if(lstDecipher[-1] == "ゑ"):
		lstDecipher = lstDecipher[:-1]
	if(lstDecipher[-1] == "ゑ"):
		lstDecipher = lstDecipher[:-1] # On supprime les caractères liés au padding
	final = ''.join(lstDecipher) # On cast la liste en chaîne de caractère
	return final # On retourne le message déchiffré
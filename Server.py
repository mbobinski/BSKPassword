#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from socket import *
from random import randint

def ELGServ(client):
    test = client.recv(1024).split(',')
    M = randint(1,int(test[2]))
    k = 127
    c1 = (int(test[1])**k) % int(test[2])
    c2 = (M*int(test[0])**k) % int(test[2])
    client.send(str(c1)+","+str(c2))
    if(M != int(client.recv(1024))):
        return 1
    return 0

#utworzenie gniazda AF_INET - IPv4, SOCK_STREAM - gniazda TCP
s = socket(AF_INET,SOCK_STREAM)
#owiązdanie do portu 8888
s.bind(('',8888))
s.listen(5)

#Stworzenie słownika loginów
login = {}

#funkcja tworząca konto
def create_account(client,log,passw):

    #sprawdzenie wszystki utworzonych loginow
    for nick in login:
        #jeżeli jest już taki login użyty - wypisz komunikat i zakończ funkcję
        if(nick == log):
            client.send("Podany login jest zajęty")
            return 0;
    #jeżeli nie ma takiego loginu - dodaj login i hasło do słownika
    login[log] = passw
    #odesłanie komunikatu zwrotnego
    print "Użytkownik "+log+" zostal zarejestrowany"
    client.send("Konto zostalo zalozone")
    
def login_account(client,log,passw):
    #sprawdzenie wszystki utworzonych loginow
    for nick in login:
        #login poprawny
        if(nick == log):
            if(login[log] == passw):
                #hasło poprawne
                client.send("Zostales zalogowany")
                print "Użytkownik "+log+" zostal zalogowany"
                return 0;
            else:
                #hasło błędne
                client.send("Błędne hasło")
                return 0;
    #błędny użytkownik
    client.send("Nie ma takiego użytkownika")
    
def change_password(client,log,passw,newpassw):
    #sprawdzenie wszystki utworzonych loginow
    for nick in login:
        #login poprawny
        if(nick == log):
            if(login[log] == passw):
                #hasło poprawne
                login[log] = newpassw
                client.send("Hasło zostało poprawnie zmienione, zaloguj się ponowanie")
                print "Użytkownik "+log+" zmienił hasło"
                return 0;
            else:
                #hasło błędne
                client.send("Błędne hasło, zostałeś wylogowany")
                return 0;
    #błędny użytkownik
    client.send("Nie ma takiego użytkownika")

while 1:
    #odebranie połączenia
    client, addr = s.accept()
    test = ELGServ(client)
    if(test == 1):
        client.send("Wykryto próbę włamania, połączenie zerwane!")
        break;
    else:
        client.send("Autoryzajca przebiegła pomyślnie")
    #odbiór danych - umieszczenie w tablicy, rozdzielając przysałny ciąg dzięki przecinkom
    message = client.recv(1024).split(',')
    #jeżeli c - to stwórz konto
    if(message[0] == "c"):
        create_account(client,message[1],message[2])
    #jeżeli l - to zaloguj
    if(message[0] == "l"):
        login_account(client,message[1],message[2])
    #jezeli z - to zmień hasło
    if(message[0] == "z"):
        change_password(client,message[1],message[2],message[3])        
    #zamknięcie połączenia
    client.close()
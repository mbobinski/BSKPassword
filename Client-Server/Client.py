#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from socket import *
from random import randint
import hashlib

#Rozszerzony algorytm euklidesa - znajduje odwrotność modulo
def odw(a,b):
    u = 1 
    x = 0
    w = a 
    z = b
    while w != 0:
        if(w < z):
            q = u 
            u = x 
            x = q
            q = w 
            w = z 
            z = q
        
        q = w / z
        u = u - q * x
        w = w - q * z
    if(z == 1):
        if(x < 0): 
            x += b
        return x
    else:
        return -1

#algorytm El Gamal'a
def ELGClient(s):
    p = 229
    g = 6
    a = randint(1,p-2)
    b = (g**a) % p
    #Przesłanie klucza publicznego do servera
    s.send(str(b)+","+str(g)+","+str(p))
    #Odebranie liczb do rozszyfrowania
    test = s.recv(1024).split(',')
    M = long(test[1])*odw(long(test[0])**a,p)%p
    #Przesłanie do servera odpowiedzi na pytanie
    s.send(str(M))
    test = s.recv(1024)
    if(test == "Wykryto próbę włamania, połączenie zerwane!"):
        print test
        return 1
    else:
        return 0

#Pętla nieskończona, w której można wybierać pomiędzy funkcjonalnościami programu
while 1:
    #utworzenie gniazda AF_INET - IPv4, SOCK_STREAM - gniazda TCP
    s = socket(AF_INET, SOCK_STREAM) 
    #nawiązanie połaczenia
    s.connect(('localhost', 8888))
    #przedstawienie się serverowi
    test = ELGClient(s)
    if(test == 1):
        break;
    #wczytanie z klawiatury informacji o wybranej przez użytkownika akcji
    inpt = raw_input("Jeżeli chcesz się zalogować wciśnij - l, jeżeli stworzyć konto - c: ")
    print inpt
    #jeżeli niepoprawna akcja - przerwij pętlę
    if(inpt != 'l' and inpt != 'c'):
        break;
    else:
        #jeżeli akcja poprawna, podaj login i hasło z klawiatury
        login = raw_input("Podaj login: ")
        password = raw_input("Podaj haslo: ")
        #sprawdzanie czy hasło ma więcej niż 6 znaków
        if(len(password) >= 6):
            temp = ""
            #jeżeli 'l' - to zaloguj
            if(inpt == "l"):
                temp = "l,"
            #jeżeli 'c' - to zarejestruj
            if(inpt == "c"):
                temp = "c,"
            
            temp += login+","+hashlib.sha256(password).digest()
            s.send(temp)
            message = s.recv(1024)
            print message
        else:
            message = ""
            print "Hasło jest za krótkie musi składać się z przynajmniej 6 znaków"
        
        #zamknij socekt            
        s.close()
        
        #ekran dla zalogowanych użytkowników
        if(message == "Zostales zalogowany"):
            while 1:
                #utworzenie gniazda AF_INET - IPv4, SOCK_STREAM - gniazda TCP
                s = socket(AF_INET, SOCK_STREAM) 
                #nawiązanie połaczenia
                s.connect(('localhost', 8888))
                #przedstawienie się serverowi
                test = ELGClient(s)
                if(test == 1):
                    break;
                inpt = raw_input("Jeżeli chcesz zmienić hasło wciśnij - z, jeżeli wylogować - w: ")
                if(inpt != "z" and inpt != "w"):
                    print "Błędny wybór, spróbuj jeszcze raz: "
                else:
                    if(inpt == "z"):
                        #szyfrowanie haseł
                        oldpassword = hashlib.sha256(raw_input("Podaj stare hasło: ")).digest()
                        password = raw_input("Podaj nowe hasło: ")
                        password2 = hashlib.sha256(raw_input("Powtórz nowe hasło: ")).digest()
                        #Sprawdzanie czy hasło spełnia wymogi długości
                        if(len(password) < 6):
                            print "Hasło jest za krótkie musi składać się z przynajmniej 6 znaków"
                        else:
                            password = hashlib.sha256(password).digest()
                            #sprawdzenie czy nowe haslo nie jest losowym ciągiem znaków
                            if(password == password2 and password != oldpassword):
                                #wysłanie zapytania o zmienie hasla
                                s.send("z,"+login+","+oldpassword+","+password)
                                print s.recv(1024)
                                break;
                            else:
                                if(password != password2):
                                    print "Nowe hasła nie są takie same"
                                elif(password == oldpassword):
                                    print "Stare i nowe hasło nie mogę być takie same!"
                    #wylogowanie wraca do ekranu logowania i rejestracji
                    if(inpt == "w"):
                        break;
                    
                s.close()
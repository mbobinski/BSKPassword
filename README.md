BSKPassword
===========

Client-Server architecture, autorisation via password (ELG, md5) Python.

Subject: Security of computer systems

Program składa się z dwóch plików:

Server.py - serwer całej aplikacji, miejsce przechowywania haseł, zawiera algorytm El Gamala, oraz hasła hashowane metodą sha256.
Client.py - aplikacja kliencka, miejsce w którym tworzymy, logujemy się oraz modyfikujemy nasze konta. Posiada drugą część algorytmu El Gamala, 
właśnie tutaj hasła są hashowane przed wysłaniem do serwera.

Instrukcja:
1. Najpierw należy uruchomić Server.py i on już sobie będzie działał (po założeniu konta, logowaniu, zmianie hasła będą się tam wyświetlały odopwiednie informacje).
2. Teraz włączamy Client.py (Tutaj będziemy pracować).
3. Pytanie od Clienta: "Jeżeli chcesz się zalogować wciśnij - l, jeżeli stworzyć konto - c:"
	3a. Wciskamy l -> prosi o podanie loginu i hasła w zależności czy dane się zgadzają z tymi z servera bądź nie daje odpowiedni komunikat.
	3b. Wciskamy c -> prosi o podanie loginu i hasła - jeżeli hasło ma minimum 6 znaków i taki login nie jest już używany zostaje stworzone nowe konto.
4. Jeżeli udało nam się zalogować, dostaniemy kolejne pytanie: "Jeżeli chcesz zmienić hasło wciśnij - z, jeżeli wylogować - w:"
	4a. Wciskamy z -> prosi o podanie starego hasła, nowego oraz powtórzenie noweg hasła -> jeżeli stare hasło się zgadza, 
	    dwa nowe są takie same i mają więcej niż 6 znaków dostaniemy komunikat o zmianie hasła i zostaniemy wylogowani, aby zalogować się nowymi danymi.
	4b. Wciskamy w -> wylogowuje nas z konta i przenosi do kroku 3.
5. Aby zakończyć program należy się wylogować, a następnie wcisnąć dowolny klawisz poza "l" i "c".

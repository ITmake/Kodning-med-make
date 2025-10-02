Beskrivning

-Detta projekt implementerar en enkel TCP-server och TCP-klient i Python för att låta flera BeagleBone Green 
(BBG)-kort kommunicera med varandra över nätverket.

-Servern körs på ett av BBG-korten och lyssnar efter inkommande anslutningar. När en klient (ett annat BBG-kort) 
ansluter skickar servern en hälsning och startar en separat tråd för att hantera kommunikationen. Detta gör att flera klienter kan prata med servern samtidigt.

Funktioner

-Enkel TCP-server som lyssnar på port 5000.
-Stöd för flera klienter samtidigt via threading.
-Klienten tar emot ett välkomstmeddelande och kan skicka text till servern.
-Servern ekar tillbaka alla mottagna meddelanden.

server.py

-Startar en TCP-server på en BeagleBone Green.
-Accepterar anslutningar från klienter.
-Skickar en hälsning: hello from BBG #1.
-Loggar inkommande meddelanden.
-Skickar tillbaka samma meddelande till klienten.

client.py

-Ansluter till servern via serverns IP-adress.
-Tar emot serverns hälsning
-Skickar ett meddelande, t.ex. hi from BBG #2.

Nätverkskrav

-Båda BeagleBone Green-korten måste vara anslutna till samma nätverk (t.ex. via Ethernet eller Wi-Fi).
-Kontrollera IP-adresser med: "ifconfig"

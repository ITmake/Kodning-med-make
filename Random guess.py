#Definiera en funktion
import random
def guess():
    num =  random.randint(1,100) # Nummer att gissa
    i = 0 # Räknare för antal försök
    gratulationer = [
    "Grattis, du gissade rätt!",
    "Rätt gissat, bra jobbat!",
    "Fantastiskt, du hittade det rätta numret!",
    "Wow, vilken träffsäkerhet!",
    "Snyggt! Du prickade in rätt siffra!",
    "Imponerande, du klarade det!",
    "Du har verkligen tur idag!",
    "Otroligt, du valde rätt!",
    "Perfekt gissning!",
    "Du är en riktig mästare på att gissa!"
]
    s_gissning = input("Gissa på ett nummer mellan 1 och 100: ")
    while True:
        i = i + 1 # i += 1 
        try:
            gissning = int(s_gissning)
        except:
            print("Ange tal, inte bokstäver")    
            s_gissning = input("Gissa nu med numror: ") 
            continue   
        if gissning > num:
            print("Ditt nummer var för stort")
        elif gissning < num:
            print("Ditt nummer var för litet")
        else:
            print(f"{random.choice(gratulationer)} Du gissade rätt på {i} försök")
            break # Avbryt while-loopen
        s_gissning = input("Gissa igen: ")

#Kör funktionen
guess()
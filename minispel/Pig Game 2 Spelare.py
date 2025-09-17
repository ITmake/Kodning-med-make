import random

def kasta(spelare):
    sum = 0
    while True:
        num =  random.randint(1,6)
        print(f"{spelare} kastar: {num}")
        if num == 1:
            print(f"Sorry, {spelare} tappade sina poäng")
            return 0
        sum += num
        print(f"Summa för detta varv: {sum}")
        val = input(f"{spelare}, tryck på k för att kasta på nytt eller s för att spara: ")
        match val: 
            case "k":
                continue
            case "s":
                return sum

def main():
    namn1 = input("Spelare 1, ange namn: ") or "Spelare 1"
    namn2 = input("Spelare 2, ange namn: ") or "Spelare 2"
    totalt = {namn1: 0, namn2: 0}
    spelare = namn1
    while True:
        print(f"\n{spelare}s tur. Totalpoäng: {totalt[spelare]}")
        totalt[spelare] += kasta(spelare)
        if totalt[spelare] >= 100:
            print(f"Grattis {spelare}, du kom upp till 100 poäng och vann!")
            break
        print(f"{spelare} har nu {totalt[spelare]} poäng")
        input("Tryck 'Enter' för att byta spelare")
        spelare = namn2 if spelare == namn1 else namn1

main()
import random
def fav():
    attempts = 0
    while True:
        num = random.randint(1,100)
        attempts += 1
        if num == 5:
            print("you guessed it right")
            print(f"It took you {attempts} attempts.")
            break
        else:
            print("wrong guess, try again")

fav()
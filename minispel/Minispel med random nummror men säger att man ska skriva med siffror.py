import random

secret_number = random.randint(1, 100)
print("Guess the number between 1 and 100!")

while True:
    try:
        guess = int(input("Your guess: "))
    except ValueError:
        print("Skriv med siffror, inte bokstäver!")
        continue
    if guess < secret_number:
        print("Too low!")
    elif guess > secret_number:
        print("Too high!")
    else:
        print("Congratulations! You guessed the number.")
        break
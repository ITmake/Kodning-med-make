#frågar bara engång#

s = input("enter a number: ").strip()
try:
    num = int(s)  #försöker göra om till heltal
    print("my favorite number is " + str(num+7))
except ValueError:
    print("bara siffror tack.")


#frågar begär att skriva pånytt om du inte skriver med siffror#

while True:
    s = input("enter a number: ").strip()
    if s.lstrip('-').isdigit():
        num = int(s)
        break
    print("bara siffror tack.")
print("my favorite number is " + str(num + 7))

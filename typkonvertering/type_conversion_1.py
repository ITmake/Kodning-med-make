s = input("enter a number: ").strip()
try:
    num = int(s)  #försöker göra om till heltal
    print("my favorite number is " + str(num+7))
except ValueError:
    print("bara siffror tack.")

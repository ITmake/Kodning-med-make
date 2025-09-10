veckodagar = ["måndag", "tisdag", "onsdag", "torsdag", "fredag", "lördag"]

veckodagar.remove("måndag")
veckodagar.append("söndag")

print("Nu kommer den printa ut alla veckodagar i ordning:")
for dag in veckodagar:
    print(dag)
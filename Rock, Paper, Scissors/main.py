import random

def gameWin(comp, you):
    
    if comp == you:
        return None
    
    elif comp == 'r':
        if you == 's':
            return False
        elif you == 'p':
            return True
        
    elif comp == 'p':
        if you == 'r':
            return False
        elif you == 's':
            return True
        
    elif comp == 's':
        if you == 'p':
            return False
        elif you == 'r':
            return True
        
        
print ("Computer Turn: Rock(r), Paper(p), Scissors(s)?")
rmd = random.randint(1, 3)
if rmd == 1:
    comp = 'r'
elif rmd == 2:
    comp = 'p'
elif rmd == 3:
    comp = 's'
    
you = input("YOU: PLEASE CHOOSE: (r)Rock, (p)Paper, (s)Scissors:\n")
a = gameWin(comp, you)

print(f"Computer chose:{comp}")
print(f"You chose:{you}")

if a == None:
    print("It is a tie")
elif a:
    print("You Win!")
else:
    print("You Lose!")
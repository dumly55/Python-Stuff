#
#   The game of "pig"
#
#   The object of the game is to score as many points as possible.
#   You can either roll a die or keep your current total.
#   If you roll a 1, you lose. If you roll any other number, it is
#   added to your current score.
#

import random

#
#   This function will repeatedly ask you if you want to roll the die
#   or hold (keep your current total). If you enter 'r' or 'R', it will
#   return 'r' (for roll); if you enter 'h' or 'H', it will return 'h' (for
#   hold). If you enter any other string, the function gives an error message
#   and asks you for input again. 

def get_roll_or_hold():
    valid = False
    while not valid:
        answer = input('R)oll or H)old? ')
        if answer in 'rRhH':
            valid = True
        else:
            print("Please enter R to roll or H to hold.")
    return answer  


#   This function will repeatedly ask you if you want to play again or not
#   If you enter 'y' or 'Y', it will return True; if you enter 'n' or 'N',
#   it will return False. If you enter any other string, the function gives
#   an error message and asks you for input again. 

def play_again():
    valid = False
    while not valid:
        answer = input('Play again? (Y/N) > ')
        if answer in 'yY':
            valid = True
        elif answer in 'nN':
            valid = False
            return valid
        else:
            print('Please enter Y for yes or N for no')
    return answer

playing = True
print('Welcome to the game of "pig."')
      
while playing:
    total = 0
    rolling = True
    while rolling:
        response = get_roll_or_hold()
        if response == 'R' or response == 'r':
            die = random.randrange(1, 7)
            print("You rolled a", die)
            if die is 1:
                print("Sorry, you lost this round")
                rolling = False
            else:
                total += die
                print("Your total is now", total)
        else:
            rolling = False


    if response == 'h' or response == 'H':
        print("Your total for this round is", total)


    print() # for spacing
    playing = play_again()  # will set playing to True or False
    print(f"playing is {playing}")

print('Thanks for playing the game.')



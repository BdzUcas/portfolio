import random

def stringify(list):
    #turn every item in the given list into a string
    return [str(i) for i in list]

#random chance based on chance given
def chance(chance):
    if random.random() <= chance:
        return True
    return False

#input from choices
def choice_input(choices,prompt = '> '):
    #loop forever
    while True:
        #take user input
        choice = input(prompt).strip().lower()
        #if it is a valid choice
        if choice in choices:
            #return it
            return choice
        #otherwise
        else:
            #tell the user to select a valid choice
            print('Please select a valid choice!')


#number input
def int_input(max = 100000,prompt='> ',min = 0):
    #loop fovever
    while True:
        #get user input
        num = input(prompt).strip()
        try:
            num = int(num)
        #if it is not a number
        except:
            #tell user
            print('Input is not a number!')
            continue
        #if it is within range
        if num <= max and num >= min:
            #return it
            return num
        else:
            print('Input is out of range!')
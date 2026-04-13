from pet_sim.formatting import *
from pet_sim.helper import *
from time import sleep
from pet_sim.pet import pet as pet_creator
from pet_sim.data import *
import random
#time variable stores current hour (1-24) in game. Doing activities increases it. As time increases events occur that can cause decreases in resources, so you have to balance your time between obtaining different resources.
time = 8
#money stores how much in-game money you have. This is gained by working and spent on food for yourself and your pets, or toys for your pets to increase hapiness.
money = 100
#inventory stores what resources you have. This includes food and toys for your pets. It is a list of strings (ie 'pet food' 'tug rope')
inventory = []
def create_pet():
    #ask user what type of pet they want and what name
    print('What type of pet do you want?\n1. Dog\n2. Cat\n3. hamster\n4. Rock')
    pet_type = choice_input(['1','2','3','4'])
    types = {'1':'dog','2':'cat','3':'hamster','4':'rock'}
    diets = {
        '1': ['kibble','canned food','hearty kibble','high-quality canned food','treats'],
        '2': ['kibble','canned food','hearty kibble','high-quality canned food','treats'],
        '3': ['seeds','high-quality seeds','treats','greens'],
        '4': ['sand']
    }
    print('What do you want to name your pet?')
    name = input()
    pet = pet_creator(name=name,type=types[pet_type],age_ticks = 0,hunger = 0,hapiness = 50,boredom = 0, diet = diets[pet_type],asleep = False, status = 'happy')
    return pet
def menu():
    #introduce user to program and give instructions
    print(f"{f('###')} Pet Simulator {f('###')}")
    print(f'Welcome to the {f('cyan', 'pet simulator')}!')
    print(f'Do you need instructions? ({f('lime','yes')}/{f('bright red','no')})')
    instruct = choice_input(['y','n','yes','no'])
    if instruct in ('y','yes'):
        print('This pet simulator lets you take care of pets!')
        sleep(1)
        print('You can have as many pets as you want, but multiple can be hard to take care of.')
        sleep(1)
        print("Pets will get hungry, bored, or sad if you don't care for them!")
        sleep(1)
        print("But properly caring for pets requires money and time, so you have to maintain a balance of work, play, and sleep.")
        sleep(1)
        print("Let's get started!")
    #ask for username
    user = input('Enter username: ')
    #if it exists
    try:
        #load data
        account_data = load_data(user)
    #otherwise
    except:
        #make new account with default data
        account_data = {"time": 8, "money": 100, "toys": [], "food": [], 'pets': [], "last tick": 8}
        save_data(user,account_data)
        print('Account Registered!')
    #forever
    while True:
        #clear screen
        print(f("clear"))
        #print time and money
        print(ftime(account_data['time']))
        print(f'${account_data['money']}')
        #if it has been 8 hours since last tick
        if account_data['time'] - account_data['last tick'] >= 8:
            #tick all pets
            for pet in account_data['pets']:
                pet.tick()
        #if it is between 10 pm and 5 am
        if account_data['time'] % 24 > 21 or account_data['time'] % 24 < 6:
            #tell the user they slept and increase time by 8 hours
            print("It's late. You go to sleep...")
            print("8 hours passed!")
            account_data['time'] += 8
            sleep(2)
            #restart loop
            continue
        #if they have pets
        if account_data['pets']:
            #display each pet and status
            print('Pets:')
            for pet in account_data['pets']:
                pet.status_update()
                print(f"  {pet.name}: {pet.status}")
        #othewise
        else:
            #tell them to make a pet
            print("Looks like you don't have any pets! Let's make one!")
            account_data['pets'].append(create_pet())
        #ask user what they want to do
        action = choice_input(['1','2','3','4'],f"What would you like to do?\n1. {f("gray","Pets")}\n2. {f("gray","Shop")}\n3. {f("gray","Work")}\n4. {f("gray","Save & Quit")}\n> ")
        match action:
            #if they chose pets
            case '1':
                #ask user what pet to interact with
                print('Which pet would you like to interact with?')
                #make a list of numbers (one for each pet)
                pet_choices = range(1,len(account_data['pets']) + 1)
                #print out all pets with their number
                for pet in pet_choices:
                    print(f"{pet}. {account_data['pets'][pet - 1].name}")
                #turn every item in pet choices into a string
                pet_choices = stringify(pet_choices)
                #get user choice
                choice = choice_input(pet_choices)
                pet = account_data['pets'][int(choice) - 1]
                #ask user if they want to check up on, play with, or feed their pet
                print(f'What do you want to do with {pet.name}?\n1. Check Up\n2. Play\n3. Feed')
                action = choice_input(['1','2','3'])
                match action:
                    #if they choose check up
                    case '1':
                        #display pet stats
                        print(f'Hapiness: {pet.hapiness}%')
                        print(f'Boredom: {pet.boredom}%')
                        print(f'Hunger: {pet.hunger}%')
                        input(f('green','press ENTER to continue >'))
                    #if they choose play
                    case '2':
                        toys = account_data['toys']
                        #if they have any toys
                        if toys:
                            #ask which one they want to play with
                            print(f'What toy do you want to play with {pet.name} with?')
                            toy_choices = range(1,len(toys) + 1)
                            for toy in toy_choices:
                                print(f'{toy}. {toys[toy - 1]}')
                            toy = choice_input(stringify(toy_choices))
                            toy = toys[int(toy) - 1]
                        #if they don't
                        else:
                            #set toy to self
                            toy = 'self'
                        #run pet's "play" method
                        broke = pet.play(toy)
                        #if the toy broke
                        if broke:
                            #remove it from toy list
                            account_data['toys'].remove(toy)
                        #advance time 2 hours
                        print('2 hours passed!')
                        sleep(1)
                        account_data['time'] += 2
                        sleep(2)
                    #if they chose feed
                    case '3':
                        food_list = account_data['food']
                        #if they have food
                        if food_list:
                            #ask what they want to feed to the pet
                            print(f'What food do you want to feed to {pet.name}? They might not like everything.')
                            food_choices = range(1,len(food_list) + 1)
                            for food in food_choices:
                                print(f'{food}. {food_list[food - 1]}')
                            chosen_food = choice_input(stringify(food_choices))
                            chosen_food = food_list[int(chosen_food) - 1]
                            #run pet's "feed" method
                            pet.feed(chosen_food)
                            account_data['food'].remove(chosen_food)
                            #advance time 2 hours
                            print('2 hours passed!')
                            sleep(1)
                            account_data['time'] += 2
                            sleep(2)
                        #if they don't
                        else:
                            #tell them they can't
                            print(f'You have no food for {pet.name}')
            #if they chose the store
            case '2':
                print('Welcome to the store!')
                sleep(1)
                store_hours = 0
                #loop forever
                while True:
                    #advance "store hours" by one
                    store_hours += 1
                    #ask them if they would like to buy a pet, buy an item, or leave
                    print('What would you like to do?\n1. Buy Pet ($50)\n2. Buy Item\n3. Exit')
                    action = choice_input(['1','2','3'])
                    match action:
                        #if they want to buy a pet
                        case '1':
                            #ask for 50 dollars
                            print("That'll be $50.")
                            if account_data['money'] >= 50:
                                account_data['money'] -= 50
                                #if they have it take it and make a pet
                                account_data['pets'].append(create_pet())
                            else:
                                print("You don't have enough money!")
                        #if they chose to buy an item
                        case '2':
                            item_costs = {"kibble": 10,"canned food": 20,"hearty kibble": 30,"high-quality canned food": 30,"treats": 5,"seeds": 10,"high-quality seeds": 20,"greens": 20,"sand": 15,"stick":5,"rope":10,"sqeaky toy":20,"frisbee":20,"string":5,"ball":15,"rock":0}
                            items = ["kibble","canned food","hearty kibble","high-quality canned food","treats","seeds","high-quality seeds","greens","sand","stick","rope","sqeaky toy","frisbee","string","ball","rock"]
                            food = ["kibble","canned food","hearty kibble","high-quality canned food","treats","seeds","high-quality seeds","greens","sand"]
                            toys = ["stick","rope","sqeaky toy","frisbee","string","ball","rock"]
                            #ask them what item to buy
                            print('What would you like to buy?')
                            item_choices = range(1,len(items) + 1)
                            for item in item_choices:
                                #display each item and its cost
                                print(f'{item}. {items[item-1]} (${item_costs[items[item-1]]})')
                            choice = items[int(choice_input(stringify(item_choices))) - 1]
                            #if they have enough money for it
                            if account_data['money'] >= item_costs[choice]:
                                #take the money and add the item to inventory
                                account_data['money'] -= item_costs[choice]
                                if choice in food:
                                    account_data['food'].append(choice)
                                elif choice in toys:
                                    account_data['toys'].append(choice)
                            else:
                                #otherwise tell them they don't have enough money
                                print("You don't have enough money!")
                        case '3':
                            #if they chose to exit
                            #advance time "store hours" amount
                            print(f'{store_hours} hours passed.')
                            account_data['time'] += store_hours
                            sleep(1)
                            #exit loop
                            break
            #if they chose work
            case '3':
                #pick a random number between 20 and 50
                print('You go to work!')
                sleep(1)
                profit = random.randint(20,50)
                #give them that much money
                print(f'You gained ${profit}!')
                account_data['money'] += profit
                sleep(1)
                #advance time 8 hours
                print('Eight hours passed!')
                account_data['time'] += 8
                sleep(2)
                continue
            #if they chose to quit
            case '4':
                #save data and end program
                save_data(user,account_data)
                print('Data saved!')
                break
import json
from pet_sim.pet import pet as pet_creator
def load_data(user):
    #turn user json into a dictionary
    with open(f'src/pet_sim/docs/user_data/{user}.json','r') as file:
            account_data = json.load(file)
    #turn pet dictionaries into objects
    pet_dicts = account_data['pets']
    pets = []
    for pet in pet_dicts:
        pets.append(pet_creator(name=pet['name'],type=pet['type'],age_ticks=pet['age_ticks'],hunger=pet['hunger'],hapiness=pet['hapiness'],boredom=pet['boredom'],diet=pet['diet'],asleep=pet['asleep'],status=pet['status']))
    account_data['pets'] = pets
    #return account data
    return account_data
def save_data(user,account_data):
    #convert pet objects to dictionaries
    pets = []
    for pet in account_data['pets']:
        pets.append(pet.__dict__)
    account_data['pets'] = pets
    #save user data
    with open(f'src/pet_sim/docs/user_data/{user}.json','w') as file:
        json.dump(account_data,file)
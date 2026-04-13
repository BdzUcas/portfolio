#BZ 1st Text Adventure Game
import time as t
import random as r
def getAction(options):
    while True:
            action_full = input().strip().lower()
            if ' ' in action_full:
                action = action_full[0:action_full.find(' ')]
                acted = action_full[action_full.find(' ') + 1:]
            else:
                action = action_full
                acted = ''
            if action in options:
                return action, acted
            else:
                print('Please select a valid action!')
def choiceInput(valid_choices, error = 'Please select a valid choice!'):
    while True:
        choice = input().strip().lower()
        if choice in valid_choices:
            return choice
        elif choice.isdigit():
            choice = int(choice)
            if choice <= len(valid_choices) and choice > 0:
                return valid_choices[choice-1]
        print(error)
def display(text = 'Message not defined!', wait = 0):
    if wait == 0:
        wait = len(text)/40
    print(text)
    t.sleep(wait)
def charismaCheck(cha,goal):
    if r.randint(1,10) + cha < goal:
        return False
    else:
        return True
def useItem(player, item):
    if item == 'dinner':
        player['hp'] = player['hp'] + 3
        if player['hp'] > player['max hp']:
            player['hp'] = player['max hp']
        else:
            display('Your HP increased by 2!')
        player['inventory'].remove('dinner')
    elif item == 'beer':
        if player['max hp'] < 7:
            player['max hp'] = player['max hp'] + 1
            player['hp'] += 1
            display('Your max HP increased!')
        player['drunk turns'] = player['drunk turns'] + 2
        player['inventory'].remove('beer')
        
    elif item in ['mustache','hat','badge','bandanna']:
        if item in player['equipped']:
            print('You already have that equipped!')
        else:
            if (item == 'bandanna') and 'hat' in player['equipped']:
                display('You remove the Cowboy Hat.')
                player['equipped'].remove('hat')
                player['charisma'] -= 1
            if (item == 'hat') and 'bandanna' in player['equipped']:
                display('You remove the Bandit Bandanna')
                player['equipped'].remove('bandanna')
                player['charisma'] -= 1
            player['equipped'].append(item)
            player['charisma'] += 1
    display(items[item]['use'])
    return player
def combat(enemy, player):
    display(f'{enemy['name']} begins combat!')
    turn = 0
    while True:
        player['drunk turns'] -= 1
        if player['drunk turns'] > 0:
            display('You feel a little less tipsy.')
        elif player['drunk turns'] == 0:
            display('You no longer feel tipsy.')
        turn += 1
        print("Attack, Persuade, or Use?")
        action, acted = getAction(['attack','persuade','use'])
        if turn == 1:
            enemy_choice = r.choice(['persuade','attack'])
        elif enemy['hp'] < 2:
            enemy_choice = r.choice(['attack','persuade','persuade'])
        else:
            enemy_choice = r.choice(['attack','attack','persuade'])
        if action == 'use':
            if enemy_choice == 'attack':
                player['hp'] -=  2
                display(f'{enemy['name']} shoots you for two damage!')
                if player['hp'] < 1:
                    display('You died!')
                    return False
                else:
                    display(f'You have {player['hp']} health remaining!')
            elif enemy_choice == 'persuade':
                display(f'{enemy['name']} tries to persuade you to not use an item... and fails.')
            if player['inventory']:
                if acted:
                    if not acted in player['inventory']:
                        display(f'You don\'t have a {acted}')
                        continue
                    else:
                        used = acted
                else:
                    display('What item are you using?')
                    used = choiceInput(player['inventory'],'Please select a valid item to use!')
                player = useItem(player,used)
            else:
                display("You don't have an item to use!")
        elif action == 'attack':
            if enemy_choice == 'attack':
                display('You both shoot!')
                if r.randint(0,1) == 0:
                    player['hp'] -= 2
                    display(f'Your bullet goes wide! {enemy['name']} shoots you for two damage!')
                    if player['hp'] < 1:
                        display('You died!')
                        return False
                    else:
                        display(f'You have {player['hp']} health remaining!')
                else:
                    enemy['hp'] -= 1
                    display(f'You shot {enemy['name']}!')
                    if enemy['hp'] < 1:
                        if enemy['name'] != 'your Grandma':
                            display(f'{enemy['name']} dies!')
                        return player
                    else:
                        display('They survived!')
            elif enemy_choice == 'persuade':
                if player['drunk turns'] > 0:
                    persuaded = charismaCheck(enemy['charisma'], 4 + player['charisma'])
                else:
                    persuaded = charismaCheck(enemy['charisma'], 5 + player['charisma'])
                if persuaded:
                    display(f'{enemy['name']} persuades you not to shoot them!')
                else:
                    enemy['hp'] -= 1
                    display(f'You shot {enemy['name']}!')
                    if enemy['hp'] < 1:
                        if enemy['name'] != 'your Grandma':
                            display(f'{enemy['name']} dies!')
                        return player
                    else:
                        display('They survived!')
        elif action == 'persuade':
            if enemy_choice == 'attack':
                if player['drunk turns'] > 0:
                    persuaded = charismaCheck(player['charisma'] - 1, 5 + enemy['charisma'])
                else:
                    persuaded = charismaCheck(player['charisma'] - 1, 5 + enemy['charisma'])
                if persuaded:
                    display(f'You persuade {enemy['name']} not to shoot you!')
                else:
                    player['hp'] -= 2
                    display(f'You try to persuade them, but {enemy['name']} still shoots you for two damage!')
                    if player['hp'] < 1:
                        display('You died!')
                        return False
                    else:
                        display(f'You have {player['hp']} health remaining!')
            elif enemy_choice == 'persuade':
                display(f'You persuade {enemy['name']} not to persuade you to not persuade them to not persuade you to not persuade them to not persuade you')
items = {
    'cookie': {
        'name': "Grandma's Cookie", 
        'inspect': "A chocolate chip cookie from your grandma. It's still warm!",
        'use': "..For what? It looks too good to eat. Maybe someone else will take it?"
    },
    'dinner': {
        'name': "Western Dinner", 
        'inspect': "A nice western dinner of steak and potatoes. A hearty meal that will fill you up even if you're starving. Eat it to gain 2 HP (1 gun shot).",
        'use': "You eat the Western Dinner. Yum!"
    },
    'beer': {
        'name': "Western Beer", 
        'inspect': "A strong alchoholic drink traditional to Westville. What could go wrong? Increases your max HP by 1 up to 3 times.",
        'use': "You drink the Western Beer. You feel a bit tipsy."
    },
    'mustache': {
        'name': "Glue-On Mustache", 
        'inspect': "A silly mustache that attaches just below your nose. It makes you look very sophisticated. Increases your charisma when worn.",
        'use': "You equip the Glue-On Mustache. How suave! Your charisma increased!"
    },
    'hat': {
        'name': "Cowboy Hat", 
        'inspect': "A traditional western hat. Perfect for a sheriff like you! Increases your charisma when worn.",
        'use': "You don the Cowboy Hat. How dashing! Your charisma increased!"
    },
    'badge': {
        'name': "Sheriff's Badge", 
        'inspect': "A leather badge adorned with a metal star. Lets everyone know who you are! Increases your charisma and makes bandits hostile when worn.",
        'use': "You equip the Sheriff's Badge!"
    },
    'dentures': {
        'name': "Old Dentures", 
        'inspect': "An old pair of dentures... gross. Maybe an old person will want them?",
        'use': "For- what? Gross!"
    },
    'ranch': {
        'name': "Rancher Ranch", 
        'inspect': "Ranch made by a Rancher. Goes great with a salad!",
        'use': "You're just going to eat it plain? Ew!"
    },
    'milk': {
        'name': "Milk", 
        'inspect': "A bottle of cold milk. It doesn't smell very good...",
        'use': "You lift the bottle to your lips but gag at the mere taste. Maybe someone else will want it?"
    },
    'key': {
        'name': "Priest's Key", 
        'inspect': "A fancy key presumable used to unlock the church.",
        'use': "There aren't any locks around! What might it unlock?"
    },
    'handcuffs': {
        'name': "Handcuffs", 
        'inspect': "Strong handcuffs for strong criminals.",
        'use': "On who? Yourself?"
    },
    'bandanna': {
        'name': "Bandit Bandanna", 
        'inspect': "A bandanna worn by the Westville Bandits. Makes you look just like one!",
        'use': "You equip the Bandit Bandanna. Intimidating! Makes you look just like one!"
    },
    'weasel trap': {
        'name': "Weasel Trap", 
        'inspect': "A clever trap for a weasel.",
        'use': "There aren't any weasels around! Maybe there's one in the forest?"
    },
    'captured weasel': {
        'name': "Captured Weasel", 
        'inspect': "A fat weasel caught in a trap. Looks like it has been eating well.",
        'use': "You can't figure out how to get it open. Maybe Rancher Bob will want it?"
    }
}
rooms = {
    'town square': 1,
    'westaurant': 2,
    "grandma's house": 3,
    'grandmas house': 3,
    'grandma': 3,
    'grandma house': 3,
    "sheriff's office": 4,
    'sheriffs office': 4,
    'sheriff office': 4,
    'sheriff': 4,
    'clothes shop': 5,
    'church': 6,
    'ranch': 7,
    'forest': 8,
    'hideout': 9,
    'back room': 10
}
def sheriffOffice(room,player):
    if room['jay']:
        display('You are in your office building. There is a \033[36mdesk\033[0m, and a small \033[36mcell\033[0m with \033[36mJay the Outlaw\033[0m in it. There are two doors, one in the back and one in the front')
    else:
        display('You are in your office building. There is a \033[36mdesk\033[0m, and a small empty jail \033[36mcell\033[0m. There are two \033[36mdoors\033[0m, one in the \033[36mback\033[0m and one in the \033[36mfront\033[0m.')
    while True:
        print('Use, Inventory, or Inspect?')
        action, acted = getAction(['use','inventory','inspect','leave','move'])
        if action == 'inspect':
            if room['jay']:
                options = player['inventory'] + ['jay','outlaw','jay the outlaw','desk','front door','back door','door','cancel','no','nevermind','exit','cell']
            else:
                options = player['inventory'] + ['desk','front door','back door','door','cancel','no','nevermind','exit','cell']
            if acted:
                if acted in options:
                    inspected = acted
                else:
                    display(f'There is no {acted} here. Try inspecting a person to talk to them.')
                    continue
            else:
                print('What are you inspecting?')
                inspected = choiceInput(options,f'That isn\'t here. What are you inspecting?')
            if inspected == 'desk':
                display("It's a wooden desk with some papers on it. Nothing special.")
            elif inspected in ['jay','outlaw','jay the outlaw']:
                display('You approach Jay the Outlaw. He speaks out to you in a weathered voice.')
                display("> 'Ey there sheriff. Come to play at my game? Or to set me free? *wink wink*", 2)
                display('Leave, Play, or Free?')
                action = choiceInput(['leave','play','free'])
                if action == 'leave':
                    display(">'kay then, come back later!")
                    continue
                elif action == 'play':
                    display("> 'kay then, how much you wagerin'?")
                    display(f'You have ${player['money']}.')
                    while True:
                        wager = input().replace('$','').replace(' ','')
                        if wager.isdigit():
                            wager = int(wager)
                            if wager <= player['money']:
                                display("Wow! Quite confident, aren't ya?")
                                player['money'] -= wager
                                break
                            else:
                                display("> Do ya really have that much? Didn't think so.")
                        else:
                            display("While ya can't play if ya don't wager nothin'! How much?")
                    display("> I'm flippin' a coin. If it's heads, ya get the money. If it's tails, I get the money!")
                    coin = r.randint(1,2)
                    if coin == 1:
                        display('> Tails! I win. He He! Come back later!')
                    else:
                        display('> Heads! Darn.')
                        player['money'] += wager * 2
                        display(f'You got ${wager}!')
                        continue
                elif action == 'free':
                    display("> You've come to free me? Yipee! Take me handcuffs.")
                    display('You got the handcuffs!')
                    player['inventory'].append('handcuffs')
                    room['jay'] = False
                    continue
            elif inspected == 'front door':
                display("It's a wooden door. It leads to the town square")
            elif inspected == 'back door':
                display("It's a wooden door. It leads to the forest")
            elif inspected == 'door':
                display("It's a wooden door.")
            elif inspected == 'cell':
                display('It\'s an old cell, built a while ago. Still sturdy though. Jay the Outlaw is sitting inside it, flipping a coin.')
            elif inspected in ['cancel','no','nevermind','exit']:
                continue
            else:
                display(items[inspected]['inspect'])
        elif action == 'use':
            options = player['inventory'] + ['front door','back door','cancel','no','nevermind','exit']
            if acted:
                if acted in options:
                    used = acted
                else:
                    display(f'You can\'t use that.')
                    continue
            else:
                print('Use what?')
                used = choiceInput(options,'You can\'t use that! Try using the back door to move out into the forest, or "cancel" to try doing something else.')
            if used == 'front door':
                display('You go through the front door, out into the town square.')
                return room, player, 1
            elif used == 'back door':
                display('You go through the back door, out into the forest.')
                return room, player, 8
            elif used == 'door':
                display('Which door? Try "use back door" instead')
            elif used in ['cancel','no','nevermind','exit']:
                continue
            else:
                player = useItem(player,used)
        elif action in ['leave', 'move']:
            display('Try "Use Front Door" or "Use Back Door".')
        elif action == 'inventory':
            print(f'Inventory: {', '.join(player['inventory'])}')
            print(f'Money: {player['money']}')
            print(f'Equipped: {', '.join(player['equipped'])}')
def townSquare(room, player):
    display("You are in the town square. There is an old \033[36mbeggar\033[0m sitting on a \033[36mbench\033[0m. You can head off to the \033[36mWestaurant\033[0m, the \033[36mchurch\033[0m, the \033[36mranch\033[0m, the \033[36mclothes shop\033[0m, or the \033[36msheriff's office\033[0m.")
    while True:
        display("Use, Move, Inventory, or Inspect?")
        action, acted = getAction(['inspect', 'use', 'inventory', 'move'])
        if action == 'inspect':
            options = player['inventory'] + ['beggar','cancel','no','nevermind','exit','bench']
            if acted:
                if acted in options:
                    inspected = acted
                else:
                    display(f'There is no {acted} here. Try inspecting a person to talk to them.')
                    continue
            else:
                print('What are you inspecting?')
                inspected = choiceInput(options,'That isn\'t here. What are you inspecting?')
            if inspected == 'beggar':
                display('>Food for the poor?')
                if 'dinner' in player['inventory'] and room['begging']:
                    display('Offer food?')
                    choice = choiceInput(['y','yes','n','no'],'Enter yes/no!')
                    if choice in ['yes','y']:
                        player['inventory'].remove('dinner')
                        display('>Really? Here, take these as a sign of my gratitude')
                        player['inventory'].append('dentures')
                        display('You got the Old Dentures!')
                        room['begging'] = False
                    else:
                        display('You hide the Western Dinner.')
            elif inspected == 'bench':
                display("It's a simple bench, and well maintained.")
            elif inspected in ['cancel','no','nevermind','exit']:
                continue
            else:
                display(items[inspected]['inspect'])
        elif action == 'use':
            options = player['inventory'] + ['cancel','no','nevermind','exit']
            if acted:
                if acted in options:
                    used = acted
                else:
                    display(f'You can\'t use that.')
                    continue
            else:
                print('Use what?')
                used = choiceInput(options,'You can\'t use that! Type "cancel" to try doing something else.')
            if used in ['cancel','no','nevermind','exit']:
                continue
            player = useItem(player,used)
        elif action == 'inventory':
            print(f'Inventory: {', '.join(player['inventory'])}')
            print(f'Money: {player['money']}')
            print(f'Equipped: {', '.join(player['equipped'])}')
        elif action == 'move':
            options = ['westaurant', 'church', 'ranch', 'clothes shop', "sheriff's office"]
            if acted:
                if acted in options:
                    moved = acted
                else:
                    display(f'You can\'t move there.')
                    continue
            else:
                print('Move where?')
                moved = choiceInput(options,'You can\'t move there! Try moving to the \033[36mranch\033[0m, or type "cancel" to try doing something else.')
            if moved == 'church':
                if 'key' in player['inventory']:
                    display('You unlock the door with the key')
                else:
                    display("It's locked!")
                    continue
            return room, player, rooms[moved]
def grandmaHouse(room, player):
    display("You enter your grandma's house. She is sitting in a rocking chair. The door is behind you.")
    if not room['visited']:
        display('>Oh hello dearie! How is the job going? Are you getting hungry?')
        input('>')
        display('>Of course you are! Take a cookie.')
        player['inventory'].append('cookie')
        display("You got Grandma's Cookie! It looks too good to eat.")
        room['visited'] = True
        if 'dentures' in player['inventory']:
            display(">Oh! My dentures! Hand 'em over!")
            display(">Thanks for returning them! Here, have another cookie.")
            player['inventory'].append('cookie')
            display("You got Grandma's Cookie!")
            room['dentures'] = True
    elif not room['dentures']:
        display(">Oh hello dearie! I have another cookie in the oven for you. I only made one since I can't eat them without my dentures.")
        if 'dentures' in player['inventory']:
            display(">Oh! Those must be them! Hand 'em over!")
            display(">Thanks for returning them! Here, have a cookie.")
            player['inventory'].append('cookie')
            display("You got Grandma's Cookie!")
            room['dentures'] = True
        else:
            display('>Oh i wish i could find them…')
    elif not (player['charisma'] == 3 and not room['bandanna']):
        display("She appears to be asleep.")
    if player['charisma'] == 3 and not room['bandanna']:
        display(">Oh hello dearie! Want to hear a story?")
        input('>')
        display(">Of course you do! Back when i was young i was part of this fantasmic group of flapjacks. We had so much fun! We used to wear these scarves on our head. Like this one!")
        player['inventory'].append('bandanna')
        display('You got the Bandit Bandanna! It makes you look just like one if you equip it (use).')
        display(">We always used to hang out at the church, you know?")
        display(">Have fun!")
        room['bandanna'] = True
    display("You leave through the door.")
    if (not room['dentures']) or (not room['bandanna']):
        display('>Come back later!')
        if not 'badge' in player['inventory']:
            display('>And put some clothes on!')
    return room, player, 8
def forest(room, player):
    if not room['weasel']:
        if room['bart']:
            display("You enter the forest. There is a \033[36mweasel\033[0m hiding under a fern. Your \033[36mgrandma's house\033[0m is just a short walk away. The \033[36mranch\033[0m and \033[36mSheriff's Office\033[0m are nearby.")
        else:
            display("You enter the forest. There is a \033[36mbandit\033[0m sitting on a tree \033[36mstump\033[0m and a \033[36mweasel\033[0m hiding under a fern. Your \033[36mgrandma's house\033[0m is just a short walk away. The \033[36mranch\033[0m and \033[36mSheriff's Office\033[0m are nearby.")
    else:
        if room['bart']:
            display("You enter the forest. Your \033[36mgrandma's house\033[0m is just a short walk away. The \033[36mranch\033[0m and \033[36mSheriff's Office\033[0m are nearby.")
        else:
            display("You enter the forest. There is a \033[36mbandit\033[0m sitting on a tree \033[36mstump\033[0m. Your \033[36mgrandma's house\033[0m is just a short walk away. The \033[36mranch\033[0m and \033[36mSheriff's Office\033[0m are nearby.")
    if 'badge' in player['equipped'] and not room['bart']:
        display(">Hang on a minute… You're the sheriff! Take this!")
        player = combat({'name': 'Bandit Bart','charisma': 0,'hp': 2}, player)
        if not player:
            return False, False, False
        room['bart'] = True
        player['money'] += 5
        display("You got $5!")
    while True:
        display("Use, Move, Inventory, or Inspect?")
        action, acted = getAction(['inspect', 'use', 'inventory', 'move'])
        options = player['inventory'] + ['cancel','no','nevermind','exit','stump']
        if not room['bart']:
            options.append('bandit')
        if not room['weasel']:
            options.append('weasel')
        if action == 'inspect':
            if acted:
                if acted in options:
                    inspected = acted
                else:
                    display(f'There is no {acted} here.')
                    continue
            else:
                print('What are you inspecting?')
                inspected = choiceInput(options,'That isn\'t here. What are you inspecting?')
            
            if inspected == 'bandit':
                display('>Hey dude.')
            elif inspected == 'weasel':
                display("It's just a weasel. It is a bit fat, looks like it has been eating well.")
            elif inspected == 'stump':
                display("A tree stump from an old tree. It's sturdy and covered in moss.")
            else:
                display(items[inspected]['inspect'])
        elif action == 'use':
            options = player['inventory'] + ['cancel','no','nevermind','exit']
            if acted:
                if acted in options:
                    used = acted
                else:
                    display(f'You can\'t use that.')
                    continue
            else:
                print('Use what?')
                used = choiceInput(options,'You can\'t use that! Type "cancel" to try doing something else.')
            if used == 'weasel trap':
                display("You catch the weasel in the trap!")
                player['inventory'].remove('weasel trap')
                player['inventory'].append('captured weasel')
                room['weasel'] = True
            elif used in ['cancel','no','nevermind','exit']:
                continue
            else:
                player = useItem(player,used)
        elif action == 'inventory':
            print(f'Inventory: {', '.join(player['inventory'])}')
            print(f'Money: {player['money']}')
            print(f'Equipped: {', '.join(player['equipped'])}')
        elif action == 'move':
            options = ["grandma's house",'grandmas house','grandma','grandma house','ranch', "sheriff's office",'sheriffs office','sheriff office']
            if acted:
                if acted in options:
                    moved = acted
                else:
                    display(f'You can\'t move there.')
                    continue
            else:
                print('Move where?')
                moved = choiceInput(options,'You can\'t move there! Try moving to grandma\'s house, or type "cancel" to try doing something else.')
            
            return room, player, rooms[moved]
def clothesShop(room, player):
    display("Taylor the Taylor is sitting at a desk.")
    display(">Hello! What can I do for you today?")
    if 'cookie' in player['inventory'] and not 'badge' in player['inventory']:
        display(">Wait a minute… is that a cookie I smell? Could I have it?")
        choice = choiceInput(['y','yes','n','no'],'Enter yes/no!')
        if choice in ['y', 'yes']:
            display(">Thanks! Here, take this. I think you lost it.")
            player['inventory'].remove('cookie')
            player['inventory'].append('badge')
            display("You got the sheriff's badge! Maybe you should equip it (use).")
        else:
            display(">Aw… okay.")
        if not ('mustache' in player['inventory'] and 'hat' in player['inventory']):
            display(">Anyways, would you like to buy some clothes?")
    if (not 'mustache' in player['inventory']) and (not 'hat' in player['inventory']):
        display(">We have the glue-on mustache and the cowboy hat!")
        display("Mustache, Hat, or Leave?")
        choice = choiceInput(["mustache", "hat", "leave"],'Please select a valid action (mustache, hat, or leave)')
    elif ('mustache' in player['inventory']) and (not 'hat' in player['inventory']):
        display(">We have the cowboy hat!")
        display("Hat, or Leave?")
        choice = choiceInput(['hat', 'leave'], 'Please select a valid action (hat or leave)')
    elif (not 'mustache' in player['inventory']) and ('hat' in player['inventory']):
        display(">We have the glue-on mustache!")
        display("Mustache, or Leave?")
        choice = choiceInput(['mustache', 'leave'],'Please select a valid action (mustache or leave)')
    else:
        display("I can't do much for you, we're fresh out of clothes.")
        choice = ''
    if choice == 'mustache':
        display(f'>That will be ${4 - player['charisma']}.')
        if player['money'] >= 4 - player['charisma']:
            display('You got the Glue-On Mustache! Equip it (use) to gain charisma!')
            player['money'] -= 4 - player['charisma']
            player['inventory'].append('mustache')
        else:
            display(">Aw, darn… you don't have enough. Come back later when you have some more!")
    elif choice == 'hat':
        display(f'>That will be ${4 - player['charisma']}.')
        if player['money'] >= 4 - player['charisma']:
            display('You got the Cowboy Hat! Equip it (use) to gain charisma!')
            player['money'] -= 4 - player['charisma']
            player['inventory'].append('hat')
        else:
            display(">Aw, darn… you don't have enough. Come back later when you have some more!")
    display("You leave through the door.")
    if not 'badge' in player['inventory']:
        display(">Man… i could sure use a treat about now.")
    return room, player, 1
def church(room, player):
    if not room['garret']:
        display('You enter the church. \033[36mGarret the Guard\033[0m is standing guard over the entrance to the hideout.')
        if 'bandanna' in player['equipped']:
            display(">Oh, hey! Come to hang out in the hideout? Go ahead!")
            display("You can walk down into the bandit hideout or out into the town square.")
            moved = choiceInput(['hideout', 'town square', 'bandit hideout'], 'Please select a valid place to move (Hideout or Town Square)')
            if moved in ['hideout','bandit hideout']:
                display('You move down into the bandit hideout.')
                return room, player, 9
            else:
                display('You leave the church.')
                return room, player, 1
        elif 'badge' in player['equipped']:
            display('>Hey! You!')
            player = combat({'name': 'Garret the Guard','charisma': 2,'hp': 2}, player)
            if not player:
                return False, False, False
            room['garret'] = True
            player['money'] += 5
            display("You got $5!")
        else:
            display("You can walk down into the \033[36mbandit hideout\033[0m or out into the \033[36mtown square\033[0m.")
            moved = choiceInput(['hideout', 'town square', 'bandit hideout'], 'Please select a valid place to move (Hideout or Town Square)')
            if moved in ['hideout','bandit hideout']:
                display('>Uh.. you can\'t go down there.')
            display('You leave the church.')
            return room, player, 1
    if room['garret']:
        display("You can walk down into the \033[36mbandit hideout\033[0m or out into the \033[36mtown square\033[0m.")
        moved = choiceInput(['hideout', 'town square', 'bandit hideout'], 'Please select a valid place to move (Hideout or Town Square)')
        if moved in ['hideout','bandit hideout']:
            display('You move down into the bandit hideout.')
            return room, player, 9
        else:
            display('You leave the church.')
            return room, player, 1
def westaurant(room, player):
    if room['jed']:
        display("You enter the westaurant. Jed is dead, but Leviticus is still here.")
        display('>Ranch?')
        if 'ranch' in player['inventory']:
            display('>Ranch!')
            display("Leviticus seizes the ranch. He drops a key from his pocket without noticing.")
            player['inventory'].remove('ranch')
            player['inventory'].append('key')
            display("You got the Priest's Key!")
        display("You can move into the back room or into the town square.")
        moved = choiceInput(['town square', 'back room'], 'Please select a valid place to move (Back Room or Town Square)')
        if moved == 'back room':
            display("You move down into the back room.")
            return room, player, 10
        else:
            display("You leave the westaurant.")
            return room, player, 1
    else:
        display("You enter the westaurant. Jed is tending the counter.")
        display("A strange voice rings out from the corner")
        display('>Ranch?')
        display("Leviticus is sitting in the corner, wearing priest's robes covered in ranch stains.")
        if 'badge' in player['equipped']:
            display("Jed is staring at your badge")
            display(">Hang on… you're the new sheriff! Take this!")
            display("Jed takes off his hat, revealing a bandit bandanna.")
            player = combat({'name': 'Jed','charisma': 3,'hp': 1}, player)
            if not player:
                return False, False, False
            room['jed'] = True
            player['money'] += 5
            display("You got $5!")
            display("You can move into the back room or into the town square.")
            moved = choiceInput(['town square', 'back room'], 'Please select a valid place to move (Back Room or Town Square)')
            if moved == 'back room':
                display("You move down into the back room.")
                return room, player, 10
            else:
                display("You leave the westaurant.")
                return room, player, 1
        else:
            display("Jed is looking at you.")
            display(">Hey! Would you like to buy some food?")
            display("Western Dinner, Western Beer, or Leave?")
            choice = choiceInput(['dinner', 'western dinner', 'western beer' 'beer', 'leave'], 'Please select a valid item (Dinner, Beer, or Leave)')
            if choice in ['dinner', 'western dinner']:
                display(f">That will be ${3 - player['charisma']}.")
                if player['money'] >= 3 - player['charisma']:
                    player['money'] -= 3 - player['charisma']
                    display('You got the Western Dinner! Save it for later to restore some health.')
                    player['inventory'].append('dinner')
                else:
                    display(">Aw, darn… you don't have enough. Come back later when you have some more!")
            elif choice in ['beer','western beer']:
                display(f">That will be ${2 - player['charisma']}.")
                if player['money'] >= 2 - player['charisma']:
                    player['money'] -= 2 - player['charisma']
                    display('You got the Western Beer! It will increase your max health but might have some side effects...')
                    player['inventory'].append('beer')
                else:
                    display(">Aw, darn… you don't have enough. Come back later when you have some more!")
            display("You leave through the door.")
            display('>Ranch?')
            return room, player, 1
def ranch(room, player):
    if not room['weasel trap']:
        display("You enter the ranch. \033[36mRancher Bob\033[0m is tending to the animals and \033[36mBilly the Kid\033[0m is running around with a strange metal trap. You can move to the \033[36mforest\033[0m or \033[36mtown square\033[0m.")
    else:
        display("You enter the ranch. \033[36mRancher Bob\033[0m is tending to the animals and \033[36mBilly the Kid\033[0m is eating a cookie.  You can move to the \033[36mforest\033[0m or \033[36mtown square\033[0m.")
    while True:
        display("Use, Move, Inventory, or Inspect?")
        action, acted = getAction(['inspect', 'use', 'inventory', 'move'])
        if action == 'inspect':
            options = player['inventory'] + ['bob','billy','rancher','rancher bob','billy the kid','kid','cancel','no','nevermind','exit']
            if acted:
                if acted in options:
                    inspected = acted
                else:
                    display(f'There is no {acted} here.')
                    continue
            else:
                print('What are you inspecting?')
                inspected = choiceInput(options,'That isn\'t here. What are you inspecting?')
            
            if inspected in ['bob','rancher','rancher bob']:
                if room['weasel trade']:
                    display('>Hey there! Thanks for earlier!')
                else:
                    display('>Oh, hello.')
                    display('Rancher Bob looks sad')
                    display(">Sorry about me, i'm just down because this weasel keeps eating my crops. I can never catch it!")
                    if not room['weasel trap']:
                        display(">Billy is trying to catch it with that weasel trap he has.")
                    elif 'captured weasel' in player['inventory']:
                        display("Wait! That's the weasel! Thank you so much! Take this.")
                        player['inventory'].remove('captured weasel')
                        player['inventory'].append('ranch')
                        display("You got the Rancher's Ranch! Maybe someone will want it?")
                    if not 'handcuffs' in player['inventory']:
                        display(">I really appreciate all the work you do as sheriff.")
                        display(">I can't wait for you to catch that rascal.")
                        display(">Too bad you used your only handcuffs on Jay.")
                    display(">Anyways, see you later.")
            elif inspected in ['billy', 'billy the kid','kid']:
                if room['weasel trap']:
                    display(">Hi mister! Thanks for the cookie!")
                else:
                    display(">Hi mister! I'm trying to catch a weasel!")
                    display(">All this running around is making me hungry. I could sure go for a cookie and some milk about now!")
                    if 'cookie' in player['inventory'] and 'milk' in player['inventory']:
                        display('>Oh hey! Look at that!')
                        display('Billy grabs the cookie and milk from you.')
                        player['inventory'].remove('cookie')
                        player['inventory'].remove('milk')
                        player['inventory'].append('weasel trap')
                        display("He drops his weasel trap as he runs away.")
                        display("You got the weasel trap! It is primed and ready to catch a weasel (use)")
                        room['weasel trap'] = True
            elif inspected in ['cancel','no','nevermind','exit']:
                continue
            else:
                print(items[inspected]['inspect'])
        elif action == 'use':
            options = player['inventory'] + ['cancel','no','nevermind','exit']
            if acted:
                if acted in options:
                    used = acted
                else:
                    display(f'You can\'t use that.')
                    continue
            else:
                print('Use what?')
                used = choiceInput(options,'You can\'t use that! Type "cancel" to try doing something else.')
            
            if used in ['cancel','no','nevermind','exit']:
                continue
            player = useItem(player,used)
        elif action == 'inventory':
            print(f'Inventory: {', '.join(player['inventory'])}')
            print(f'Money: {player['money']}')
            print(f'Equipped: {', '.join(player['equipped'])}')
        elif action == 'move':
            options = ['town square', 'forest']
            if acted:
                if acted in options:
                    moved = acted
                else:
                    display(f'You can\'t move there.')
                    continue
            else:
                print('Move where?')
                moved = choiceInput(options,'You can\'t move there! Try moving to the forest, or type "cancel" to try doing something else.')
            return room, player, rooms[moved]
def hideout(player):
    display("You enter the hideout. Standing in the center of the room is a familiar face.")
    display("Wearing a bandit bandanna, and munching on one of her signature cookies.")
    display(">That's right… I am Bad Guy Bill! Didn't expect that, now did you?")
    display(">The clues were there all along- but of course a young whippersnapper like you wouldn't be able to figure them out!")
    if 'bandanna' in player['inventory']:
        display(">I gave you the bandanna you used to sneak in here!")
    display(">I gave you the cookies to give to Taylor and Billy!")
    display(">I helped you along every step of your journey!")
    if 'bandanna' in player['inventory']:
        display(">I even hinted that I was Bad Guy Bill!")
        display(">I told you I was a bandit!")
    display(">All to get you here.")
    display(">Why?")
    display(">This town doesn't need a sheriff.")
    display(">Crime is the way of the world!")
    display(">I couldn't kill you myself, of course.")
    display('>"Sheriff murdered by deranged outlaw" is a much better headline than "Sheriff murdered by senile grandma"')
    display(">So that brings us to here.")
    display(">Now prepare to die!")
    player = combat({'name': 'your Grandma','charisma': 3,'hp': 4}, player)
    if not player:
        return False
    display(">You don't want to kill me!")
    display(">I'm your sweet old grandma!")
    display(">Here, take a cookie! Take a whole batch!")
    display("Your grandma throws a tray of cookies in your face!")
    display("She runs to the door to escape!")		
    if 'handcuffs' in player['inventory']:
            player['inventory'].remove('handcuffs')
            display("She trips as she realizes- her ankles are handcuffed together")
            display(">You… handcuffed me? With your only pair of handcuffs?")
            display(">Nooooo!!!! My crime empire!!!!!")
            display("With the town saved, you are revered as the greatest sheriff Westville has ever seen.")
            display("And seriously…")
            display("Those cookies were pretty good.")
            display("THE END")
            return True
    else:
        display('You run out the door after her!')
        display("As she is running away, you fire a shot from your pistol.")
        display("Congratulations. You killed your grandma.")
        display("With the town saved, you are revered as the greatest sheriff Westville has ever seen.")
        display("But you will forever have to live with your regret.")
        display("THE END")
        return True
def backRoom(room,player):
    display("You enter the back room of the westaurant.")
    if not room['milk']:
        display("There is some food stored in crates, a small kitchen, and a bottle of milk sitting out. There is also quite a few western dinners around.")
        display("You got the Milk! Maybe someone will want it?")
        room['milk'] = True
        player['inventory'].append('milk')
    else:
        display("There is some food stored in crates, and a small kitchen. There is also quite a few western dinners around.")
    display("You got a Western Dinner!")
    player['inventory'].append('dinner')
    display("You leave back into the main room.")
    return room, player, 2
def run_adventure():
    while True:
        player_info = {
            'charisma': 0,
            'max hp': 4,
            'hp': 4,
            'money': 5,
            'drunk turns': 0,
            'inventory': [],
            'equipped': []
        }
        town_square = {
            'begging': True
        }
        sheriff_office = {
            'jay': True
        }
        ranch_info = {
            'weasel trap': False,
            'weasel trade': False
        }
        westaurant_info = {
            'jed': False
        }
        forest_info = {
            'weasel': False,
            'bart': False
        }
        grandma_house = {
            'visited': False,
            'dentures': False,
            'bandanna': False
        }
        church_info = {
            'garret': False
        }
        back_room = {
            'milk': False
        }
        clothes_shop = {}
        room_num = 4
        display("Welcome to Westville! This rough-and-tumble town is troubled by a gang of bandits led by the infamous Bad Guy Bill. The previous sheriff of this town was killed by Bad Guy Bill. Now you are the replacement. Your mission: Find and incarcerate Bad Guy Bill. Only trouble is, nobody knows where or who he is. Maybe you should ask your grandma.", 6)
        while True:
            player_info['drunk turns'] -= 1
            if player_info['drunk turns'] > 0:
                display('You feel a little less tipsy.')
            elif player_info['drunk turns'] == 0:
                display('You no longer feel tipsy.')
            if room_num == 1:
                town_square, player_info, room_num = townSquare(town_square, player_info)
            elif room_num == 2:
                westaurant_info, player_info, room_num = westaurant(westaurant_info, player_info)
            elif room_num == 3:
                grandma_house, player_info, room_num = grandmaHouse(grandma_house, player_info)
            elif room_num == 4:
                sheriff_office, player_info, room_num = sheriffOffice(sheriff_office, player_info)
            elif room_num == 5:
                clothes_shop, player_info, room_num = clothesShop(clothes_shop, player_info)
            elif room_num == 6:
                church_info, player_info, room_num = church(church_info,  player_info)
            elif room_num == 7:
                ranch_info, player_info, room_num = ranch(ranch_info, player_info)
            elif room_num == 8:
                forest_info, player_info, room_num = forest(forest_info, player_info)
            elif room_num == 9:
                player_info = hideout(player_info)
            elif room_num == 10:
                back_room, player_info, room_num = backRoom(back_room, player_info)
            if not player_info:
                display("GAME OVER")
                break
            if player_info == True:
                break
        
        print('Play Again?')
        choice = choiceInput(['y', 'yes', 'n', 'no'],'Enter yes/no!')
        if choice in ['n','no']:
            break
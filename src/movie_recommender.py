#BZ 2nd Movie Recomender
import csv as csv


#number input
def int_input(max = 100000,prompt='> ',min = 0):
    while True:
        num = input(prompt).lower()
        try:
            num = int(num)
        except:
            print('Input is not a number!')
            continue
        if num <= max and num >= min:
            return num
        else:
            print('Input is out of range!')



#input from choices
def choice_input(choices,prompt = '> '):
    while True:
        choice = input(prompt).lower()
        if choice in choices:
            return choice
        else:
            print('Please select a valid choice!')



#CSV to dictionary function
def csv_to_dictionary(file_path):
    #create empty list
    finished = []
    #open csv file in read mode
    with open(file_path, mode = 'r') as file:
        #create csv reader
        reader = csv.reader(file)
        #get first line in reader
        header = next(reader)
        #loop through reader:
        for line in reader:
            #create empty dictionary
            current_line = {}
            #set iterator to 0
            i = 0
            #loop through first line:
            for column in header:
                #create new line in the dictionary with the first line value as the key and the respective line value as the value
                current_line[column] = line[i]
                i += 1
            #add dictionary to list
            finished.append(current_line)
        return finished



#print anything function
def uniprint(to_print, indentation = ''):
    #get type of thing to print
    method = type(to_print)
    #if it is an integer, float, or string
    if method is int or method is str or method is float:
        #print it
        print(indentation + to_print)
    #if it is a list, tuple, or set
    elif method is list or method is tuple or method is set:
        #loop through it
        for item in to_print:
            #uniprint item
            uniprint(item, indentation)
            #print new line
            print()
    #if it is a dictionary:
    elif method is dict:
        #loop through the keys
        for key in to_print.keys():
            #get type of value
            nest_method = type(to_print[key])
            #if value is a string, float, or integer:
            if nest_method is int or nest_method is str or nest_method is float:
                #print the key and a colon followed by the value
                print(f'{indentation}{key}: \033[34m{to_print[key]}\033[0m')
            #otherwise:
            else:
                #print the key and a colon
                print(f'{indentation}{key}:')
                #uniprint value
                uniprint(to_print[key],indentation + ' ')



#check function
def check(condition,dictionary):
    #seperate values
    key, method, compare = condition.split('|')
    #find value in dictionary with key provided
    value = dictionary[key]
    #if it is comparing strings
    if method == 'has':
        #check if it contains the compare value
        if compare.lower() in value.lower():
            #if so, return true
            return True
        else:
            #otherwise return false
            return False
    #else if it is comparing greater than
    elif method == '>':
        try:
            #if the value is more than the compare
            if value > compare:
                #return true
                return True
        except:
            pass
        #otherwise return false
        return False
    #else if it is comparing less than
    elif method == '<':
        try:
            #if the value is less than the compare
            if value < compare:
                #return true
                return True
        except:
            pass
        #otherwise return false
        return False
    


#movie print function
def movie_print(movies):
    if not movies:
        print('No results!')
        return
    iterator = 1
    #loop through movies
    for i in movies:
        #print movie
        uniprint(f'{iterator}: \033[37m{i['Title']}\033[0m')
        iterator += 1
    #ask user if they want the detailed view of a movie
    print('Type movie number for detailed view or ENTER to exit')
    chosen = input('> ')
    
    if chosen == '':
        return
    #check if it is one of the printed movies
    try:
        if int(chosen) >= iterator:
            print('Invalid choice!')
            return
    except:
        #if not
        #tell user to use a valid choice
        print('Invalid choice!')
        return
    #print the detailed view of what movie they chose
    if int(chosen) < iterator:
        uniprint(movies[int(chosen) - 1])



#check multiple conditions function
def multicheck(conditions, dictionary):
    #loop through conditions
    for con in conditions:
        #if the dictionary does not satisfy current condition
        if not check(con,dictionary):
            #return false
            return False
    #return true
    return True



#search function
def search(movies):
    #loop forever
    conditions = []
    while True:
        #ask user whether to add a condition or search
        print('1. \033[37mAdd Condition\n\033[0m2. \033[37mSearch\033[0m')
        action = input('> ')
        match action:
            #if they choose to add a condition
            case '1':
                #ask them what field to check
                print("What would you like to check?")
                checkers = ['title','director','genre','rating','length (in minutes)','notable actors']
                iterator = 0
                for i in checkers:
                    iterator += 1
                    print(f"{iterator}. \033[37m{i.title()}\033[0m")
                action = choice_input(['1','2','3','4','5','6'],'> ')
                #if they chose a field that's not length
                if action in ('1','2','3','4','6'):
                    #ask them what to check it against
                    print(f'What would you like to check {checkers[int(action) - 1]} contains?')
                    compare = input('> ')
                    #create condition based on gathered information
                    condition = f'{checkers[int(action) - 1].title()}|has|{compare.lower()}'
                #else if they chose length
                elif action == '5':
                    #ask them whether they want to set a min or max
                    print('1. \033[37mMin Length\n\033[0m2. \033[37mMax Length\033[0m')
                    match choice_input(['1','2'],'> '):
                        #if they want to set a min
                        case '1':
                            #store that
                            operator = '>'
                        #otherwise if they want to set a max
                        case '2':
                            #store that
                            operator = '<'
                    #ask them what to compare it against
                    print('What are you comparing it against?')
                    compare = int_input()
                    condition = f'Length (min)|{operator}|{compare}'
                #add condition to conditions list
                conditions.append(condition)
            #else if they want to search
            case '2':
                matched = []
                #loop through all movies
                for movie in movies:
                    #if current movie satisfies all conditions
                    if multicheck(conditions,movie):
                        #add movie to matched movies
                        matched.append(movie)
                #print all matched movies
                movie_print(matched)
                break
            case _:
                print('Please select 1 or 2!')

    


#main menu function
def menu(movies):
    #ask user what to do
    print('\033[30m###\033[36m MAIN MENU \033[30m###\033[0m\n1. \033[37mSearch\n\033[0m2. \033[37mShow Movies\n\033[0m3. \033[37mExit\033[0m')
    match input('> '):
        #if they chose to search
        case '1':
            #search
            search(movies)
        #if they chose to show full list
        case '2':
            #print out all movies
            movie_print(movies)
        #if they chose to exit
        case '3':
            #return true
            return True
        
def run_movie_searcher():
    #create dictionary of movies
    movies = csv_to_dictionary('docs/movies.csv')

    #introduce program
    print('This is a Movie Database Searcher.')
    input('\033[32mPress ENTER to start! > \033[0m')

    #forever
    while True:
        print('\033c', end='')
        #main menu
        if menu(movies):
            break
        input('\033[32mPress ENTER to continue > \033[0m')

    print('Thank you for using the movie searcher')
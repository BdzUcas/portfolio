from tkinter import *
#result class, used for passing information locally to globally
class Result():
    def __init__(self):
        self.result = ''

#menu function, for creating a menu with the given options
def menu(options,prompt,title_text='Menu',width=0,height=0,titlesize=20,font='Helvetica',buttonsize=10):
    #finds the longest bit of text out of the title and all the buttons
    longest = len(prompt)*titlesize*0.6
    for i in options:
        length = len(i)*buttonsize*0.6
        if length > longest:
            longest = length
    #if height is 0 (unset)
    if height == 0:
        #calculate height by amount of buttons and size of title and buttons
        height = int(titlesize*4 + len(options) * buttonsize * 5)
    #if width is 0 (unset)
    if width == 0:
        #calculate width based on longest text
        width = int(longest) + 100
    #create a screen
    root = Tk()
    root.title(title_text)
    root.geometry(f'{width}x{height}')
    #create a heading with given size and font
    heading = Label(root,text=prompt,font=(font,titlesize))
    heading.pack(pady=titlesize*1.5)
    #create a Result object for storing what the user clicks on
    result = Result()
    #function that runs when a button is pushed
    def button_push(result,text):
        #set the result property of the given Result object to the text of the button
        result.result = text
        #kill the screen
        root.destroy()
    #make an empty list for the buttons
    buttons = []
    #loop through options
    for option in options:
        #make a button with given font and size that runs the button push function
        button = Button(root,text=option,command = lambda option=option: button_push(result,option),font=(font,buttonsize))
        #add it to the buttons list
        buttons.append(button)
        #put it on the screen
        button.pack(pady=buttonsize/2)
    #run the screen
    root.mainloop()
    #return the result property of the Result object
    return result.result
#display function
def display(text=['No text provided'],font='Helvetica',fontsize=10,buttontext='exit',title_text='Display',alt_button_text=''):
    #find longest text
    longest = 0
    for line in text:
        length = len(line)*fontsize*0.6
        if length > longest:
            longest = length
    #create a screen
    root = Tk()
    #determine amount of extra space to add (more if second button is enabled)
    button_space = 2
    if alt_button_text:
        button_space += 1
    #change dimensions of screen to fit longest text and amount of text/buttons
    root.geometry(f'{int(longest+100)}x{int((len(text)+button_space)*fontsize*3)}')
    root.title(title_text)
    #loop through the text
    for line in text:
        #create a label with the line of text, and place it on the screen
        label = Label(root,text=line,font=(font,fontsize))
        label.pack(pady=fontsize/2)
    #create a result object to store which button was bushed
    result = Result()
    #create a function for button pushing
    def destroy(result,return_val):
        result.result = return_val
        root.destroy()
    #make the main button that always shows
    exit_button = Button(root,text=buttontext,command = lambda: destroy(result,True),font=(font,fontsize))
    exit_button.pack(pady=fontsize/2)
    #if text is provided for a second button, make it too
    if alt_button_text:
        alt_button = Button(root,text=alt_button_text,command = lambda: destroy(result,False),font=(font,fontsize))
        alt_button.pack(pady=fontsize/2)
    #run main loop
    root.mainloop()
    #return the result of which button was pushed (true for main button, false for alt button)
    return result.result 
#BZ 1st maze generator
#import libraries
import random as r
import turtle as t
#create empty maze list
maze = []
#create width variable
#create function for neighbors choice
def find_neighbors(x, y, visited, width):
    neighbors = []
    #create a list of all neighbor cells
    neighbors = [[x,y+1],[x-1,y],[x+1,y],[x,y-1]]
    loop_neighbors = [[x,y+1],[x-1,y],[x+1,y],[x,y-1]]
    #remove items that match an item in the visited list OR contain coords outside of the maze
    for i in loop_neighbors:
        if i in visited:
            neighbors.remove(i)
        elif i[0] < 0 or i[1] < 0:
            neighbors.remove(i)
        elif i[0] >= width or i[1] >= width:
            neighbors.remove(i)
    #return neighbors
    return neighbors
#create function for calculating size values
def find_size():
    width = r.randint(16,48)
    size = 400 / width
    full_width = size * 2 * width
    half_width = size * width
    return width, size, full_width, half_width
#create function for generating maze
def generate_maze(width):
    #loop through y coordinates of the maze
    for y in range(0,width):
        #empty row list
        row = []
        #loop through x coordinates of the maze
        for x in range(0,width):
            #add [1,1,1,1] to row list. This represents the sides, with 1 being wall and 0 being no wall, starting at the top and moving clockwise
            row.append([1,1,1,1])
        #add row list to maze list
        maze.append(row)
    maze[width-1][r.randint(0,width-1)][0] = 0
    return maze
def run_maze_generator():
    #Get size
    width, size, full_width, half_width = find_size()
    #Generate maze
    maze = generate_maze(width)
    #set x and y starting coords
    x, y = 0, 0
    #create an empty "visited" list
    visited = []
    #create an empty "stack" list
    stack = []
    #loop until visited list contains all cells
    exit = False
    while len(visited) < width ** 2:
        #add current x and y coordinate to the visited list and a "stack" list
        visited.append([x,y])
        #reset neighbors list
        neighbors = []
        #loop while we have no neighbors
        while not neighbors:
            #find neighbors
            neighbors = find_neighbors(x,y,visited,width)
            #if there are neighbors
            if neighbors:
                #pick a random neighbor
                neighbor = r.choice(neighbors)
                #exit loop
                break
            #if there are no neighbors
            else:
                #if there are items in the stack
                if stack:
                    #remove top item from stack and update our x and y coords to it
                    x, y = stack.pop()
                else:
                    #exit main loop
                    exit = True
                    break
        if exit:
            break
        #add chosen neighbor to stack
        stack.append(neighbor)
        #remove wall between current cell and chosen neighbor cell
        if neighbor[0] == x - 1:
            neighbor_remove = 1
            self_remove = 3
        elif neighbor[0] == x+1:
            neighbor_remove = 3
            self_remove = 1
        elif neighbor[0] == x:
            if neighbor[1] == y-1:
                neighbor_remove = 0
                self_remove = 2
            elif neighbor[1] == y+1:
                neighbor_remove = 2
                self_remove = 0
        maze[neighbor[1]][neighbor[0]][neighbor_remove] = 0
        maze[y][x][self_remove] = 0
        #set x and y coordinate to that of the chosen neighbor
        x,y = neighbor
    #setup turtle
    t.hideturtle()
    t.pensize(3)
    t.speed(0)
    t.pendown()
    #move turtle to top left
    t.teleport(half_width / -1,half_width - size * 2)
    #loop through maze rows
    for row in maze:
        #loop through cells in row
        for cell in row:
            #if there is a wall on the top of the current cell
            if cell[0] == 1:
                #move forward one wall
                t.forward(size*2)
            #otherwise
            else:
                #teleport forward one wall
                t.teleport(t.xcor() + size * 2, t.ycor())
        #teleport down one wall and back to the left
        t.teleport(half_width / -1,t.ycor()-size*2)
    #teleport to the top left
    t.teleport(half_width / -1,half_width)
    #face turtle down
    t.right(90)
    #loop through maze rows
    for row in maze:
        #loop through cells in row
        for cell in row:
            if cell[3] == 1:
                t.forward(size*2)
                t.teleport(t.xcor(), t.ycor() + size * 2)
            #teleport forward one wall
            t.teleport(t.xcor() + size * 2, t.ycor())
            
        t.teleport(half_width / -1,t.ycor()-size*2)
    t.teleport(half_width,half_width)
    t.forward(full_width)
    t.teleport(half_width / -1,half_width)
    t.left(90)
    t.forward(full_width - size * 2)
    t.done()
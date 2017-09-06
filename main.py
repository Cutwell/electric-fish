#  a modular setip for cellular automata programs

#  each cell is a class
#  the environment is a 2d list
#  behaviour and changes to the environment are handled in the main loop function
#  each cell has a position variable
#  all instances of the class cell are held within a list
#  a seperate list is used for each species of cell, to avoid identification errors
#  and to allow application of different behaviours

import random
import inspect
import time

class cell:

    def __init__(self, species, symbol, id, breed_time, hunger=10, gender=None, trait=None):
        self.id = id
        self.symbol = symbol
        self.species = species
        self.gender = gender if gender != None else random.choice(["male", "female"])
        self.trait = trait if trait != None else random.choice(["...", "..."])
        self.breed_time = breed_time
        self.hunger = 10
        self.gen = 0

    def __str__(self):
        return self.symbol

def generate_coords(background, environment, len_x, len_y):    #  generate some coordinates not occupied
    x, y = 0, 0
    while environment[y][x] != background:
        x, y = random.randint(0, len_x-1), random.randint(0, len_y-1)
    return x, y

def get_surroundings(environment, x, y, len_x, len_y):

    surroundings = [environment[y-1][x-1], environment[y-1][x], "", environment[y][x-1], "", "", "", ""]

    surroundings[2] = environment[y-1][x+1] if x < len_x-1 else environment[y-1][0]

    surroundings[4] = environment[y][x+1] if x < len_x-1 else environment[y][0]

    surroundings[5] = environment[y+1][x-1] if y < len_y-1 else environment[0][x-1]
    surroundings[6] = environment[y+1][x] if y < len_y-1 else environment[0][x]

    s_y = y+1 if y < len_y-1 else 0
    s_x = x+1 if x < len_x-1 else 0
    surroundings[7] = environment[s_y][s_x]

    return surroundings

def move(environment, x, y, len_x, len_y, free_space):

    options = ["environment[y-1][x-1]=item", "environment[y-1][x]=item", "", "environment[y][x-1]=item", "", "", "", ""]

    options[2] = "environment[y-1][x+1]=item" if x < len_x-1 else "environment[y-1][0]=item"

    options[4] = "environment[y][x+1]=item" if x < len_x-1 else "environment[y][0]=item"

    options[5] = "environment[y+1][x-1]=item" if y < len_y-1 else "environment[0][x-1]=item"
    options[6] = "environment[y+1][x]=item" if y < len_y-1 else "environment[0][x]=item"

    s_y = "y+1" if y < len_y-1 else "0"
    s_x = "x+1" if x < len_x-1 else "0"
    options[7] = "environment[{}][{}]=item".format(s_y, s_x)

    return options

def spawn(environment, x, y, len_x, len_y, free_space):    #  creates a custom list of options, then picks one based upon the available free space

    options = ["environment[y-1][x-1]=cell('prey', '$', id, 10)", "environment[y-1][x]=cell('prey', '$', id, 10)", "", "environment[y][x-1]=cell('fish', '$', id, 10)", "", "", "", ""]

    options[2] = "environment[y-1][x+1]=cell('prey', '$', id, 10)" if x < len_x-1 else "environment[y-1][0]=cell('prey', '$', id, 10)"

    options[4] = "environment[y][x+1]=cell('prey', '$', id, 10)" if x < len_x-1 else "environment[y][0]=cell('prey', '$', id, 10)"

    options[5] = "environment[y+1][x-1]=cell('prey', '$', id, 10)" if y < len_y-1 else "environment[0][x-1]=cell('prey', '$', id, 10)"
    options[6] = "environment[y+1][x]=cell('prey', '$', id, 10)" if y < len_y-1 else "environment[0][x]=cell('prey', '$', id, 10)"

    s_y = "y+1" if y < len_y-1 else "0"
    s_x = "x+1" if x < len_x-1 else "0"
    options[7] = "environment[{}][{}]=cell('prey', '$', id, 10)".format(s_y, s_x)

    return options


def main_loop():

    gen = 1    #  min gen of 1

    len_x, len_y = 10, 10

    tick = 0.5    #  the time waited between generations
    frame_rate = 0.1    #  the time waited between updating the display

    background = "~"
    environment = [[background] * len_x for c in range(len_y)]    #  generate a 2d array

    for id in range(2):    #  generate some prey
        x, y = generate_coords(background, environment, len_x, len_y)
        environment[y][x] = cell("prey", "$", id, 10)

    for id in range(1):    #  generate some predators
        x, y = generate_coords(background, environment, len_x, len_y)
        environment[y][x] = cell("predator", "£", id, 10)

    while True:

        time.sleep(tick)

        x, y = 0, 0
        for row in environment:

            for item in row:

                if isinstance(item, cell) == True:

                    if item.species == "prey":

                        if item.gen < gen:    #  prevent applying rules to the same cell twice or more in a single generation

                            surroundings = get_surroundings(environment, x, y, len_x-1, len_y-1)
                            free_space = [a for a, b in enumerate(surroundings) if b == background]    #  a space is considered 'free' if it is only occupied by a background tile
                            mate = None
                            if any(isinstance(surround, cell) for surround in surroundings) == True:    #  check if there is an instance of the same class within the surrounding area

                                for surround in surroundings:
                                    if isinstance(surround, cell) == True:
                                        mate = surround

                                #  breed_time will get as low as 1, and only moves to 0 once a mate has been found
                                item.breed_time = 0 if item.breed_time == 1 else item.breed_time
                                mate.breed_time = 0 if mate.breed_time == 1 else mate.breed_time

                                if item.gender == "female" and mate.gender == "male" and free_space != [] and item.breed_time == 0 and mate.breed_time == 0:

                                    exec(spawn(environment, x, y, len_x, len_y, free_space)[int(random.choice(free_space))])    #  spawn a new fish at a random free space

                                    item.breed_time = 11
                                    mate.breed_time = 10

                            if free_space != [] and item.breed_time != 0:

                                exec(move(environment, x, y, len_x, len_y, free_space)[int(random.choice(free_space))])    #  move to a random free space
                                environment[y][x] = "~"

                            item.breed_time = item.breed_time-1 if item.breed_time > 1 else item.breed_time

                            item.gen += 1

                    elif item.species == "predator":

                        print(item.hunger)

                        if item.gen < gen:

                            if item.hunger == 0:
                                environment[y][x] = "~"    #  the predator dies due to hunger

                            surroundings = get_surroundings(environment, x, y, len_x-1, len_y-1)
                            free_space = [a for a, b in enumerate(surroundings) if b == background]    #  a space is considered 'free' if it is only occupied by a background tile
                            prey = None
                            if any(isinstance(surround, cell) for surround in surroundings) == True:    #  check if there is an instance of the same class within the surrounding area

                                for surround in surroundings:
                                    if isinstance(surround, cell) == True:
                                        prey = surround

                                if prey.species == "prey":
                                    
                                    exec(move(environment, x, y, len_x, len_y, free_space)[surroundings.index(prey)])
                                    environment[y][x] = "~"

                                    item.hunger += 3

                            if free_space != [] and prey == None:

                                exec(move(environment, x, y, len_x, len_y, free_space)[int(random.choice(free_space))])    #  move to a random free space
                                environment[y][x] = "~"

                            item.hunger = item.hunger-1 if item.hunger > 0 else item.hunger
                            item.gen += 1
                            
                    #  update the screen
                    time.sleep(frame_rate)
                    print("\x1b[0;0H")    #  resets screen and moves pointer to top left
                    print("Electric Fish // Gen: {} // Tick: {} // Size: {}x{}".format(gen, tick, len_x, len_y))
                    for row in environment:
                        for item in row:
                            print(" {} ".format(item), end="")
                        print()

                x+=1
            x = 0
            y+=1

        gen+=1


        

if __name__ == "__main__":
    main_loop()

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

    def __init__(self, species, symbol, id, breed_time, gender=random.choice(["male", "female"]), trait=random.choice(["male", "female"])):
        self.id = id
        self.symbol = symbol
        self.species = species
        self.gender = gender
        self.breed_time = breed_time

    def __str__(self):
        return self.symbol

def generate_coords(background, environment, len_x, len_y):    #  generate some coordinates not occupied
    x, y = 0, 0
    while environment[y][x] != background:
        x, y = random.randint(0, len_x-1), random.randint(0, len_y-1)
    return x, y

def get_surroundings(environment, x, y, len_x, len_y):

    surroundings = [environment[y-1][x-1], environment[y-1][x], "", environment[y][x-1], "", "", "", ""]

    surroundings[2] = environment[y-1][x+1] if x < len_x else environment[y-1][0]

    surroundings[4] = environment[y][x+1] if x < len_x else environment[y][0]

    surroundings[5] = environment[y+1][x-1] if y < len_y else environment[0][x-1]
    surroundings[6] = environment[y+1][x] if y < len_y else environment[0][x]

    s_y = y+1 if y < len_y else 0
    s_x = x+1 if x < len_x else 0
    surroundings[7] = environment[s_y][s_x]

    return surroundings

def main_loop():

    gen = 0

    len_x, len_y = 10, 10

    tick = 0.05

    background = "~"
    environment = [[background] * len_x for c in range(len_y)]    #  generate a 2d array

    spawn = {    #  link surroundings indexes to environment for breeding
    0:"environment[y+1][x-1]=cell('fish', '$', id, 10)",
    1:"environment[y+1][x]=cell('fish', '$', id, 10)",
    2:"environment[y+1][x+1]=cell('fish', '$', id, 10)",
    3:"environment[y][x-1]=cell('fish', '$', id, 10)",
    4:"environment[y][x+1]=cell('fish', '$', id, 10)",
    5:"environment[y-1][x-1]=cell('fish', '$', id, 10)",
    6:"environment[y-1][x]=cell('fish', '$', id, 10)",
    7:"environment[y-1][x+1]=cell('fish', '$', id, 10)"
    }

    move = {    #  link surroundings indexes to environment for movement
    0:"environment[y+1][x-1]=item",
    1:"environment[y+1][x]=item",
    2:"environment[y+1][x+1]=item",
    3:"environment[y][x-1]=item",
    4:"environment[y][x+1]=item",
    5:"environment[y-1][x-1]=item",
    6:"environment[y-1][x]=item",
    7:"environment[y-1][x+1]=item"
    }

    for id in range(2):    #  generate some fish
        x, y = generate_coords(background, environment, len_x, len_y)
        environment[y][x] = cell("fish", "$", id, 10)

    while True:

        time.sleep(tick)

        x, y = 0, 0
        for row in environment:

            for item in row:

                if isinstance(item, cell) == True:

                    surroundings = get_surroundings(environment, x, y, len_x-1, len_y-1)
                    free_space = [a for a, b in enumerate(surroundings) if b == background]

                    if item.symbol in surroundings:    #  breed
                        mate = surroundings[surroundings.index(item.symbol)]

                        if item.gender == "female" and mate.gender == "male" and free_space != [] and item.breed_time == 0 and mate.breed_time == 0:

                            exec(spawn[free_space[0]])    #  spawn a new fish at the first free space

                            item.breed_time = 11
                            mate.breed_time = 11

                    elif free_space != []:

                        exec(move[random.choice(free_space)])
                        environment[y][x] = "~"

                    item.breed_time -= 1

                x+=1
            x = 0
            y+=1

        gen+=1


        #  update the screen
        print("\x1b[0;0H")    #  resets screen and moves pointer to top left
        print("Electric Fish // Gen: {} // Tick: {} // Size: {}x{}".format(gen, tick, len_x, len_y))
        for row in environment:
            for item in row:
                print(" {} ".format(item), end="")
            print()

if __name__ == "__main__":
    main_loop()

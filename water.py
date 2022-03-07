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

    options = ["environment[y-1][x-1]='~'", "environment[y-1][x]='~'", "", "environment[y][x-1]='~'", "", "", "", ""]

    options[2] = "environment[y-1][x+1]='~'" if x < len_x-1 else "environment[y-1][0]='~'"

    options[4] = "environment[y][x+1]='~'" if x < len_x-1 else "environment[y][0]='~'"

    options[5] = "environment[y+1][x-1]='~'" if y < len_y-1 else "environment[0][x-1]='~'"
    options[6] = "environment[y+1][x]='~'" if y < len_y-1 else "environment[0][x]='~'"

    s_y = "y+1" if y < len_y-1 else "0"
    s_x = "x+1" if x < len_x-1 else "0"
    options[7] = "environment[{}][{}]='~'".format(s_y, s_x)

    return options


def main_loop():

    gen = 1    #  min gen of 1

    len_x, len_y = 10, 10

    tick = 0.5    #  the time waited between generations

    background = ""
    #environment = [[background] * len_x for c in range(len_y)]    #  generate a 2d array

    environment = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "", "", "", "", "", "", "", "", "#"],
    ["#", "", "", "", "", "", "", "", "", "#"],
    ["#", "", "", "", "", "", "", "", "", "#"],
    ["#", "", "", "", "", "", "", "", "", "#"],
    ["#", "", "", "", "", "", "", "", "", "#"],
    ["#", "", "", "", "", "", "", "", "", "#"],
    ["#", "", "", "", "", "", "", "", "", "#"],
    ["#", "", "", "", "", "", "", "", "", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ]

    while True:

        #  generate water infinitly
        environment[1][1] = "~"

        time.sleep(tick)

        x, y = 0, 0

        for row in environment:

            for item in row:

                if item == "~":

                    surroundings = get_surroundings(environment, x, y, len_x, len_y)
                    free_space = [a for a, b in enumerate(surroundings) if b == background]    #  a space is considered 'free' if it is only occupied by a background tile

                    print(free_space)

                x+=1
            x = 0
            y+=1

        gen+=1

        #  update the screen
        print("\x1b[0;0H")    #  resets screen and moves pointer to top left
        print("Gen: {} // Tick: {} // Size: {}x{}".format(gen, tick, len_x, len_y))
        for row in environment:
            for item in row:
                color = "\033[36m" if isinstance(item, cell) == False else "\033[33m" if item.species == "prey" else "\033[31m"    #  determine color for item
                print(" {}{}{} ".format(color, item, "\x1b[0m"), end="")    #  print item onto same line with added color
            print()


if __name__ == "__main__":
    main_loop()

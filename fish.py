# Electric Fish
import random
import sys
import os
import time

class environment(object):

    def __init__(self):
        self.domain = [
        "#","#","#","#","#","#","#","#","#","#",
        "#","~","~","~","~","~","~","~","~","#",
        "#","~","~","~","~","~","~","~","~","#",
        "#","~","~","~","~","~","~","~","~","#",
        "#","~","~","~","~","~","~","~","~","#",
        "#","~","~","~","~","~","~","~","~","#",
        "#","~","~","~","~","~","~","~","~","#",
        "#","~","~","~","~","~","~","~","~","#",
        "#","~","~","~","~","~","~","~","~","#",
        "#","~","~","~","~","~","~","~","~","#",
        "#","#","#","#","#","#","#","#","#","#",
        ]

    def animate_water(self):
        pass

    def generate_land(self):
        pass


class predator(object):

    def __init__(self, id):
        self.species = "predator"
        self.id = id

        self.gender = random.choice(["male", "female"])

        self.breed_time = 10

        self.surroundings = [
           "",
        "",   "",
           "",
        ]

        self.stuck = False

    def update_surroundings(self, domain, coord):
        self.surroundings[0] = "#" if coord < 10 else domain[coord-10]
        self.surroundings[1] = "#" if coord == 0 else domain[coord-1]
        self.surroundings[2] = "#" if coord == 99 else domain[coord+1]
        self.surroundings[3] = "#" if coord > 88 else domain[coord+10]


class prey(object):

    def __init__(self, id, inherit=False):
        self.species = "prey"
        self.id = id

        self.gender = random.choice(["male", "female"])

        self.breed_time = 10

        if inherit != False:
            self.trait = inherit.trait    #  inherit parents trait
        else:
            self.trait = random.choice(["run", "freeze", "ignore"])    #  otherwise gen a random trait

        self.surroundings = [
           "",
        "",   "",
           "",
        ]

        self.stuck = False

    def update_surroundings(self, domain, coord):
        self.surroundings[0] = "#" if coord < 10 else domain[coord-10]
        self.surroundings[1] = "#" if coord == 0 else domain[coord-1]
        self.surroundings[2] = "#" if coord == 99 else domain[coord+1]
        self.surroundings[3] = "#" if coord > 88 else domain[coord+10]
        #  some quick checks
        if "" in self.surroundings:
            self.surroundings[self.surroundings.index("")] = "~"


def empty_space():
    while True:
        coord = random.randint(0, 99)
        if environment.domain[coord] == "~":
            break
    return coord

if __name__ == "__main__":

    #  initialise the environment
    environment = environment()

    tick = 1

    gen = 0

    animals = {}

    #  split string function
    split_string = lambda x, n: [x[i:i+n] for i in range(0, len(x), n)]

    #  generate 10 prey
    for new_id in range(10):
        coord = empty_space()
        animals.update({prey(new_id):coord})
        environment.domain[coord] = "$"

    #  generate 1 predator
    for new_id in range(1):
        coord = empty_space()
        animals.update({predator(new_id):coord})
        environment.domain[coord] = "£"

    #  main loop
    while True:
        time.sleep(tick)

        for animal, self_coord in animals.items():

            if animal.breed_time != 0:
                animal.breed_time -= 1

            animal.update_surroundings(environment.domain, animals[animal])    #  make sure animal is aware of surroundings

            if animal.species == "prey":

                move = True

                for item in animal.surroundings:
                    if item == "£":
                        if animal.trait == "freeze":
                            move = False

                        elif animal.trait == "run":
                            run = {0:3, 1:2, 2:1, 3:0}
                            move = run[animal.surroundings.index(item)]
                    elif item == "$":

                        #  find instance of mate
                        coords = [-10,-1,1,10]
                        if "$" in animal.surroundings:
                            mate_coord = self_coord+coords[animal.surroundings.index(item)]
                            for animal, coord in animals.items():
                                if animal == "prey" and coord == mate_coord:
                                    mate = animal

                        if (
                            ('mate' in vars() or 'mate' in globals())
                            and animal.breed_time == 0
                            and mate.breed_time == 0
                            and animal.gender == "female"
                            and animal.gender != mate.gender
                        ):
                            for item in animal.surroundings:
                                if item == "~":
                                    coord = self_coord+coords[animal.surroundings.index(item)]
                                    animals.update({prey(id, animal):coord})    #  inherit some parental traits

                                    #  reset the breed time for both animals
                                    animal.breed_time = 10
                                    mate.breed_time = 10


                free_space = [
                    index - 1
                    for index in range(4)
                    if animal.surroundings[index - 1] == "~"
                ]

                if not free_space:
                    stuck = True

                else:
                    animal.stuck = False
                    stuck = False

                if animal.stuck == True and stuck:
                    #  animal dies
                    pass

                elif stuck:
                    move = False
                    animal.stuck = True

                if move != False:
                    if move == True:
                        self_coord = animals[animal]
                        coords = [-10,-1,1,10]
                        try:
                            direction = random.choice(free_space)
                        except:
                            direction = 0
                        if self_coord+coords[direction] < 0:
                            move = False
                        else:
                            move = self_coord+coords[direction]

                    #  move to specified coords
                    try:
                        if environment.domain[move] == "~":
                            environment.domain[animals[animal]] = "~"    #  remove animal from previous location
                            environment.domain[move] = "$"    #  move animal to new location
                            animals[animal] = move    #  update the animals coordinates in memory
                    except:
                        pass    #  cannot move to location, so remain still


        #  update screen
        print("\x1b[0;0H")    #  resets screen and moves pointer to top left
        print("Electric Fish // Gen: {} // Tick speed: {} // Alive: {}".format(gen, tick, len(animals)))    #  add some info

        out = " ".join(environment.domain)
        out = split_string(out, 20)

        for row in out:
            print(row)

        gen += 1

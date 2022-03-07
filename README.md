# Electric Fish

A collection of electric animal cellular automata..

These animals (predators and prey) act first upon their behaviors (which are defined at birth) and then upon the rules for their movement.

## Environment rules:
As the simulation is within an aquatic environment, certain rules apply to the creatures inside of it.

 - If an animal cannot move around, they cannot breathe and so die.
 - Both predator and prey can be forced into this situation.
 - Exceptions are made for if the prey has the Freeze trait and a predator is close by.

## Animal rules:
 - All animals can see directly above, below, left and right of them by one cell.
 - They can also move in any of those directions, providing the space is unoccupied.

## Predators:
Predators need to feed upon prey in order to survive. Eating a fish will keep it alive for 5 ticks (stackable).

### Predator behavior:
 - If a predator meets another predator, they will react according to their birth trait:
    1. Avoid, moving in the opposite direction to the other predator.
    3. Passive, ignoring the predator completely
Predators will not attack other predators.

### Predator movement:
 - A predator will always eat a prey if it can reach it.
 - If multiple prey are within range, it will eat the prey it encounters first (views surroundings from top left along to bottom right).
 - If there are no prey, it will move towards the last known location of a prey.
 - If no prey have been encountered, or if the predator cannot move into the location (e.g.: a wall is blocking it), they will move in a random available direction.


## Prey:
Prey do not need to feed to survive (i.e.: they feed off invisible algae in the water).

#### Prey behavior:
 - If they are close to a predator, they will react according to their birth trait:
    1. Run, moving directly away from the predator.
    2. Freeze, remain still and not move.
    3. Ignore, continue as if the predator was not there.
- If they are close to another prey of the opposite gender, they will mate and the offspring will move into the next available space. If there is no available space, they will not mate.

### Prey movement:
The rules for prey movement will only apply if there is no predator nearby, or if the prey's trait is to ignore the predator.
 - The prey will select a random direction that it is allowed to move into (i.e.: not blocked by a wall and not occupied by another prey or predator).

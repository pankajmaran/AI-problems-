# wumpus world

import random
import numpy as np
count = 1
class WumpusWorld:
    def __init__(self, blocks, pits, gold, wumpus, initial_location):
        self.initial_location = initial_location  # copy the input
        self.wumpus = wumpus
        self.pits = pits
        self.gold = gold
        self.blocks = blocks
        self.player = self.initial_location
        self.has_arrow = True

        self.breeze = {}  # stores locations of breezy squares
        self.stench = {}  # stores location of smelly squares

        for p in self.pits:  # initalise breezy squares
            for l in self.neighbours(p):
                self.breeze[l] = True
        for w in self.wumpus:  # intialise smelly squares
            for l in self.neighbours(w):
                self.stench[l] = True

    def neighbours(self, loc):  # returns neighbours of tuple loc = (x,y)
        return [(loc[0] + 1, loc[1]), (loc[0] - 1, loc[1]), (loc[0], loc[1] + 1), (loc[0], loc[1] - 1)]

    def arrow_hits(self, location, dx, dy):  # scans to see if the arrow hits
        while location not in self.blocks:
            location = (location[0] + dx, location[1] + dy)
            if location in self.wumpus:
                return True
        return False

    def print(self):  # print the board state (useful for debugging)
        global count
        if count > 10:
            return 
        count+=1
        print(self.player)
        xmin = min([x for x, y in self.blocks])
        xmax = max([x for x, y in self.blocks])
        ymin = min([y for x, y in self.blocks])
        ymax = max([y for x, y in self.blocks])
        for y in range(ymin, ymax + 1):
            for x in range(xmin, xmax + 1):

                if (x, ymax - y) in self.blocks:
                    print('B', end='')
                elif (x, ymax - y) in self.wumpus:
                    print('W', end='')
                elif (x, ymax - y) in self.pits:
                    print('P', end='')
                elif (x, ymax - y) in self.gold:
                    print('G', end='')
                elif self.player == (x, ymax - y):
                    print('Y', end='')
                else:
                    print(' ', end='')
            print("")
        b = self.player in self.breeze  # is their square breezy?
        s = self.player in self.stench  # is it smelly?
        print("arrow: " + str(self.has_arrow))
        print("breezy: " + str(b))
        print("stenchy: " + str(s))

    def sim(self, agent):
        t = 0
        self.has_arrow = True
        self.player = self.initial_location
        while t < 1000:
            t += 1

            self.print()

            b = self.player in self.breeze  # is their square breezy?
            s = self.player in self.stench  # is it smelly?
            agent.give_senses(self.player, b, s)  # give the agent its senses
            action = agent.get_action()  # get the agents action
            print(action, end='\n\n')

            new_location = self.player
            if action == 'MOVE_UP':  # update the location for moving up/down/left/right
                new_location = (self.player[0], self.player[1] + 1)
            elif action == 'MOVE_DOWN':
                new_location = (self.player[0], self.player[1] - 1)
            elif action == 'MOVE_LEFT':
                new_location = (self.player[0] - 1, self.player[1])
            elif action == 'MOVE_RIGHT':
                new_location = (self.player[0] + 1, self.player[1])
            elif not self.has_arrow and action[0:5] == 'SHOOT':  # check the agent has the arrow if they shot
                return 'NO ARROW'
            elif action == 'SHOOT_UP':  # check to see if the agent killed the wumpus
                if self.arrow_hits(self.player, 0, 1):
                    self.wumpus = {}
                    agent.killed_wumpus()
            elif action == 'SHOOT_DOWN':
                if self.arrow_hits(self.player, 0, -1):
                    self.wumpus = {}
                    agent.killed_wumpus()
            elif action == 'SHOOT_LEFT':
                if self.arrow_hits(self.player, -1, 0):
                    self.wumpus = {}
                    agent.killed_wumpus()
            elif action == 'SHOOT_RIGHT':
                if self.arrow_hits(self.player, 1, 0):
                    self.wumpus = {}
                    agent.killed_wumpus()
            elif action == 'QUIT':
                return 'QUIT'

            if action[0:5] == 'SHOOT':  # remove the arrow if it was shot
                self.has_arrow = False

            if new_location in self.pits:  # check if fell into a pit
                return 'FELL'
            if new_location in self.wumpus:  # check if eaten by wumpus
                return 'EATEN'
            if new_location in self.gold:  # check if found gold
                return 'GOLD'

            if new_location not in self.blocks:  # if agent ran into a wall, then reset position
                self.player = new_location


class Agent:
    def __init__(self):
        self.wump = [['A' for i in range(50)] for j in range(50)]
        self.kb = [['A' for i in range(50)] for j in range(50)]
        self.moves = []
        self.move = 1
        self.tb = False
        self.move_stack = []
        self.unsafe = []
        self.border = False
        self.prev = []
        self.f = False
        self.exp_t = False
        self.shoot = ""
        self.arrow_fired = False
        self.visited = []
        self.a = False
        self.right_border = False
        self.left_border = False
        self.last_move = 'null'
        self.step_back = False
        self.counter = 0

    def get_action(self):
        actions = ['MOVE_UP', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_RIGHT']
        extras = ['SHOOT_UP', 'SHOOT_DOWN', 'SHOOT_LEFT', 'SHOOT_RIGHT']
        self.counter += 1
        if self.counter > 999:
            return "QUIT"
        if self.shoot in extras and self.arrow_fired == False:
            if self.move_p == actions[0]:
                self.last_move = actions[1]
            if self.move_p == actions[1]:
                self.last_move = actions[0]
            if self.move_p == actions[2]:
                self.last_move = actions[3]
            if self.move_p == actions[3]:
                self.last_move = actions[2]
            self.step_back = True
            self.arrow_fired = True
            return self.shoot

        if self.step_back == True:
            self.step_back = False
            return self.last_move

        if self.f == False:
            if self.exp_t == True:
                # self.unsafe=[
                self.exp_t = False
                self.f = True
            else:
                return (self.explore_world())

        if self.f == True:
            t = self.make_move()
            self.f = False
            return t

    def explore_world(self):
        actions = ['MOVE_UP', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_RIGHT']
        if self.move == 1 and self.tb == False:
            self.tb = True
            self.moves.append(actions[0])
            self.move_p = actions[0]
            return actions[0]
        if self.move == 1 and self.tb == True:
            self.tb = False
            self.move = 2
            if self.border == False:
                return actions[1]
            else:
                return actions[0]

        if self.move == 2 and self.tb == False:
            self.tb = True
            self.moves.append(actions[1])
            self.move_p = actions[1]
            return actions[1]
        if self.move == 2 and self.tb == True:
            self.tb = False
            self.move = 3
            if self.border == False:
                return actions[0]
            else:
                return actions[1]

        if self.move == 3 and self.tb == False:
            self.tb = True
            self.moves.append(actions[2])
            self.move_p = actions[2]
            return actions[2]
        if self.move == 3 and self.tb == True:
            self.tb = False
            self.move = 4
            if self.border == False:
                return actions[3]
            else:
                return actions[2]

        if self.move == 4 and self.tb == False:
            self.tb = True
            self.moves.append(actions[3])
            self.move_p = actions[3]
            return actions[3]
        if self.move == 4 and self.tb == True:
            self.tb = False
            self.move = 1
            self.moves = []
            self.exp_t = True
            if self.border == False:
                return actions[2]
            else:
                return actions[3]

    def make_move(self):
        self.f = False
        actions = ['MOVE_UP', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_RIGHT']
        temp = []
        t = self.check_pit(self.prev)
        if isinstance(t, int):
            if actions[t] in self.unsafe:
                if len(self.unsafe) != 1:
                    for item in self.unsafe:
                        if item == actions[t]:
                            self.unsafe.remove(item)
        for item in actions:
            if item not in self.unsafe:
                temp.append(item)
        self.unsafe = []
        self.a = True
        if temp:
            return (random.choice(temp))

    def give_senses(self, location, breeze, stench):
        actions = ['MOVE_UP', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_RIGHT']
        extras = ['SHOOT_UP', 'SHOOT_DOWN', 'SHOOT_LEFT', 'SHOOT_RIGHT']
        x = location[0]
        y = location[1]
        if stench == True:
            self.wump[x][y] = 's'
        if breeze == True:
            self.kb[x][y] = 'b'
            self.locate_pit(location)
        if breeze == False and stench == False:
            self.kb[x][y] = 'o'
            self.wump[x][y] = 'o'
        if self.prev == location:
            self.border = True
        else:
            self.prev = location
            self.border = False
        if (breeze == True):
            self.unsafe.append(self.move_p)
        if stench == True:
            if self.arrow_fired == False:
                self.unsafe.append(self.move_p)
        c = self.killed_wumpus()
        if c in extras:
            self.shoot = c
        # input()
        # print (np.matrix(self.kb[-1::-1]))

    def killed_wumpus(self):
        c = (0, 0)
        v = (0, 0)
        x = 0
        y = 0
        l = []
        l = self.prev
        for i, lst in enumerate(self.wump):
            for j, k in enumerate(lst):
                if k == "s":
                    c = (i, j)

        if c:
            x, y = c

            if self.wump[x + 2][y] == 's':
                self.wump[x + 1][y] = 'w'
            if self.wump[x - 2][y] == 's':
                self.wump[x - 1][y] = 'w'
            if self.wump[x + 1][y + 1] == 's':
                self.wump[x + 1][y] = 'w'
            if self.wump[x + 1][y - 1] == 's':
                self.wump[x + 1][y] = 'w'
            if self.wump[x - 1][y + 1] == 's':
                self.wump[x][y + 1] = 'w'
            if self.wump[x - 1][y - 1] == 's':
                self.wump[x][y - 1] = 'w'

        extras = ['SHOOT_UP', 'SHOOT_DOWN', 'SHOOT_LEFT', 'SHOOT_RIGHT']
        for i, lst in enumerate(self.wump):
            for j, k in enumerate(lst):
                if k == "w":
                    v = (i, j)

        if l[0] == v[0]:
            if l[1] > v[1]:
                return (extras[1])
            else:
                return (extras[0])
        if l[1] == v[1]:
            if l[0] > v[0]:
                return (extras[2])
            else:
                return (extras[3])

    def locate_pit(self, location):
        x = location[0]
        y = location[1]
        if self.kb[x + 2][y] == 'b' and self.kb[x + 1][y + 1] == 'b':
            self.kb[x + 1][y] = 'p'
        if self.kb[x + 2][y] == 'b' and self.kb[x + 1][y - 1] == 'b':
            self.kb[x + 1][y] = 'p'
        if self.kb[x - 2][y] == 'b' and self.kb[x - 1][y + 1] == 'b':
            self.kb[x - 1][y] = 'p'
        if self.kb[x - 2][y] == 'b' and self.kb[x - 1][y - 1] == 'b':
            self.kb[x + 1][y] = 'p'
        if self.kb[x][y + 2] == 'b' and self.kb[x + 1][y + 1] == 'b':
            self.kb[x][y + 1] = 'p'
        if self.kb[x][y + 2] == 'b' and self.kb[x - 1][y + 1] == 'b':
            self.kb[x][y + 1] = 'p'
        if self.kb[x][y - 2] == 'b' and self.kb[x + 1][y - 1] == 'b':
            self.kb[x][y - 1] = 'p'
        if self.kb[x][y - 2] == 'b' and self.kb[x - 1][y - 1] == 'b':
            self.kb[x][y - 1] = 'p'

    def check_pit(self, l):
        x = l[0]
        y = l[1]
        if self.kb[x + 1][y] == 'p':
            return 3
        if self.kb[x - 1][y] == 'p':
            return 2
        if self.kb[x][y + 1] == 'p':
            return 0
        if self.kb[x][y - 1] == 'p':
            return 1


# width of the wumpus playgound
width = 5

# setting the intial parameters
blocks = set()

for x in range(width + 1):
    blocks.add((0, x))
    blocks.add((x, 0))
    blocks.add((width, x))
    blocks.add((x, width))

gold = {(4,1)}
pits = {(3, 3)}
wumpus_location = {(2, 2)}
initial_location = (1, 1)

world1 = WumpusWorld(blocks=blocks, gold=gold, wumpus=wumpus_location, pits=pits, initial_location=initial_location)
agent = Agent()
print(world1.sim(agent))

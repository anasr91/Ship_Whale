import math
import random
def dist(x1, y1, x2, y2):
    return int(math.sqrt((x1 - x2)**2 + (y1 - y2)**2)) # L_2

########################################################################
class Whale:

    whale_range = 10
    def __init__(self):
        self.x = random.randrange(self.whale_range)
        self.y = random.randrange(self.whale_range)

        print("whale at: ", self.x, self.y)
    def move(self):
       pass
       '''
        r = [0, -1, 1]
        zx = self.whale_range + 1
        zy = self.whale_range + 1

        while not (0 <= zx < self.whale_range):
            zx = self.x + random.choice(r)
        self.x = zx

        while not (0 <= zy < self.whale_range):
            zy = self.y + random.choice(r)
        self.y = zy
        '''
    def estimated_by(self, ship):
        ship.measure(dist(self.x, self.y, ship.x, ship.y)) # basic whale does not move in core task

    def found_by(self, ship):
        return dist(self.x, self.y, ship.x, ship.y) == 0

    def __repr__(self):
        return "Whale blows at %d,%d" % (self.x, self.y)
########################################################################

class Ship:
    def __init__(self, xwhale, ywhale):
        self.x_range = xwhale
        self.y_range = ywhale
        # this is the a priori probability
        p_w = {}
        for x in range(xwhale):
            for y in range(ywhale):
                p_w[x,y] = 1 / (xwhale * ywhale) #gets probability of whale in all grid
                # fill in expression
        self.p_w = p_w
        self.x = random.randrange(self.x_range)
        self.y = random.randrange(self.y_range)
        # characteristics of distance measure: p(d|x,y) where x,y is a
        #  possible position of the whale (remember the mine problem)






    def p_d_cond_w(self, d, x, y):
        ...
        # fill in probability p(d|x,y) of finding a distance d if x,y
        #  is the position of the whale. Note that ship has access to
        # its own position via self.x and self.y

        return int(dist(x, y, self.x, self.y) == d) # return 1 if the distance are equal 0 otherwise

    def measure(self, d):
        # for each possible position w=x,y of the whale
        #  calculate p(w|d)

        p_w_cond_d = {}
         # new probabilities for whale position, if distance ’d’ has
        #  been measured: p(w|d) = p(d|w) p(w)
        ...
        # fill in the Bayesian formula for calculating p_w_cond_d, i.e. p(w|d)



        count = 0 # count the number of places whale might be

        for i in range(self.x_range):
            for j in range(self.y_range):

                if self.p_d_cond_w(d, i, j) and self.p_w[i, j] != 0:
                    self.p_w[i, j] = 1 # put 1 in all places whale might be
                    count += 1
                else:
                    self.p_w[i, j] = 0

        for key, value in self.p_w.items():
            if value == 1 and self.p_w[key] != 0:
                self.p_w[key] = 1/count # divides count in all the places that has 1 (whale places)


    def show_model(self):

        # 0,0 is on the bottom left
        print("ship now at ", self.x, self.y)
        for y in (reversed(range(self.y_range))): #reversed y and swaped x and y so the 0,0 can be on the bottom left as a normal x-y axis
            for x in (range(self.x_range)):
                if self.x == x and self.y == y:
                    print("ship ", end="- ")
                else:
                    print("%.2f" % self.p_w[x, y], end=" - ")
            print("\n")

        # fill in a print routine printing the current Bayesian model # p(w|d) where w is the whale position (x,y)

    def move(self):
        ...
        # fill in a ship’s move. Begin with random jumps, for simplicity
        '''
        # ship moves random
        r = [0, -1, 1]
        zx = self.x_range + 1
        zy = self.y_range + 1

        while not(0 <= zx < self.x_range):
            zx = self.x + random.choice(r)
        self.x = zx

        while not(0 <= zy < self.y_range):
            zy = self.y + random.choice(r)
        self.y = zy
        '''

        if (self.p_w[self.x, self.y] == 1): # if the ship and the whale are at the same point it wont move
            return

        # get points of p_w and save in list_w
        list_w = [] # where i will save whale points in list in a list.
        for key, value in self.p_w.items():
            if self.p_w[key] != 0:
                list_w.append([key[0], key[1]])

        # get points of ship neighbors and save them in list_n
        list_n = {}
        for x in range(self.x_range):
            for y in range(self.y_range):
                for x, y in [(self.x + i, self.y + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
                    if (x, y) in self.p_w:
                        list_n[(x, y)] = self.p_w[(x, y)]

        list_nn = []
        #convert the list_n dict to list_nn list so i can use it with list_w
        for key, value in list_n:
            list_nn.append([key, value])

        x = 1111 # anylarge value so i can compare the fist time
        count = 0# the count of number of times i get the lowest distance
        ii = [] # is a list that will take the index of list_nn and the count

        for i in range(len(list_nn)):
            for j in range(len(list_w)):
                d = dist(list_w[j][0], list_w[j][1], list_nn[i][0], list_nn[i][1])
                if d < x:
                    x = d
                    ii = [[i, count]]
                    count = 0

                elif d == x:
                    count += 1
                    ii.append([i, count])

        x=1111 # anylarge value so i can compare the fist time
        ln = [] # new list save the index that i will use in the list_nn

        for t in range(len(ii)):
            if ii[t][1] < x:
                ln.append(t)
        x = 1111

        for i in range(len(ii)):
            if ii[i][1] < x:
                x = ii[i][0]

        self.x = list_nn[x][0]
        self.y = list_nn[x][1]



        '''
        count = []
        inttt = 0
        intt = 0
        for i, j in list_n.items():
            for key, value in self.p_w.items():
                zz = dist(key[0],key[1],i[0],i[1])
                dd = zz
                inttt += 1
                if dd <= zz:
                    count.insert(dd, inttt)
            intt += 1
        z = 1111
        pp = 0
        for i in count:
            if i < z:
                z = i

        for key, value in list_n.items():
            pp += 1
            if pp == z:
                self.x = key[0]
                self.y = key[1]

        '''
    def __repr__(self):
        return "Ship at %d,%d" % (self.x, self.y) # pretty print

def run(whale, ship):
    while not whale.found_by(ship):
        input()
        whale.move()
        whale.estimated_by(ship) # ship gets distance
        ship.show_model() # show current Bayesian model
        ship.move() # to be filled in
        print(ship)
    print("Whale found")


whale = Whale()
ship = Ship(whale.whale_range, whale.whale_range)
run(whale, ship)
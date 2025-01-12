import numpy as np
import box
from box import point, Box, space, d1
import copy
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# from timeit import default_timer as timer
# from model import d2


# THIS FILE CONTAINS THE MAIN FUNCTIONS FOR THE HIT AND RUN ALGORITHM

class hitAndRun:

    def __init__(self, U, S):
        self.lang = S
        self.space = U
        self.samples = []
        self.n = U.dim

    def run(self, N):
        while True:
            x = self.space.sample(10)[0]
            if d1(x,self.lang) >= 0:
                break
        self.samples = [x]
        for i in range(0,N):
            p = self.hitAndRun(self.samples[-1])
            if p != None:
                self.samples.append(p)
    
    def hitAndRun(self, x):
        while True:
            y = self.moveInDirection(copy.deepcopy(x))
            if y == None:
                return None
            z = self.pointOnSeg(x,y)
            return z
    
    def moveInDirection(self,x):
        direction = np.zeros(x.dim)
        for i in range(x.dim):
            direction[i] = random.uniform(-1, 1)
        direction = direction/np.linalg.norm(direction)
        print(direction)
        dist = d1(x,self.lang)
        if dist < 0.001:
            dist = 1
        xcoord = np.array(x.coord)
        dist1 = -1000
        while not (dist < 0.001 and dist < dist1) and dist >= -1E-3:
            dist1 = dist
            xcoord = xcoord + dist*direction
            x.coord = xcoord.tolist()
            dist = d1(x,self.lang)
            if dist < -1E-3:
                return None
        return x
    
    def pointOnSeg(self, x, y):
        # Chooses randomly a point on the segment [x,d]
        t = random.uniform(0,1)
        print(t)
        # t= 0.5
        z = point(x.dim)
        for i in range(0,x.dim):
            z.coord[i] = (1-t)*x.coord[i] + t*y.coord[i]
        return z
    

if __name__ == "__main__":
    U = space(2)
    B0 = Box(2)
    B0.Borders = [[0,20],[0,20]]
    U.addBoxes(B0)
    S = space(2)
    B = Box(2)
    B.Borders = [[3,6],[3,14]]
    B1 = Box(2)
    B1.Borders = [[5,14],[12,17]]
    S.addBoxes(B)
    S.addBoxes(B1)
    H = hitAndRun(U,S)
    H.run(1000)

    fig, ax = plt.subplots()
    for i in H.samples:
        print(i.coord)
        i.plot(ax,1)
    
    S.plot(ax)
    print("done")




    

import numpy as np
import box
from box import point, Box, space, d1, d1D
import copy
import random
import matplotlib
from sklearn.cluster import KMeans
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
        self.tlist = []
        self.n = U.dim

    def run(self, N):
        while True:
            x = self.lang.sample(10)
            x = random.choice(x)
            if d1(x,self.lang) >= 0:
                break
        self.samples.append(x)
        self.tlist.append(0)
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
        dist = d1(x,self.lang)
        if dist < 0.1:
            dist = 1
        xcoord = np.array(x.coord)
        dist1 = -1000
        while not (dist < 0.01 and dist < dist1) and dist >= 0:
            dist1 = dist
            if dist == 1:
                dist1 = d1(x,self.lang)
            xcoord = xcoord + dist*direction
            x.coord = xcoord.tolist()
            dist = d1(x,self.lang)
            if dist < -1E-3:
                return None
        return x
    
    def pointOnSeg(self, x, y):
        # Chooses randomly a point on the segment [x,d]
        t = random.uniform(0,1)
        # t= 0.5
        z = point(x.dim)
        for i in range(0,x.dim):
            z.coord[i] = (1-t)*x.coord[i] + t*y.coord[i]
        self.tlist.append(t)
        return z
    

if __name__ == "__main__":
    n = 2
    U = space(n)
    B0 = Box(n)
    B0.repeatBorders(0,20)
    U.addBoxes(B0)
    S = space(n)
    
    B = Box(n)
    B.repeatBorders(4,12)

    B1 = Box(n)
    B1.repeatBorders(10,14)
    B1.repeatBorders(6,10,n//2)

    S.Boxes = [B,B1]
    H = hitAndRun(U,S)
    for i in range(0,100):
        H.run(10000)
    # H.run(10000)

    # fig, ax = plt.subplots()
    disT = 0
    wall_dict = []
    for i in range(0,len(H.samples)):
        dis, wall = d1D(H.samples[i],S)
        # disT += dis
        # if wall not in wall_dict:
        #     wall_dict.append(wall)
        # H.samples[i].plot(ax, 1)

    # print(disT/len(H.samples))
    # wall_dict.sort()
    # print(wall_dict)
    # print(len(wall_dict))

    # Convert samples to numpy array for clustering
    sample_coords = np.array([sample.coord for sample in H.samples])
    print("done sampling")

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=2, random_state=0).fit(sample_coords)

    # Get cluster centers and labels
    centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    # Get the clusters
    clusters = {i: [] for i in range(2)}
    for idx, label in enumerate(labels):
        clusters[label].append(H.samples[idx])


    # Print the cluster centers
    print("Cluster centers:\n", centers)

    
    # S.plot(ax)
    print("done")




    
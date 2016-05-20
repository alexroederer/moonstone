'''
analysis.py runs analysis on a cooccurance matrix to find clusters 
Current implementation uses Shi-Malik algorithm (normalized cuts): 
use symmetric normalized Laplacian, find second-smallest eigenvalue, use eigenvector. 

@author: Alexander Roederer
@date: May 16, 2016

Note: figure out where lonely 'mayonnaise' item in dataset (no other ingredients in recipe) is coming from

'''

from log_recipe import DataLog

import numpy as np
from scipy.cluster.vq import vq, kmeans2
from scipy.linalg import eigh

from matplotlib import pyplot as plt

class ClusterCooccurance:
    def __init__(self, weightedAdjacency):
        self.wadjM = weightedAdjacency
        self.fadjM = (self.wadjM != 0).astype(int)
        #Remove self-loops
        np.fill_diagonal(self.fadjM, 0)
        np.fill_diagonal(self.wadjM, 0)

        #Drop empty rows/columns in both matricies; 
        #Theoretically, if the recipe parser were good, this should never happen;
        #Single-ingredient recipes are rare. 
        empty = np.where(np.sum(self.fadjM,0) == 0)
        self.wadjM = np.delete(self.wadjM, empty, axis=0)
        self.wadjM = np.delete(self.wadjM, empty, axis=1)
        self.fadjM = np.delete(self.fadjM, empty, axis=0)
        self.fadjM = np.delete(self.fadjM, empty, axis=1)

        #Create degree matrix
        self.degreeM = np.diag(np.sum(self.wadjM,0))

        #Create inverse rooted degree matrix
        self.degreeMSplit = np.diag(1/np.sqrt((np.sum(self.wadjM,0)*1.0)))

        #Simple laplacian
        #self.laplacian = self.degreeM - self.wadjM

        #Normalized laplacian
        #Laplacian ends up being identity matrix??? TODO
        self.laplacian = self.degreeMSplit * ( self.degreeM -  self.wadjM )* self.degreeMSplit

        #Decompose laplacian to find eigenvalues
        self.eigenvalues, self.eigenvectors = eigh(self.laplacian)
        self.k = 20  #num clusters

        #Select largest eigenvalues to form clusters
        self.largeEigVal = self.evals[0:self.k]
        self.largeEigVec = self.evecs[0:self.k]

        self.newFeatures = np.transpose(self.largeEigVec)
        #K-means over them to find clusters
        centers, self.clusters = kmeans2(self.newFeatures, self.k)

    def printClusterContents(self, labels, cluster):
        a, = np.where(cc.clusters==cluster)
        print(labels[a])

if __name__ == '__main__':
    print("Beginning Analysis")

    print("Create data")
    #fileLoc = './data/openrecipes.txt'
    #fileLoc = './data/recipeitems-latest.json'

    pickleFile = './data.pkl'
    dlog = DataLog(None, pickleLoc=pickleFile)
    
    print("Run Analysis")
    cc = ClusterCooccurance(dlog.cooccuranceMatrix)

    print(cc.clusters)
    f = np.array(dlog.foods)
    for i in range(0, cc.k):
        cc.printClusterContents(f, i)
    

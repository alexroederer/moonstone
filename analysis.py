'''
analysis.py runs analysis on a cooccurance matrix to find clusters 
Current implementation finds vertex covers 

@author: Alexander Roederer
@date: May 16, 2016

Note: figure out where lonely mayonnaise is coming from? 

'''

from log_recipe import DataLog

import numpy as np
from scipy.cluster.vq import vq, kmeans2

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
        self.degreeM = np.diag(np.sum(self.fadjM,0))
        #Simple laplacian
        self.laplacian = self.degreeM - self.wadjM

        #Decompose laplacian to find eigenvalues
        self.evals, self.evecs = np.linalg.eig(self.laplacian)
        self.k = 10  #num clusters

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
    fileLoc = './data/openrecipes.txt'
    #fileLoc = './data/recipeitems-latest.json'
    dlog = DataLog(fileLoc)
    
    print("Run Analysis")
    cc = ClusterCooccurance(dlog.cooccuranceMatrix)

    print(cc.clusters)
    f = np.array(dlog.foods)
    for i in range(0, cc.k):
        cc.printClusterContents(f, i)
    

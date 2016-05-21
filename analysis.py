'''
analysis.py runs analysis on a cooccurance matrix to find clusters 
Current implementation uses Shi-Malik algorithm (normalized cuts): 
use symmetric normalized Laplacian, find second-smallest eigenvalue, use 
its eigenvector, and you get a minimized normalized graph cut. 

Use this repeatedly for hierarchical clustering. 

@author: Alexander Roederer
@date: May 16, 2016

Note: figure out where lonely 'mayonnaise' item in dataset 
(no other ingredients in recipe) is coming from

'''

from log_recipe import DataLog

import numpy as np
from scipy.cluster.vq import vq, kmeans2
from scipy.linalg import eigh

from matplotlib import pyplot as plt

class ClusterCooccurance:
    def __init__(self):
        pass

    #Given an adjacency matrix and a set of rows/cols to consider, 
    #and returns the indexes split into two sets based on max cut clustering
    def splitIndexes(self, adj, indexes):
        subAdjMat = adj[indexes,:]
        subAdjMat = subAdjMat[:,indexes]
        split = self.findCluster(subAdjMat)
        return indexes[split], indexes[~split]

    def findCluster(self, weightedAdjacency):
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
        #self.fadjM = np.delete(self.fadjM, empty, axis=0)
        #self.fadjM = np.delete(self.fadjM, empty, axis=1)

        #Create degree matrix
        self.degreeM = np.diag(np.sum(self.wadjM,0))

        #Create inverse rooted degree matrix
        self.degreeMSplit = np.diag(1/np.sqrt((np.sum(self.wadjM,0)*1.0)))

        #Simple laplacian
        #self.laplacian = self.degreeM - self.wadjM

        #Normalized laplacian
        #Note that repeated multiplication doesn't seem to work properly? 
        #Small values get truncated which ruins the laplacian
        self.laplacian = np.dot(np.dot(self.degreeMSplit,
            (self.degreeM - self.wadjM )),self.degreeMSplit)

        #Decompose laplacian to find eigenvalues
        self.eigenvalues, self.eigenvectors = eigh(self.laplacian)

        #Use second smallest eigenvalue's eigenvector 
        goodEigenvector = self.eigenvectors[:, 1]
        #Threshold based on mean (median is noisy)
        return goodEigenvector < np.mean(goodEigenvector)

    def printClusterContents(self, labels, cluster):
        a, = np.where(cc.clusters==cluster)
        print(labels[a])

if __name__ == '__main__':
    print("Beginning Analysis")

    print("Create data")
    #fileLoc = './data/openrecipes.txt'
    #fileLoc = './data/recipeitems-latest.json'
    #dlog = DataLog(fileLoc)

    pickleFile = './data.pkl'
    dlog = DataLog(None, pickleLoc=pickleFile)
    
    print("Run Analysis")
    #Create clusterer object
    cc = ClusterCooccurance()
    maxClusterSize = 10

    allIndexes = np.arange(np.shape(dlog.cooccuranceMatrix)[0])
    clusterQueue = [allIndexes]
    finishedClusters = []

    while len(clusterQueue) > 0:
        index = clusterQueue.pop(0)
        split1, split2 = cc.splitIndexes(dlog.cooccuranceMatrix, index)
    
        if len(split1) < 1 or len(split2) < 1: 
            print("Cannot split group further")
            finishedClusters.append(split1)
            finishedClusters.append(split2)
        else:
            for split in [split1, split2]:
                if len(split) > maxClusterSize:
                    clusterQueue.append(split)
                else:
                    finishedClusters.append(split)

    for cluster in finishedClusters:
        f = np.array(dlog.foods)
        print(f[cluster])
    

"""
visualize.py

@author:Alexander Roederer
@date: May 16, 2016

Creates visualizations from recipe data
"""

from matplotlib import pyplot as plt
import numpy as np

def labelBars(bars, ax):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., 1.02*height, '%d' % int(height), ha='center', va='bottom', size=10)

#Creates a plot of number of times an ingredient appears in a recipe. 
def frequencyHistogram(itemCounts):
    itemCountsPairs = []
    for item in itemCounts:
        itemCountsPairs.append((item, itemCounts[item]))

    itemCountsPairs.sort(key=lambda itemPair: itemPair[1])
    itemCountsPairs.reverse()
    items = [i[0] for i in itemCountsPairs]
    counts = [i[1] for i in itemCountsPairs]

    ind = range(len(itemCountsPairs))
    print(list(ind))
    print(counts)
    width = 0.35

    fig, ax = plt.subplots()
    bars = ax.bar(ind, counts, align='center')

    ax.set_ylabel('Counts')
    ax.set_xlabel('Food Item')

    ax.set_xticklabels(items, size=10, rotation='vertical')
    ax.set_xlim(0, max(ind))
    plt.xticks(ind)

    labelBars(bars, ax)

def cooccuranceHeatmap(coocMat, labels):
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(coocMat, cmap=plt.cm.Blues)

    #Put major ticks at middle of each cell
    ax.set_xticks(np.arange(coocMat.shape[0])+0.5, minor=False)
    ax.set_yticks(np.arange(coocMat.shape[1])+0.5, minor=False)

    #Use a table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    ax.set_yticklabels(labels, minor=False, size=8)
    ax.set_xticklabels(labels, minor=False, rotation='vertical', size=8)

    

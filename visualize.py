"""
visualize.py

@author:Alexander Roederer
@date: May 16, 2016

Creates visualizations from recipe data
"""

from matplotlib import pyplot as plt

def frequencyHistogram(itemCounts):
    itemCountsPairs = []
    for item in itemCounts:
        itemCountsPairs.append((item, itemCounts[item]))

    itemCountsPairs.sort(key=lambda itemPair: itemPair[1])
    items = [i[0] for i in itemCountsPairs]
    counts = [i[1] for i in itemCountsPairs]

    ind = range(len(itemCountsPairs))
    print(list(ind))
    print(counts)
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(ind, counts, align='center')

    ax.set_ylabel('Counts')
    ax.set_xlabel('Food Item')

    ax.set_xticklabels(items, size=10, rotation='vertical')
    ax.set_xlim(0, max(ind))
    plt.xticks(ind)


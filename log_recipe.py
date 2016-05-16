'''
log_recipe.py

@author:Alexander Roederer
@date: May 10, 2016

Creates data structure from multiple recipes for further analysis

Initial approach: create simple count association matrix for food type
Note that some cleanup of food types will likely be necessary as ingredient parsing 
is a non-trivial problem; more advanced ingredient parsing may be possible with Conditional 
Random Fields (as seen in NYTimes/ingredient-phrase-tagger)

For now, we use Ingreedy, which is structural rather than probabilistic, and thus 
more prone to error in unique cases. 


'''

import numpy as np
from ingreedypy import Ingreedy

class DataLog():
    def __init__(self):
        pass
        
if __name__ == '__main__':
    print("Data Log Test") 
    ing = Ingreedy()
    int.parse("12 oysters")

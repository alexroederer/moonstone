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
from read_data import DatasetManager

class DataLog():
    def __init__(self):
        self.itemCounts = {}
        self.totalItems = 0
        self.associationCounts = None

    def addItem(self, ingredient):
        if ingredient in self.itemCounts:
            self.itemCounts[ingredient] += 1
        else:
            self.itemCounts[ingredient] = 1
            self.totalItems += 1

    def countIngredients(self, f):
        dataset = DatasetManager(f)
        recipe = dataset.getNextRecipeJSON()
        while recipe is not None:
            #Collect list of all ingredients
            ings = dataset.getIngr(recipe)
            ings = ings.split('\n')
            for ing in ings:
                ing = dataset.cleanIngredient(ing.lower())
                try:
                    parsedIngParts = Ingreedy().parse(ing)
                    ingFood = parsedIngParts['ingredient']
                    self.addItem(ingFood)
                except Exception as e:
                    #Exception case occurs when food cannot be parsed; 
                    #As parser is weak, this happens fairly frequently
                    pass
            recipe = dataset.getNextRecipeJSON()

    def removeRareItems(self):
        rareItems = []
        for food in self.itemCounts:
            if self.itemCounts[food] < 2:
                rareItems.append(food)
        for food in rareItems:
            del self.itemCounts[food]
            self.totalItems -= len(rareItems)

    def createIndex(self):
        pass
            
        
if __name__ == '__main__':
    print("Data Log Test") 
    dlog = DataLog()
    #Get ingredient counts
    with open('./data/openrecipes.txt', 'r') as f:
        dlog.countIngredients(f)
    #Remove rare items from ingredients list
    dlog.removeRareItems()
    with open('./data/openrecipes.txt', 'r') as f:
        pass
    print(dlog.itemCounts)



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
import pickle

class DataLog():
    def __init__(self, dataFileLoc, pickleLoc=None):
        #Counts of ingredients (used to construct cooccurance matrix)
        self.itemCounts = {}            #Num times food appears in recipes
        self.totalItems = 0             #Total num foods

        #Saved recipes (for speedup)
        self.recipeIngredients = None

        self.cooccuranceMatrix = None   #Cooccurance matrix
        self.foods = []                 #List of foods considered in cooccurance
        self.itemIndex = {}             #Indexes for foods into cooccurance 

        if pickleLoc is None:
            self.initCountIngredients(dataFileLoc)
            self.initCooccurance()
        else:
            self.loadSetupFromPickle(pickleLoc)

    def loadSetupFromPickle(self, pickleLoc):
        setupDict = None
        with open(pickleLoc, 'rb') as pickleFile:
            setupDict = pickle.load(pickleFile)
        if setupDict is not None:
            self.itemCounts = setupDict['itemCounts']
            self.totalItems = setupDict['totalItems']
            self.recipeIngredients = setupDict['recipeIngredients']
            self.cooccuranceMatrix = setupDict['cooccuranceMatrix']
            self.foods = setupDict['foods']
            self.itemIndex = setupDict['itemIndex']
        else:
            print("Warning: Pickle Load unsuccessful.")

    def saveSetupToPickle(self, fileLoc):
        setup = {'itemCounts': self.itemCounts, 
                'totalItems': self.totalItems, 
                'recipeIngredients': self.recipeIngredients, 
                'cooccuranceMatrix': self.cooccuranceMatrix, 
                'foods': self.foods, 
                'itemIndex': self.itemIndex}

        with open(fileLoc, 'wb') as output:
            pickle.dump(setup, output)

    #Runs the initial ingredient count
    def initCountIngredients(self, dataFileLoc):
        self.recipeIngredients = []
        self.itemCounts = {}
        self.totalItems = 0

        #Get ingredient counts
        with open(dataFileLoc, 'r') as f:
            self.countIngredients(f)
        #Remove rare items from ingredients list
        self.removeRareItemsToReachSize(1000)

    #Runs the initial cooccurance matrix creation
    def initCooccurance(self):
        #TODO: print warning if ingredient count has not been performed

        #Create matrix structure
        self.cooccuranceMatrix = np.zeros((self.totalItems, self.totalItems))
        #Create index for each food
        self.createIndex()
        #Iterate through recipes counting food pairs
        #Recipes should have already been collected by item counter
        for ingredients in self.recipeIngredients:
            usedIngredients = [f for f in ingredients if f in self.itemIndex]
            for food1 in usedIngredients:
                for food2 in usedIngredients:
                    self.cooccuranceMatrix[self.itemIndex[food1], 
                        self.itemIndex[food2]] += 1

    #Adds a food item to the item counts dictionary
    def addItem(self, ingredient):
        if ingredient in self.itemCounts:
            self.itemCounts[ingredient] += 1
        else:
            self.itemCounts[ingredient] = 1
            self.totalItems += 1

    #Get counts of all ingredients from recipes file
    def countIngredients(self, f):
        dataset = DatasetManager(f)
        recipe = dataset.getNextRecipeJSON()
        recipeCount = 0 #DEBUG
        while recipe is not None:
            #Collect list of all ingredients
            ingredients = self.getCleanIngredients(dataset, self.getIngredientsFromRecipe(dataset, recipe))
            self.recipeIngredients.append(ingredients)
            for food in ingredients:
                self.addItem(food)
            recipe = dataset.getNextRecipeJSON()
            recipeCount += 1
            print(recipeCount, self.totalItems) #DEBUG

    #Gets clean list of ingredients in a recipe
    def getCleanIngredients(self, dataset, ings):
        ingredientsList = []
        for ing in ings:
            ing = dataset.cleanIngredient(ing.lower())
            try:
                parsedIngParts = Ingreedy().parse(ing)
                ingFood = parsedIngParts['ingredient'].strip()
                ingredientsList.append(ingFood)
            except Exception as e:
                #Exception case occurs when food cannot be parsed; 
                #As parser is weak, this happens fairly frequently
                pass
        return ingredientsList

    def getIngredientsFromRecipe(self, dataset, recipe):
        ings = dataset.getIngr(recipe)
        ings = ings.split('\n')
        return ings

    #Removes items which occur cutoff times or less from itemCounts
    def removeRareItems(self, cutoffCount):
        rareItems = []
        for food in self.itemCounts:
            if self.itemCounts[food] <= cutoffCount:
                rareItems.append(food)
        for food in rareItems:
            del self.itemCounts[food]
        self.totalItems -= len(rareItems)
        return self.totalItems

    #Removes rarer items until only the specified number of items or fewer are left in itemCounts
    def removeRareItemsToReachSize(self, numItemsDesired):
        itemsByCount = {}
        for food in self.itemCounts:
            count = self.itemCounts[food]
            if count not in itemsByCount:
                itemsByCount[count] = [food]
            else:
                itemsByCount[count].append(food)
        numItemsWithEachCount = []
        for count in itemsByCount:
            numItemsWithEachCount.append((count, len(itemsByCount[count])))
        numItemsWithEachCount.sort(key=lambda item: item[0])

        itemsToRemove = []
        totalRemoved = 0

        for (count, number) in numItemsWithEachCount:
            itemsToRemove.extend(itemsByCount[count])
            totalRemoved += number
            if ((self.totalItems - totalRemoved) <= numItemsDesired):
                break
        for food in itemsToRemove:
            del self.itemCounts[food]
        self.totalItems -= totalRemoved
        return self.totalItems

    #Creates indexes into cooccurance matrix
    def createIndex(self):
        for (index, food) in enumerate(self.itemCounts):
            self.itemIndex[food] = index
            self.foods.append(food)

if __name__ == '__main__':
    print("Data Log Test") 
#    fileLoc = './data/openrecipes.txt'
    fileLoc = './data/recipeitems-latest.json'
    dlog = DataLog(fileLoc)
    #dlog.initCooccurance(fileLoc)
    #print(dlog.cooccuranceMatrix)


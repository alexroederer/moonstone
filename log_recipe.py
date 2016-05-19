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
    def __init__(self, dataFileLoc):
        self.itemCounts = {}            #Num times food appears in recipes
        self.totalItems = 0             #Total num foods
        self.foods = []                 #List of foods considered in cooccurance
        self.itemIndex = {}             #Indexes for foods into cooccurance 

        self.cooccuranceMatrix = None   #Cooccurance matrix

        self.initCountIngredients(dataFileLoc)

    #Runs the initial ingredient count
    def initCountIngredients(self, dataFileLoc):
        #Get ingredient counts
        with open(dataFileLoc, 'r') as f:
            self.countIngredients(f)
        #Remove rare items from ingredients list
        self.removeRareItemsToReachSize(100)

    #Runs the initial cooccurance matrix creation
    def initCooccurance(self, dataFileLoc):
        #Create cooccurance matrix 
        with open(dataFileLoc, 'r') as f:
            #Create matrix structure
            self.cooccuranceMatrix = np.zeros((self.totalItems, self.totalItems))
            #Create index for each food
            self.createIndex()
            #Iterate through recipes counting food pairs
            dataset = DatasetManager(f)
            recipe = dataset.getNextRecipeJSON()
            while recipe is not None:
                ingredients = self.getCleanIngredients(dataset, self.getIngredientsFromRecipe(dataset, recipe))
                usedIngredients = [f for f in ingredients if f in self.itemIndex]
                for food1 in usedIngredients:
                    for food2 in usedIngredients:
                        self.cooccuranceMatrix[self.itemIndex[food1], 
                            self.itemIndex[food2]] += 1
                recipe = dataset.getNextRecipeJSON()

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
        recipeCount = 0
        while recipe is not None:
            #Collect list of all ingredients
            ingredients = self.getCleanIngredients(dataset, self.getIngredientsFromRecipe(dataset, recipe))
            for food in ingredients:
                self.addItem(food)
            recipe = dataset.getNextRecipeJSON()
            recipeCount += 1
            print(recipeCount, self.totalItems)

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
    fileLoc = './data/openrecipes.txt'
#    fileLoc = './data/recipeitems-latest.json'
    dlog = DataLog(fileLoc)
    #dlog.initCooccurance(fileLoc)
    #print(dlog.cooccuranceMatrix)


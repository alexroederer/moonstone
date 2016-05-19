'''
read_data.py

@author: Alexander Roederer
@date: May 10, 2016

Prepares data for reading from Fictive Kin openrecipes project
'''

'''
DatasetManager object
Currently only supports reading recipes in order
Currently only supports acquisition of name and ingredients;
    full recipe can be retrieved using recipe-scraper package and URL
'''
import json
#from recipe_scrapers import scrap_me
import re

class DatasetManager:
    #Constructor requires pass-in reference for file containing database;
    #Context management done by outside holding function
    def __init__(self, dataHandle): 
        self.dataHandle = dataHandle    #Data handle
        self.currentRecipe = 0          #Recipe counter

        #Compile regex objects
        self.ingredientDelRegex = [re.compile(r',.*'), 
            #Additional clauses
            re.compile(r' \+ .+'), 
            re.compile(r'\([^)]*\)'), 
            re.compile(r' \/ .+'), 
            re.compile(r'\*'),
            #Extra metric units
            re.compile(r'[0-9]+ *g *\/ *'), 
            re.compile(r'[0-9]+ *ml *\/ *'), 
            #Leading spaces
            re.compile(r'^ +')]

        self.ingredientSpaceRegex = [re.compile('-'), 
            re.compile(r'  ')]

        self.ingredientFracRegex = [re.compile(r'½'), 
            re.compile(r'¼'),
            re.compile(r'¾'),
            re.compile(r'⅓')]

        #Remove special fraction symbols
        self.ingredientFracReplace = [' 1/2', 
        ' 1/4', 
        ' 3/4', 
        ' 1/3'] 

        #Remove verbs
        self.ingredientVerbsRegex = re.compile(r' *(heaped|cold|sliced|slices|chopped|melted|grated|minced|ground|splash of|to taste|lots|finely|whole|large|scant|fine|assorted|weight|storebought|containers|diced|dice|more|cut|small|fine|medium|ground|roughly|thinly|thin|big) *')

    #Returns next recipe in file as JSON object
    def getNextRecipeJSON(self):
        recipeString = self.dataHandle.readline()
        if recipeString is '':
            #End of file reached
            return None
        else:
            x = json.loads(recipeString)
            self.currentRecipe += 1
            return x

    #Utility functions for easy attribute aquisition
    def getName(self, recipe):
        return recipe['name']

    def getIngr(self, recipe):
        return recipe['ingredients']

    def getURL(self, recipe):
        return recipe['url']

    def getSource(self, recipe):
        return recipe['source']

    def getNumRecipesSeen(self):
        return self.currentRecipe

    #Cleaning function for ingredients; 
    #    mostly manages punctuations, removes 
    #    parantheticals, removes header lines 
    #    will be unnecessary when parser is upgraded
    def cleanIngredient(self, ingr):
        for pattern in self.ingredientDelRegex:
            ingr = pattern.sub('',ingr)

        for pattern, repl in zip(self.ingredientFracRegex, self.ingredientFracReplace):
            ingr = pattern.sub(repl,ingr)

        ingr = self.ingredientVerbsRegex.sub(' ', ingr)

        #Extra spaces
        for pattern in self.ingredientSpaceRegex:
            ingr = pattern.sub(' ',ingr)
        ingr = ingr.strip()
        return ingr

#Test main method; prints first 100 recipe names
if __name__ == '__main__':
    filename = './data/openrecipes.txt'
    filename = './data/recipeitems-latest.json'
    with open(filename, 'r') as f:
        dataset = DatasetManager(f)
        r = dataset.getNextRecipeJSON()
        while r is not None and dataset.getNumRecipesSeen() < 100:
            print(dataset.getName(r))
            ings = dataset.getIngr(r).split('\n')
            for ing in ings:
                ing = ing.lower()
                print(dataset.cleanIngredient(ing))
            r = dataset.getNextRecipeJSON()


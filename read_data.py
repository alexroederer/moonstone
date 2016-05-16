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

    #Returns next recipe in file as JSON object
    def getNextRecipeJSON(self):
        recipeString = self.dataHandle.readline()
        if recipeString is '':
            #End of file reached
            return None
        else:
            x = json.loads(self.dataHandle.readline())
            self.currentRecipe += 1
            return x

    #Utility functions for easy attribute aquisition
    def getName(self, recipe):
        return recipe['name']

    def getIngr(self, recipe):
        return recipe['ingredients']

    def getURL(self, recipe):
        return recipe['url']

    def getNumRecipesSeen(self):
        return self.currentRecipe

    #Cleaning function for ingredients; 
    #    mostly manages punctuations, removes 
    #    parantheticals, removes header lines 
    #    will be unnecessary when parser is upgraded
    def cleanIngredient(self, ingr):
        ingr = ingr.replace(',','')
        ingr = ingr.replace('-',' ')
        ingr = ingr.replace('_','')
        ingr = re.sub(r'\([^)]*\)', '', ingr)
        #Remove verbs
        ingr = re.sub(r' *(sliced|slices|chopped|melted|grated|minced|ground|splash of|to taste|lots|finely|whole|large|scant|fine|assorted|weight|storebought|containers|dice|diced|more|cut|small|fine|medium) *',' ',ingr)
        ingr = re.sub(r' *(sliced|slices|chopped|melted|grated|minced|ground|splash of|to taste|lots|finely|whole|large|scant|fine|assorted|weight|storebought|containers|dice|diced|more|cut|small|fine|medium) *',' ',ingr)
        ingr = re.sub(r'^ *','',ingr)
        ingr = re.sub(r' for .+','',ingr)
        ingr = re.sub(r' \+ .+','',ingr)
        ingr = re.sub(r' \/ .+','',ingr)
        ingr = re.sub(r'^\*.*','',ingr)
        return ingr

#Test main method; prints first 100 recipe names
if __name__ == '__main__':
    with open('./data/openrecipes.txt', 'r') as f:
        dataset = DatasetManager(f)
        r = dataset.getNextRecipeJSON()
        while r is not None and dataset.getNumRecipesSeen() < 100:
            print(dataset.getName(r))
            ings = dataset.getIngr(r).split('\n')
            for ing in ings:
                ing = ing.lower()
                print(dataset.cleanIngredient(ing))
            r = dataset.getNextRecipeJSON()


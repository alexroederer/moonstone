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

#Test main method; prints first 100 recipe names
if __name__ == '__main__':
    with open('./data/openrecipes.txt', 'r') as f:
        dataset = DatasetManager(f)
        r = dataset.getNextRecipeJSON()
        count = 1
        while r is not None and count < 100:
            print(dataset.getName(r))
            print(dataset.getIngr(r))
            r = dataset.getNextRecipeJSON()
            count += 1


# moonstone
A small package to scrape recipes and analyze them to produce flavour profile network.

## General structure

- *read_data.py*: fictivekin/openrecipes data dump manager
- *log_recipe.py*: logs useful information from recipe in data structure
- *analysis.py*: spectral clustering of ingredients in recipes by cooccurance
- *visualize.py*: visualize analysis results

Note: for proper operation, DB dump data from the [openrecipes database](https://github.com/fictivekin/openrecipes) should be placed 
in a folder labeled `data`. 

Once the data has been logged once, it can be pickled for faster reloading (as only recipe ingredients are used, large amounts of data can be discarded)



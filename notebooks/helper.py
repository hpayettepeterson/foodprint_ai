import pandas as pd
import json
import os
from string import digits
import itertools
import re, pickle
import functools
from IPython.display import HTML
import string
from food_extractor.food_model import FoodModel

def load_data_im2recipe(recipes_folder='../raw_data/sample_im2recipes/'):
    ''' Helper function to load and concat data from im2recipes
        Loading data with this function may take time if not using cache. '''
    
    # Load the basic information on the recipes
    df = pd.DataFrame(columns=['id', 'recipeName', 'ingredients'])
    for file in os.listdir(recipes_folder):
        file_path = os.path.join(recipes_folder, file)
        with open(file_path) as sd:
            recipes = json.load(sd)
            for recipe in recipes:
                cdf = {}
                
                cdf['id'] = recipe['id']
                cdf['recipeName'] = recipe['title']
                
                ingredients = []
                cdf['ingredients'] = []
                
                for ingredient in recipe['ingredients']:
                    ingredients.append(ingredient['text'].replace(',',''))
                    
                cdf['ingredients'] = [ingredients]
                
                cdf = pd.DataFrame(cdf)
                df = pd.concat([df, cdf])
    return df.reset_index(drop=True)

def load_data(lists_folder='../raw_data/lists/', recipes_folder='../raw_data/recipes/', 
              pickle_file='../raw_data/cached.pickle', cache=True):
    ''' Helper function to load and concat data
        Loading data with this function may take time if not using cache. '''
    
    # Load the data from the cached file
    if cache and os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as pf:
            df = pickle.load(pf)
            print(df)
        return df
    
    # Load the basic information on the recipes
    df = None
    for file in os.listdir(lists_folder):
        if 'DS_' in file:
            continue
        file_path = os.path.join(lists_folder, file)
        with open(file_path) as sd:
            data = json.load(sd)['matches']
        cdf = pd.DataFrame(data)
        cdf['cuisine'] = file.split('.')[0].split('_')[-2]
        df = (cdf if df is None else pd.concat([df, cdf]))
    df = df[['flavors', 'id', 'ingredients', 'recipeName', 'cuisine']]
    
    # Load the cooking time and the recipes images from the rest of data
    df_more =  pd.DataFrame(columns = ['id','PrepTime', 'img','ingredientQty'])
    for file in os.listdir(recipes_folder):
        if 'DS_' in file:
            continue
        file_path = os.path.join(recipes_folder, file)
        
        with open(file_path) as sd:
            data = json.load(sd)
        cdf = {}
        cdf['id'] = [data['id']]
        if('totalTimeInSeconds' not in data):
            print(data['id'])
        cdf['PrepTime']= data['totalTimeInSeconds']/60.0
        cdf['img'] = data['images'][0]['imageUrlsBySize']['360']
        cdf['ingredientQty'] = [data['ingredientLines']]
        cdf = pd.DataFrame(cdf)
        df_more = pd.concat([df_more, cdf])
    
    # Merge the two data frames in one on the recipe id
    df = pd.merge(df, df_more, on='id')
    
    # Cache the resulting dataframe if caching option if enabled
    if cache:
        with open(pickle_file, 'wb') as pf:
            pickle.dump(df, pf)
            
    df = df.drop_duplicates(['id'])
    df = df.reset_index(drop=True)
    return df[['id', 'recipeName','ingredients']]

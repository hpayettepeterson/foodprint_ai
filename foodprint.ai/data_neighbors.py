import os
import json
import pandas as pd
import numpy as np


def load_data_im2recipe(recipes_folder='./data/im2recipes/'):
    
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


def load_data_yummly(lists_folder='./data/lists/', 
                    recipes_folder='./data/recipes/'):
    
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
    
    df = df.drop_duplicates(['id'])
    df = df.reset_index(drop=True)
    return df[['id', 'recipeName','ingredients']]
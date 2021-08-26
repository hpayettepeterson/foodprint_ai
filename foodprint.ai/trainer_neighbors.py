import pandas as pd
import numpy as np
from food_extractor.food_model import FoodModel
from data_neighbors import load_data_im2recipe, load_data_yummly
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestNeighbors
import pickle
import joblib   


def get_data(add_random_co2=False):
    df_yummly = load_data_yummly(recipes_folder='./data/sample_recipes/')
    df_im2recipe = load_data_im2recipe(recipes_folder='./data/sample_im2recipes/')
    df = pd.concat([df_yummly, df_im2recipe]).reset_index(drop=True)
    
    if add_random_co2:
        df = add_random_co2_data(df)
    
    return df

def add_random_co2_data(df):
    import random
    df['co2'] = 100 * np.random.randn(df.shape[0]) + 1000
    return df

def extract_cleaned_ingredients(df):
    model = FoodModel("chambliss/distilbert-for-food-extraction")
    df_cleaned = df.copy()
    df_cleaned['ingredients2'] = df_cleaned['ingredients'].apply(lambda x : [ing['text'] for ing in model.extract_foods(','.join([ing for ing in x]))[0]['Ingredient']])
    df_cleaned.drop(columns=['ingredients'], inplace=True)
    df_cleaned.rename(columns={'ingredients2':'ingredients'}, inplace=True)
    return df_cleaned

def convert_to_dict(arr):
    ''' Helper function to convect an array of ingredients to a dictionary '''
    d={}
    for a in arr:
        d[a]=1
    return d

def find_n_components(df):
    import numpy as np 
    vect_test = DictVectorizer(sparse=False)
    X_test = vect_test.fit_transform(df.bow.tolist())
    pca_test = PCA(n_components=min(df.shape[0], X_test.shape[1]))
    pca_test.fit(X_test)
    n_components = np.argmax(pca_test.explained_variance_ratio_.cumsum() > 0.9)
    return n_components

def pipeline(n_components):
    pipe = Pipeline([
        ('dict_vectorizer', DictVectorizer(sparse=False)),
        ('pca', PCA(n_components=n_components))
    ])
    return pipe

def get_processed_data():
    df = get_data(add_random_co2=True)
    df_cleaned = extract_cleaned_ingredients(df)
    df_cleaned['bow'] = df_cleaned.ingredients.apply(convert_to_dict)
    n_components = find_n_components(df_cleaned)
    pipe = pipeline(n_components)
    X_recipes = pipe.fit_transform(df_cleaned.bow.tolist())
    return (df_cleaned, X_recipes)

def save_processed_data(df_cleaned, X_recipes):
    
    with open("./data/cached_informational_data.pickle", "wb") as file:
        pickle.dump(df_cleaned, file)

    with open("./data/cached_vectorized_data.pickle", "wb") as file:
        pickle.dump(pd.DataFrame(X_recipes, index=df_cleaned.id), file)


def train_n_neighbors(n_neighbors = 10):
    X_recipes = np.array(pickle.load(open("./data/cached_vectorized_data.pickle","rb")))
    n_neighbors_model = NearestNeighbors(n_neighbors=n_neighbors)
    n_neighbors_model.fit(X_recipes)
    return n_neighbors_model

def save_n_neighbors_model(n_neighbors_model):
    # Export pipeline as pickle file
    with open("../models/nneighbors_model.pkl", "wb") as file:
        pickle.dump(n_neighbors_model, file)
    
    with open("../models/nneighbors_model.joblib", "wb") as file:
        joblib.dump(n_neighbors_model, file)


if __name__ == '__main__':
    (df_cleaned, X_recipes) = get_processed_data()
    print('df_cleaned : ')
    print(df_cleaned)
    print('\n')

    print('X_recipes : ')
    print(X_recipes)
    print('\n')

    save_processed_data(df_cleaned, X_recipes)
    n_neighbors_model = train_n_neighbors(n_neighbors = 5)
    print('n_neighbors_model.n_samples_fit_ : ')
    print(n_neighbors_model.n_samples_fit_)
    print('\n')

    save_n_neighbors_model(n_neighbors_model)

    




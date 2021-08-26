import pytz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from predict_neighbors import load_vectorized_data, load_informational_data, get_recipe_input, load_model, get_neighbors

app = FastAPI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/')
def index():
    return dict(greeting='hello')

#@app.get('/predict')
#def predict(recipe_id='Pork-ramen-soup-310007', n_neighbors=5):
    # loading preprocessed data
    #df_recipes_vect = load_vectorized_data()
    #df_recipes_info = load_informational_data()
    #recipe_input = get_recipe_input(recipe_id, df_recipes_vect)
    #nneighbors_model = load_model()
    #df_neighbors = get_neighbors(recipe_input, df_recipes_info, nneighbors_model, n_neighbors=n_neighbors)
    #return dict(prediction=df_neighbors)
    #return dict(greeting='hello') 
    
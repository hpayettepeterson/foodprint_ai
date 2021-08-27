import requests
import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
############## LOADING SESSION #######################################
complete_df = pd.read_csv("raw_data/temp_dishes_with_co2.csv")

######################################################################

st.markdown("""
    # Welcome to **Foodprint.ai**! (Project with **<3** with **LE WAGON**)
    ## If you want to know the CO2 foodprint of your dish, upload a foto of your dish. Just get started!**or** just type in the recipe below.
""")

dish_selection = ["nothing"]
dish_selection = st.multiselect( 'What dish do you want to eat?',  complete_df["dish_name"])
dish_number = st.slider('How many dish recommendations you want to see?', 1, 10, 5)
st.write(dish_number)
#st.write('You selected:', dish_selection[0])
#st.write(temp_id, temp_ingredients, temp_weight_per_ingr, temp_total_dish_weight, temp_total_footprint, temp_dish_footprint_per_100gr, temp_confidence_score, temp_dish_footprint_per_kilo, temp_co2_score,temp_km_driven_per_100gr)

if st.button('PRESS ME DAMN IT I CANNOT WAIT!'):
    ### variables
    temp_df = complete_df.loc[complete_df['dish_name'].isin(dish_selection)]
    temp_id = temp_df["id"].values[0]
    temp_ingredients = temp_df["ingredients"].values[0]
    temp_weight_per_ingr = temp_df["weight_per_ingr"].values[0]
    temp_total_dish_weight = temp_df["total_dish_weight"].values[0]
    temp_total_footprint = temp_df["total_footprint"].values[0]
    temp_dish_footprint_per_100gr = temp_df["dish_footprint_per_100gr"].values[0]
    temp_confidence_score = temp_df["confidence_score"].values[0]
    temp_dish_footprint_per_kilo = temp_df["dish_footprint_per_kilo"].values[0]
    temp_co2_score = temp_df["co2_score"].values[0]
    temp_km_driven_per_100gr = temp_df["km_driven_per_100gr"].values[0]
    ## text
    st.write("You have select: "+ dish_selection[0]+ "(ID: "+ temp_id+")")
    st.write(" The ingredients are: " + str(temp_ingredients)[1:-1])
    st.write(" Total dish weight is " + str(temp_total_dish_weight.round(2)) + "g")
    st.write(" total CO2 footprint is: " + str(temp_total_footprint.round(2)))
    st.write(" CO2 footprint per 100g is:  " + str(temp_dish_footprint_per_100gr.round(2)) + " CO2 footprint per 1kg is : " + str(temp_dish_footprint_per_kilo.round(2)))
    st.write(" We are " + str(temp_confidence_score*100)+"%"  + " sure, " + "that our CO2 score of " + str(temp_co2_score) + " is correct.")
    st.write(" Car" + str(temp_km_driven_per_100gr.round(2))  + "km")
    st.table(temp_df[["ingredients", "weight_per_ingr"]])

    #### TALK TO THE API
    url=f'https://foodprint-m7tvgzo76q-ew.a.run.app/predict?recipe_id={temp_id}&n_neighbors={dish_number}'
    response = requests.get(url)
    st.write(response)
    #st.write(response.json())
    j_response = response.json()
    api_input_df=pd.DataFrame.from_dict(j_response["prediction"])
    #api_input_df["distance"] = api_input_df["distance"].apply(lambda x: x)
    #### Plotting the result
    fig = px.scatter_3d(api_input_df, title="better choices", x='distance',y='marker_size',z='co2', size_max=18,hover_name='name', color='co2')
    st.plotly_chart(fig)



    #st.write(j_response[0])
    #import plotly.express as px
    #fig = px.scatter_3d(response[""], x='sepal_length', y='sepal_width', z='petal_width',
    #          color='species')
    #fig.show()
else:
    st.write('')


st.write("Sources and explainations here!")

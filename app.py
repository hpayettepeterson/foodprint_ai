import requests
import streamlit as st
import datetime
import pandas as pd


############## LOADING SESSION #######################################
complete_df = pd.read_csv("raw_data/temp_dishes_with_co2.csv")


#####################################################################

st.markdown("""
    # Welcome to **Foodprint.ai**! (Project with **<3** with **LE WAGON**)

    ## If you want to know the CO2 foodprint of your dish, upload a foto of your dish. Just get started!

    **or** just type in the recipe below.
""")

dish_selection = ["nothing"]
dish_selection = st.multiselect( 'What dish do you want to eat?',  complete_df["dish_name"])
#dish_number = st.slider('How many dishes?', 1, 10, 5)
# variables



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
    st.write("ID: " + temp_id + " The ingredients are: " + temp_ingredients) 
    st.write(" weight per ingredient: " + str(temp_weight_per_ingr)+ " Total dish weight: " +str(temp_total_dish_weight))
    st.write(" total CO2 footprint is: " + str(temp_total_footprint) + " CO2 footprint per 100g is:  " + str(temp_dish_footprint_per_100gr) + " CO2 footprint per 1kg is : " + str(temp_dish_footprint_per_kilo)) 
    st.write(" We are " + str(temp_confidence_score)  + " sure, " + "that our CO2 score of " + str(temp_co2_score) + " is correct.")
    st.write(" Per 100g of this dish a car would have driven " + str(temp_km_driven_per_100gr)  + "km")
else:
    st.write('PRESS ME!')


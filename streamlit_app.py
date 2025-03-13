# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests



# Write directly to the app
st.title(" :cup_with_straw: Customize your Smoothie :cup_with_straw: ")
st.write("Choose the fruits you want in your custom smoothie?")


name_on_order = st.text_input("Name on the Smoothie")
st.write("The name on your smoothie will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))

ingredients = st.multiselect(
    "Choose upto 5 ingredients",    my_dataframe, max_selections=5)

if ingredients:
    ingredients_string = ''

    for fruit in ingredients:
        ingredients_string +=  fruit + ' '
        st.subheader(fruit + 'Nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '""" + name_on_order + """'  )"""
    
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+ name_on_order + '!', icon="✅")




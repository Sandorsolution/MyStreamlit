# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize Your Smoothie! :balloon:")
st.write(
    """Choose the fruits you waint in your custom Smoothie.
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The current name on Smoothie will be ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choos up to five ingredients',
    my_dataframe,
    max_selections = 5
)

if ingredients_list and name_on_order:
    ingredients_string = ''
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '
        st.subheader(fruit_choosen + ' Nutrition information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choosen)
        fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width = True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
                values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    
    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")


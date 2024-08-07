# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Add this line to create a connection to Snowflake
cnx = st.connection("snowflake")

# Change this line to use the new connection
session = cnx.session()

# Write directly to the app
st.title(':cup_with_straw: Customize Your Smoothie :cup_with_straw:')
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

fruit_options = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME')).collect()

# Convert the fruit options to a list
fruit_list = [row['FRUIT_NAME'] for row in fruit_options]

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=6
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    # Formulate the insert statement correctly
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}', icon="✅")

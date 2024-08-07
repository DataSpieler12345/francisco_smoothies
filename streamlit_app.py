# Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Set up the Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(':cup_with_straw: Customize Your Smoothie :cup_with_straw:')
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

# Get fruit options from Snowflake
fruit_options = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME')).collect()

# Convert the fruit options to a list
fruit_list = [row['FRUIT_NAME'] for row in fruit_options]

# User selects ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=6  # Changed to 6 to match the problem statement
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    # Formulate the insert statement correctly
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Button to submit the order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie has been ordered, {name_on_order}', icon="✅")
    
    # New section to display fruityvice nutrition information
    import requests
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    # st.text(fruityvice_response.json())
    fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

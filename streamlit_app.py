# Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

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
my_dataframe = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'), col('SEARCH_ON')).to_pandas()
st.dataframe(data=my_dataframe, use_container_width=True)

# Convert the fruit options to a list
fruit_list = my_dataframe['FRUIT_NAME'].tolist()

# User selects ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5  # Match the requirement
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)

    # Formulate the insert statement correctly
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER, ORDER_FILLED)
    VALUES ('{ingredients_string}', '{name_on_order}', FALSE)
    """

    # Button to submit the order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie has been ordered, {name_on_order}', icon="✅")

if ingredients_list:
    for fruit_chosen in ingredients_list:
        search_on = my_dataframe.loc[my_dataframe['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
        
        st.subheader(f'{fruit_chosen} Nutrition Information')
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        
        try:
            fruityvice_response.raise_for_status()
            fv_data = fruityvice_response.json()
            st.json(fv_data)
        except requests.exceptions.HTTPError as e:
            st.error(f"Failed to retrieve data for {fruit_chosen}")
            st.write(e)

# Function to update the order status
def update_order_status(name, ingredients, filled):
    update_stmt = f"""
    UPDATE smoothies.public.orders
    SET ORDER_FILLED = {filled}
    WHERE NAME_ON_ORDER = '{name}' AND INGREDIENTS = '{ingredients}'
    """
    session.sql(update_stmt).collect()

# Adding orders as per the requirement
if st.button('Add Predefined Orders'):
    # Kevin's order
    kevin_ingredients = 'Apples, Lime, Ximenia'
    kevin_stmt = f"""
    INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER, ORDER_FILLED)
    VALUES ('{kevin_ingredients}', 'Kevin', FALSE)
    """
    session.sql(kevin_stmt).collect()

    # Divya's order
    divya_ingredients = 'Dragon Fruit, Guava, Figs, Jackfruit, Blueberries'
    divya_stmt = f"""
    INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER, ORDER_FILLED)
    VALUES ('{divya_ingredients}', 'Divya', TRUE)
    """
    session.sql(divya_stmt).collect()

    # Xi's order
    xi_ingredients = 'Vanilla Fruit, Nectarine'
    xi_stmt = f"""
    INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER, ORDER_FILLED)
    VALUES ('{xi_ingredients}', 'Xi', TRUE)
    """
    session.sql(xi_stmt).collect()

    st.success('Predefined orders have been added.', icon="✅")

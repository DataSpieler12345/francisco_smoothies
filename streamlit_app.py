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
my_dataframe = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Display the dataframe for debugging
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

# Convert the Snowpark DataFrame to a Pandas DataFrame
pd_df = my_dataframe.to_pandas()

# Convert the fruit options to a list
fruit_list = pd_df['FRUIT_NAME'].tolist()

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
    
if ingredients_list:
    for fruit_chosen in ingredients_list:
        st.subheader(f'{fruit_chosen} Nutrition Information')
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_chosen}")
        
        try:
            fruityvice_response.raise_for_status()
            fv_data = fruityvice_response.json()
            st.json(fv_data)
        except requests.exceptions.HTTPError as e:
            st.error(f"Failed to retrieve data for {fruit_chosen}")
            st.write(e)

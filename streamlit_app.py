# Importar paquetes de Python
import streamlit as st
from snowflake.snowpark.functions import col

# Configuración de la conexión a Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Escribir directamente en la aplicación
st.title(':cup_with_straw: Personaliza tu Smoothie :cup_with_straw:')
st.write(
    """¡Elige las frutas que quieres en tu Smoothie personalizado!
    """
)

nombre_en_pedido = st.text_input('Nombre en el Smoothie:')
st.write("El nombre en tu Smoothie será:", nombre_en_pedido)

# Obtener opciones de frutas de Snowflake
fruit_options = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME')).collect()

# Convertir las opciones de frutas a una lista
fruit_list = [row['FRUIT_NAME'] for row in fruit_options]

# El usuario selecciona ingredientes
ingredients_list = st.multiselect(
    'Elige hasta 5 ingredientes:',
    fruit_list,
    max_selections=5  # Cambiado a 5 para coincidir con el enunciado del problema
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    # Formular la sentencia de inserción correctamente
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
    VALUES ('{ingredients_string}', '{nombre_en_pedido}')
    """

    # Botón para enviar el pedido
    tiempo_para_insertar = st.button('Enviar Pedido')

    if tiempo_para_insertar:
        session.sql(my_insert_stmt).collect()
        st.success(f'Tu Smoothie ha sido ordenado, {nombre_en_pedido}', icon="✅")

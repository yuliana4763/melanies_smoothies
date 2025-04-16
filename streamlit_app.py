# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie!.
  """)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list and name_on_order:  # Pastikan ada bahan dan nama
    # Gabungkan daftar bahan menjadi string dengan koma sebagai pemisah
    ingredients_string = ', '.join(ingredients_list)

    # Tombol untuk mengonfirmasi pesanan
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        # Gunakan parameterized query agar lebih aman
        session.sql(
            "INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES (?, ?)", 
            [ingredients_string, name_on_order]
        ).collect()

        st.success('Your Smoothie is ordered!', icon="✅")
      
# New section to display smoothiefroot nutrition information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)


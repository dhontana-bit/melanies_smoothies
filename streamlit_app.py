# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  """Choose fruits you want in your custom Smoothie!
  """
)





session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

name=st.text_input("How is your name?")
if name:
    ingredients = st.multiselect(
        "Hi "+name+", choose up 5 ingredients!",
        my_dataframe,
        max_selections=5
        
    )
    if ingredients:     
        ingredients_string=''
    
        for fruit_chosen in ingredients:
            ingredients_string+= fruit_chosen +' '
    
        st.write(ingredients_string)
    
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order )
                values ('""" + ingredients_string + "',\'" + name +"""')"""
        
        time_to_insert=st.button('Submit Order')
        
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered '+name+'!', icon="✅")

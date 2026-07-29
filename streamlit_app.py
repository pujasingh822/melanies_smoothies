# Streamlit smoothie order form with emoji title
# Co-authored with CoCo
# Import python packages
import streamlit as st
import pandas as pd
import requests 
#from snowflake.snowpark.context import get_active_session
import os
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(f" :banana: Customize Your Smoothie! :banana: ")
st.write(
  """Choose the fruits you want in your custom smoothie !
  """)

#option = st.selectbox(
#    "What is your favorite fruit?",
#   ("Banana", "Strawberries", "Peaches"),
#)

#st.write("Your favorite fruit is:", option) 

name_on_order = st.text_input("Name on Smoothie")
st.write("The Name on your smoothie will be ", name_on_order)
cnx=st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('Search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#convert snowpark dataframe to pandas dataframe so that we can use loc function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
#st.stop()

ingredients_list=st.multiselect('Choose upto 5 ingredients :',my_dataframe,max_selections=5)
if  ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/+{SEARCH_ON}" )  
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                        values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
  
#import requests  
#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
#sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

        
        



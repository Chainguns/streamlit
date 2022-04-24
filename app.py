#henlo
import pandas as pd
import streamlit
import pandas
import requests


streamlit.header('Fruittyvice.com fruit advice!')
choice = streamlit.text_input('What fruit would you like advice on?', value='Watermelon')
streamlit.write('The fruit you chose is: ' + choice)
resp = requests.get("https://www.fruityvice.com/api/fruit/" + choice)
normalized = pd.json_normalize(resp.json())
streamlit.dataframe(normalized)

df = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
df.set_index('Fruit', inplace=True)
fruits_selected = streamlit.multiselect("Pick some fruits:", list(df.index),['Avocado','Strawberries'])
fruits_to_show = df.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
streamlit.title("Diner app title")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

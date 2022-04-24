
import pandas as pd
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

def fruit_choice(choice):
    streamlit.write('The fruit you chose is: ' + choice)
    resp = requests.get("https://www.fruityvice.com/api/fruit/" + choice)
    normalized = pd.json_normalize(resp.json())
    return streamlit.dataframe(normalized)

streamlit.header('Fruittyvice.com fruit advice!')
try:
    choice = streamlit.text_input('What fruit would you like advice on?', value='Watermelon')
    if not choice:
        streamlit.error('Please enter a fruit!')
    else:
        fruit_choice(choice)
        

except URLError as e:
    streamlit.error('Error!' + e)

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




streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("You are connected to Snowflake as user: %s, account: %s, region: %s" % my_data_row)
my_cur.execute("select * from fruit_load_list")
rows = my_cur.fetchall()
streamlit.header("Fruit Load List")
streamlit.dataframe(pd.DataFrame(rows))

add = streamlit.text_input('What fruit would you like to add?', value='Watermelon')
add_query = "insert into pc_rivery_db.public.fruit_load_list values ('" + add + "')"
my_cur.execute(add_query)
my_cur.execute("select * from fruit_load_list")
streamlit.write('The fruit you added is: ' + add)
rows = my_cur.fetchall()
streamlit.header("Fruit Load List")
streamlit.dataframe(pd.DataFrame(rows))

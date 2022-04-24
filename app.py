
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

def insert_row(fruit_name):
    with my_cnx.cursor() as cur:
        cur.execute("INSERT INTO fruit_load_list VALUES ('" + fruit_name + "')")
        return "You added " + fruit_name + " to your fruit load list!"

def get_fruit_load_list():
    with my_cnx.cursor() as cur:
        cur.execute("SELECT * FROM fruit_load_list")
        return cur.fetchall()

if streamlit.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.header("Fruit Load List")
    streamlit.dataframe(pd.DataFrame(rows))

streamlit.stop()



add = streamlit.text_input('What fruit would you like to add?', value='Watermelon')
add_query = "insert into pc_rivery_db.public.fruit_load_list values ('" + add + "')"
my_cur.execute(add_query)
my_cur.execute("select * from fruit_load_list")
streamlit.write('The fruit you added is: ' + add)
rows = my_cur.fetchall()
streamlit.header("Fruit Load List")
streamlit.dataframe(pd.DataFrame(rows))

import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#-- Global Variable
debug_text = ''

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list order by 1 asc")
    return my_cur.fetchall()
  
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


#--Print out the header information
streamlit.title("My Parents New Healthy Diner")
streamlit.header("Breakfast Menu")

#--Some of the body work
streamlit.text("🥣 OMega 3 & Blueberry Oatmeal")
streamlit.text("🥬 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avacado Toast")

streamlit.header("🍌🥭 Build Your Own Fruit Smoothy 🥝🍇")

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    streamlit.write('The user entered ', fruit_choice)
except URLError as e:
  streamlit.error()


#----
streamlit.header("The fruit load list contains:")  
streamlit.write("--> " + debug_text + " <--")
  
if streamlit.button("Get Fruit Load List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_load_list()
  streamlit.dataframe(my_data_row)
  my_cnx.close()
  
try:
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  add_fruit_choice = streamlit.text_input('What fruit would you like to add?')
  if add_fruit_choice:
     fruit_message =  insert_row_snowflake(add_fruit_choice)
     streamlit.write(fruit_message)
  my_cnx.close()
  fruit_choice = ''
  add_fruit_choice = ''
except URLError as e:
  streamlit.error()





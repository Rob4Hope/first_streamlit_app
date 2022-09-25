import streamlit
import pandas
import requests

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

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

#--streamlit.text(fruityvice_response.json())

#--Puts the data into a format that it can be used as a dataframe
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#--Displays the dataframe
streamlit.dataframe(fruityvice_normalized)

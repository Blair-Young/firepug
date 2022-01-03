import json
import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd
from datetime import datetime


key_dict = json.loads(st.secrets["textkey"])

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

client = gspread.service_account_from_dict(key_dict)

sheet = client.open('locations').get_worksheet(0)

records_data = sheet.get_all_records()

df = pd.DataFrame.from_dict(records_data)


def search(database, criteria=False):
	if not criteria:
 		return database.sample()


def search_output(search_result, criteria=False):
 	if not criteria:
 		return search_result.iloc[0]['name']

def add_place(df, entry_criteria):
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	db_logging = [len(df)+1, current_time]
	db_entry = db_logging + entry_criteria
	print(db_entry)	
	sheet.append_rows(values=[db_entry])
		


st.title("Hello FIRE PUG user")

suggestion_cta = st.button('Get suggestion')

if suggestion_cta:
	suggested_output = search_output(search(df))
	st.success(f'let\'s go to {suggested_output}!')
	st.write(suggested_output)
	st.balloons()



my_expander = st.expander(label='Add a place')
with my_expander:
	with st.form(key='new_place_form', clear_on_submit=True):
		place_name = st.text_input("Place name")

		st.text('Meal type')
		breakfast_option, brunch_option, lunch_option, dinner_option, roast_option, drinks_option = st.columns(6)
		with breakfast_option:
			breakfast = st.checkbox('Breakfast')
		with brunch_option:
			brunch = st.checkbox('Brunch')
		with lunch_option:
			lunch = st.checkbox('Lunch')
		with dinner_option:
			dinner = st.checkbox('Dinner')
		with roast_option:
			roast = st.checkbox('Roast')
		with drinks_option:
			drinks = st.checkbox('Drinks')

		st.text('Venue type')
		restaurant_option, cafe_option, bar_option, pub_option = st.columns(4)
		with restaurant_option:
			restaurant = st.checkbox('Restaurant')
		with cafe_option:
			cafe = st.checkbox('Cafe')
		with bar_option:
			bar = st.checkbox('Bar')
		with pub_option:
			pub = st.checkbox('Pub')

		added_by = st.radio("Added by", ('Blair', 'Grace'))

		anything_else = st.text_input("Anything else?")

		submit_button = st.form_submit_button(label='Submit')

	entry_criteria = [place_name, breakfast, brunch, lunch,
					  dinner, roast, drinks, restaurant,
					  cafe, bar, pub, added_by, anything_else]


	if submit_button:
	    add_place(df, entry_criteria)
	    st.success(f'{place_name} has been added!')





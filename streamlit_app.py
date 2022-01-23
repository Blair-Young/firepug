import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
from database_engine import Database, Location

db = Database()

st.title("Hello FIRE PUG user")


suggestion_expander = st.expander(label='Get suggestion')
with suggestion_expander:
	random_suggestion_cta = st.button('Get random suggestion')
	if random_suggestion_cta:
		query = db.generate_query('Don\'t mind', 'Don\'t mind')
		suggested_result = db.search(query)
		st.success(f'let\'s go to {suggested_result}!')
		st.balloons()
	
	with st.form(key="suggestion_requirements_form", clear_on_submit=True):
		meal_type = st.radio("Meal type", ('Don\'t mind','Breakfast', 'Brunch', 'Lunch',
										   'Dinner', 'Roast', 'Drinks'))

		st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

		venue_type = st.radio("Venue type", ('Don\'t mind', 'Restaurant', 'Cafe', 'Bar'))
		st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

		suggestion_submit_button = st.form_submit_button(label='Submit')
	if suggestion_submit_button:
		query = db.generate_query(meal_type, venue_type)
		suggested_result = db.search(query)
		if suggested_result != 'No entries with this criteria':
			st.success(f'let\'s go to {suggested_result}!')
			st.balloons()
		else:
			st.error(suggested_result)
	


add_place_expander = st.expander(label='Add a place')
with add_place_expander:
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

		anything_else = st.text_input("Anything else?").rstrip()

		submit_button = st.form_submit_button(label='Submit')

	entry_criteria = [place_name, breakfast, brunch, lunch,
					  dinner, roast, drinks, restaurant,
					  cafe, bar, pub, added_by, anything_else]


	if submit_button:
		if not db.place_exists(place_name):
			db.add_place(entry_criteria)
			st.success(f'{place_name} has been added!')
		else:
			st.error('This place has already been added!')


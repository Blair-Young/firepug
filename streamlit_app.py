import json
import streamlit as st
from google.oauth2 import service_account
import gspread
import pandasql as ps
import pandas as pd
from datetime import datetime
import uuid


key_dict = json.loads(st.secrets["textkey"])

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

client = gspread.service_account_from_dict(key_dict)

sheet = client.open('locations').get_worksheet(0)

records_data = sheet.get_all_records()

df = pd.DataFrame.from_dict(records_data)
booleanDictionary = {"TRUE": True, "FALSE": False}
df = df.replace(booleanDictionary)
pysqldf = lambda q: ps.sqldf(q, globals())


def format_result(result):
    if len(result):
        return result[0]
    return 'No entries with this criteria'

def random_search(database):
    query = """SELECT * FROM df ORDER BY RANDOM()"""
    return format_result(pysqldf(query)['name'].values)

def suggested_search(database, meal_criteria, venue_criteria):

    if meal_criteria=='Don\'t mind' and venue_criteria=='Don\'t mind':
        return random_search(database)

    if meal_criteria=='Don\'t mind' and venue_criteria!='Don\'t mind':
        venue_criteria_filter = f'venue_type_{venue_criteria}'.lower()
        query = f"""SELECT * FROM df WHERE {venue_criteria_filter}=True ORDER BY RANDOM() LIMIT 1"""
        return format_result(pysqldf(query)['name'].values)
    
    if venue_criteria=='Don\'t mind' and meal_criteria!='Don\'t mind':
        meal_criteria_filter = f'meal_type_{meal_criteria}'.lower()
        query = f"""SELECT * FROM df WHERE {meal_criteria_filter}=True ORDER BY  RANDOM() LIMIT 1"""
        return format_result(pysqldf(query)['name'].values)
    
    else:
        meal_criteria_filter = f'meal_type_{meal_criteria}'.lower()
        venue_criteria_filter = f'venue_type_{venue_criteria}'.lower()
        query = f"""SELECT * FROM df WHERE {meal_criteria_filter}=True AND
        {venue_criteria_filter}=True ORDER BY  RANDOM() LIMIT 1"""
        return format_result(pysqldf(query)['name'].values)



def add_place(df, entry_criteria):
	now = datetime.now()
	current_time = now.strftime("%d/%m/%Y %H:%M:%S")
	uid = str(uuid.uuid4())
	db_logging = [uid, current_time]
	db_entry = db_logging + entry_criteria
	sheet.append_rows(values=[db_entry])
	
def check_entry(database, name):
	places = database['name'].tolist()
	print(places)
	if name not in places:
		return True
	return False
		



st.title("Hello FIRE PUG user")


suggestion_expander = st.expander(label='Get suggestion')
with suggestion_expander:
	random_suggestion_cta = st.button('Get random suggestion')

	if random_suggestion_cta:
		suggested_output = random_search(df)
		st.success(f'let\'s go to {suggested_output}!')
		st.write(suggested_output)
		st.balloons()
	
	with st.form(key="suggestion_requirements_form", clear_on_submit=True):
		meal_type = st.radio("Meal type", ('Don\'t mind','Breakfast', 'Brunch', 'Lunch',
										   'Dinner', 'Roast', 'Drinks'))

		st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

		venue_type = st.radio("Venue type", ('Don\'t mind', 'Restaurant', 'Cafe', 'Bar'))
		st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

		suggestion_submit_button = st.form_submit_button(label='Submit')
		if suggestion_submit_button:
			print(meal_type)
			print(venue_type)
			suggested_result = suggested_search(df, meal_type, venue_type)
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

		anything_else = st.text_input("Anything else?")

		submit_button = st.form_submit_button(label='Submit')

	entry_criteria = [place_name, breakfast, brunch, lunch,
					  dinner, roast, drinks, restaurant,
					  cafe, bar, pub, added_by, anything_else]


	if submit_button:
		if check_entry(df, place_name):
			add_place(df, entry_criteria)
			st.success(f'{place_name} has been added!')
		else:
			st.error('This place has already been added!')





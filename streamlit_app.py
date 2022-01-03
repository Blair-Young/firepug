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
booleanDictionary = {"TRUE": True, "FALSE": False}
df = df.replace(booleanDictionary)



def random_search(database, criteria=False):
	if not criteria:
 		return database.sample()



def suggested_search(database, meal_criteria, venue_criteria):

	results = {'status': None,
			  'payload': None}


	if True not in meal_criteria.values() and True not in venue_criteria.values():
		results['status'] = 'Random search applied'
		results['payload'] = random_search(database)
		return results


	if True not in meal_criteria.values():
		database_query = database[
							  (database['venue_type_restaurant']==venue_criteria['restaurant']) &
							  (database['venue_type_cafe']==venue_criteria['cafe']) &
							  (database['venue_type_bar']==venue_criteria['bar']) &
							  (database['venue_type_pub']==venue_criteria['pub'])]

		if len(database_query)==0:
			results['status'] = 'No results'
			return results
		else:
			results['status'] = 'search applied over venue'
			results['payload'] = random_search(database_query)
			return results



	if True not in venue_criteria.values():
		database_query = database[(database['meal_type_breakfast']==meal_criteria['breakfast']) &
							  (database['meal_type_brunch']==meal_criteria['brunch']) &
							  (database['meal_type_lunch']==meal_criteria['lunch']) &
							  (database['meal_type_dinner']==meal_criteria['dinner']) &
							  (database['meal_type_roast']==meal_criteria['roast']) &
							  (database['meal_type_drinks']==meal_criteria['drinks'])]
		print(database_query)
		if len(database_query)==0:
			results['status'] = 'No results'
			return results
		else:
			results['status'] = 'search applied over meal'
			results['payload'] = random_search(database_query)
			return results


	database_query = database[(database['meal_type_breakfast']==meal_criteria['breakfast']) &
							  (database['meal_type_brunch']==meal_criteria['brunch']) &
							  (database['meal_type_lunch']==meal_criteria['lunch']) &
							  (database['meal_type_dinner']==meal_criteria['dinner']) &
							  (database['meal_type_roast']==meal_criteria['roast']) &
							  (database['meal_type_drinks']==meal_criteria['drinks']) &
							  (database['venue_type_restaurant']==venue_criteria['restaurant']) &
							  (database['venue_type_cafe']==venue_criteria['cafe']) &
							  (database['venue_type_bar']==venue_criteria['bar']) &
							  (database['venue_type_pub']==venue_criteria['pub'])]


	

	if len(database_query)==0:
		results['status'] = 'No results'
		return results
	results['status'] = 'Search applied over database'
	results['payload'] = random_search(database_query)
	return results

	


def search_output(search_result, criteria=False):
 	if not criteria:
 		return search_result.iloc[0]['name']

def add_place(df, entry_criteria):
	now = datetime.now()
	current_time = now.strftime("%d/%m/%Y %H:%M:%S")
	uid_generator = df['uid'].max()+1
	db_logging = [int(uid_generator), current_time]
	print(db_logging)
	db_entry = db_logging + entry_criteria
	sheet.append_rows(values=[db_entry])
		



st.title("Hello FIRE PUG user")




suggestion_expander = st.expander(label='Get suggestion')
with suggestion_expander:
	random_suggestion_cta = st.button('Get random suggestion')

	if random_suggestion_cta:
		suggested_output = search_output(random_search(df))
		st.success(f'let\'s go to {suggested_output}!')
		st.write(suggested_output)
		st.balloons()
	
	with st.form(key="suggestion_requirements_form", clear_on_submit=True):
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

		suggestion_submit_button = st.form_submit_button(label='Submit')
		meal_criteria = {'breakfast': breakfast,
						 'brunch' : brunch,
						 'lunch' : lunch,
						 'dinner' : dinner,
						 'roast' : roast,
						 'drinks': drinks}

		venue_criteria = {'restaurant':restaurant,
						  'cafe':cafe,
						  'bar': bar,
						  'pub': pub}


		if suggestion_submit_button:
			results = suggested_search(df, meal_criteria, venue_criteria)
			if results['status'] != 'No results':
				st.success(search_output(results['payload']))
			else:
				st.error('No entries with this criteria')
	


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
	    add_place(df, entry_criteria)
	    st.success(f'{place_name} has been added!')





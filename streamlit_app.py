import json
import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd

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
 		return search_result.iloc[0]['Name']

def add_place(name, df, criteria=False):
	if not criteria:
		sheet.append_rows(values=[[len(df)+1, str(name)]])
		


st.title("Hello FIRE PUG user")

suggestion_cta = st.button('Get suggestion')

if suggestion_cta:
	suggested_output = search_output(search(df))
	st.write(suggested_output)
	st.balloons()


name = st.text_input("Or add a new place place below")

if st.button('Submit'):
	result = name.title()
	add_place(result, df)
	st.success(f'{result} has been added!')




















# if add_place_cta:
# 	name = st.text_input("label goes here")
# 	if(st.button('Submit')):
# 		result = name.title()
# 		st.success(result)
# 		print(result)


 
# display the name when the submit button is clicked
# .title() is used to get the input text string
# if(st.button('Submit')):
#     result = name.title()
#     st.success(result)

# if add_place_cta:
# 	place_name = st.text_area("label goes here")
# 	print('ddd')
# 	print(place_name.title())
# 	print(type(place_name))
# 	add_place(place_name, df)

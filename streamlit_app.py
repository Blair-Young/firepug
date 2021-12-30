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

st.title("Hello FIRE PUG user")

suggestion = st.button('Get suggestion')

if suggestion:
	suggested_output = search_output(search(df))
	st.write(suggested_output)
	st.balloons()

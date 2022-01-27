import psycopg2
import streamlit as st
import pandas as pd
from datetime import datetime
import uuid


class Database():
	def __init__(self):
		self.connection = psycopg2.connect(host= st.secrets['host'],
										database=st.secrets['database'],
										user=st.secrets['user'],
										password=st.secrets['password'])

	def search(self, query):
		cur = self.connection.cursor()
		cur.execute(query)
		result = cur.fetchall()
		cur.close()
		self.connection.close()
		return self.format_results(result)

	def format_results(self, result):
		if not len(result):
			return 'No entries with this criteria'
		return Location(result[0]).name

	def generate_query(self, meal_criteria=None, venue_criteria=None):
		if meal_criteria=='Don\'t mind' and venue_criteria=='Don\'t mind':
			return """SELECT * FROM locations ORDER BY RANDOM()"""
		
		if meal_criteria=='Don\'t mind' and venue_criteria!='Don\'t mind':
			venue_criteria_filter = f'venue_type_{venue_criteria}'.lower()
			return f"""SELECT * FROM locations WHERE {venue_criteria_filter}=True ORDER BY RANDOM() LIMIT 1"""

		if venue_criteria=='Don\'t mind' and meal_criteria!='Don\'t mind':
			meal_criteria_filter = f'meal_type_{meal_criteria}'.lower()
			return f"""SELECT * FROM locations WHERE {meal_criteria_filter}=True ORDER BY  RANDOM() LIMIT 1"""
		else:
			meal_criteria_filter = f'meal_type_{meal_criteria}'.lower()
			venue_criteria_filter = f'venue_type_{venue_criteria}'.lower()
			return f"""SELECT * FROM locations WHERE {meal_criteria_filter}=True AND {venue_criteria_filter}=True ORDER BY  RANDOM() LIMIT 1"""


	def add_place(self, entry_criteria):
		now = datetime.now()
		current_time = now.strftime("%d/%m/%Y %H:%M:%S")
		uid = str(uuid.uuid4())
		db_logging = [uid, current_time]
		location_attributes = db_logging + entry_criteria
		print('loc att', location_attributes)
		db_entry = Location(location_attributes)
		command = f"""SET DateStyle TO European;
						INSERT INTO locations VALUES(
													'{db_entry.uid}', 
													'{db_entry.date_added}',
													'{db_entry.name}',
													{db_entry.meal_type_breakfast},
													{db_entry.meal_type_brunch},
													{db_entry.meal_type_lunch},
													{db_entry.meal_type_dinner},
													{db_entry.meal_type_roast},
													{db_entry.meal_type_drinks},
													{db_entry.venue_type_restaurant},
													{db_entry.venue_type_cafe},
													{db_entry.venue_type_bar},
													{db_entry.venue_type_pub},
													'{db_entry.added_by}',
													'{db_entry.anything_else}')
													"""
		print(command)
		cur = self.connection.cursor()
		cur.execute(command)
		self.connection.commit()
		cur.close()
		self.connection.close()

	def place_exists(self, place_name):
		query = f"""SELECT * FROM locations WHERE LOWER(name) = LOWER('{place_name}')"""
		print(query)
		cur = self.connection.cursor()
		cur.execute(query)
		result = cur.fetchall()
		print(result)
		if len(result):
			return True
		return False 

class Location():
	def __init__(self, attributes):
		self.uid = attributes[0]
		self.date_added= attributes[1]
		self.name = attributes[2]
		self.meal_type_breakfast= attributes[3]
		self.meal_type_brunch= attributes[4]
		self.meal_type_lunch= attributes[5]
		self.meal_type_dinner= attributes[6]
		self.meal_type_roast= attributes[7]
		self.meal_type_drinks= attributes[8]
		self.venue_type_restaurant= attributes[9]
		self.venue_type_cafe= attributes[10]
		self.venue_type_bar= attributes[11]
		self.venue_type_pub= attributes[12]
		self.added_by= attributes[13]
		self.anything_else= attributes[14]


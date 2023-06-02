import streamlit as st
import pandas as pd
import numpy as np
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from PIL import Image
import matplotlib.pyplot as plt
import openai

#EXL logo
image = Image.open('exl.png')

with st.sidebar:
	st.image(image, width = 150)
	st.write('Ask any question on your BI report')
	st.write(' ')
	st.write(' ')
	role = st.selectbox('Please select your role',('HR Manager', 'Sales Manager', 'Claims Manager'))

tab1, tab2 = st.tabs(['Analysis','Communication'])

with tab1:
	
	llm = OpenAI(api_token=st.secrets["chat_gpt_key"])
	
	pandas_ai = PandasAI(llm, conversational=False, enforce_privacy = True)
	
	df1 = pd.read_csv('employees.csv')
	df2 = pd.read_csv('sales_data.csv')
	df3 = pd.read_csv('claims_data.csv')
	
	ls = ['chart','plot','graph','trend']
	#to check if prompt have chart, graph words
	def contains_substring(string, substrings):
		for substring in substrings:
			if substring in string:
				return True
		return False
		
		
	#based on role selected show BI report  
	if role == 'HR Manager':
		df = df1
	elif role == 'Sales Manager':
		df = df2
	elif role == 'Claims Manager':
		df = df3
	
	st.header("Conversational BI")
	st.subheader("BI Report (Structure): " + role.replace('Manager',''))
	st.dataframe(df.head())
	
	with st.form("conversation_bi"):
		
		query = st.text_input(label ="Enter a question" , placeholder = 'Enter your query')
		# Every form must have a submit button.
		submitted1 = st.form_submit_button("Submit")
		if submitted1:
			if contains_substring(query.lower(),ls): 
				fig, x = plt.subplots()
				response1 = pandas_ai(df, prompt=query)
				st.pyplot(fig)
				st.text(response1)
			else:
				response1 = pandas_ai(df, prompt=query)
				st.text(response1)
				


with tab2:

	openai.api_key = st.secrets["chat_gpt_key"]
	
	df = pd.read_csv('performance.csv')
	
	def openai_response(query):
		response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages = [
			{"role":"system", "content":"You are helpful assistant."},
			{"role":"user","content": query}
		]
		)
		return response.choices[0]['message']['content']   
		
	
	st.header("Personalized communication ")
	response2 = ''
	with st.form("communication"):
		name = st.selectbox('Please select name',df["name"])
		intent_of_mail = st.text_input(label ="Intent of mail" , placeholder = 'Intent')
		category = df[df.name == name]['performance'].to_string(index=False)
		target = df[df.name == name]['target'].to_string(index=False)
		latest_performance = df[df.name == name]['latest_month_performance'].to_string(index=False)
		
		# Every form must have a submit button.
		submitted2 = st.form_submit_button("Submit")
		if submitted2:
			response2 = openai_response(f"""Write a {intent_of_mail} mail to a salesperson {name} as their employer based on following information starts and ends with triplle dashes marks,
					Analyse the data to determine whether a salesperson's performance is above or below target and how it impacts the performance category,
					offer some insight based on performance and their category,
					--- {name} is {category} with their target, their latest target was {target} and latest performance was {latest_performance} ---
					""")
			st.text(f"""Category : {category}\nTarget : {target}\nLatest performance : {latest_performance}""")
			st.write()
			st.markdown(response2)
			st.download_button(
			    label="Download data as CSV",
			    data='employees.csv',
			    file_name='large_df.csv',
			    mime='text/csv',
			)
	if response2 != '':
		st.download_button('Download text', response2)
					st.download_button(
			    label="Download data as CSV",
			    data='employees.csv',
			    file_name='large_df.csv',
			    mime='text/csv',
			)

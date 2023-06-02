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
df = pd.read_csv('data.csv')
with st.sidebar:
	st.image(image, width = 150)
	st.write('Ask any question on your BI report')

tab1, tab2 = st.tabs(['Analysis','Communication'])

with tab1:
	
	llm = OpenAI(api_token=st.secrets["chat_gpt_key"])
	
	pandas_ai = PandasAI(llm, conversational=False, enforce_privacy = True)
	
	
	ls = ['chart','plot','graph','trend']
	#to check if prompt have chart, graph words
	def contains_substring(string, substrings):
		for substring in substrings:
			if substring in string:
				return True
		return False

	
	st.header("Conversational BI")
	st.subheader("BI Report (Structure): ")
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
	
	send_button = st.button("Send communication")
	if send_button:
		st.write('Communication sent')
		
	with st.form("communication"):
		name = st.selectbox('Please select name',df["name"])
		category = df[df.name == name]['performance'].to_string(index=False)
		target = df[df.name == name]['target'].to_string(index=False)
		latest_performance = df[df.name == name]['latest_month_performance'].to_string(index=False)
		
		# Every form must have a submit button.
		submitted2 = st.form_submit_button("Submit")
		if submitted2:
			response2 = openai_response(f"""Write a feedback mail to a salesperson {name} as their employer based on following information starts and ends with triplle dashes marks,
					Analyse the data to determine whether a salesperson's performance is above or below target and how it impacts the performance category,
					offer some insight based on performance and their category,
					--- {name} is {category} with their target, their latest target was {target} and latest performance was {latest_performance} ---
					""")
			st.text(f"""Name: {name}\nCategory : {category}\nTarget : {target}\nLatest performance : {latest_performance}""")
			st.write()
			st.markdown(response2)


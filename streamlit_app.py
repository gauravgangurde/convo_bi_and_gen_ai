import streamlit as st
import pandas as pd
import numpy as np
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from PIL import Image
import matplotlib.pyplot as plt
import openai
from openpyxl import workbook

#EXL logo
image = Image.open('exl.png')
df = pd.read_csv('data.csv')
with st.sidebar:
	st.image(image, width = 150)
	st.write('Ask any question on your BI report')

tab1, tab2 = st.tabs(['Analysis','Communication'])

with tab1:
	
	llm = OpenAI(api_token=st.secrets["chat_gpt_key"])
	
	pandas_ai = PandasAI(llm, conversational=False)#, enforce_privacy = True)
	
	
	ls = ['chart','plot','graph','trend']
	#to check if prompt have chart, graph words
	def contains_substring(string, substrings):
		for substring in substrings:
			if substring in string:
				return True
		return False

	
	st.header("Conversational BI")
	st.subheader("Sample data structure ")
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
		],
		temperature = 0,
		)
		return response.choices[0]['message']['content']   
		
	
	st.header("Personalized communication ")
	
	send_button = st.button("Send communication")
	if send_button:
		st.write('')
		
	with st.form("communication"):
		name = st.selectbox('Please select agent to check outgoing communication',df["Name"])
		category = df[df.Name == name]['Category'].to_string(index=False)
		target = df[df.Name == name]['Target'].to_string(index=False)
		curr_sales = df[df.Name == name]['Sales'].to_string(index=False)
		growth = df[df.Name == name]['Growth'].to_string(index=False)
		
		# Every form must have a submit button.
		submitted2 = st.form_submit_button("Submit")
		if submitted2:
			#response2 = openai_response(f"""Your task is to write mail to {name} about their performance data delimited by three backticks,
			#		analysing performance data, give feedback, suggesting improvment areas, and it should include 2 sales improvement article or training link references based on performance category
			#		Please keep the mail concise and sign it as 'Manager'
			#		performance data : ```{name} is {category} with their target, their latest target was {target} and current sales performance is {curr_sales}
			#		 and their total sales growth with respective previous month sales performance is {growth}```
			#		 """)
			#st.text(f"""Name: {name}\nCategory : {category}\nTarget : ${target}\nCurrnt Sales : ${curr_sales}\nSales growth: {growth}""")
			#st.write()
			#st.markdown(response2)
			
			wb= workbook('data-mail.xlsx')
			ws = wb.active
			
			#df_mail = pd.read_excel('data-mail.xlsx')
			#
			#category = df_mail[df_mail.Name == name]['Category'].to_string(index=False)
			#target = df_mail[df_mail.Name == name]['Target'].to_string(index=False)
			#curr_sales = df_mail[df_mail.Name == name]['Sales'].to_string(index=False)
			#growth = df_mail[df_mail.Name == name]['Growth'].to_string(index=False)
			
			st.text(f"""Name: {name}\nCategory : {category}\nTarget : ${target}\nCurrnt Sales : ${curr_sales}\nSales growth: {growth}""")
			st.write()
			st.markdown(ws.cell(row = df.loc[df_mail.Name == name].index[0], column = 10))


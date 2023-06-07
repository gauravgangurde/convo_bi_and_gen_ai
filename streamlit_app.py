import streamlit as st
import pandas as pd
import numpy as np
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from PIL import Image
import matplotlib.pyplot as plt
import openai
import openpyxl

#EXL logo
image = Image.open('exl.png')
df = pd.read_csv('data.csv')


with st.sidebar:
	st.image(image, width = 150)
	st.write('Ask any question on your data')

#define tabs
tab1, tab2, tab3 = st.tabs(['Analysis','Report', 'Validation'])

ls = ['chart','plot','graph','trend', 'histogram']
#to check if prompt have chart, graph words
def contains_substring(string, substrings):
	for substring in substrings:
		if substring in string:
			return True
	return False


# tab1 for raw data analysis
with tab1:
	
	llm = OpenAI(api_token=st.secrets["chat_gpt_key"])
	
	pandas_ai = PandasAI(llm, conversational=False)#, enforce_privacy = True)

	
	st.header("Conversational BI")
	st.subheader("Sample data structure ")
	st.dataframe(df.head())
	
	with st.form("conversation_bi"):
	
		query = st.text_input(label ="Enter a question" , placeholder = 'Enter your query')
		# Every form must have a submit button.
		submitted1 = st.form_submit_button("Submit")
		if submitted1:
			#based on type of response
			if contains_substring(query.lower(),ls): 
				fig, x = plt.subplots()
				response1 = pandas_ai(df, prompt=query)
				st.pyplot(fig)
			else:
				response1 = pandas_ai(df, prompt=query)
				if isinstance(response, str):
					st.text(response1)
				elif isinstance(response1, pd.DataFrame):
					st.dataframe(response1)
				else:
					st.text(response1.to_string(index=False))
				


with tab2:

	df2 = pd.read_csv('report.csv')
	col1, col2 = st.columns(2)
	
	with col1:
		#pie chart for sales by category
		total_sales = df2.groupby('Category')['Sales'].sum()
		fig1, ax1= plt.subplots(figsize=(6,6))
		ax1.pie(total_sales.values, labels=total_sales.index, autopct='%1.1f%%')
		ax1.set_title('Sales by Category')
		st.pyplot(fig1)
		
		#average sales by region
		average_sales2 = df2.groupby('Region')['Sales'].mean().reset_index()
		fig4, ax4= plt.subplots(figsize=(6,6))
		ax4.bar(average_sales2['Region'], average_sales2['Sales'])
		ax4.set_title('Average Sales by Region')
		plt.xticks(rotation=45)
		st.pyplot(fig4)
		


	with col2:	
		#average sales by category
		average_sales = df2.groupby('Category')['Sales'].mean().reset_index()
		fig2, ax2= plt.subplots(figsize=(10,6))
		ax2.bar(average_sales['Category'], average_sales['Sales'])
		ax2.set_title('Average Sales by Region')
		plt.xticks(rotation=45)
		st.pyplot(fig2)
		
		#pie chart for sales by region
		total_sales2 = df2.groupby('Region')['Sales'].sum()
		fig3, ax3= plt.subplots(figsize=(10,6))
		ax3.pie(total_sales2.values, labels=total_sales2.index, autopct='%1.1f%%')
		ax3.set_title('Sales by Region')
		st.pyplot(fig3)
	
	
	generate_mails = st.button("Generate Communication", key = '1')
	if generate_mails:
		st.write('Go to next tab to validate communication')

with tab3:
			
	st.header("Personalized communication ")
	

		
	with st.form("communication"):
		name = st.selectbox('Please select agent to check outgoing communication',df["Name"])
		category = df2[df2.Name == name]['Category'].to_string(index=False)
		target = df2[df2.Name == name]['Target'].to_string(index=False)
		curr_sales = df2[df2.Name == name]['Sales'].to_string(index=False)
		# Every form must have a submit button.
		submitted2 = st.form_submit_button("Validate")
		if submitted2:
			
			path = "data-mail.xlsx"
			wb= openpyxl.load_workbook(path)
			ws = wb.active
			st.text(f"""Name: {name}\nCategory : {category}\nTarget : ${target}\nCurrnt Sales : ${curr_sales}""")
			st.write()
			st.markdown(ws.cell(row = df.loc[df.Name == name].index[0] + 2, column = 10).value)
			

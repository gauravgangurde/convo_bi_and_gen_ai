import streamlit as st
import pandas as pd
import numpy as np
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from PIL import Image
import matplotlib.pyplot as plt
import openai
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

#EXL logo
image = Image.open('exl.png')
#read data file in dataframe
#df = pd.read_csv('data.csv')
df = pd.read_excel('Mort_V1.xlsx', header=2)


with st.sidebar:
	st.image(image, width = 150)
	st.write('Ask any question on your data')


ls = ['chart','plot','graph','trend', 'histogram']
#to check if prompt have chart, graph words
def contains_substring(string, substrings):
	for substring in substrings:
		if substring in string:
			return True
	return False

def query_mapper(query):
	if query.lower() == 'show mortality experience analysis by product and duration':
		return """Create a tabular report to show actual deaths divided by expected deaths as Mortality for each product and duration. Show Mortality in percentage format Product in rows and duration as columns. Add one row to show overall number for each column. Show all values in %"""
	elif query.lower() == 'show mortality experience analysis by product and smoker status':
		return """Create a tabular report to show actual deaths divided by expected deaths as Mortality for each product and smoker status Show Mortality in percentage format. Product in rows and smoker status as columns. Add one row to show overall number for each column. Show all values in %"""
	elif query.lower() == 'show mortality experience analysis by sum assured class and product':
		return """Create a tabular report to show actual deaths divided by expected deaths as Mortality for each "Sum Assured Class" and product. Show Mortality in percentage format. "Sum Assured Class" in rows and product as columns. Add one row to show overall number for each column. Show all values in %"""
	elif query.lower() == 'show mortality experience analysis by issue year':
		return """Create a tabular report to show Actual Deaths, Expected Deaths, actual deaths divided by expected deaths as Mortality for each issue year. Show Mortality in percentage format and Issue year in YYYY format"""
	elif query.lower() == 'show mortality experience analysis by uw class':
		return """Create a tabular report to show Actual Deaths, Expected Deaths, actual deaths divided by expected deaths as Mortality for each UW Class. Show Mortality in percentage format"""
	else:
		return query
	



llm = OpenAI(api_token=st.secrets["chat_gpt_key"])

pandas_ai = PandasAI(llm, conversational=False)#, enforce_privacy = True)


st.subheader("Conversational BI")
st.write("Sample data structure ")
st.dataframe(df.head())

#with st.form("conversation_bi"):

inp_query = st.text_input(label ="Enter a question" , placeholder = 'Enter your query')
#query = inp_query.lower().replace('mortality experience', 'percent of total actual death with respective total expected death')
query = query_mapper(inp_query).replace('mortality experience', 'actual deaths divided by expected deaths in percent as Mortality')
st.subheader(query)


#submitted1 = st.form_submit_button("Submit")
if st.button("Submit"):
	#based on type of response, check if user required graph/chart
	if contains_substring(query.lower(),ls): 
		fig, x = plt.subplots()
		response1 = pandas_ai(df, prompt=query)
		st.pyplot(fig)
	else:
		response1 = pandas_ai(df, prompt=query)
		#check if output is in dataframe and download option
		if isinstance(response1, pd.DataFrame):
			st.dataframe(response1)
			workbook = Workbook()
			sheet = workbook.active
			for row in dataframe_to_rows(response1):
				sheet.append(row)
			workbook.save('output.xlsx')
			with open("output.xlsx", "rb") as file:
				st.download_button(
					label="Download data",
					data=file,
					file_name='data.xlsx'
				)
		#check if output is in tuple
		elif isinstance(response1, tuple):
			st.text(response1)
		#check if output is in series, convert it to dataframe and download option
		elif isinstance(response1, pd.Series):
			#st.text(response1)
			response_df = response1.to_frame().reset_index()
			st.dataframe(response_df)
			workbook = Workbook()
			sheet = workbook.active
			for row in dataframe_to_rows(response_df, index=False):
				sheet.append(row)
			workbook.save('output.xlsx')
			with open("output.xlsx", "rb") as file:
				st.download_button(
					label="Download data",
					data=file,
					file_name='data.xlsx'
				)
		#for all other output formats
		else:
			st.text(response1)
		

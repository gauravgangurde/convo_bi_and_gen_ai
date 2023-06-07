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


# tab1 for raw data analysis
with tab1:
	
	llm = OpenAI(api_token=st.secrets["chat_gpt_key"])
	
	pandas_ai = PandasAI(llm, conversational=False)#, enforce_privacy = True)
	
	
	ls = ['chart','plot','graph','trend', 'histogram']
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
	
	#pie chart for sales by category
	plt.pie(df2['Sales'], labels= df2['category'], autopct='%1.1f%%')
	plt.title('Sales by Category')
	plt.show()

	#average sales by category
	average_sales = df.groupby('Category')['Sales'].mean().reset_index()
	plt.bar(average_sales['Category'], average_sales['Sales'])
	plt.xlabel('Category')
	plt.ylabel('Average Sales')
	plt.title('Average Sales by Category')
	plt.xticks(rotation=45)
	plt.show()
	
	generate_mails = st.button("Generate Communication")
	if generate_mails:
		st.write('Go to nexttab to validate')

with tab3:
			
	st.header("Personalized communication ")
	
	send_button = st.button("Generate Communication")
	if send_button:
		st.write('')
		
	with st.form("communication"):
		name = st.selectbox('Please select agent to check outgoing communication',df["Name"])
		category = df[df.Name == name]['Category'].to_string(index=False)
		target = df[df.Name == name]['Target'].to_string(index=False)
		curr_sales = df[df.Name == name]['Sales'].to_string(index=False)
		# Every form must have a submit button.
		submitted2 = st.form_submit_button("Validate")
		if submitted2:
			
			path = "data-mail.xlsx"
			wb= openpyxl.load_workbook(path)
			ws = wb.active
			st.text(f"""Name: {name}\nCategory : {category}\nTarget : ${target}\nCurrnt Sales : ${curr_sales}""")
			st.write()
			st.markdown(ws.cell(row = df.loc[df.Name == name].index[0] + 2, column = 10).value)
			

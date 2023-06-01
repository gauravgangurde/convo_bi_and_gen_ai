import streamlit as st
import pandas as pd
import numpy as np
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from PIL import Image
import matplotlib.pyplot as plt
import openai

#st.set_option('deprecation.showPyplotGlobalUse', False)
image = Image.open('exl.png')


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

#query to open AI
def openai_response(query):
	response = openai.ChatCompletion.create(
	model="gpt-3.5-turbo",

	messages = [
		{"role":"system", "content":"You are helpful assistant."},
		{"role":"user","content": query}
	]
   )
	return response.choices[0]['message']['content']
    
with st.sidebar:
	st.image(image, width = 150)
	st.header('Conversational BI')
	st.write('Ask any question on your BI report')
	st.write(' ')
	st.write(' ')
	role = st.selectbox('Please select your role',('HR Manager', 'Sales Manager', 'Claims Manager'))


#based on role selected show BI report  
if role == 'HR Manager':
	df = df1
elif role == 'Sales Manager':
	df = df2
elif role == 'Claims Manager':
	df = df3

st.header("BI Report (Structure): " + role.replace('Manager',''))
st.dataframe(df.head())

with st.form("my_form"):

	query = st.text_input(label ="Enter a question" , placeholder = 'Enter your query')
	cols_2_pass = openai_response(f"""Please only output in Python list style, with the names of each expected column separated by commas, such as 'column1', 'column2','column3'
                                 A dataframe with following column names : {df.columns}. 
                                 Find all column names which will be used in following query: {query}""")
   # Every form must have a submit button.
	submitted = st.form_submit_button("Submit")
	if submitted:
		st.write(cols_2_pass)
#		if contains_substring(query.lower(),ls): 
#			fig, x = plt.subplots()
#			response = pandas_ai(df, prompt=query)
#			st.pyplot(fig)
#			st.text(response)
#		else:
#			response = pandas_ai(df, prompt=query)
#			st.text(response)


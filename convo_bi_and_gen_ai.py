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
#read data file in dataframe
#df = pd.read_csv('data.csv')
df = pd.read_excel('Mort.xlsx', header=2)

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



llm = OpenAI(api_token=st.secrets["chat_gpt_key"])

pandas_ai = PandasAI(llm, conversational=False)#, enforce_privacy = True)


st.subheader("Conversational BI")
st.write("Sample data structure ")
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
			if isinstance(response1, pd.DataFrame):
				st.dataframe(response1)
			else:
				st.text(response1)
			

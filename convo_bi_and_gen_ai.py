import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from fpdf import FPDF
from openpyxl.drawing.image import Image as ii


#EXL logo
image = Image.open('exl.png')
#read data file in dataframe
#df = pd.read_csv('data.csv')
df = pd.read_excel('Mort_V1.xlsx', header=2)


with st.sidebar:
	st.image(image, width = 150)
	st.write('Ask any question on your data')


def pivot1(df,ind, col):
	#Pivot the data and calculate the total actual and expected deaths for each product and duration 
	pivot_table = pd.pivot_table(df, values=['Actual Deaths','Expected Deaths'], index=ind, columns = col, aggfunc='sum', margins=True, margins_name="Total")
	
	#Calculate the percentage of total actual deaths compared to total expected deaths 
	for i in df[col].unique():
		pivot_table['Percentage',i] = (pivot_table['Actual Deaths',i]/ pivot_table['Expected Deaths',i]* 100).round().map('{:.0f}%'.format)
	pivot_table['Percentage','Total'] = (pivot_table['Actual Deaths','Total']/ pivot_table['Expected Deaths','Total']* 100).round().map('{:.0f}%'.format)
	
	# Display the pivot table with both headers
	
	#Add a title to the pivot table 
	#title = "Percentage of Total Actual Deaths vs Total Expected Deaths for Different Products and Durations" 
	#pivot_table_with_title = pd.concat([pd.DataFrame([title], columns=['']), pivot_table], axis=0)
	return pivot_table['Percentage']
#st.dataframe(pivot_table['Percentage'])
#st.dataframe(pivot1('Product', 'Duration'))
#st.dataframe(pivot1('Product', 'Smoker Status'))
#st.dataframe(pivot1('Product', 'Sum Assured Class'))

#def pivot2(df,col):
	

def query_mapper(query):
	if query == 'show mortality experience analysis by product and duration':
		return """Create a tabular report to show actual deaths divided by expected deaths as Mortality for each product and duration. Show Mortality in percentage format Product in rows and duration as columns. Add one row to show overall number for each column. Show all values in %"""
	elif query == 'show mortality experience analysis by product and smoker status':
		return """Create a tabular report to show actual deaths divided by expected deaths as Mortality for each product and smoker status Show Mortality in percentage format. Product in rows and smoker status as columns. Add one row to show overall number for each column. Show all values in %"""
	elif query == 'show mortality experience analysis by sum assured class and product':
		return """Create a tabular report to show actual deaths divided by expected deaths as Mortality for each "Sum Assured Class" and product. Show Mortality in percentage format. "Sum Assured Class" in rows and product as columns. Add one row to show overall number for each column. Show all values in %"""
	elif query == 'show mortality experience analysis by issue year':
		return """Create a tabular report to show Actual Deaths, Expected Deaths, actual deaths divided by expected deaths as Mortality for each issue year. Show Mortality in percentage format and Issue year in YYYY format"""
	elif query == 'show mortality experience analysis by uw class':
		return """Create a tabular report to show Actual Deaths, Expected Deaths, actual deaths divided by expected deaths as Mortality for each UW Class. Show Mortality in percentage format"""
	else:
		return query
	


st.subheader("Conversational BI")
st.write("Sample data structure ")
st.dataframe(df.head())

#with st.form("conversation_bi"):

inp_query = st.text_input(label ="Enter a question" , placeholder = 'Enter your query')
query = inp_query.lower()
#st.subheader(query)

if st.button("Submit"):

	if query == 'show mortality experience analysis by product and duration':
		df_out = pivot1(df,'Product', 'Duration')
		title = 'show mortality experience analysis by product and duration'
	elif query == 'show mortality experience analysis by product and smoker status':
		df_out = pivot1(df,'Product', 'Smoker Status')
		title = 'show mortality experience analysis by product and smoker status'
	elif query == 'show mortality experience analysis by sum assured class and product':
		df_out = pivot1(df,'Sum Assured Class', 'Product')
		title = 'show mortality experience analysis by sum assured class and product'
	elif query == 'show mortality experience analysis by issue year':
		df_out = pivot2(df,'Issue Year')
		title = 'show mortality experience analysis by issue year'
	elif query == 'show mortality experience analysis by uw class':
		df_out = pivot2(df,'UW Class')
		title = 'show mortality experience analysis by uw class'

	st.dataframe(df_out)
	df_out.reset_index(level=0, inplace=True)

	#Excel
	workbook = Workbook()
	sheet = workbook.active
	worksheet.add_image(ii('exl.png'), 'K3')
	c1 = sheet.cell(row = 1, column = 1)
	c1.value = title
	for row in dataframe_to_rows(df_out, index = False):
		sheet.append(row)
	workbook.save('output.xlsx')
	with open("output.xlsx", "rb") as file:
		st.download_button(
			label="Download Excel",
			data=file,
			file_name='data.xlsx'
		)

		

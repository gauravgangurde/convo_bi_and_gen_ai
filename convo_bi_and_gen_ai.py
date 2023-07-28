import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from fpdf import FPDF

#EXL logo
image = Image.open('exl.png')
#read data file in dataframe
#df = pd.read_csv('data.csv')
df = pd.read_excel('Mort_V1.xlsx', header=2)


with st.sidebar:
	st.image(image, width = 150)
	st.write('Ask any question on your data')



#Pivot the data and calculate the total actual and expected deaths for each product and duration 
pivot_table = pd.pivot_table(df, values=['Actual Deaths','Expected Deaths'], index="Product", columns = 'Duration', aggfunc='sum', margins=True, margins_name="Total")

#Calculate the percentage of total actual deaths compared to total expected deaths 
for i in range(13):
	pivot_table['Percentage',i+1] = (pivot_table['Actual Deaths',i+1]/ pivot_table['Expected Deaths',i+1]* 100).round()#.astype(int)
pivot_table['Percentage','Total'] = (pivot_table['Actual Deaths','Total']/ pivot_table['Expected Deaths','Total']* 100).round()#.astype(int)

# Display the pivot table with both headers

#Add a title to the pivot table 
#title = "Percentage of Total Actual Deaths vs Total Expected Deaths for Different Products and Durations" 
#pivot_table_with_title = pd.concat([pd.DataFrame([title], columns=['']), pivot_table], axis=0)

st.dataframe(pivot_table['Percentage'])

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
query = query_mapper(inp_query.lower())
#st.subheader(query)

def df_to_pdf(df, output_file):
	# Initialize PDF document
	pdf = FPDF()
	pdf.add_page()
	
	# Set font and font size
	pdf.set_font("Arial", size=12)
	
	# Add table header
	for column in df.columns:
		pdf.cell(200, 10, str(column), 1)
	pdf.ln()
	
	# Add table data
	for index, row in df.iterrows():
		for value in row:
			pdf.cell(200, 10, str(value), 1)
		pdf.ln()
	
	# Save PDF to the specified output file
	pdf.output(output_file)


# Usage example
output_pdf_file = 'output_dataframe.pdf'
df_to_pdf(pivot_table, output_pdf_file)


with open("output_dataframe.pdf", "rb") as file:
	st.download_button(
		label="Download data",
		data=file,
		file_name='report.pdf'
	)


if st.button("Submit"):
	with open("output.xlsx", "rb") as file:
		st.download_button(
			label="Download data",
			data=file,
			file_name='data.xlsx'
		)

		

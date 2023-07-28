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
	df1 = pivot_table['Percentage']
	df1.reset_index(level=0, inplace=True)
	df1.columns.values[0] = ind + '/'+ col
	return df1


def pivot2(df,col):
	df1 = df.groupby(col)[['Actual Deaths','Expected Deaths']].sum()
	df1['Mortality'] = (df1['Actual Deaths']/df1['Expected Deaths'] * 100).round().map('{:.0f}%'.format)
	df1.reset_index(level=0, inplace=True)
	return df1
	


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
		title = 'Mortality experience by Product and Duration'

		df_t = df_out.set_index('Product/Duration').T.reset_index()

		# Define the labels for the x-axis
		x_labels = df_t['index'].tolist()
		
		# Set the positions of the bars on the x-axis
		x = range(len(x_labels))
		
		# Plot the bar graph for each value of Term and Endowment
		fig, ax = plt.subplots()
		bar_width = 0.25
		for i, label in enumerate(['Endowment', 'Term']):
			ax.bar([pos + bar_width * i for pos in x], df_t[label], bar_width, label=label)
	
		# Label the axes and add a title
		ax.set_xlabel('Duration')
		ax.set_ylabel('Mortality')
		ax.set_title('Endowment and Term Percentage')
		
		# Set the y-axis limit to match the percentage values (0 to 100)
		ax.set_ylim(0, 100)
		
		# Set the x-axis labels
		ax.set_xticks([pos + bar_width / 2 for pos in x])
		ax.set_xticklabels(x_labels)
		
		# Show the legend
		ax.legend()
		
		# Show the plot
		plt.tight_layout()
		plt.show()

		fig.savefig(option+'.png')

	elif query == 'show mortality experience analysis by product and smoker status':
		df_out = pivot1(df,'Product', 'Smoker Status')
		title = 'Mortality experience by Product and Smoker Status'
	elif query == 'show mortality experience analysis by sum assured class and product':
		df_out = pivot1(df,'Sum Assured Class', 'Product')
		title = 'Mortality experience sum assured Class and Product'
	elif query == 'show mortality experience analysis by issue year':
		df_out = pivot2(df,'Issue Year')
		df_out['Issue Year'] = df_out['Issue Year'].astype(str).str.replace(',', '')
		title = 'Mortality experience by Issue Year'
	elif query == 'show mortality experience analysis by uw class':
		df_out = pivot2(df,'UW Class')
		title = 'Mortality experience by UW Class'

	st.write(title)
	st.dataframe(df_out,)

	#Excel
	workbook = Workbook()
	sheet = workbook.active
	sheet.title = 'Report'

	c1 = sheet.cell(row = 1, column = 1)
	c1.value = title
	for row in dataframe_to_rows(df_out, index = False):
		sheet.append(row)

	#formatting graph
	sheet2 = workbook.create_sheet(title='Graph')
	graph = ii('graph1.png')
	aspect_ratio = graph.width / graph.height
	graph.width = 800
	graph.height = graph.width/aspect_ratio
	#adding graph to sheet
	sheet2.add_image(graph, 'B2')

	workbook.save('output.xlsx')

	
	with open("output.xlsx", "rb") as file:
		st.download_button(
			label="Download Excel",
			data=file,
			file_name='data.xlsx'
		)

		

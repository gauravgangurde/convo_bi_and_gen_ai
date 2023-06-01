import streamlit as st
import pandas as pd
import numpy as np
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from PIL import Image
import matplotlib.pyplot as plt

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
    
    
with st.sidebar:
    st.image(image, width = 150)
    st.header('Conversational BI')
    st.write('Ask any question on your BI report')
    st.write(' ')
    st.write(' ')
    role = st.selectbox('Please select your role',('HR Manager', 'Sales Manager', 'Claims Manager'))


#based on role selected show BI report  
if   role == 'HR Manager':
    df = df1
elif role == 'Sales Manager':
    df = df2
elif role == 'Claims Manager':
    df = df3

st.header("BI Report (Structure): " + role.replace('Manager',''))
st.dataframe(df.head())

with st.form("my_form"):

   query = st.text_input(label ="Enter a question" , placeholder = 'Enter your query')
   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       if contains_substring(query.lower(),ls): 
        fig, x = plt.subplots()
        response = pandas_ai(df, prompt=query)
        st.pyplot(fig)
        st.text(response)
       else:
        response = pandas_ai(df, prompt=query)
        st.text(response)




import streamlit as st

# Sidebar
my_select_box = st.sidebar.selectbox('Select', ['US', 'UK', 'DE', 'FR'])

my_slider = st.sidebar.slider('My slider', min_value=0, max_value=10)

left_column, right_colum =  st.columns(2)

import random

data = [random.random() for _ in range(100)]

with left_column:
    st.subheader('A line chart')
    st.line_chart(data)


right_colum.subheader('Data')

right_colum.write(data[:50])


col1, col2, col3 = st.columns([0.2, 0.5, 0.3])

col1.markdown('Hello Streamlite world')

col2.write(data[5:10])

with col3:
    st.header('A cat')
    st.image('https://www.petz.com.br/blog/wp-content/uploads/2020/08/cat-sitter-felino.jpg')


# Expander
with st.expander('Click to expand'):
    st.bar_chart({'Data': [random.randint(2, 10) for _ in range(25)]})
    st.write('This a image of a cat')
    st.image('https://www.petz.com.br/blog/wp-content/uploads/2020/08/cat-sitter-felino.jpg')





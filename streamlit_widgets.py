import streamlit as st
import pandas as pd
from io import StringIO
# Text input

name = st.text_input('Your name')

if name:
    st.write(f'Hello {name}')

number = st.number_input('Enter a numbser', min_value=1, max_value=99, step=1)

if number:
    st.write(f'The current number is {number}')

st.divider()


 # button
clicked = st.button('Send')

if clicked:
    st.write(':ghost:' * int(number))

# Checkbox

agree = st.checkbox('I agree')

if agree:
    'Gerate, you agreed!'

checked = st.checkbox('Continue', value=True)

if checked:
    ':+1:' * 5

df = pd.DataFrame({'Name': ['Anne', 'Mario', 'Douglas'],
                   'Age': [30, 40, 45]
                   })

if st.checkbox('Show data'):
    df

st.divider()
# Radio button

pets = ['cat', 'dogs', 'fish', 'turtle']

pet = st.radio('favorite pet', pets, index=2, key='your_pet')

if pet:
    st.write(f'Favorite pet: {pet}')
    st.write(st.session_state.your_pet)

st.divider()

# Select box
cities = ['London', 'Berlim', 'Paris', 'Madrid']

city = st.selectbox('Your city', cities)

if city:
    st.write(f'You city: {city}')


st.divider()

# Slider

slider_value = st.slider('x', value=10, min_value=0, max_value=50, step=2)

st.write(f'Slider value in {slider_value}')

st.divider()

uploaded_file = st.file_uploader('Upload a file:', type=['txt', 'csv', 'xlxs'])

if uploaded_file:
    match uploaded_file.type:
        case 'text/plain':
            string_io = StringIO(uploaded_file.getvalue().decode('utf-8'))

            string_data = string_io.read()

            st.write(string_data)
        
        case 'text/csv':
            df = pd.read_csv(uploaded_file)

            st.write(df)
        
        case _:
            df = pd.read_csv(uploaded_file)

            st.write(df)
    
st.divider()

take_shot_agree = st.checkbox('Take a photo agree', value=False)

if take_shot_agree:

    # Camara input
    camera_photo = st.camera_input('Take a photo')

    if camera_photo:
        st.image(camera_photo)

st.image('https://www.presidenteprudente.sp.gov.br/site/imagem/104921')

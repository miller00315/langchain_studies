import streamlit as st
import pandas as pd

st.title("Hellooooooo Streamlite :100:")

my_select_box = st.sidebar.selectbox(
    "Select country", list(["US", "UK", "DE", "FR", "JP"])
)

my_slider = st.sidebar.slider("Temperature C")

st.sidebar.write(f"Temperature F: {my_slider * 1.8 + 32}")

l1 = [1, 2, 3]

st.write(l1)

l2 = list("abc")

d1 = dict(zip(l1, l2))

st.write(d1)

# usign magic


"Displaying using magic :smile:"

df = pd.DataFrame({"first_colummn": [1, 2, 3, 4], "second_column": [10, 20, 30, 40]})

df  # st.write(df)

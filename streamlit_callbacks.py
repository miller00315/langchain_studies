import streamlit as st

st.subheader("Distance converter")

col1, buff, col2 = st.columns([2, 1, 2])


def miles_to_kilometers():
    st.session_state["km"] = st.session_state["miles"] * 1.609


def kilometers_to_miles():
    st.session_state["miles"] = st.session_state["km"] * 0.621


with col1:
    miles = st.number_input("Miles: ", key="miles", on_change=miles_to_kilometers)


with col2:
    km = st.number_input("Km:", key="km", on_change=kilometers_to_miles)

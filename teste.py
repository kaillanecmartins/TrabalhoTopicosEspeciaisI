import streamlit as st

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.title("Horror Movies")
st.button("Botão de teste")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Filmes de Terror')
st.text('Analisando dados sobre filmes de terror')

df = pd.read_csv('horror_movies.csv')
df.set_index('id', inplace=True)

# criando coluna de lista de generos pra cada filme
df['genres'] = df['genre_names'].str.split(', ')

df_horror = df[df['genres'].apply(lambda x: 'Horror' in x if isinstance(
    x, list) else False)]  # criando filtro apenas do genero horror

st.dataframe(df_horror)

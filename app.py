import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title('Filmes de Terror')
st.text('Analisando dados sobre filmes de terror')

# carregando dados
df = pd.read_csv('horror_movies.csv')
df.set_index('id', inplace=True)

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

df['year'] = df['release_date'].dt.year  # criando coluna de ano

df['profit'] = df['revenue'] - df['budget']  # criando coluna lucro

# criando coluna de lista de generos pra cada filme
df['genres'] = df['genre_names'].str.split(', ')

df_horror = df[df['genres'].apply(lambda x: 'Horror' in x if isinstance(
    x, list) else False)]  # criando filtro apenas do genero horror

cols_to_drop = ['poster_path', 'backdrop_path', 'overview',
                'tagline', 'adult', 'status', 'collection_name', 'collection', 'profit', 'budget', 'original_title', 'revenue']
df = df.drop(columns=cols_to_drop)  # deu erro pq eu ja havia rodado


# configurando streamlit

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# mostrando na tela
st.dataframe(df)

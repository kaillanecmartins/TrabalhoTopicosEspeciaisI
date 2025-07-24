import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

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
                'tagline', 'adult', 'status', 'collection_name', 'collection', 'profit', 'budget', 'original_title']
df = df.drop(columns=cols_to_drop)  # deu erro pq eu ja havia rodado

# df_filtered = df['original_language'].value_counts()

# fig_language = px.bar(df_filtered)

# ordenando dados por ano

df = df.sort_values('release_date')

# sidebar com ano

year = st.sidebar.selectbox("Ano", df['year'].unique())

# aplicando filtros por ano
df_filtered = df[df['year'] == year]

# mostrando na tela dados por ano
st.dataframe(df_filtered)

# organizando estrutura do dashboard
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)


fig_date = px.bar(df, x="year", y="popularity",
                  title="Faturamento por filme")

col1.plotly_chart(fig_date)

import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Análise de Filmes de Terror", layout="wide")

# Título do aplicativo
st.title("Análise de Filmes de Terror")

# Carregar os dados


@st.cache_data
def load_data():
    return pd.read_csv("horror_movies_limpo.csv")


df = load_data()

# Sidebar com filtros
st.sidebar.header("Filtros")
year_filter = st.sidebar.slider("Ano de lançamento",
                                min_value=int(
                                    df['release_date'].str[:4].min()),
                                max_value=int(
                                    df['release_date'].str[:4].max()),
                                value=(2010, 2022))

rating_filter = st.sidebar.slider("Avaliação mínima",
                                  min_value=0.0,
                                  max_value=10.0,
                                  value=6.0)

# Aplicar filtros (CORREÇÃO AQUI)
filtered_df = df[
    (df['release_date'].str[:4].astype(int) >= year_filter[0]) &
    (df['release_date'].str[:4].astype(int) <= year_filter[1]) &
    (df['vote_average'] >= rating_filter)
].copy()

# Mostrar estatísticas básicas
st.header("Estatísticas Básicas")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Filmes", len(filtered_df))
col2.metric("Avaliação Média", f"{filtered_df['vote_average'].mean():.1f}")
col3.metric("Duração Média", f"{filtered_df['runtime'].mean():.0f} min")

# Tabela com os filmes mais populares
st.header("Filmes Mais Populares")
top_movies = filtered_df.sort_values('popularity', ascending=False).head(10)[
    ['title', 'release_date', 'vote_average', 'popularity', 'genre_names']
]
st.dataframe(top_movies)

# Análise de gêneros
st.header("Distribuição de Gêneros")
genre_counts = filtered_df['genre_names'].str.split(
    ', ', expand=True).stack().value_counts()
st.bar_chart(genre_counts.head(10))

# Análise de lucratividade (para filmes com dados disponíveis)
if 'profit' in filtered_df.columns:
    st.header("Filmes Mais Lucrativos")
    profitable_movies = filtered_df.dropna(subset=['profit']).sort_values('profit', ascending=False).head(5)[
        ['title', 'budget', 'revenue', 'profit']
    ]
    st.dataframe(profitable_movies)

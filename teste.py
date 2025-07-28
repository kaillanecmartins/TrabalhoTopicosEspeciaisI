import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Importar estilo
# with open("styles.css") as f:
# st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Configuração da página
st.set_page_config(page_title="Análise de Filmes de Terror",
                   page_icon='💀', layout="wide")

# Título do aplicativo
st.title("Análise Completa de Filmes de Terror")

# Carregar os dados


@st.cache_data
def load_data():
    df = pd.read_csv("horror_movies_limpo.csv")
    df['release_year'] = pd.to_datetime(df['release_date']).dt.year
    df['profit_margin'] = (df['profit'] / df['revenue']) * \
        100 if 'profit' in df.columns and 'revenue' in df.columns else None
    return df


df = load_data()

st.sidebar.markdown("💀 **HORROR MOVIES**")
st.sidebar.markdown("---")

# Sidebar com filtros
st.sidebar.header("Filtros")
year_range = st.sidebar.slider(
    "Ano de lançamento",
    min_value=int(df['release_year'].min()),
    max_value=int(df['release_year'].max()),
    value=(2010, 2022)
)

rating_filter = st.sidebar.slider(
    "Avaliação mínima",
    min_value=0.0,
    max_value=10.0,
    value=6.0,
    step=0.1
)

genre_options = [
    'Todos'] + sorted(df['genre_names'].str.split(', ').explode().unique().tolist())
selected_genre = st.sidebar.selectbox("Gênero", genre_options)

# Aplicar filtros
filtered_df = df[
    (df['release_year'] >= year_range[0]) &
    (df['release_year'] <= year_range[1]) &
    (df['vote_average'] >= rating_filter)
]

if selected_genre != 'Todos':
    filtered_df = filtered_df[filtered_df['genre_names'].str.contains(
        selected_genre, na=False)]

# Seção 1: Métricas Principais
st.header("Métricas Principais")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Filmes", len(filtered_df))
col2.metric("Avaliação Média", f"{filtered_df['vote_average'].mean():.1f}")
col3.metric("Duração Média", f"{filtered_df['runtime'].mean():.0f} min")
if 'profit' in filtered_df.columns:
    col4.metric(
        "Lucro Médio", f"${filtered_df['profit'].mean()/1e6:.1f}M" if not filtered_df['profit'].isna().all() else "N/A")

# Seção 2: Distribuição e Relacionamentos
st.header("Distribuição e Relacionamentos")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Distribuição de Avaliações")
    fig = px.histogram(filtered_df, x='vote_average', nbins=20,
                       labels={'vote_average': 'Avaliação Média'}, color_discrete_sequence=['#990000'])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Duração vs Avaliação")
    fig = px.scatter(filtered_df, x='runtime', y='vote_average',
                     hover_data=['title'],
                     labels={'runtime': 'Duração (min)', 'vote_average': 'Avaliação'}, color_discrete_sequence=['#990000'])
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
# Seção 3: Análise Temporal
st.header("Evolução Temporal")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Lançamentos por Ano")
    movies_per_year = filtered_df['release_year'].value_counts().sort_index()
    fig = px.line(movies_per_year, labels={
                  'index': 'Ano', 'value': 'Número de Filmes'}, color_discrete_sequence=['#990000'])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Avaliação Média por Ano")
    yearly_ratings = filtered_df.groupby(
        'release_year')['vote_average'].mean().reset_index()
    fig = px.line(yearly_ratings, x='release_year', y='vote_average',
                  labels={'release_year': 'Ano', 'vote_average': 'Avaliação Média'}, color_discrete_sequence=['#990000'])
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Seção 4: Gêneros
st.header("Análise de Gêneros")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Gêneros Mais Comuns")
    genre_counts = filtered_df['genre_names'].str.split(
        ', ').explode().value_counts().head(10)
    fig = px.bar(genre_counts, orientation='h',
                 labels={'index': 'Gênero', 'value': 'Contagem'}, color_discrete_sequence=['#990000'])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Duração Média por Gênero")
    genre_runtime = filtered_df.explode('genre_names').groupby(
        'genre_names')['runtime'].mean().sort_values(ascending=False).head(10)
    fig = px.bar(genre_runtime, orientation='h',
                 labels={'index': 'Gênero', 'value': 'Duração Média (min)'}, color_discrete_sequence=['#990000'])
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Seção 5: Análise Financeira (se disponível)
if 'profit' in filtered_df.columns and not filtered_df['profit'].isna().all():
    st.header("Performance Financeira")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Orçamento vs Receita")
        fig = px.scatter(filtered_df.dropna(subset=['budget', 'revenue']),
                         x='budget', y='revenue', color='vote_average',
                         hover_data=['title'],
                         labels={'budget': 'Orçamento', 'revenue': 'Receita'}, color_continuous_scale=['#FFCCCB', '#FF6666', '#FF0000', '#990000'])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Margem de Lucro por Ano")
        yearly_profit = filtered_df.dropna(subset=['profit_margin']).groupby(
            'release_year')['profit_margin'].mean().reset_index()
        fig = px.line(yearly_profit, x='release_year', y='profit_margin',
                      labels={'release_year': 'Ano', 'profit_margin': 'Margem de Lucro (%)'}, color_discrete_sequence=['#990000'])
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Filmes por Lucro")
    profitable_movies = filtered_df.dropna(subset=['profit']).sort_values('profit', ascending=False).head(5)[
        ['title', 'release_year', 'budget', 'revenue', 'profit', 'profit_margin']
    ]
    st.dataframe(profitable_movies.style.format({
        'budget': '${:,.0f}',
        'revenue': '${:,.0f}',
        'profit': '${:,.0f}',
        'profit_margin': '{:.1f}%'
    }), height=210)

st.markdown("---")
# Seção 6: Tabelas de Destaque
st.header("Filmes em Destaque")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Mais Populares")
    top_movies = filtered_df.sort_values('popularity', ascending=False).head(5)[
        ['title', 'release_year', 'popularity', 'genre_names']
    ]
    st.dataframe(top_movies, height=210)

with col2:
    st.subheader("Melhores Avaliados")
    top_rated = filtered_df.sort_values('vote_average', ascending=False).head(5)[
        ['title', 'release_year', 'vote_average', 'genre_names']
    ]
    st.dataframe(top_rated, height=210)

# Rodapé
st.markdown("---")
st.caption(
    "Dashboard criado para análise de filmes de terror, para a disciplina de Tópicos Especiais I")

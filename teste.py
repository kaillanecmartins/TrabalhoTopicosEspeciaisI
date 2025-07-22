import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Teste Dashboard!')
st.text('Testando estilos com Streamlit')

data = {
    'Nome': ['Fran', 'Kat', 'Kauan'],
    'Idade': ['21', '23', '22'],
    'Salário': [3100, 2000, 1000]
}

df = pd.DataFrame(data)
st.dataframe(df)

fig, ax = plt.subplots()
ax.bar(df['Nome'], df['Salário'])
st.pyplot(fig)

if st.button('Clique Aqui'):
    st.write('Botão clicado vez!')

idade = st.slider('Selecione sua idade', 0, 100, 25)
st.write(f'Idade selecionada: {idade}')

opcao = st.selectbox(
    'Escolha um departamento:',
    ['TI', 'Administrativo', 'Vendas']
)

st.write(f'Departamento selecionado: {opcao}')

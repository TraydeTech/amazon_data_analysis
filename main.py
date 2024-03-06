# pip install streamlit pandas matplotlib seaborn
# pip install tabulate
import pandas as pd
import streamlit as st

# importar dados e fazer limpeza
df = pd.read_csv('amazon_prime_titles.csv')
df.columns = ['id', 'tipo', 'titulo',
              'diretor', 'elenco',
              'pais','data', 'ano',
              'classificacao','duration',
              'categoria', 'descricao']
df.drop(columns=['id', 'data'], inplace=True)
df['ano'] = df['ano'].astype('int')

paises = pd.unique(df['pais'])
paises_unicos = set()
for pais in paises:
    try:
        nomes = pais.split(', ')
        for nome in nomes:
            paises_unicos.add(nome)
    except:
        continue
df_paises = {}
for pais in paises_unicos:
    df_paises[pais] = df['pais'].str.contains(pais).sum()

# tipos = set()
# for tipo in df['tipo']:
#     tipos.add(tipo)
tipos = pd.unique(df['tipo'])

tab_df, tab_dash = st.tabs(['Dados', 'Dashboard'])

# adicionar filtros
with tab_df:
    tipos_selecionados = st.multiselect('Tipos', tipos)
    paises_selecionados = st.multiselect('País', paises_unicos)

    # filtrar tipo
    if len(tipos_selecionados) == 1:
        df = df.query(f'tipo == "{tipos_selecionados[0]}"')
    # filtrar pais
    if len(paises_selecionados) > 0:
        df = df.query("pais in @paises_selecionados")

    st.dataframe(df, hide_index=True, column_config={'ano': st.column_config.NumberColumn(format='%d')})

with tab_dash:
    df_agrupado_ano = pd.DataFrame(df.groupby(['ano']).size())
    df_agrupado_ano.column = ['quantidade']
    st.subheader('Titulos por ano')
    transparencia = st.slider('Transparencia', min_value=0.2, max_value=0.99, value=0.5, step=0.01)
    st.area_chart(df_agrupado_ano, use_container_width=True, color=(255, 255,255,transparencia))

with tab_dash:
    df_agrupado_tipo = pd.DataFrame(df.groupby(['tipo']).size())
    df_agrupado_ano.column = ['quantidade']
    st.subheader('Categorias')
    st.bar_chart(df_agrupado_tipo, use_container_width=True)


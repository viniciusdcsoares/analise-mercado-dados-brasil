# %% [1] Importando os pacotes e carregando os dados, etc
# Importando pacotes
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly as pt
import plotly.express as px
import plotly.graph_objects as go

# Carregando dados
from funcoes.funcoes import TratamentoDados

tratador = TratamentoDados()

df_migracao, salarios = tratador.retornar_migracao()

# %% Título, e settings

st.markdown("""
    <div style="text-align: center;">
        <h1> Gráficos da Análise Regional </h1>
""", unsafe_allow_html=True)

st.markdown("""

""")

gradientes = {
    'Rosa': 'PuRd',       # Cores vermelhas
    'Laranja': 'Oranges', # Cores laranja
    'Tomate': 'Reds',     # Cores tomate
    'Verde': 'Greens',    # Cores verdes
    'Azul': 'Blues',      # Cores azuis
    'Cinza': 'Greys'      # Cores cinzas
}

# Sidebar para escolha da cor
with st.sidebar.expander("Escolha as cores para os gráficos 🎨", expanded=True):
    cor_nome = st.selectbox('Escolha uma cor de preferência:',
                           ['Rosa', 'Laranja', 'Tomate', 'Verde', 'Azul', 'Cinza'])
    cor_gradiente = gradientes[cor_nome]

# Templates carregados - Forçando o uso do template correto da sessão
if "template_graph" in st.session_state and st.session_state.template_graph is not None:
    template_graph = st.session_state.template_graph
else:
    template_graph = "black"  # Default para tema escuro
    
if "template_plotly" in st.session_state and st.session_state.template_plotly is not None:
    template_plotly = st.session_state.template_plotly
else:
    template_plotly = "plotly_dark"  # Default para tema escuro
    
if "template_graph_texto" in st.session_state and st.session_state.template_graph_texto is not None:
    template_graph_texto = st.session_state.template_graph_texto
else:
    template_graph_texto = "white"  # Default para tema escuro

if "template_plotly_mapa" in st.session_state and st.session_state.template_plotly_mapa is not None:
    template_plotly_mapa = st.session_state.template_plotly_mapa
else:
    template_plotly_mapa = "plotly_dark"  # Default para tema escuro

# Debug das variáveis de tema    
st.sidebar.markdown("### Configurações de tema")
st.sidebar.write(f"Tema Plotly: {template_plotly}")
st.sidebar.write(f"Tema Plotly mapa: {template_plotly_mapa}")
st.sidebar.write(f"Tema Graph: {template_graph}")
st.sidebar.write(f"Tema Texto: {template_graph_texto}")

if template_graph == "white":
    letras_sns = "black"

else:
    letras_sns = "white"

# %% Grafico 1 de salario:
    
fig = px.choropleth(
    salarios,
    geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
    locations="Sigla onde mora",  
    featureidkey="properties.sigla",  
    color='Salarios',
    scope='asia', # Necessario para nao "puxar" o mapa da america do sul inteiro
    color_continuous_scale=cor_gradiente#,
    #title=f'Quantidade de profissionais que migraram de f{va_estado}'
)

fig.update_layout(
        coloraxis_colorbar=dict(title="Contagem"),
        geo=dict(scope="asia" # Necessario para nao "puxar" o mapa da america do sul
        ),
    )
    
    # "visible" impede de ampliar o mapa e ver a asia
    # e fitbounds garante que apenas os locais com dados aparecerão
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(width=1000, height=700, 
                       template=template_plotly_mapa,
                       paper_bgcolor=template_graph,
                       plot_bgcolor=template_graph,
                       coloraxis_colorbar=dict(
                           tickfont=dict(color=template_graph_texto)  # Cor dos números na barra de cores
                           #titlefont=dict(color=template_graph_texto)  # Cor do título da barra de cores
                           ))

st.markdown(f"<h3 style='text-align: center'> 🤑 Mapa do Salário Médio por Região 💸 </h3>", unsafe_allow_html=True)
st.plotly_chart(fig)

# %% dicionario(s)

dic_uni2 = {
        "Região de Migração": (
        "A tabela revela a distribuição dos profissionais por região de origem e localização atual, mostrando uma forte concentração nas regiões mais desenvolvidas do Brasil. "
        "A região Sudeste destaca-se com a maior quantidade de profissionais, com 121 oriundos dessa região e 235 de outras. Isso sugere que o Sudeste é um polo central tanto "
        "para a origem quanto para a atual localização dos profissionais, atraindo um grande número de talentos de diversas partes do país. Além disso, o Sudeste é também a "
        "principal região de destino, com destaque para profissionais provenientes de Nordeste e Centro-Oeste.<br><br>"
        
        "O Nordeste tem uma distribuição mais equilibrada, com 29 profissionais oriundos da própria região e 135 de outras áreas. Isso demonstra uma migração considerável para o "
        "Nordeste, que pode ser explicada por fatores como o crescimento de setores e a busca por novas oportunidades nesse território. Já o Sul tem uma distribuição similar, "
        "com 81 profissionais atualmente na região e 58 oriundos de outros locais. A presença de profissionais do Centro-Oeste na região Sul também indica um movimento migratório, "
        "possivelmente em busca de melhores oportunidades de trabalho.<br><br>"
        
        "Por outro lado, as regiões Centro-Oeste e Norte mostram uma concentração maior de profissionais locais. O Centro-Oeste tem 22 profissionais em sua própria região e "
        "12 oriundos de outras áreas, enquanto o Norte tem 17 na região e 16 provenientes de outras. Essas duas regiões tendem a manter uma maior parte de sua força de trabalho "
        "local, com uma mobilidade migratória mais baixa. A região Exterior tem uma representação menor, com destaque para a presença de profissionais provenientes do Sudeste e "
        "Nordeste."
        ),
    }
            
# %% graficos

st.markdown("""
    <div style="text-align: center;">
        <h1> ✈️ Mapa de Calor das Migrações ✈️ </h1>
""", unsafe_allow_html=True)

if 'preguiça' == 'preguiça':
    tabela_migracao = pd.crosstab(df_migracao['Região de Origem'], df_migracao['Região Atual'])

    # Normalize the table to get proportions
    tabela_migracao_proporcional = tabela_migracao.div(tabela_migracao.sum(axis=1), axis=0)

    # Let the user choose between Proporção and Números Absolutos
    opcao_selecao = st.radio('Escolha a versão para visualização:', 
                             ('Proporção', 'Números Absolutos'))

    # Conditional logic to set the table to display based on the user choice
    if opcao_selecao == 'Proporção':
        tabela_exibicao = tabela_migracao_proporcional
        titulo_grafico = 'Região de Origem vs Região Atual (Proporção)'
        fmt = ".2f"  # Format for proportions
    else:
        tabela_exibicao = tabela_migracao
        titulo_grafico = 'Região de Origem vs Região Atual (Contagem)'
        fmt = "d"  # Format for absolute counts
    
    # Create the heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(tabela_exibicao, annot=True, cmap=cor_gradiente, fmt=fmt, ax=ax)
    
    # Customize labels and font sizes
    ax.set_title(titulo_grafico, fontsize=16, color=letras_sns)
    ax.set_xlabel('Região Atual', fontsize=12, color=letras_sns)
    ax.set_ylabel('Região de Origem', fontsize=12, color=letras_sns)
    ax.tick_params(axis='x', colors=letras_sns)  # x-axis ticks color
    ax.tick_params(axis='y', colors=letras_sns)  # y-axis ticks color
    fig.patch.set_facecolor(template_graph)  # Set background color to black
    
    # Show the plot
    st.pyplot(fig)


    #st.subheader('Tabela de Migração entre Regiões')
    #st.write(tabela_migracao)
    st.markdown(dic_uni2['Região de Migração'], unsafe_allow_html=True)

estados_brasil = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 
                  'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

va_estado = st.selectbox('Escolha um estado para o gráfico:', (estados_brasil))

# Filtrando os dados por estado escolihdo
para_estado = df_migracao[df_migracao["Sigla onde mora"] == va_estado]
do_estado = df_migracao[df_migracao["Sigla de origem"] == va_estado]

contagem_para_estado = para_estado["Sigla de origem"].value_counts().reset_index()
contagem_do_estado = do_estado["Sigla onde mora"].value_counts().reset_index()

todos_estados_df = pd.DataFrame({'Sigla de origem': estados_brasil})
todos_estados_df["Sigla onde mora"] = todos_estados_df["Sigla de origem"]

#
contagem_completa_para_estado = pd.merge(todos_estados_df, contagem_para_estado, on="Sigla de origem", how="left")
contagem_completa_do_estado = pd.merge(todos_estados_df, contagem_do_estado, on="Sigla onde mora", how="left")

# Substituir na por 1 para plotagem
contagem_completa_para_estado['count'] = contagem_completa_para_estado['count'].fillna(0)
contagem_completa_do_estado['count'] = contagem_completa_do_estado['count'].fillna(0)


# Criar o gráfico de choropleth
fig1 = px.choropleth(
    contagem_completa_para_estado,
    geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
    locations="Sigla de origem",  
    featureidkey="properties.sigla",  
    color='count',
    scope='asia', # Necessario para nao "puxar" o mapa da america do sul inteiro
    color_continuous_scale=cor_gradiente#,
    #title=f'Quantidade de profissionais que migraram para {va_estado}'
)

fig2 = px.choropleth(
    contagem_completa_do_estado,
    geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
    locations="Sigla onde mora",  
    featureidkey="properties.sigla",  
    color='count',
    scope='asia', # Necessario para nao "puxar" o mapa da america do sul inteiro
    color_continuous_scale=cor_gradiente#,
    #title=f'Quantidade de profissionais que migraram de f{va_estado}'
)

for fig in [fig1, fig2]:
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Contagem",
            len=0.5,  # Reduzir o tamanho da barra de cores para 50% do padrão
            thickness=15,  # Reduzir a espessura da barra
            x=0.95,  # Posicionar mais à direita
            tickfont=dict(color=template_graph_texto, size=8)  # Fonte menor
        ),
        geo=dict(
            scope="asia",  # Necessario para nao "puxar" o mapa da america do sul
            projection_scale=5,  # Aumentar a escala do mapa
            center=dict(lat=-15, lon=-55),  # Centrar o mapa no Brasil
            lonaxis=dict(range=[-75, -30]),  # Ajustar longitude para focar mais no Brasil
            lataxis=dict(range=[-35, 5])  # Ajustar latitude para focar mais no Brasil
        ),
    )
    
    # "visible" impede de ampliar o mapa e ver a asia
    # e fitbounds garante que apenas os locais com dados aparecem
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        width=800, 
        height=800, 
        template=template_plotly_mapa,
        paper_bgcolor=template_graph,
        plot_bgcolor=template_graph,
        margin=dict(l=0, r=0, t=0, b=0)  # Reduzir margens para maximizar o espaço do mapa
    )

# Criar os gráficos lado a lado usando colunas do Streamlit
st.markdown(f"<h3 style='text-align: center'> ✈️ Mapas de Migração do Estado: {va_estado} ✈️ </h3>", unsafe_allow_html=True)

# Criando container com largura expandida
with st.container():
    # Criando duas colunas para exibir os gráficos lado a lado
    col1, col2 = st.columns(2)
    
    # Colocando os mapas lado a lado
    with col1:
        st.markdown(f"<h4 style='text-align: center'> 🛬 Migrações PARA {va_estado} </h4>", unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown(f"<h4 style='text-align: center'> 🛫 Migrações DE {va_estado} </h4>", unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)

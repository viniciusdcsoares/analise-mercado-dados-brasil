import streamlit as st
import os

# Configuração da página
st.set_page_config(
    page_title="Dashboard do Mercado de Dados Brasileiro",
    page_icon="🤓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Detecta o tema atual do Streamlit e configura o template do Plotly
tema_atual = "dark" if st.get_option("theme.base") == "dark" else "light"

# Tema dos gráficos baseados no tema do Streamlit
if tema_atual == "dark":
    # Para fundo preto/escuro
    st.session_state.template_graph = "black"
    st.session_state.template_plotly = "plotly_dark"  # Tema escuro do Plotly
    st.session_state.template_graph_texto = "white"
    st.session_state.template_plotly_mapa = "plotly_dark"
else:
    # Para fundo branco/claro
    st.session_state.template_graph = "white"
    st.session_state.template_plotly = "plotly_white"  # Tema claro do Plotly
    st.session_state.template_graph_texto = "black"
    st.session_state.template_plotly_mapa = "plotly_white"

# Força os valores padrão para o tema escuro
if "template_graph" not in st.session_state or st.session_state.template_graph is None:
    st.session_state.template_graph = "black"  # Tema escuro por padrão
if "template_plotly" not in st.session_state or st.session_state.template_plotly is None:
    st.session_state.template_plotly = "plotly_dark"  # Tema escuro por padrão
if "template_graph_texto" not in st.session_state or st.session_state.template_graph_texto is None:
    st.session_state.template_graph_texto = "white"  # Tema escuro por padrão
if "template_plotly_mapa" not in st.session_state or st.session_state.template_plotly_mapa is None:
    st.session_state.template_plotly_mapa = "plotly_dark"  # Tema escuro por padrão

# Definindo as páginas
paginas = {
    "": [
        st.Page("paginas/home.py", title="Página Inicial", icon="🤓", default=True)
    ],
    "Páginas Exploratórias": [
        st.Page("paginas/univariadas.py", title="Análise Geral das Variáveis", icon="📊"),
        st.Page("paginas/univariadas2.py", title="Análise Regional", icon="🗺️"),
        st.Page("paginas/bivariadas.py", title="Análise Bivariada", icon="🔄")
    ],
    "Predição de Salário 🤖": [
        st.Page("paginas/machine_learning.py", title="Descubra seu salário!", icon="🤖")
    ]
}

pg = st.navigation(paginas)
pg.run() 

import streamlit as st

# %% [3] Página principal
# %% Título

st.markdown("""
    <div style="text-align: center;">
        <h1> 👩‍💻 O Perfil do Profissional de Dados no Brasil 🎲 </h1>
""", unsafe_allow_html=True)


###############Opções de Preferencia##########

# %% opções de preferencia 

st.markdown("""
    <div style="text-align: center;">
        <h1>Opções de Preferência 🎨</h1>
""", unsafe_allow_html=True)

st.markdown("""
Antes de tudo, temos uma ótima notícia: Você tem a possibilidade de escolher alguns detalhes para personalizar os 
gráficos gerados. 📊

Nada muito complicado, apenas um toque para tornar a experiência ainda mais sua! 😊

À esquerda da página, escolha a cor que mais agrada e aproveite os gráficos de forma personalizada! 🌈
""")
st.markdown("""
    <div style="text-align: center;">
        <h2 >🌓Alterar tema 🌓</h2>
""", unsafe_allow_html=True)
st.markdown("""
Para trocar entre tema claro e escuro:
1. Clique no menu "⋮" (canto superior direito)
2. Selecione "Settings" (Configurações)
3. Escolha "Light" ou "Dark" em "Theme"
""")

st.markdown("---")

# %% Descrição Geral da Base

st.markdown("""
    <div style="text-align: center;">
        <h1>Descrição Geral da Base 🔍</h1>
""", unsafe_allow_html=True)

st.markdown("""
Antes de mais nada vamos lhe fornecer uma visão 
geral dos dados, para que assim você possa melhor 
percorrer pelas secções a seguir. 🚀

A base se refere ao **Perfil do Profissional de Dados 
no Brasil**. Sendo composta por de 5 293 
indivíduos e 400 variáveis, mas, devido ao tempo, 
nossas análises referem-se apenas a um subconjunto 
dessas variáveis. 

Esse subconjunto incluem as seguintes variáveis 
presentes na base:

- *Área de Formação*: A área de formação acadêmica desses profissionais.
- *Cargo*: Cargo atual ocupado pelos profissionais de dados.
- *Etnia*: Cor/raça/etnia dos participantes.
- *Escolaridade*: Nível de escolaridade dos profissionais.
- *Estado onde Mora*: Estado em que o profissional reside atualmente.
- *Experiência*: O tempo de experiência na área de dados.
- *Faixa Salarial*: Divisão da faixa salarial dos profissionais.
- *Gênero*: Distribuição de gênero entre os profissionais.
- *Idade*: Faixa etária dos profissionais de dados.
- *Nível*: Nível de experiência ou senioridade dentro da área de dados.
- *Região de Origem*: Local onde o profissional nasceu ou cresceu.

Essas variáveis ajudam a criar um panorama detalhado 
sobre a formação e o perfil dos profissionais de 
dados no Brasil, permitindo análises mais 
profundas e insights valiosos sobre esse setor. 💡


""")

st.markdown("---")

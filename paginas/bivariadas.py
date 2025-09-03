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
link = 'https://raw.githubusercontent.com/ricardorocha86/Datasets/refs/heads/master/State_of_data_BR_2023_Kaggle%20-%20df_survey_2023.csv'
df_o = pd.read_csv(link)
df = df_o.copy()



# Renomeando alguams colunas
df.rename(columns={"('P1_a ', 'Idade')": 'Idade', "('P1_a_1 ', 'Faixa idade')": "Faixa de Idade",
                   "('P1_c ', 'Cor/raca/etnia')": 'Etnia',
                   "('P1_b ', 'Genero')": 'Gênero', "('P2_f ', 'Cargo Atual')": 'Cargo',
                   "('P2_h ', 'Faixa salarial')": 'Faixa Salarial', "('P2_g ', 'Nivel')": 'Nível',
                   "('P1_l ', 'Nivel de Ensino')": 'Escolaridade', "('P1_m ', 'Área de Formação')": 'Área',
                   "('P2_i ', 'Quanto tempo de experiência na área de dados você tem?')": 'Experiência'
                   }, inplace=True)
df['Contagem'] = 1

# %% Título, e settings

st.markdown("""
    <div style="text-align: center;">
        <h1>Análise Bivariada 🌐</h1>
""", unsafe_allow_html=True)

st.markdown("""

 Nesta seção, você poderá visualizar 
gráficos que propomos para analisar a 
relação entre duas variáveis da base. 

Divirta-se ✨

""")


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

# Debug das variáveis de tema    
st.sidebar.markdown("### Configurações de tema")
st.sidebar.write(f"Tema Plotly: {template_plotly}")
st.sidebar.write(f"Tema Graph: {template_graph}")
st.sidebar.write(f"Tema Texto: {template_graph_texto}")

gradientes = {
    'Rosa': 'PuRd',       # Cores vermelhas
    'Laranja': 'Oranges', # Cores laranja
    'Tomate': 'Reds',     # Cores tomate
    'Verde': 'Greens',    # Cores verdes
    'Azul': 'Blues',      # Cores azuis
    'Cinza': 'Greys'      # Cores cinzas
}

with st.sidebar.expander("Escolha as cores para os gráficos 🎨", expanded=True):
    cor_nome = st.selectbox('Escolha um gradiente de cor de preferência:',
                           ['Rosa', 'Laranja', 'Tomate', 'Verde', 'Azul', 'Cinza'])
    cor_gradiente = gradientes[cor_nome]
    cor = st.color_picker("Escolha uma cor!", "#00f900")

    


# %% dicionarios 

dic_bivariada1 = {"Cargo": ("Devido a similaridade entre algumas profissões, ou por conveniência devido à baixa frequência de observações,agrupamos as profissões de "
                            "sumarizamos seus originais valores na tabela a baixo"),
                  "Idade": (""),
                  "Etnia": (""),
                  "Gênero": (""),
                  "Faixa Salarial": (""),
                  "Escolaridade": (""),
                  "Nível": (""),
                  "Experiência": (""),}

# %% Gráficos

variavel_selecionada = st.selectbox('Escolha um cruzamento de variáveis para análise:',
                                    sorted(['Etnia X Idade', 'Etnia X Faixa Salarial', 'Faixa Salarial X Idade','Experiência X Faixa Salarial', #'Cargo X Nível', 'Cargo X Nível X Salário'
                                            ]))


if variavel_selecionada == 'Etnia X Idade':
    
    # Calcular a média das idades por Etnia
    Idades_Etnia = df.groupby('Etnia')['Idade'].mean().sort_values(ascending=True).index

    # Criar o gráfico Boxplot
    fig = px.box(df, x="Etnia", y="Idade",
                 labels={"Etnia": "Etnia", "Idade": "Idades"},
                 title="Boxplot das Idades por Etnia",
                 category_orders={"Etnia": Idades_Etnia})

    fig.update_traces(marker=dict(color=cor))

    fig.update_layout(title_x=0.5)

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)

elif variavel_selecionada == 'Etnia X Faixa Salarial':

    faixas_salariais = {
        "Menos de R$ 1.000/mês": 500,
        "de R$ 1.001/mês a R$ 2.000/mês": 1500,
        "de R$ 2.001/mês a R$ 3.000/mês": 2500,
        "de R$ 3.001/mês a R$ 4.000/mês": 3500,
        "de R$ 4.001/mês a R$ 6.000/mês": 5000,
        "de R$ 6.001/mês a R$ 8.000/mês": 7000,
        "de R$ 8.001/mês a R$ 12.000/mês": 10000,
        "de R$ 12.001/mês a R$ 16.000/mês": 14000,
        "de R$ 16.001/mês a R$ 20.000/mês": 18000,
        "de R$ 20.001/mês a R$ 25.000/mês": 22500,
        "de R$ 25.001/mês a R$ 30.000/mês": 27500,
        "de R$ 30.001/mês a R$ 40.000/mês": 35000,
        "Acima de R$ 40.001/mês": 45000
    }

    df['Faixa Salarial Numérica'] = df['Faixa Salarial'].map(faixas_salariais)

    # Calcular a média dos salários por Etnia
    salario_etnia = df.groupby('Etnia')['Faixa Salarial Numérica'].mean().sort_values(ascending=True).index

    # Criar o gráfico Boxplot para Salários X Etnia
    fig = px.box(df, x="Etnia", y="Faixa Salarial Numérica",
                 labels={"Etnia": "Etnia", "Faixa Salarial Numérica": "Faixa Salarial"},
                 title="Boxplot da Faixa Salarial Médios por Etnia",
                 category_orders={"Etnia": salario_etnia})

    fig.update_traces(marker=dict(color=cor))

    fig.update_layout(title_x=0.5)

    st.plotly_chart(fig)

elif variavel_selecionada == 'Faixa Salarial X Idade':
    # Criar o gráfico Boxplot de Idades por Faixa Salarial, com a ordenação por 'salarios'
    fig = px.box(df.sort_values(by='Faixa Salarial'), x='Faixa Salarial', y="Idade",
                 labels={'Faixa salarial': "Faixa Salarial", "Idade": "Idade"},
                 title="Boxplot das Idades por Faixa Salarial", color="Faixa Salarial")

    # Alterar a cor para uma cor específica
    fig.update_traces(marker=dict(color=cor))  # cor deve ser um valor válido como 'red', 'blue', ou código hexadecimal como '#FF5733'

    # Ajustar o layout do gráfico
    fig.update_layout(title_x=0.5)

    # Ajustar a rotação dos rótulos do eixo X
    fig.update_xaxes(tickangle=90)

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)


elif variavel_selecionada == 'Experiência X Faixa Salarial':
    
    ordem_faixas = [
    "Menos de R$ 1.000/mês",
    "de R$ 1.001/mês a R$ 2.000/mês",
    "de R$ 2.001/mês a R$ 3.000/mês",
    "de R$ 3.001/mês a R$ 4.000/mês",
    "de R$ 4.001/mês a R$ 6.000/mês",
    "de R$ 6.001/mês a R$ 8.000/mês",
    "de R$ 8.001/mês a R$ 12.000/mês",
    "de R$ 12.001/mês a R$ 16.000/mês",
    "de R$ 16.001/mês a R$ 20.000/mês",
    "de R$ 20.001/mês a R$ 25.000/mês",
    "de R$ 25.001/mês a R$ 30.000/mês",
    "de R$ 30.001/mês a R$ 40.000/mês",
    "Acima de R$ 40.001/mês"
    ]
    
    ordem_exp = [
    "Sem experiência",
    "Menos de 1 ano",
    "de 1 a 2 anos",
    "de 3 a 4 anos",
    "de 4 a 6 anos",
    "de 7 a 10 anos",
    "Mais de 10 anos"
    ]
    # Adicionar um radio button para o usuário escolher entre "Contagem" ou "Normalizada"
    opcao_selecao = st.radio('Escolha a versão para visualização:', 
                             ('Contagem', 'Normalizada'))

# Definir a tabela a ser exibida com base na seleção
    tabela_exp_faixa = pd.crosstab(df['Faixa Salarial'], df['Experiência'])
    tabela_exp_faixa = tabela_exp_faixa.reindex(index=ordem_faixas, columns=ordem_exp, fill_value=0)

# Calcular a versão normalizada
    tabela_exp_faixa_p = tabela_exp_faixa.div(tabela_exp_faixa.sum(axis=1), axis=0)

# Condicional para escolher qual versão mostrar
    if opcao_selecao == 'Contagem':
        tabela_exibicao = tabela_exp_faixa
        titulo_grafico = 'Experiência vs Faixa Salarial (Contagem)'
        fmt = "d"  # Formato de contagem
    else:
        tabela_exibicao = tabela_exp_faixa_p
        titulo_grafico = 'Experiência vs Faixa Salarial (Normalizado)'
        fmt = ".3f"  # Formato normalizado com 3 casas decimais

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(tabela_exibicao, annot=True, cmap=cor_gradiente, fmt=fmt, ax=ax)
    plt.title(titulo_grafico, fontsize=16)
    plt.xlabel('Experiência', fontsize=12)
    plt.ylabel('Faixa Salarial', fontsize=12)
    st.pyplot(fig)

elif variavel_selecionada == 'Cargo X Nível':
    
    def faixa_para_valor(faixa):
        try:
            # Extrair os valores mínimo e máximo de cada faixa
            valores = faixa.split(" a ")
            min_valor = int(valores[0].replace("de R$", "").replace("mês", "").replace(",", "").strip())
            max_valor = int(valores[1].replace("R$", "").replace("mês", "").replace(",", "").strip())
            
            # Retornar a média da faixa salarial
            return (min_valor + max_valor) / 2
        except Exception as e:
            return None  # Caso o formato não seja esperado, retorna None

    # Aplicar a função para converter 'Faixa Salarial' para valores numéricos
    df['Faixa Salarial Valor'] = df['Faixa Salarial'].apply(faixa_para_valor)

    nivel_agrupado = df.groupby(["Cargo", "Nível"], as_index=False)["Faixa Salarial Valor"].mean()

    # Ordenar os cargos com base na média dos salários
    salarios_cargo = df.groupby('Cargo')['Faixa Salarial Valor'].mean().sort_values(ascending=True).index

    # Criar o gráfico de barras
    fig = px.bar(nivel_agrupado, x="Cargo", y="Faixa Salarial Valor",
                 labels={"Cargo": "Cargos", "Faixa Salarial Valor": "Faixa Salarial", "Nível": "Nível"},
                 title="Salários Médios por Cargos e Nível de Senioridade",
                 color="Nível", barmode="group",
                 category_orders={'Cargo': salarios_cargo})

    # Ajustar o layout do gráfico
    fig.update_layout(title_x=0.5)

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)
   
    
   
elif variavel_selecionada == 'Cargo X Nível X Salário':
    
    nivel_agrupado = df.groupby(["Cargo", "Nível"], as_index=False)["Faixa Salarial"].mean()


    salarios_cargo = df.groupby('Cargo')['Faixa Salarial'].mean().sort_values(ascending=True).index


    fig = px.bar(nivel_agrupado, x="Cargo", y="Faixa Salarial",
             labels={"Cargo": "Cargos", "Faixa Salarial": "Salários", "Nível": "Nível"},
             title="Faixa Salarial Média por Cargos e Nível de Senioridade",
             color="Nível", barmode="group",
             category_orders={'Cargo': salarios_cargo})

    fig.update_layout(title_x=0.5)

    st.plotly_chart(fig)
    
    nivel_agrupado = df.groupby(["Cargo", "Nível"], as_index=False)["salarios"].mean()


    salarios_cargo = df.groupby('Cargo')['salarios'].mean().sort_values(ascending=True).index


    fig = px.bar(nivel_agrupado, x="Cargo", y="salarios",
             labels={"Cargo": "Cargos", "salarios": "Salários", "Nível": "Nível"},
             title="Salários Médios por Cargos e Nível de Senioridade",
             color="Nível", barmode="group",
             category_orders={'Cargo': salarios_cargo})

    fig.update_layout(title_x=0.5)

    st.plotly_chart(fig)
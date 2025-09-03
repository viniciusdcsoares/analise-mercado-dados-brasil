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

from funcoes.funcoes import TratamentoDados
from funcoes.funcoes import grafico_barras_ordenado

tratador = TratamentoDados()

df = tratador.retornar_dados()

# %% Título, e settings

st.markdown("""
    <div style="text-align: center;">
        <h1> Análise Geral das Viaráveis </h1>
""", unsafe_allow_html=True)

st.markdown("""
Nessa secção você pode visualizar alguns 
gráficos, que propomos para a análise 
individual das variáveis da base. Além disso, 
fornecemos também insights acerca dos 
gráficos gerados, para que você não 
precise ter esse trabalho. 🧠

Tudo o que vai precisar fazer é selecionar a 
variável desejada e se divertir com o processo!🙃
""")

# Sidebar para escolha da cor
with st.sidebar.expander("🎨 Escolha as cores dos gráficos 🎨", expanded=True):
    cor = st.color_picker("Escolha uma cor!", "#00f900")
    

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

# %% Gráficos de distribuição   

st.markdown("""
    <div style="text-align: center;">
        <h1>📶 Gráficos da Distribuição de Algumas Variáveis 📶</h1>
""", unsafe_allow_html=True)

variavel_distribuicao = st.selectbox('Escolha uma variável para análise:',
                                    sorted(['Idade', 'Faixa Salarial', 'Experiência']))

st.markdown(f"<h3 style='text-align: center'>  Distribuição de {variavel_distribuicao}  </h3>", unsafe_allow_html=True)
    
# %%% tratamento para distribuicao

ordem_faixas_resumida = [
            "< 1k", "1k < 2k", "2k < 3k", "3k < 4k", "4k < 6k", "6k < 8k",
            "8k < 12k", "12k < 16k", "16k < 20k", "20k < 25k", "25k < 30k",
            "30k < 40k", "40k <"
        ]
        
ordem_experiencia = [
            "Sem experiência",
            "Menos de 1 ano",
            "de 1 a 2 anos",
            "de 3 a 4 anos",
            "de 4 a 6 anos",
            "de 7 a 10 anos",
            "Mais de 10 anos"
        ]

df['Faixa Salarial'].value_counts().index.tolist()


# %%% dicionarios de interpretação e etc

dic_distribuicao = {
    "Idade": (
        "A distribuição etária dos profissionais no mercado de dados no Brasil mostra uma predominância de jovens na faixa etária de 20 a 30 anos, que representam uma parcela "
        "significativa da base. A maior concentração está na faixa de 26 anos, com 323 profissionais (6.1%), seguida pela faixa de 27 anos, com 374 profissionais (7.1%), "
        "indicando uma forte presença de profissionais em início de carreira ou em transição para posições mais consolidadas. As faixas etárias mais altas, como 50 anos ou mais, "
        "têm uma representatividade bem menor, com apenas 1 a 2 profissionais em cada faixa etária acima de 60 anos, evidenciando uma baixa participação de profissionais mais "
        "velhos no setor. Esse cenário reflete um mercado de dados mais jovem, com a maioria dos profissionais em fases iniciais ou intermediárias de sua carreira."
        ),
    "Faixa Salarial": (
        "A distribuição salarial no mercado de dados no Brasil revela uma clara concentração nas faixas intermediárias, com destaque para o intervalo de 8 001 a 12 000 reais, "
        "com 1 026 profissionais, seguido por 4 001 a 6 000 reais, com 745 profissionais, e 12 001 a 16 000 reais, com 650 profissionais. As faixas salariais mais altas, como "
        "16 001 a 20 000 reais (328 profissionais) e Acima de 40 000  reais (72 profissionais), têm uma presença mais modesta, sugerindo que apenas uma pequena parcela dos "
        "profissionais alcançam esses valores. Já as faixas mais baixas, como Menos de 1 000 reais (30 profissionais), têm uma representação reduzida, indicando que a maioria "
        "dos profissionais está concentrada nas faixas intermediárias ou mais altas."
        ),
    "Experiência": (
        "A experiência também é um fator importante nesse mercado. Cerca de 40% dos profissionais (aproximadamente 2.000 indivíduos) possuem entre 1 e 4 anos de experiência, "
        "o que mostra que a maior parte da base está em fase de formação ou em transição para cargos mais seniores. Esse dado sugere uma alta rotatividade e a constante entrada "
        "de novos profissionais no mercado de dados.<br><br>"
        
        "Outro dado relevante é que 3% (aproximadamente 160 profissionais) são iniciantes, com nenhuma experiência formal na área, mas provavelmente com potencial para crescer "
        "à medida que o mercado se expande e a demanda por dados aumenta.<br><br>"
        
        "Entre os profissionais mais experientes, há um equilíbrio entre as faixas de 4 a 6 anos e 7 a 10 anos de experiência, com um número ligeiramente maior de profissionais "
        "na faixa de 4 a 6 anos. Isso indica uma estabilização na distribuição de experiência, com uma concentração significativa de profissionais já consolidados entre 4 e 10 anos "
        "de atuação no setor de dados."
        ),
    }

dic_graficos = {"Faixa Salarial": ordem_faixas_resumida, "Experiência": ordem_experiencia}
# %% Distribuicao




if variavel_distribuicao == "Idade":
    # figura
    fig = px.histogram(
        df,
        x=variavel_distribuicao,
        color_discrete_sequence=[cor]
    )
    
    # layout
    fig.update_layout(
        template=template_plotly,
        xaxis_title=variavel_distribuicao,
        yaxis_title="Frequência",
        bargap=0.2,    
        paper_bgcolor=template_graph,
        plot_bgcolor=template_graph,
        font=dict(color=template_graph_texto),  # Ensure all text is visible
        xaxis=dict(
            #titlefont=dict(color=template_graph_texto),
            tickfont=dict(color=template_graph_texto)
            ),
        yaxis=dict(
            #titlefont=dict(color=template_graph_texto),
            tickfont=dict(color=template_graph_texto)
            )
        )
    
    st.plotly_chart(fig)

    st.markdown(f"<h3 style='text-align: center'>{variavel_distribuicao}</h3>", unsafe_allow_html=True)

    st.markdown(dic_distribuicao[variavel_distribuicao], unsafe_allow_html=True)
    

else: 
    novo = df.groupby(variavel_distribuicao).size().reset_index(name='Contagem')
    novo['Porcentagem'] = (novo['Contagem'] / novo['Contagem'].sum()) * 100

    novo[variavel_distribuicao] = pd.Categorical(novo[variavel_distribuicao], categories=dic_graficos[variavel_distribuicao], ordered=True)
    novo.sort_values(by=variavel_distribuicao, inplace=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=novo[variavel_distribuicao],  # Categorical x-axis
        y=novo['Contagem'],                 # Bar heights
        text=[f'{p:.1f}%' for p in novo['Porcentagem']],  # Percentages as text
        textposition='outside',             # Position text above bars
        marker_color=cor,
        textfont=dict(color=template_graph_texto)         # Bar color
    ))
        
    # Layout settings
    fig.update_layout(
        template=template_plotly,
        xaxis_title=variavel_distribuicao,
        yaxis_title='Frequência',
        xaxis=dict(categoryorder='array', categoryarray=ordem_faixas_resumida,
                   #titlefont=dict(color=template_graph_texto),
                   tickfont=dict(color=template_graph_texto)),  # Enforce custom order
        yaxis=dict(range=[0, novo['Contagem'].max() * 1.1],
                   #titlefont=dict(color=template_graph_texto),
                   tickfont=dict(color=template_graph_texto)), # extendendo um pouco o limite de y
        paper_bgcolor=template_graph,  
        plot_bgcolor=template_graph)
    
    st.plotly_chart(fig)

    st.markdown(f"<h3 style='text-align: center'>{variavel_distribuicao}</h3>", unsafe_allow_html=True)

    st.markdown(dic_distribuicao[variavel_distribuicao], unsafe_allow_html=True)

# %% Outros graficos (pizza ou barras)

layout = [cor, template_graph_texto, template_graph, template_plotly]

st.markdown("""
    <div style="text-align: center;">
        <h1> Outros Gráficos </h1>
""", unsafe_allow_html=True)

grafico_escolhido = st.selectbox('Escolha o tipo de gráfico que você deseja!',
                                    ['📊 Barras 📊', '🍕 Pizza 🍕'])


# dicionario com as interepretações dos graficos de pizza
dic_texto = {
    "Etnia": (
        "A análise da etnia dos profissionais também revela um panorama interessante. "
        "A maioria dos indivíduos na base se identifica como branca, representando 65% (3.414) dos participantes. "
        "Em seguida, pardos e pretos somam 32% (1.668), o que representa menos da metade do número de indivíduos identificados como brancos. "
        "Pode-se, assim, afirmar que o mercado de Dados no Brasil está, de forma esmagadora, sendo 'dominado' por brancos.<br><br>"
        
        "Por outro lado, as etnias amarela e indígena têm uma presença mais modesta, representando apenas 3% (159) dos profissionais, "
        "o que pode refletir um padrão demográfico mais restrito, ainda em processo de inclusão em áreas mais tecnológicas."
    ),
    "Gênero": (
        "A distribuição de gênero no mercado de dados no Brasil é predominantemente masculina, com 75% (3.905 profissionais) "
        "se identificando como homens, enquanto 24% (1.293 profissionais) são mulheres. "
        "A presença de profissionais que se identificam com outro gênero é bastante pequena, representando apenas 1% (9 profissionais) da base. "
        "Isso indica uma disparidade significativa entre os gêneros, com a maioria dos cargos ainda sendo ocupada por homens."
    ),
    "Escolaridade": (
        "Em relação à escolaridade, a base de profissionais apresenta uma diversidade interessante. "
        "34% (1.818) dos indivíduos possuem pós-graduação, destacando o alto nível de especialização presente no mercado de dados. "
        "Esse número é similar ao de profissionais com graduação (também 34%, ou 1.798), mostrando que a formação superior continua sendo "
        "um pré-requisito essencial, tanto para cargos de análise quanto para cargos mais técnicos.<br><br>"
        
        "Por outro lado, 2% (105) dos profissionais não possuem graduação, uma porcentagem pequena, mas que pode indicar a presença de "
        "profissionais com trajetórias não convencionais ou autodidatas, especialmente em campos técnicos onde a experiência prática "
        "muitas vezes suplanta a formação acadêmica formal. Já os PhDs ou Doutores representam 4% (210) da base, o que reflete a presença "
        "de especialistas com um nível de formação avançado, muitas vezes voltados para pesquisas, desenvolvimento de novos métodos ou "
        "inovações na área de dados."
    ),
    "Nível": (
        "A distribuição dos níveis de experiência no mercado de dados no Brasil é bastante equilibrada, com *20% (1.046 profissionais)* "
        "em cargos *juniores*, **27% (1.419 profissionais)* em cargos *sêniores*, **26% (1.419 profissionais)* em cargos *plenos* e "
        "*27% (1.436 profissionais)* em cargos *NA*. O fato de haver uma quantidade equivalente de profissionais em cargos **plenos* e "
        "*sêniores* é surpreendente, indicando que a área de dados não só está em constante renovação, mas também mantém um bom equilíbrio "
        "entre profissionais com menos e mais experiência, refletindo uma estabilidade na estrutura de carreiras dentro do setor.<br><br>"
        
        "Além disso, a presença de 27% (1.436 profissionais) com valores faltantes (NA) é uma questão relevante, pois indica uma lacuna "
        "significativa nas informações sobre o nível de experiência de uma parte expressiva dos profissionais. Essa falta de dados claros "
        "prejudica a análise precisa do perfil do mercado, tornando difícil entender a real composição das carreiras no setor."
    ),
    "Cargo": (
        "Devido à similaridade entre algumas profissões, ou por conveniência devido à baixa frequência de observações, agrupamos as profissões "
        "em categorias conforme apresentado na tabela após o texto. "
        "Quase 50% (1 647) dos profissionais dessa base ocupam o cargo de Analista de Dados, o que mostra como essa profissão tem se destacado "
        "e se tornado essencial à medida que mais empresas investem em dados para tomar decisões estratégicas.<br><br>"
        
        "Por outro lado, Estatísticos e Economistas são as profissões com a menor representatividade, somando menos de 1% da base (26) – uma evidência "
        "de que o mercado tem se concentrado mais em habilidades voltadas para a prática e o uso de dados no dia a dia das empresas.<br><br>"
        
        "É interessante notar que, juntos, os cargos de Engenheiro de Dados e Cientista de Dados quase chegam ao número de Analistas de Dados (1 605). "
        "Essa tríade – Analistas, Engenheiros e Cientistas de Dados – responde por mais de 80% da base (3 248), o que revela uma clara tendência: "
        "o mercado está cada vez mais centrado em profissionais que dominam o universo dos dados, seja para analisá-los, estruturá-los "
        "ou transformá-los em insights valiosos."
    )
}



va_outros = st.selectbox('Escolha uma variável para o gráfico:',
                                    sorted(['Etnia', 'Gênero', 'Escolaridade', 'Nível', 'Cargo']))

if grafico_escolhido == '📊 Barras 📊':
    st.markdown("""
        <div style="text-align: center;">
            <h1>Gráficos de barras! 📊 </h1>
    """, unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center'> 📊 Gráfico para {va_outros} 📊 </h3>", unsafe_allow_html=True)
elif grafico_escolhido == '🍕 Pizza 🍕':
    st.markdown("""
        <div style="text-align: center;">
            <h1>Gráficos de pizza!😋🍕</h1>
    """, unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center'> 🍕 Gráfico para {va_outros} 🍕 </h3>", unsafe_allow_html=True)

if va_outros == 'Cargo':
    
    agrupar_cargo = st.selectbox('Você deseja agrupar os cargos?',
                                        ['Não', 'Sim'])
    
    if agrupar_cargo == 'Não':
        if grafico_escolhido == '🍕 Pizza 🍕': 
            fig = px.pie(df, values="Contagem", names=va_outros)
            fig.update_layout(template=template_plotly,
                paper_bgcolor=template_graph,
                plot_bgcolor=template_graph)
            #fig.update_layout(title_x=0.5)
            st.plotly_chart(fig)
    
            # Centered title for va_outros
            st.markdown(f"<h3 style='text-align: center'>{va_outros}</h3>", unsafe_allow_html=True)
    
            # Display dictionary content with line breaks
        elif grafico_escolhido == '📊 Barras 📊':
            grafico_barras_ordenado(df, va_outros, va_outros, layout=layout, rotation=0, ha='center')
            
        st.markdown("O gráfico apresenta a distribuição de diferentes cargos ocupados por profissionais da área de dados, destacando a frequência relativa "
                "de cada posição. Observa-se que os cargos mais comuns são Analista de Dados, que representa 23,5% das ocorrências, seguido por "
                "Cientista de Dados (17,8%) e 'Engenheiro de Dados/Data Engineer' (17,7%). Outras posições, como Analista de BI/BI Analyst "
                "(13,1%) e Engenheiro de BI/BI Engineer (6,8%), também apresentam relevância significativa, sendo bastante semelhantes com a profissão de "
                "Analista de Dados. À medida que avançamos no gráfico, a frequência de outros cargos Administrador de Banco de Dados, Economista "
                ", Estatístico (etc...) diminui consideravelmente, indicando que profissionais com esses cargos são menos comuns dentro do setor"
                , unsafe_allow_html=True)     
    
    elif agrupar_cargo == "Sim":
        analista = ['Analista de Negócios/Business Analyst', 'Analista de BI/BI Analyst', 'Analista de Dados/Data Analyst', 'Analista de Inteligência de Mercado/Market Intelligence']
        cientista = ['Cientista de Dados/Data Scientist', 'Engenheiro de Machine Learning/ML Engineer/AI Engineer']
        engenheiro = ['Engenheiro de Dados/Arquiteto de Dados/Data Engineer/Data Architect', 'DBA/Administrador de Banco de Dados', 'Analytics Engineer']
        ti = ['Analista de Suporte/Analista Técnico', 'Desenvolvedor/ Engenheiro de Software/ Analista de Sistemas']
        outro = ['Outra Opção', 'Outras Engenharias (não inclui dev)']
        EE = ['Economista', 'Estatístico']
        prof = ['Professor/Pesquisador']
        manager = ['Data Product Manager/ Product Manager (PM/APM/DPM/GPM/PO)']
        
        cargo_original = df['Cargo'].value_counts().reset_index(name='Contagem')
        cargo_original.columns = ['Cargo', 'Contagem']
        
        def categorizar_cargo(cargo):
            if cargo in analista:
                return 'Analista de Dados'
            elif cargo in cientista:
                return 'Cientista de Dados'
            elif cargo in engenheiro:
                return 'Engenheiro de Dados'
            elif cargo in ti:
                return 'Software'
            elif cargo in outro:
                return 'Outra Opção'
            elif cargo in EE:
                return 'EE'
            elif cargo in prof:
                return 'Professor/Pesquisador'
            elif cargo in manager:
                return 'Gerente'
            else:
                return 'Outros'
    
        cargo_original['Categoria'] = cargo_original['Cargo'].apply(categorizar_cargo)
        cargo_show = cargo_original.copy()
        # Adicionando uma linha de total
        total_linhas = cargo_original['Contagem'].sum()
        total_row = pd.DataFrame([['Total', total_linhas, 'Total']], columns=['Cargo', 'Contagem', 'Categoria'])
        cargo_original = pd.concat([cargo_original, total_row], ignore_index=True)
    
        # Ordenando a tabela pela coluna 'Categoria' (segunda coluna)
        cargo_original = cargo_original.sort_values(by='Categoria', ascending=True)
    
        # Reorganizando as colunas para que 'Contagem' seja a última
        cargo_original = cargo_original[['Cargo', 'Categoria', 'Contagem']]
        
        # Substituindo os cargos para as categorias simplificadas
        df['Cargo'] = df['Cargo'].replace(analista, 'Analista de Dados')
        df['Cargo'] = df['Cargo'].replace(cientista, 'Cientista de Dados')
        df['Cargo'] = df['Cargo'].replace(engenheiro, 'Engenheiro de Dados')
        df['Cargo'] = df['Cargo'].replace(ti, 'Software')
        df['Cargo'] = df['Cargo'].replace(outro, 'Outra Opção')
        df['Cargo'] = df['Cargo'].replace(EE, 'EE')
        df['Cargo'] = df['Cargo'].replace(manager, 'Gerente')
    
        # Calculando a contagem de cada cargo após as substituições
        cargo_contagem = df.groupby('Cargo')['Cargo'].count().reset_index(name='Contagem')

        if grafico_escolhido == '📊 Barras 📊':
            grafico_barras_ordenado(df, va_outros, va_outros, layout=layout, rotation=0, ha='center')
        
        if grafico_escolhido == '🍕 Pizza 🍕':
            fig = px.pie(cargo_contagem, values="Contagem", names="Cargo")
            fig.update_layout(template=template_plotly,
                paper_bgcolor=template_graph,
                plot_bgcolor=template_graph)
            
            st.plotly_chart(fig)
        st.subheader("Tabela com Quantidades Originais de Cargos")
        st.dataframe(cargo_show[['Cargo', 'Categoria', 'Contagem']], hide_index=True)
        
        st.markdown(f"<h3 style='text-align: center'>{va_outros}</h3>", unsafe_allow_html=True)
        
            # Display dictionary content with line breaks
        st.markdown(dic_texto[va_outros], unsafe_allow_html=True)


else: 
    # Pie chart
    if grafico_escolhido == '🍕 Pizza 🍕':
        fig = px.pie(df, values="Contagem", names=va_outros)
        fig.update_layout(template=template_plotly,
            paper_bgcolor=template_graph,
            plot_bgcolor=template_graph)
        #fig.update_layout(title_x=0.5)
        st.plotly_chart(fig)
    

    if grafico_escolhido == '📊 Barras 📊': 
        grafico_barras_ordenado(df, va_outros, va_outros, layout=layout, rotation=0, ha='center')
        
        
    st.markdown(f"<h3 style='text-align: center'>{va_outros}</h3>", unsafe_allow_html=True)
    
    st.markdown(dic_texto[va_outros], unsafe_allow_html=True)
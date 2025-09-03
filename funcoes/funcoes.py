import pandas as pd
import numpy as np 
import plotly.graph_objects as go
import streamlit as st


# %% grafico de barras ordenado
def grafico_barras_ordenado(df, coluna, xlabel, layout, titulo="", rotation=0, ha='center'):
    cor, template_graph_texto, template_graph, template_plotly = layout
    
    novo = df.groupby(coluna).size().reset_index(name='Contagem')
    novo['Porcentagem'] = (novo['Contagem'] / novo['Contagem'].sum()) * 100
    
    # Sort by descending order of Contagem
    novo = novo.sort_values(by='Contagem', ascending=False)

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=novo[coluna],  # Categorical x-axis
        y=novo['Contagem'],             # Bar heights
        text=[f'{p:.1f}%' for p in novo['Porcentagem']],  # Percentages as text
        textposition='outside',             # Position text above bars
        marker_color=cor,
        textfont=dict(color=template_graph_texto)         # Bar color
    ))
        
    # Layout settings
    fig.update_layout(
        template=template_plotly,
        xaxis_title=coluna,
        yaxis_title='Frequência',
        xaxis=dict(#titlefont=dict(color=template_graph_texto),
                   tickfont=dict(color=template_graph_texto)),  # Enforce custom order
        yaxis=dict(range=[0, novo['Contagem'].max() * 1.1],
                   #titlefont=dict(color=template_graph_texto),
                   tickfont=dict(color=template_graph_texto)), # extendendo um pouco o limite de y
        paper_bgcolor=template_graph,  
        plot_bgcolor=template_graph)
    
    st.plotly_chart(fig)

# %% tratamento de dados
class TratamentoDados:
    def __init__(self, ano='2023'):
        ############################### inicializando o objeto e realizando as primeiras transformacoes ##############################
        
        links = {
            '2023': 'https://raw.githubusercontent.com/vinicius-soares26/Datasets/refs/heads/main/State%20of%20Data%20Brazil/State_of_data_BR_2023_Kaggle%20-%20df_survey_2023.csv',
            '2022': 'https://raw.githubusercontent.com/vinicius-soares26/Datasets/refs/heads/main/State%20of%20Data%20Brazil/State_of_data_2022.csv',
            '2021': 'https://raw.githubusercontent.com/vinicius-soares26/Datasets/89c4bc185744b51b5b3563255cefabaca82abe42/State%20of%20Data%20Brazil/State%20of%20Data%202021%20-%20Dataset%20-%20Pgina1.csv'
            }

        link = links.get(ano)
        
        self.df = pd.read_csv(link)  # Store DataFrame as an instance variable
        
        # Renomeando colunas
        self.df.rename(columns={
            "('P1_a ', 'Idade')": 'Idade',
            "('P1_a_1 ', 'Faixa idade')": "Faixa de Idade",
            "('P1_c ', 'Cor/raca/etnia')": 'Etnia',
            "('P1_b ', 'Genero')": 'Gênero',
            "('P2_f ', 'Cargo Atual')": 'Cargo',
            "('P2_h ', 'Faixa salarial')": 'Faixa Salarial',
            "('P2_g ', 'Nivel')": 'Nível',
            "('P1_l ', 'Nivel de Ensino')": 'Escolaridade',
            "('P1_m ', 'Área de Formação')": 'Área',
            "('P2_i ', 'Quanto tempo de experiência na área de dados você tem?')": 'Experiência'
        }, inplace=True)

        self.df['Contagem'] = 1





        ########################################### performando transformações em salarios e experiencia  #######################################  
        
        # Substituindo poucas observações 
        self.df['Faixa Salarial'] = self.df['Faixa Salarial'].replace(
            'de R$ 101/mês a R$ 2.000/mês', 'de R$ 1.001/mês a R$ 2.000/mês')

        # Dicionário para transformar as faixas em valores nominais
        faixa_salario_para_valor = {
            'de R$ 8.001/mês a R$ 12.000/mês': 10000,
            'de R$ 4.001/mês a R$ 6.000/mês': 5000,
            'de R$ 12.001/mês a R$ 16.000/mês': 14000,
            'de R$ 6.001/mês a R$ 8.000/mês': 7000,
            'de R$ 3.001/mês a R$ 4.000/mês': 3500,
            'de R$ 16.001/mês a R$ 20.000/mês': 18000,
            'de R$ 2.001/mês a R$ 3.000/mês': 2500,
            'de R$ 1.001/mês a R$ 2.000/mês': 1500,
            'de R$ 20.001/mês a R$ 25.000/mês': 22500,
            'de R$ 25.001/mês a R$ 30.000/mês': 27500,
            'de R$ 30.001/mês a R$ 40.000/mês': 35000,
            'Acima de R$ 40.001/mês': 40001,
            'Menos de R$ 1.000/mês': 500,  # Aproximadamente
        }

        self.df['Salarios'] = self.df['Faixa Salarial'].map(faixa_salario_para_valor)
        self.df['Faixa Salarial Original'] = self.df['Faixa Salarial']

        # Listas das faixas salariais ordenadas para criação de nova coluna resumida
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
            "Acima de R$ 40.001/mês",
        ]
        ordem_faixas_resumida = [
            "< 1k", "1k < 2k", "2k < 3k", "3k < 4k", "4k < 6k", "6k < 8k",
            "8k < 12k", "12k < 16k", "16k < 20k", "20k < 25k", "25k < 30k",
            "30k < 40k", "40k <"
        ]

        dic_renomear = dict(zip(ordem_faixas, ordem_faixas_resumida))

        # Aplicando o mapeamento para criar nova coluna
        self.df['Faixa Salarial'] = self.df['Faixa Salarial'].map(dic_renomear)

        # Experiência
        self.df['Experiência'] = self.df['Experiência'].replace("de 5 a 6 anos", "de 4 a 6 anos")
        self.df['Experiência'] = self.df['Experiência'].replace('Não tenho experiência na área de dados', 'Sem experiência')

    def retornar_dados(self):
        """Retorna o dataframe processado"""
        return self.df
    
    def retornar_migracao(self):
        norte = ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO']
        nordeste = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']
        centro = ['DF', 'GO', 'MS', 'MT']
        sudeste = ['ES', 'MG', 'RJ', 'SP']
        sul = ['PR', 'RS', 'SC']

        categorias = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

        # Função para mapear estados para regiões
        def estado_para_regiao(coluna_antiga, coluna_nova, df_migracao):
            condicao = [
                df_migracao[coluna_antiga].str.contains('|'.join(norte), na=False),
                df_migracao[coluna_antiga].str.contains('|'.join(nordeste), na=False),
                df_migracao[coluna_antiga].str.contains('|'.join(centro), na=False),
                df_migracao[coluna_antiga].str.contains('|'.join(sudeste), na=False),
                df_migracao[coluna_antiga].str.contains('|'.join(sul), na=False)
            ]
            df_migracao[coluna_nova] = np.select(condicao, categorias, default='Exterior')
            return df_migracao

        # Supondo que o dataframe 'df' já tenha sido carregado anteriormente
        df_migracao = self.df[["('P1_k ', 'Regiao de origem')", "('P1_i ', 'Estado onde mora')", "Salarios"]]
        # Renomeando colunas
        df_migracao.rename(columns={"('P1_i ', 'Estado onde mora')": "Estado onde mora",
                                    "('P1_k ', 'Regiao de origem')": "Estado de origem"},
                                    inplace=True)
        # Extrair a sigla de onde mora
        df_migracao["Sigla onde mora"] = df_migracao["Estado onde mora"].str.extract(r'\((.*?)\)')
        df_migracao["Sigla de origem"] = df_migracao["Estado de origem"].str.extract(r'\((.*?)\)')
        
        salarios = df_migracao.groupby("Sigla onde mora")['Salarios'].mean().reset_index()

        df_migracao.dropna(inplace=True)
        
        df_migracao = df_migracao[df_migracao["Estado de origem"] != df_migracao["Estado onde mora"]].copy()

        # Renomear as colunas para algo mais acessível
        antigas = ["Estado de origem", "Estado onde mora"]
        novas = ["Região de Origem", "Região Atual"]

        for antiga, nova in zip(antigas, novas):
            df_migracao = estado_para_regiao(antiga, nova, df_migracao)
        
        


        return df_migracao, salarios


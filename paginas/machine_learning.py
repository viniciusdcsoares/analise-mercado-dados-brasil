import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
import streamlit as st
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


link = 'https://raw.githubusercontent.com/ricardorocha86/Datasets/refs/heads/master/State_of_data_BR_2023_Kaggle%20-%20df_survey_2023.csv'
df = pd.read_csv(link)

mapa_cargos = {
    'Analista de Negócios/Business Analyst': 'Analista de BI',
    'Analista de BI/BI Analyst': 'Analista de BI',
    'Analista de Inteligência de Mercado/Market Intelligence': 'Analista de BI',

    'Analista de Dados/Data Analyst': 'Analista de Dados',
    'Analytics Engineer': 'Analista de Dados',

    'Cientista de Dados/Data Scientist': 'Cientista de Dados',
    'Engenheiro de Machine Learning/ML Engineer/AI Engineer': 'Cientista de Dados',
    'Estatístico' : 'Cientista de Dados',

    'Engenheiro de Dados/Arquiteto de Dados/Data Engineer/Data Architect': 'Engenheiro de Dados',
    'DBA/Administrador de Banco de Dados': 'Engenheiro de Dados',

    'Data Product Manager/ Product Manager (PM/APM/DPM/GPM/PO)': 'Outra Opção',
    'Outra Opção': 'Outra Opção',
    'Outras Engenharias (não inclui dev)': 'Outra Opção',
    'Analista de Suporte/Analista Técnico': 'Outra Opção',
    'Desenvolvedor/ Engenheiro de Software/ Analista de Sistemas': 'Outra Opção',
    'Economista': 'Outra Opção',
    'Professor/Pesquisador': 'Outra Opção'
}

df['Cargo'] = df["('P2_f ', 'Cargo Atual')"].map(mapa_cargos).fillna('Outra Opção')

df = df[df['Cargo'] != 'Outra Opção']

colunas_manter = [
    "('P1_a ', 'Idade')",
    "('P1_i ', 'Estado onde mora')",
    "('P1_l ', 'Nivel de Ensino')",
    "('P1_m ', 'Área de Formação')",
    "('P2_g ', 'Nivel')",
    "('P2_i ', 'Quanto tempo de experiência na área de dados você tem?')",
    "('P2_a ', 'Qual sua situação atual de trabalho?')",
    "('P2_c ', 'Numero de Funcionarios')",
    "('P2_b ', 'Setor')",
    "('P2_r ', 'Atualmente qual a sua forma de trabalho?')"
]

y_col = ["('P2_h ', 'Faixa salarial')"]

prefixos_chave = ["P4_d_", "P4_g_", "P4_h_", "P4_j_"]

colunas_a_pegar = [col for col in df.columns if any(prefixo in col for prefixo in prefixos_chave)]


df_ml = df[y_col + colunas_manter + ['Cargo'] + colunas_a_pegar].copy()

colunas_renomeadas = [col.split(", ")[1].strip("')") for col in (y_col + colunas_manter)]

df_ml.columns = colunas_renomeadas + ['Cargo'] + colunas_a_pegar

df_ml['Faixa salarial'] = df_ml['Faixa salarial'].replace('de R$ 101/mês a R$ 2.000/mês', 'de R$ 1.001/mês a R$ 2.000/mês')
df_ml['Quanto tempo de experiência na área de dados você tem?'] = df_ml['Quanto tempo de experiência na área de dados você tem?'].replace('de 5 a 6 anos', 'de 4 a 6 anos')

def renomear_coluna(col):
    prefix_map = {
        'P4_j_': 'BI_',
        'P4_h_': 'Cloud_',
        'P4_g_': 'Banco_',
        'P4_d_': 'Linguagens_'
    }

    # Limpa a string removendo parênteses e aspas
    col = col.strip("()").strip("'").strip('"')

    partes = col.split(", ")
    if len(partes) < 2:
        return col  # não está no formato esperado

    chave = partes[0].strip("'").strip('"')
    nome = partes[1].strip("'").strip('"')

    for prefixo_original, novo_prefixo in prefix_map.items():
        if chave.startswith(prefixo_original):
            return f"{novo_prefixo}{nome}"

    return col  # se não bate com nenhum prefixo


df_ml.columns = [renomear_coluna(col) for col in df_ml.columns]

df_ml = df_ml.dropna(subset=colunas_renomeadas + ['Cargo'])

colunas_categoricas = [
    'Estado onde mora', 'Nivel de Ensino', 'Área de Formação', 'Nivel',
    'Quanto tempo de experiência na área de dados você tem?',
    'Qual sua situação atual de trabalho?', 'Numero de Funcionarios',
    'Setor', 'Atualmente qual a sua forma de trabalho?', 'Cargo'
]
df_ml[colunas_categoricas] = df_ml[colunas_categoricas].astype(str)
df_final = pd.get_dummies(df_ml, columns=colunas_categoricas, drop_first=False)

mapeamento_salarios = {
    'Menos de R$ 1.000/mês': 800,
    'de R$ 1.001/mês a R$ 2.000/mês': 1500,
    'de R$ 2.001/mês a R$ 3.000/mês': 2500,
    'de R$ 3.001/mês a R$ 4.000/mês': 3500,
    'de R$ 4.001/mês a R$ 6.000/mês': 5000,
    'de R$ 6.001/mês a R$ 8.000/mês': 7000,
    'de R$ 8.001/mês a R$ 12.000/mês': 10000,
    'de R$ 12.001/mês a R$ 16.000/mês': 14000,
    'de R$ 16.001/mês a R$ 20.000/mês': 18000,
    'de R$ 20.001/mês a R$ 25.000/mês': 22500,
    'de R$ 25.001/mês a R$ 30.000/mês': 27500,
    'de R$ 30.001/mês a R$ 40.000/mês': 35000,
    'Acima de R$ 40.001/mês': 45000
}

df_final['Faixa salarial'] = df_final['Faixa salarial'].map(mapeamento_salarios)

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
df_final['Idade'] = scaler.fit_transform(df_final[['Idade']])

# tive que dropar
df_final.dropna(inplace=True)

X = df_final.drop(columns=['Faixa salarial'])
y = df_final['Faixa salarial']

# Dividindo os dados em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Treinando os modelos em segundo plano
knn_model = KNeighborsRegressor(n_neighbors=7)
knn_model.fit(X_train, y_train)

dt_model = DecisionTreeRegressor(max_depth=6, min_samples_split=195, min_samples_leaf=10, random_state=42)
dt_model.fit(X_train, y_train)

# Título da página
st.title("Predictor de Salários em Dados")

# Importância das features para guiar o usuário
st.write("### Features mais importantes para a predição salarial")
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': dt_model.feature_importances_
}).sort_values('Importance', ascending=False)

# Mostrar as 15 features mais importantes
top_features = feature_importance.head(15)
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x='Importance', y='Feature', data=top_features, ax=ax)
ax.set_title('Top 15 Features Mais Importantes')
st.pyplot(fig)

# Dicionários de opções para entrada do usuário
st.write("## Complete o formulário abaixo para obter sua previsão salarial")

with st.form("salary_prediction_form"):
    st.write("### Dados pessoais e profissionais")
    col1, col2 = st.columns(2)
    
    with col1:
        idade = st.slider("Idade", 18, 70, 30)
        
        estado_opcoes = sorted(df_ml['Estado onde mora'].unique())
        estado = st.selectbox("Estado onde mora", estado_opcoes)
        
        nivel_ensino_opcoes = sorted(df_ml['Nivel de Ensino'].unique())
        nivel_ensino = st.selectbox("Nível de Ensino", nivel_ensino_opcoes)
        
        area_formacao_opcoes = sorted(df_ml['Área de Formação'].unique())
        area_formacao = st.selectbox("Área de Formação", area_formacao_opcoes)
        
        cargo_opcoes = ['Analista de BI', 'Analista de Dados', 'Cientista de Dados', 'Engenheiro de Dados']
        cargo = st.selectbox("Cargo", cargo_opcoes)
    
    with col2:
        nivel_opcoes = sorted(df_ml['Nivel'].unique())
        nivel = st.selectbox("Nível", nivel_opcoes)
        
        experiencia_opcoes = sorted(df_ml['Quanto tempo de experiência na área de dados você tem?'].unique())
        experiencia = st.selectbox("Experiência na área de dados", experiencia_opcoes)
        
        situacao_trabalho_opcoes = sorted(df_ml['Qual sua situação atual de trabalho?'].unique())
        situacao_trabalho = st.selectbox("Situação atual de trabalho", situacao_trabalho_opcoes)
        
        num_funcionarios_opcoes = sorted(df_ml['Numero de Funcionarios'].unique())
        num_funcionarios = st.selectbox("Número de Funcionários", num_funcionarios_opcoes)
        
        setor_opcoes = sorted(df_ml['Setor'].unique())
        setor = st.selectbox("Setor", setor_opcoes)
        
        forma_trabalho_opcoes = sorted(df_ml['Atualmente qual a sua forma de trabalho?'].unique())
        forma_trabalho = st.selectbox("Forma de trabalho", forma_trabalho_opcoes)
    
    st.write("### Habilidades Técnicas")
    
    # Linguagens de programação
    st.write("#### Linguagens de Programação")
    linguagens_cols = [col for col in X.columns if col.startswith('Linguagens_')]
    linguagens_names = [col.replace('Linguagens_', '') for col in linguagens_cols]
    
    linguagens_selecionadas = {}
    col1, col2, col3 = st.columns(3)
    for i, linguagem in enumerate(linguagens_names):
        if i % 3 == 0:
            linguagens_selecionadas[linguagem] = col1.checkbox(f"{linguagem}")
        elif i % 3 == 1:
            linguagens_selecionadas[linguagem] = col2.checkbox(f"{linguagem}")
        else:
            linguagens_selecionadas[linguagem] = col3.checkbox(f"{linguagem}")
    
    # Bancos de dados
    st.write("#### Bancos de Dados")
    banco_cols = [col for col in X.columns if col.startswith('Banco_')]
    banco_names = [col.replace('Banco_', '') for col in banco_cols]
    
    banco_selecionados = {}
    col1, col2, col3 = st.columns(3)
    for i, banco in enumerate(banco_names):
        if i % 3 == 0:
            banco_selecionados[banco] = col1.checkbox(f"{banco}")
        elif i % 3 == 1:
            banco_selecionados[banco] = col2.checkbox(f"{banco}")
        else:
            banco_selecionados[banco] = col3.checkbox(f"{banco}")
    
    # Cloud
    st.write("#### Serviços Cloud")
    cloud_cols = [col for col in X.columns if col.startswith('Cloud_')]
    cloud_names = [col.replace('Cloud_', '') for col in cloud_cols]
    
    cloud_selecionados = {}
    col1, col2, col3 = st.columns(3)
    for i, cloud in enumerate(cloud_names):
        if i % 3 == 0:
            cloud_selecionados[cloud] = col1.checkbox(f"{cloud}")
        elif i % 3 == 1:
            cloud_selecionados[cloud] = col2.checkbox(f"{cloud}")
        else:
            cloud_selecionados[cloud] = col3.checkbox(f"{cloud}")
    
    # BI
    st.write("#### Ferramentas de BI")
    bi_cols = [col for col in X.columns if col.startswith('BI_')]
    bi_names = [col.replace('BI_', '') for col in bi_cols]
    
    bi_selecionados = {}
    col1, col2, col3 = st.columns(3)
    for i, bi in enumerate(bi_names):
        if i % 3 == 0:
            bi_selecionados[bi] = col1.checkbox(f"{bi}")
        elif i % 3 == 1:
            bi_selecionados[bi] = col2.checkbox(f"{bi}")
        else:
            bi_selecionados[bi] = col3.checkbox(f"{bi}")
    
    # Botão de submissão
    submitted = st.form_submit_button("Calcular Salário Previsto")
    
    if submitted:
        # Preparar os dados de entrada
        input_data = {}
        
        # Normalizar a idade
        idade_norm = (idade - df_ml['Idade'].min()) / (df_ml['Idade'].max() - df_ml['Idade'].min())
        input_data['Idade'] = idade_norm
        
        # Criar colunas one-hot para variáveis categóricas
        for col in X.columns:
            input_data[col] = 0  # Inicializa todas as colunas com 0
        
        # Preencher as variáveis categóricas
        input_data[f'Estado onde mora_{estado}'] = 1
        input_data[f'Nivel de Ensino_{nivel_ensino}'] = 1
        input_data[f'Área de Formação_{area_formacao}'] = 1
        input_data[f'Nivel_{nivel}'] = 1
        input_data[f'Quanto tempo de experiência na área de dados você tem?_{experiencia}'] = 1
        input_data[f'Qual sua situação atual de trabalho?_{situacao_trabalho}'] = 1
        input_data[f'Numero de Funcionarios_{num_funcionarios}'] = 1
        input_data[f'Setor_{setor}'] = 1
        input_data[f'Atualmente qual a sua forma de trabalho?_{forma_trabalho}'] = 1
        input_data[f'Cargo_{cargo}'] = 1
        
        # Preencher habilidades técnicas
        for linguagem, selected in linguagens_selecionadas.items():
            if selected:
                input_data[f'Linguagens_{linguagem}'] = 1
        
        for banco, selected in banco_selecionados.items():
            if selected:
                input_data[f'Banco_{banco}'] = 1
        
        for cloud, selected in cloud_selecionados.items():
            if selected:
                input_data[f'Cloud_{cloud}'] = 1
        
        for bi, selected in bi_selecionados.items():
            if selected:
                input_data[f'BI_{bi}'] = 1
        
        # Criar DataFrame com colunas na mesma ordem do modelo
        df_input = pd.DataFrame([input_data])
        df_input = df_input.reindex(columns=X.columns, fill_value=0)
        
        # Fazer predições
        knn_pred = knn_model.predict(df_input)[0]
        dt_pred = dt_model.predict(df_input)[0]
        
        # Exibir resultados
        st.success("### Previsão de Salário Calculada!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Previsão KNN", f"R$ {knn_pred:.2f}")
        with col2:
            st.metric("Previsão Árvore de Decisão", f"R$ {dt_pred:.2f}")
        
        # Média dos dois modelos
        media_pred = (knn_pred + dt_pred) / 2
        st.metric("Média das Previsões", f"R$ {media_pred:.2f}")
        
        # Faixa salarial correspondente
        faixa_correspondente = "Acima de R$ 40.001/mês"
        for faixa, valor in sorted(mapeamento_salarios.items(), key=lambda x: x[1]):
            if media_pred <= valor * 1.2:  # Considerando uma margem de 20%
                faixa_correspondente = faixa
                break
        
        #st.info(f"### Faixa Salarial Estimada: {faixa_correspondente}")
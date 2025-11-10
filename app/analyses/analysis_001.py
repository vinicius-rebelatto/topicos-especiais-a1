import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def run_analysis_001(df):
    """
    Recebe um DataFrame, trata dados nulos, calcula correlação com o preço
    e retorna um gráfico de barras (figura matplotlib).
    """

    # 2. Selecionar colunas e criar uma cópia explícita para evitar o warning
    colunas_numericas = [
        'price', 'usableAreas', 'suites', 'bathrooms',
        'bedrooms', 'parkingSpaces', 'monthlyCondoFee', 'yearlyIptu'
    ]

    # Verificar se todas as colunas necessárias existem
    colunas_faltando = [col for col in colunas_numericas if col not in df.columns]
    if colunas_faltando:
        raise ValueError(f"Colunas necessárias não encontradas no dataset: {', '.join(colunas_faltando)}")

    df_analise = df[colunas_numericas].copy()

    # 3. Tratamento de dados nulos (preenchendo com a mediana)
    for coluna in df_analise.columns:
        if df_analise[coluna].isnull().any():
            mediana = df_analise[coluna].median()
            df_analise[coluna].fillna(mediana, inplace=True)

    # 4. Calcular a matriz de correlação (Pearson)
    matriz_correlacao = df_analise.corr()

    # 5. Isolar a correlação de todos os atributos com a coluna 'price'
    correlacao_com_preco = matriz_correlacao['price'].sort_values(ascending=False)
    correlacao_com_preco = correlacao_com_preco.drop('price')

    # 6. Gerar o gráfico
    plt.style.use('seaborn-v0_8-whitegrid')

    # Criar a figura e os eixos (ax)
    fig, ax = plt.subplots(figsize=(10, 7))

    sns.barplot(
        x=correlacao_com_preco.index,
        y=correlacao_com_preco.values,
        palette='viridis',
        hue=correlacao_com_preco.index,
        legend=False,
        ax=ax  # Especificar os eixos para o plot
    )

    # Adicionar os valores nas barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points')

    ax.set_title('Força da Correlação dos Atributos com o Preço do Imóvel', fontsize=16)
    ax.set_xlabel('Atributos do Imóvel', fontsize=12)
    ax.set_ylabel('Coeficiente de Correlação de Pearson', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Retornar o objeto 'figure' em vez de salvar em arquivo
    return fig
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analisar_correlacao_preco(caminho_arquivo):
    """
    Carrega o dataset, trata valores nulos, calcula a correlação de atributos
    numéricos com o preço e gera um gráfico de barras.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV do dataset.
    """
    # 1. Carregar o dataset
    df = pd.read_csv(caminho_arquivo)

    # 2. Selecionar colunas e criar uma cópia explícita para evitar o warning
    colunas_numericas = [
        'price', 'usableAreas', 'suites', 'bathrooms',
        'bedrooms', 'parkingSpaces', 'monthlyCondoFee', 'yearlyIptu'
    ]
    # ALTERAÇÃO 1: Adicionado .copy() para criar um DataFrame independente
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
    plt.figure(figsize=(10, 7))

    # ALTERAÇÃO 2: Código do gráfico atualizado para o novo padrão do Seaborn
    ax = sns.barplot(
        x=correlacao_com_preco.index,
        y=correlacao_com_preco.values,
        palette='viridis',
        hue=correlacao_com_preco.index, # Adicionado para o novo padrão
        legend=False # Adicionado para não mostrar a legenda
    )

    # Adicionar os valores nas barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points')

    plt.title('Força da Correlação dos Atributos com o Preço do Imóvel', fontsize=16)
    plt.xlabel('Atributos do Imóvel', fontsize=12)
    plt.ylabel('Coeficiente de Correlação de Pearson', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig('01_correlation_chart.png')
    print("Gráfico '01_correlation_chart.png' salvo com sucesso!")


if __name__ == '__main__':
    arquivo_dataset = 'curitiba_apartment_real_estate_data.csv'
    analisar_correlacao_preco(arquivo_dataset)
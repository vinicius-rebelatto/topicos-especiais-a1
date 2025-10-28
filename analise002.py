import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def analisar_preco_por_bairro(caminho_arquivo):
    """
    Carrega o dataset, identifica os bairros com mais anúncios e cria um
    boxplot para visualizar a distribuição de preços em cada um deles.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV do dataset.
    """
    # 1. Carregar o dataset
    df = pd.read_csv(caminho_arquivo)

    # 2. Tratamento de dados: remover linhas sem informação de preço ou bairro
    df.dropna(subset=['price', 'neighborhood'], inplace=True)

    # 3. Filtrar outliers de preço para uma melhor visualização do boxplot
    # Removemos valores que estão a mais de 3 desvios padrão da média
    df = df[np.abs(df.price - df.price.mean()) <= (3 * df.price.std())]

    # 4. Identificar os 10 bairros com mais anúncios
    top_10_bairros = df['neighborhood'].value_counts().nlargest(10).index

    # 5. Filtrar o DataFrame para conter apenas os dados desses 10 bairros
    df_top_10 = df[df['neighborhood'].isin(top_10_bairros)]

    # 6. Calcular a mediana de preço para cada bairro e ordenar
    ordem_bairros = df_top_10.groupby('neighborhood')['price'].median().sort_values(ascending=False).index

    # 7. Gerar o gráfico
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(14, 8))

    sns.boxplot(
        x='neighborhood',
        y='price',
        data=df_top_10,
        order=ordem_bairros,  # Ordena as caixas pela mediana do preço
        palette='plasma'
    )

    plt.title('Distribuição de Preços de Apartamentos por Bairro (Top 10)', fontsize=18)
    plt.xlabel('Bairro', fontsize=12)
    plt.ylabel('Preço (R$)', fontsize=12)
    plt.xticks(rotation=45, ha='right')  # Rotaciona os nomes dos bairros para melhor leitura

    # Formatar o eixo Y para exibir os preços de forma mais legível
    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda x, p: format(int(x), ','))
    )

    plt.tight_layout()

    # Salvar o gráfico em um arquivo
    plt.savefig('02_distribution_by_neighborhood.png')
    print("Gráfico '02_distribution_by_neighborhood.png' salvo com sucesso!")


if __name__ == '__main__':
    arquivo_dataset = 'curitiba_apartment_real_estate_data.csv'
    analisar_preco_por_bairro(arquivo_dataset)
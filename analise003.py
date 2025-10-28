import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analisar_preco_vs_area(caminho_arquivo):
    """
    Carrega o dataset, limpa os dados e gera um gráfico de dispersão
    para analisar a relação entre a área útil e o preço dos imóveis.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV do dataset.
    """
    # 1. Carregar o dataset
    df = pd.read_csv(caminho_arquivo)

    # 2. Tratamento de dados: remover linhas sem informação de preço ou área útil
    df.dropna(subset=['price', 'usableAreas'], inplace=True)

    # 3. Remover outliers para uma visualização mais clara
    # Usaremos o método de quantis para focar na maior parte dos dados.
    # Removemos os 1% mais baratos/caros e os 1% menores/maiores.
    limite_preco_inf = df['price'].quantile(0.01)
    limite_preco_sup = df['price'].quantile(0.99)
    limite_area_inf = df['usableAreas'].quantile(0.01)
    limite_area_sup = df['usableAreas'].quantile(0.99)

    df_filtrado = df[
        (df['price'] >= limite_preco_inf) & (df['price'] <= limite_preco_sup) &
        (df['usableAreas'] >= limite_area_inf) & (df['usableAreas'] <= limite_area_sup)
    ]

    # 4. Gerar o gráfico de dispersão com linha de regressão
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(12, 7))

    # regplot é ideal pois plota os pontos e uma linha de tendência
    sns.regplot(
        x='usableAreas',
        y='price',
        data=df_filtrado,
        scatter_kws={'alpha': 0.3, 's': 20}, # Deixa os pontos semi-transparentes
        line_kws={'color': 'red', 'linewidth': 2} # Destaca a linha de tendência
    )

    plt.title('Relação entre Preço e Área Útil dos Apartamentos', fontsize=18)
    plt.xlabel('Área Útil (m²)', fontsize=12)
    plt.ylabel('Preço (R$)', fontsize=12)

    # Formatar os eixos para melhor leitura
    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda x, p: format(int(x), ','))
    )
    ax.get_xaxis().set_major_formatter(
        plt.FuncFormatter(lambda x, p: format(int(x), ','))
    )

    plt.tight_layout()

    # Salvar o gráfico em um arquivo
    plt.savefig('03_price_vs_area_scatter.png')
    print("Gráfico '03_price_vs_area_scatter.png' salvo com sucesso!")


if __name__ == '__main__':
    arquivo_dataset = 'curitiba_apartment_real_estate_data.csv'
    analisar_preco_vs_area(arquivo_dataset)
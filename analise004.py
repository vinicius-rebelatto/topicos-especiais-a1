import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def analisar_preco_por_quartos(caminho_arquivo):
    """
    Carrega o dataset, calcula o preço médio dos imóveis com base no
    número de quartos e gera um gráfico de barras comparativo.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV do dataset.
    """
    # 1. Carregar o dataset
    df = pd.read_csv(caminho_arquivo)

    # 2. Tratamento de dados: remover linhas sem info de preço ou quartos
    df.dropna(subset=['price', 'bedrooms'], inplace=True)

    # Converter 'bedrooms' para inteiro, caso não esteja
    df['bedrooms'] = df['bedrooms'].astype(int)

    # 3. Filtrar dados para uma análise mais focada e realista
    # Removemos apartamentos com 0 quartos ou mais de 6 (geralmente outliers)
    df_filtrado = df[(df['bedrooms'] > 0) & (df['bedrooms'] <= 6)]

    # 4. Agrupar por número de quartos e calcular o preço médio
    preco_medio_por_quarto = df_filtrado.groupby('bedrooms')['price'].mean().sort_index()

    # 5. Gerar o gráfico de barras
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(10, 7))

    ax = sns.barplot(
        x=preco_medio_por_quarto.index,
        y=preco_medio_por_quarto.values,
        palette='magma',
        hue=preco_medio_por_quarto.index,
        legend=False
    )

    plt.title('Preço Médio do Apartamento por Número de Quartos', fontsize=18)
    plt.xlabel('Número de Quartos', fontsize=12)
    plt.ylabel('Preço Médio (R$)', fontsize=12)

    # Formatar o eixo Y para exibir os preços de forma mais legível
    ax.get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda y, p: f'R$ {y:,.0f}'.replace(',', '.'))
    )

    # Adicionar os valores no topo das barras
    for p in ax.patches:
        ax.annotate(f'R$ {int(p.get_height()):,.0f}'.replace(',', '.'),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points',
                    fontsize=10,
                    fontweight='bold')

    plt.tight_layout()

    # Salvar o gráfico em um arquivo
    plt.savefig('04_price_by_bedrooms.png')
    print("Gráfico '04_price_by_bedrooms.png' salvo com sucesso!")


if __name__ == '__main__':
    arquivo_dataset = 'curitiba_apartment_real_estate_data.csv'
    analisar_preco_por_quartos(arquivo_dataset)
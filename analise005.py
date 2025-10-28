import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analisar_preco_por_vagas(caminho_arquivo):
    """
    Carrega o dataset, calcula o preço médio dos imóveis com base no
    número de vagas de garagem e gera um gráfico de barras comparativo.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV do dataset.
    """
    # 1. Carregar o dataset
    df = pd.read_csv(caminho_arquivo)

    # 2. Tratamento de dados: remover linhas sem info de preço ou vagas
    df.dropna(subset=['price', 'parkingSpaces'], inplace=True)
    df['parkingSpaces'] = df['parkingSpaces'].astype(int)

    # 3. Filtrar dados para focar na maioria do mercado (0 a 5 vagas)
    df_filtrado = df[df['parkingSpaces'].between(0, 5)]

    # 4. Agrupar por número de vagas e calcular o preço médio
    preco_medio_por_vaga = df_filtrado.groupby('parkingSpaces')['price'].mean().sort_index()

    # 5. Gerar o gráfico de barras
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(10, 7))

    ax = sns.barplot(
        x=preco_medio_por_vaga.index,
        y=preco_medio_por_vaga.values,
        palette='crest',
        hue=preco_medio_por_vaga.index,
        legend=False
    )

    plt.title('Preço Médio do Apartamento por Número de Vagas de Garagem', fontsize=18)
    plt.xlabel('Número de Vagas de Garagem', fontsize=12)
    plt.ylabel('Preço Médio (R$)', fontsize=12)

    # Formatar o eixo Y
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

    # Salvar o gráfico
    plt.savefig('05_price_by_parking_spaces.png')
    print("Gráfico '05_price_by_parking_spaces.png' salvo com sucesso!")


if __name__ == '__main__':
    arquivo_dataset = 'curitiba_apartment_real_estate_data.csv'
    analisar_preco_por_vagas(arquivo_dataset)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analisar_preco_m2_por_bairro(caminho_arquivo):
    """
    Carrega o dataset, calcula o preço por metro quadrado (m²) e gera um
    gráfico de barras comparando a mediana do m² nos principais bairros.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV do dataset.
    """
    # 1. Carregar o dataset
    df = pd.read_csv(caminho_arquivo)

    # 2. Tratamento de dados
    df.dropna(subset=['price', 'usableAreas', 'neighborhood'], inplace=True)
    # Garantir que a área útil não seja zero para evitar divisão por zero
    df = df[df['usableAreas'] > 0]

    # 3. Engenharia de Feature: Criar a coluna 'preco_m2'
    df['preco_m2'] = df['price'] / df['usableAreas']

    # 4. Filtrar outliers de preço/m² para uma análise mais justa
    limite_superior = df['preco_m2'].quantile(0.99)
    df_filtrado = df[df['preco_m2'] < limite_superior]

    # 5. Selecionar os 15 bairros com mais anúncios para o gráfico
    top_15_bairros = df_filtrado['neighborhood'].value_counts().nlargest(15).index

    df_top_15 = df_filtrado[df_filtrado['neighborhood'].isin(top_15_bairros)]

    # 6. Calcular a mediana do preço/m² e ordenar
    preco_m2_mediano = df_top_15.groupby('neighborhood')['preco_m2'].median().sort_values(ascending=False)

    # 7. Gerar o gráfico de barras
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(12, 8))

    ax = sns.barplot(
        x=preco_m2_mediano.index,
        y=preco_m2_mediano.values,
        palette='rocket',
        hue=preco_m2_mediano.index,
        legend=False
    )

    plt.title('Preço Mediano por Metro Quadrado (m²) por Bairro (Top 15)', fontsize=18)
    plt.xlabel('Bairro', fontsize=12)
    plt.ylabel('Preço Mediano por m² (R$)', fontsize=12)
    plt.xticks(rotation=45, ha='right')

    # Formatar o eixo Y
    ax.get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda y, p: f'R$ {y:,.2f}'.replace(',', '.'))
    )

    # Adicionar valores no topo das barras
    for p in ax.patches:
        ax.annotate(f'R$ {p.get_height():,.2f}'.replace(',', '.'),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points',
                    fontsize=10)

    plt.tight_layout()
    plt.savefig('06_price_per_sqm_by_neighborhood.png')
    print("Gráfico '06_price_per_sqm_by_neighborhood.png' salvo com sucesso!")


if __name__ == '__main__':
    arquivo_dataset = 'curitiba_apartment_real_estate_data.csv'
    analisar_preco_m2_por_bairro(arquivo_dataset)
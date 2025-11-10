# analyses/analysis_005.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def run_analysis_005(df):
    """
    Carrega o dataset, calcula o preço médio dos imóveis com base no
    número de vagas de garagem e gera um gráfico de barras comparativo.

    Args:
        df (pd.DataFrame): O DataFrame carregado.

    Returns:
        matplotlib.figure.Figure: A figura do gráfico de barras.
    """

    # 2. Tratamento de dados: remover linhas sem info de preço ou vagas
    df_clean = df.dropna(subset=['price', 'parkingSpaces']).copy()
    df_clean['parkingSpaces'] = df_clean['parkingSpaces'].astype(int)

    # 3. Filtrar dados para focar na maioria do mercado (0 a 5 vagas)
    df_filtrado = df_clean[df_clean['parkingSpaces'].between(0, 5)]

    # 4. Agrupar por número de vagas e calcular o preço médio
    preco_medio_por_vaga = df_filtrado.groupby('parkingSpaces')['price'].mean().sort_index()

    # 5. Gerar o gráfico de barras
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 7))

    sns.barplot(
        x=preco_medio_por_vaga.index,
        y=preco_medio_por_vaga.values,
        palette='crest',
        hue=preco_medio_por_vaga.index,
        legend=False,
        ax=ax
    )

    ax.set_title('Preço Médio do Apartamento por Número de Vagas de Garagem', fontsize=18)
    ax.set_xlabel('Número de Vagas de Garagem', fontsize=12)
    ax.set_ylabel('Preço Médio (R$)', fontsize=12)

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

    fig.tight_layout()

    # 6. Retornar a figura para o Streamlit
    return fig